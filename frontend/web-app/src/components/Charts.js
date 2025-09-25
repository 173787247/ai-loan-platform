import React from 'react';
import ReactECharts from 'echarts-for-react';

// 风险分布饼图
export const RiskDistribution = ({ data }) => {
  const option = {
    title: {
      text: '风险等级分布',
      left: 'center',
      textStyle: {
        color: '#2c3e50',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'middle',
      textStyle: {
        color: '#2c3e50'
      }
    },
    series: [
      {
        name: '风险分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '20',
            fontWeight: 'bold',
            color: '#2c3e50'
          }
        },
        labelLine: {
          show: false
        },
        data: data.map(item => ({
          value: item.count,
          name: item.level,
          itemStyle: {
            color: item.level === '低风险' ? '#28a745' : 
                   item.level === '中风险' ? '#ffc107' : '#dc3545'
          }
        }))
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: '400px', width: '100%' }} />;
};

// 贷款趋势折线图
export const LoanTrend = ({ data }) => {
  const option = {
    title: {
      text: '贷款申请趋势',
      left: 'center',
      textStyle: {
        color: '#2c3e50',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['总申请', '已批准', '已拒绝'],
      top: 'bottom',
      textStyle: {
        color: '#2c3e50'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.map(item => item.month),
      axisLabel: {
        color: '#2c3e50'
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#2c3e50'
      }
    },
    series: [
      {
        name: '总申请',
        type: 'line',
        data: data.map(item => item.total),
        smooth: true,
        itemStyle: {
          color: '#4ecdc4'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0, color: 'rgba(78, 205, 196, 0.3)'
            }, {
              offset: 1, color: 'rgba(78, 205, 196, 0.1)'
            }]
          }
        }
      },
      {
        name: '已批准',
        type: 'line',
        data: data.map(item => item.approved),
        smooth: true,
        itemStyle: {
          color: '#28a745'
        }
      },
      {
        name: '已拒绝',
        type: 'line',
        data: data.map(item => item.rejected),
        smooth: true,
        itemStyle: {
          color: '#dc3545'
        }
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: '400px', width: '100%' }} />;
};

// 风险评分分布柱状图
export const RiskScoreDistribution = ({ data }) => {
  const option = {
    title: {
      text: '风险评分分布',
      left: 'center',
      textStyle: {
        color: '#2c3e50',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.range),
      axisLabel: {
        color: '#2c3e50'
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#2c3e50'
      }
    },
    series: [
      {
        name: '申请数量',
        type: 'bar',
        data: data.map(item => ({
          value: item.count,
          itemStyle: {
            color: item.range === '0-20' ? '#28a745' :
                   item.range === '21-40' ? '#20c997' :
                   item.range === '41-60' ? '#ffc107' :
                   item.range === '61-80' ? '#fd7e14' : '#dc3545'
          }
        })),
        barWidth: '60%',
        itemStyle: {
          borderRadius: [4, 4, 0, 0]
        }
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: '400px', width: '100%' }} />;
};

// 行业风险雷达图
export const IndustryRiskRadar = ({ data }) => {
  const option = {
    title: {
      text: '行业风险分析',
      left: 'center',
      textStyle: {
        color: '#2c3e50',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {},
    legend: {
      data: data.map(item => item.name),
      bottom: '5%',
      textStyle: {
        color: '#2c3e50'
      }
    },
    radar: {
      indicator: [
        { name: '信用风险', max: 100 },
        { name: '市场风险', max: 100 },
        { name: '操作风险', max: 100 },
        { name: '流动性风险', max: 100 },
        { name: '合规风险', max: 100 }
      ],
      axisName: {
        color: '#2c3e50'
      }
    },
    series: [
      {
        name: '行业风险',
        type: 'radar',
        data: data.map((item, index) => ({
          value: item.risks,
          name: item.name,
          itemStyle: {
            color: ['#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'][index % 5]
          },
          areaStyle: {
            opacity: 0.3
          }
        }))
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: '400px', width: '100%' }} />;
};

// 实时监控仪表盘
export const RealtimeDashboard = ({ systemStats }) => {
  const option = {
    title: {
      text: '系统实时监控',
      left: 'center',
      textStyle: {
        color: '#2c3e50',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    series: [
      {
        name: 'CPU使用率',
        type: 'gauge',
        center: ['25%', '50%'],
        radius: '60%',
        min: 0,
        max: 100,
        splitNumber: 10,
        axisLine: {
          lineStyle: {
            width: 6,
            color: [
              [0.3, '#28a745'],
              [0.7, '#ffc107'],
              [1, '#dc3545']
            ]
          }
        },
        pointer: {
          itemStyle: {
            color: 'auto'
          }
        },
        axisTick: {
          distance: -30,
          splitNumber: 5,
          lineStyle: {
            width: 2,
            color: '#999'
          }
        },
        splitLine: {
          distance: -30,
          length: 30,
          lineStyle: {
            width: 4,
            color: '#999'
          }
        },
        axisLabel: {
          color: '#2c3e50',
          distance: -20,
          fontSize: 12
        },
        detail: {
          valueAnimation: true,
          formatter: '{value}%',
          color: 'auto',
          fontSize: 16
        },
        data: [
          {
            value: systemStats.cpuUsage,
            name: 'CPU'
          }
        ]
      },
      {
        name: '内存使用率',
        type: 'gauge',
        center: ['75%', '50%'],
        radius: '60%',
        min: 0,
        max: 100,
        splitNumber: 10,
        axisLine: {
          lineStyle: {
            width: 6,
            color: [
              [0.3, '#28a745'],
              [0.7, '#ffc107'],
              [1, '#dc3545']
            ]
          }
        },
        pointer: {
          itemStyle: {
            color: 'auto'
          }
        },
        axisTick: {
          distance: -30,
          splitNumber: 5,
          lineStyle: {
            width: 2,
            color: '#999'
          }
        },
        splitLine: {
          distance: -30,
          length: 30,
          lineStyle: {
            width: 4,
            color: '#999'
          }
        },
        axisLabel: {
          color: '#2c3e50',
          distance: -20,
          fontSize: 12
        },
        detail: {
          valueAnimation: true,
          formatter: '{value}%',
          color: 'auto',
          fontSize: 16
        },
        data: [
          {
            value: systemStats.memoryUsage,
            name: '内存'
          }
        ]
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: '300px', width: '100%' }} />;
};

// 导出所有图表组件
const Charts = {
  RiskDistribution,
  LoanTrend,
  RiskScoreDistribution,
  IndustryRiskRadar,
  RealtimeDashboard
};

export default Charts;