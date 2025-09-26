"""
监控和告警系统
提供实时监控和异常告警功能
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import threading
from collections import defaultdict, deque
import psutil
import os

class AlertLevel(Enum):
    """告警级别"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MetricType(Enum):
    """指标类型"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"

class AlertStatus(Enum):
    """告警状态"""
    ACTIVE = "active"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

@dataclass
class Metric:
    """指标"""
    name: str
    value: float
    metric_type: MetricType
    tags: Dict[str, str]
    timestamp: datetime

@dataclass
class AlertRule:
    """告警规则"""
    rule_id: str
    name: str
    metric_name: str
    condition: str  # 例如: "value > 100"
    threshold: float
    alert_level: AlertLevel
    duration: int  # 持续时间（秒）
    enabled: bool
    tags: Dict[str, str]

@dataclass
class Alert:
    """告警"""
    alert_id: str
    rule_id: str
    metric_name: str
    current_value: float
    threshold: float
    alert_level: AlertLevel
    status: AlertStatus
    message: str
    triggered_at: datetime
    resolved_at: Optional[datetime]
    tags: Dict[str, str]

@dataclass
class SystemMetrics:
    """系统指标"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict[str, int]
    process_count: int
    load_average: List[float]
    timestamp: datetime

class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.lock = threading.Lock()
    
    def record_metric(self, name: str, value: float, metric_type: MetricType = MetricType.GAUGE, 
                     tags: Optional[Dict[str, str]] = None):
        """记录指标"""
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            tags=tags or {},
            timestamp=datetime.now()
        )
        
        with self.lock:
            self.metrics[name].append(metric)
    
    def get_metric_value(self, name: str, default: float = 0.0) -> float:
        """获取指标值"""
        with self.lock:
            if name in self.metrics and self.metrics[name]:
                return self.metrics[name][-1].value
            return default
    
    def get_metric_history(self, name: str, minutes: int = 60) -> List[Metric]:
        """获取指标历史"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        with self.lock:
            if name not in self.metrics:
                return []
            
            return [m for m in self.metrics[name] if m.timestamp >= cutoff_time]
    
    def get_all_metrics(self) -> Dict[str, List[Metric]]:
        """获取所有指标"""
        with self.lock:
            return {name: list(metrics) for name, metrics in self.metrics.items()}

class AlertManager:
    """告警管理器"""
    
    def __init__(self):
        self.rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self.notification_handlers: List[Callable] = []
        self.lock = threading.Lock()
    
    def add_rule(self, rule: AlertRule):
        """添加告警规则"""
        with self.lock:
            self.rules[rule.rule_id] = rule
        logger.info(f"告警规则已添加: {rule.name}")
    
    def remove_rule(self, rule_id: str):
        """移除告警规则"""
        with self.lock:
            if rule_id in self.rules:
                del self.rules[rule_id]
                logger.info(f"告警规则已移除: {rule_id}")
    
    def check_alerts(self, metrics_collector: MetricsCollector):
        """检查告警"""
        with self.lock:
            for rule_id, rule in self.rules.items():
                if not rule.enabled:
                    continue
                
                current_value = metrics_collector.get_metric_value(rule.metric_name)
                
                if self._evaluate_condition(current_value, rule.condition, rule.threshold):
                    self._trigger_alert(rule, current_value)
                else:
                    self._resolve_alert(rule_id)
    
    def _evaluate_condition(self, value: float, condition: str, threshold: float) -> bool:
        """评估条件"""
        try:
            # 简单的条件评估
            if ">" in condition:
                return value > threshold
            elif "<" in condition:
                return value < threshold
            elif ">=" in condition:
                return value >= threshold
            elif "<=" in condition:
                return value <= threshold
            elif "==" in condition:
                return value == threshold
            elif "!=" in condition:
                return value != threshold
            else:
                return False
        except Exception as e:
            logger.error(f"条件评估失败: {e}")
            return False
    
    def _trigger_alert(self, rule: AlertRule, current_value: float):
        """触发告警"""
        alert_id = f"{rule.rule_id}_{int(time.time())}"
        
        if alert_id not in self.active_alerts:
            alert = Alert(
                alert_id=alert_id,
                rule_id=rule.rule_id,
                metric_name=rule.metric_name,
                current_value=current_value,
                threshold=rule.threshold,
                alert_level=rule.alert_level,
                status=AlertStatus.ACTIVE,
                message=f"{rule.name}: {rule.metric_name} = {current_value} (阈值: {rule.threshold})",
                triggered_at=datetime.now(),
                resolved_at=None,
                tags=rule.tags
            )
            
            self.active_alerts[alert_id] = alert
            self.alert_history.append(alert)
            
            # 发送通知
            self._send_notification(alert)
            
            logger.warning(f"告警触发: {alert.message}")
    
    def _resolve_alert(self, rule_id: str):
        """解决告警"""
        alerts_to_resolve = []
        
        for alert_id, alert in self.active_alerts.items():
            if alert.rule_id == rule_id:
                alerts_to_resolve.append(alert_id)
        
        for alert_id in alerts_to_resolve:
            alert = self.active_alerts[alert_id]
            alert.status = AlertStatus.RESOLVED
            alert.resolved_at = datetime.now()
            
            del self.active_alerts[alert_id]
            
            logger.info(f"告警已解决: {alert.message}")
    
    def _send_notification(self, alert: Alert):
        """发送通知"""
        for handler in self.notification_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"通知发送失败: {e}")
    
    def add_notification_handler(self, handler: Callable):
        """添加通知处理器"""
        self.notification_handlers.append(handler)
    
    def get_active_alerts(self) -> List[Alert]:
        """获取活跃告警"""
        with self.lock:
            return list(self.active_alerts.values())
    
    def get_alert_history(self, hours: int = 24) -> List[Alert]:
        """获取告警历史"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with self.lock:
            return [alert for alert in self.alert_history if alert.triggered_at >= cutoff_time]

class SystemMonitor:
    """系统监控器"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()
        self.is_monitoring = False
        self.monitor_task = None
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """设置默认告警规则"""
        # CPU使用率告警
        self.alert_manager.add_rule(AlertRule(
            rule_id="cpu_high",
            name="CPU使用率过高",
            metric_name="system.cpu_percent",
            condition=">",
            threshold=80.0,
            alert_level=AlertLevel.WARNING,
            duration=300,
            enabled=True,
            tags={"component": "system"}
        ))
        
        # 内存使用率告警
        self.alert_manager.add_rule(AlertRule(
            rule_id="memory_high",
            name="内存使用率过高",
            metric_name="system.memory_percent",
            condition=">",
            threshold=85.0,
            alert_level=AlertLevel.WARNING,
            duration=300,
            enabled=True,
            tags={"component": "system"}
        ))
        
        # 磁盘使用率告警
        self.alert_manager.add_rule(AlertRule(
            rule_id="disk_high",
            name="磁盘使用率过高",
            metric_name="system.disk_percent",
            condition=">",
            threshold=90.0,
            alert_level=AlertLevel.CRITICAL,
            duration=60,
            enabled=True,
            tags={"component": "system"}
        ))
        
        # API响应时间告警
        self.alert_manager.add_rule(AlertRule(
            rule_id="api_response_time",
            name="API响应时间过长",
            metric_name="api.response_time",
            condition=">",
            threshold=5.0,
            alert_level=AlertLevel.WARNING,
            duration=60,
            enabled=True,
            tags={"component": "api"}
        ))
        
        # API错误率告警
        self.alert_manager.add_rule(AlertRule(
            rule_id="api_error_rate",
            name="API错误率过高",
            metric_name="api.error_rate",
            condition=">",
            threshold=0.05,
            alert_level=AlertLevel.ERROR,
            duration=60,
            enabled=True,
            tags={"component": "api"}
        ))
    
    async def start_monitoring(self):
        """开始监控"""
        if self.is_monitoring:
            logger.warning("监控已在运行")
            return
        
        self.is_monitoring = True
        self.monitor_task = asyncio.create_task(self._monitoring_loop())
        logger.info("系统监控已启动")
    
    async def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("系统监控已停止")
    
    async def _monitoring_loop(self):
        """监控循环"""
        while self.is_monitoring:
            try:
                # 收集系统指标
                await self._collect_system_metrics()
                
                # 检查告警
                self.alert_manager.check_alerts(self.metrics_collector)
                
                # 等待下次收集
                await asyncio.sleep(10)  # 每10秒收集一次
                
            except Exception as e:
                logger.error(f"监控循环异常: {e}")
                await asyncio.sleep(10)
    
    async def _collect_system_metrics(self):
        """收集系统指标"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            self.metrics_collector.record_metric("system.cpu_percent", cpu_percent)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            self.metrics_collector.record_metric("system.memory_percent", memory.percent)
            
            # 磁盘使用率
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.metrics_collector.record_metric("system.disk_percent", disk_percent)
            
            # 网络IO
            network_io = psutil.net_io_counters()
            self.metrics_collector.record_metric("system.network.bytes_sent", network_io.bytes_sent)
            self.metrics_collector.record_metric("system.network.bytes_recv", network_io.bytes_recv)
            
            # 进程数量
            process_count = len(psutil.pids())
            self.metrics_collector.record_metric("system.process_count", process_count)
            
            # 负载平均值
            load_avg = psutil.getloadavg()
            self.metrics_collector.record_metric("system.load_avg_1min", load_avg[0])
            self.metrics_collector.record_metric("system.load_avg_5min", load_avg[1])
            self.metrics_collector.record_metric("system.load_avg_15min", load_avg[2])
            
        except Exception as e:
            logger.error(f"系统指标收集失败: {e}")
    
    def record_api_metric(self, api_name: str, response_time: float, success: bool):
        """记录API指标"""
        # 响应时间
        self.metrics_collector.record_metric(f"api.{api_name}.response_time", response_time)
        
        # 成功/失败计数
        self.metrics_collector.record_metric(f"api.{api_name}.success", 1 if success else 0)
        self.metrics_collector.record_metric(f"api.{api_name}.failure", 0 if success else 1)
        
        # 计算错误率
        success_count = self.metrics_collector.get_metric_value(f"api.{api_name}.success")
        failure_count = self.metrics_collector.get_metric_value(f"api.{api_name}.failure")
        total_count = success_count + failure_count
        
        if total_count > 0:
            error_rate = failure_count / total_count
            self.metrics_collector.record_metric(f"api.{api_name}.error_rate", error_rate)
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "is_monitoring": self.is_monitoring,
            "cpu_percent": self.metrics_collector.get_metric_value("system.cpu_percent"),
            "memory_percent": self.metrics_collector.get_metric_value("system.memory_percent"),
            "disk_percent": self.metrics_collector.get_metric_value("system.disk_percent"),
            "process_count": self.metrics_collector.get_metric_value("system.process_count"),
            "load_avg_1min": self.metrics_collector.get_metric_value("system.load_avg_1min"),
            "active_alerts": len(self.alert_manager.get_active_alerts()),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """获取指标摘要"""
        all_metrics = self.metrics_collector.get_all_metrics()
        
        summary = {}
        for name, metrics in all_metrics.items():
            if metrics:
                values = [m.value for m in metrics]
                summary[name] = {
                    "current": values[-1] if values else 0,
                    "min": min(values) if values else 0,
                    "max": max(values) if values else 0,
                    "avg": sum(values) / len(values) if values else 0,
                    "count": len(values)
                }
        
        return summary
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """获取告警摘要"""
        active_alerts = self.alert_manager.get_active_alerts()
        alert_history = self.alert_manager.get_alert_history(24)
        
        return {
            "active_alerts": len(active_alerts),
            "total_alerts_24h": len(alert_history),
            "alerts_by_level": {
                level.value: len([a for a in active_alerts if a.alert_level == level])
                for level in AlertLevel
            },
            "recent_alerts": [
                {
                    "alert_id": alert.alert_id,
                    "name": alert.rule_id,
                    "level": alert.alert_level.value,
                    "message": alert.message,
                    "triggered_at": alert.triggered_at.isoformat()
                }
                for alert in active_alerts[-10:]  # 最近10个告警
            ]
        }
    
    def add_custom_rule(self, rule: AlertRule):
        """添加自定义告警规则"""
        self.alert_manager.add_rule(rule)
    
    def add_notification_handler(self, handler: Callable):
        """添加通知处理器"""
        self.alert_manager.add_notification_handler(handler)

# 全局实例
system_monitor = SystemMonitor()
