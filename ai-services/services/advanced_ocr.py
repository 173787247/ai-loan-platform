#!/usr/bin/env python3
"""
高级OCR服务
集成多种OCR引擎，支持中文图片文字识别
"""

import asyncio
import aiohttp
import base64
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import os
from PIL import Image
import io

logger = logging.getLogger(__name__)

class OCREngine(Enum):
    """OCR引擎类型"""
    TESSERACT = "tesseract"
    BAIDU = "baidu"
    TENCENT = "tencent"
    ALIYUN = "aliyun"
    PADDLEOCR = "paddleocr"

@dataclass
class OCRResult:
    """OCR识别结果"""
    text: str
    confidence: float
    engine: str
    processing_time: float
    bounding_boxes: List[Dict[str, Any]] = None
    language: str = "zh"

class AdvancedOCRService:
    """高级OCR服务"""
    
    def __init__(self):
        self.engines = {
            OCREngine.TESSERACT: self._tesseract_ocr,
            OCREngine.BAIDU: self._baidu_ocr,
            OCREngine.TENCENT: self._tencent_ocr,
            OCREngine.ALIYUN: self._aliyun_ocr,
            OCREngine.PADDLEOCR: self._paddleocr_ocr
        }
        
        # OCR引擎配置
        self.config = {
            "baidu": {
                "api_key": os.getenv("BAIDU_OCR_API_KEY", ""),
                "secret_key": os.getenv("BAIDU_OCR_SECRET_KEY", ""),
                "url": "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
            },
            "tencent": {
                "secret_id": os.getenv("TENCENT_OCR_SECRET_ID", ""),
                "secret_key": os.getenv("TENCENT_OCR_SECRET_KEY", ""),
                "region": "ap-beijing"
            },
            "aliyun": {
                "access_key_id": os.getenv("ALIYUN_OCR_ACCESS_KEY_ID", ""),
                "access_key_secret": os.getenv("ALIYUN_OCR_ACCESS_KEY_SECRET", ""),
                "region": "cn-shanghai"
            }
        }
    
    async def recognize_text(
        self, 
        image_path: str, 
        engines: List[OCREngine] = None,
        language: str = "chi_sim+eng"
    ) -> List[OCRResult]:
        """识别图片中的文字"""
        if engines is None:
            engines = [OCREngine.TESSERACT, OCREngine.PADDLEOCR]
        
        results = []
        
        for engine in engines:
            try:
                logger.info(f"使用 {engine.value} 引擎进行OCR识别")
                result = await self.engines[engine](image_path, language)
                if result:
                    results.append(result)
                    logger.info(f"{engine.value} OCR识别成功: {len(result.text)} 个字符")
                else:
                    logger.warning(f"{engine.value} OCR识别失败")
            except Exception as e:
                logger.error(f"{engine.value} OCR识别异常: {e}")
        
        return results
    
    async def _tesseract_ocr(self, image_path: str, language: str) -> Optional[OCRResult]:
        """使用Tesseract OCR"""
        try:
            import pytesseract
            from PIL import Image
            
            start_time = asyncio.get_event_loop().time()
            
            # 打开图片
            image = Image.open(image_path)
            
            # 图片预处理
            image = self._preprocess_image(image)
            
            # OCR识别
            text = pytesseract.image_to_string(image, lang=language)
            
            # 获取置信度
            data = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return OCRResult(
                text=text.strip(),
                confidence=avg_confidence / 100.0,
                engine="tesseract",
                processing_time=processing_time,
                language=language
            )
            
        except ImportError:
            logger.error("Tesseract OCR未安装，请安装: pip install pytesseract")
            return None
        except Exception as e:
            logger.error(f"Tesseract OCR识别失败: {e}")
            return None
    
    async def _paddleocr_ocr(self, image_path: str, language: str) -> Optional[OCRResult]:
        """使用PaddleOCR"""
        try:
            from paddleocr import PaddleOCR
            
            start_time = asyncio.get_event_loop().time()
            
            # 初始化PaddleOCR
            ocr = PaddleOCR(use_angle_cls=True, lang='ch')
            
            # OCR识别
            result = ocr.ocr(image_path, cls=True)
            
            # 提取文字和置信度
            text_parts = []
            confidences = []
            bounding_boxes = []
            
            if result and result[0]:
                for line in result[0]:
                    if line:
                        text_parts.append(line[1][0])
                        confidences.append(line[1][1])
                        bounding_boxes.append({
                            "bbox": line[0],
                            "text": line[1][0],
                            "confidence": line[1][1]
                        })
            
            text = '\n'.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return OCRResult(
                text=text,
                confidence=avg_confidence,
                engine="paddleocr",
                processing_time=processing_time,
                bounding_boxes=bounding_boxes,
                language="zh"
            )
            
        except ImportError:
            logger.error("PaddleOCR未安装，请安装: pip install paddlepaddle paddleocr")
            return None
        except Exception as e:
            logger.error(f"PaddleOCR识别失败: {e}")
            return None
    
    async def _baidu_ocr(self, image_path: str, language: str) -> Optional[OCRResult]:
        """使用百度OCR"""
        try:
            import aiohttp
            import hashlib
            import time
            import urllib.parse
            
            config = self.config["baidu"]
            if not config["api_key"] or not config["secret_key"]:
                logger.warning("百度OCR API密钥未配置")
                return None
            
            start_time = asyncio.get_event_loop().time()
            
            # 读取图片并编码
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # 获取access_token
            token_url = "https://aip.baidubce.com/oauth/2.0/token"
            token_params = {
                "grant_type": "client_credentials",
                "client_id": config["api_key"],
                "client_secret": config["secret_key"]
            }
            
            async with aiohttp.ClientSession() as session:
                # 获取token
                async with session.post(token_url, data=token_params) as resp:
                    token_data = await resp.json()
                    access_token = token_data.get("access_token")
                
                if not access_token:
                    logger.error("获取百度OCR access_token失败")
                    return None
                
                # 调用OCR API
                ocr_url = f"{config['url']}?access_token={access_token}"
                ocr_data = {
                    "image": image_base64,
                    "language_type": "CHN_ENG",
                    "detect_direction": "true",
                    "paragraph": "true"
                }
                
                async with session.post(ocr_url, data=ocr_data) as resp:
                    result = await resp.json()
                
                # 解析结果
                if "words_result" in result:
                    text_parts = [item["words"] for item in result["words_result"]]
                    text = '\n'.join(text_parts)
                    
                    processing_time = asyncio.get_event_loop().time() - start_time
                    
                    return OCRResult(
                        text=text,
                        confidence=0.95,  # 百度OCR通常置信度较高
                        engine="baidu",
                        processing_time=processing_time,
                        language="zh"
                    )
                else:
                    logger.error(f"百度OCR识别失败: {result}")
                    return None
                    
        except Exception as e:
            logger.error(f"百度OCR识别失败: {e}")
            return None
    
    async def _tencent_ocr(self, image_path: str, language: str) -> Optional[OCRResult]:
        """使用腾讯OCR"""
        try:
            # 腾讯OCR需要SDK，这里提供接口框架
            logger.info("腾讯OCR功能待实现")
            return None
        except Exception as e:
            logger.error(f"腾讯OCR识别失败: {e}")
            return None
    
    async def _aliyun_ocr(self, image_path: str, language: str) -> Optional[OCRResult]:
        """使用阿里云OCR"""
        try:
            # 阿里云OCR需要SDK，这里提供接口框架
            logger.info("阿里云OCR功能待实现")
            return None
        except Exception as e:
            logger.error(f"阿里云OCR识别失败: {e}")
            return None
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """图片预处理"""
        try:
            # 转换为RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 调整图片大小（如果太大）
            width, height = image.size
            if width > 2000 or height > 2000:
                ratio = min(2000/width, 2000/height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 增强对比度
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            return image
            
        except Exception as e:
            logger.error(f"图片预处理失败: {e}")
            return image
    
    async def get_best_result(self, results: List[OCRResult]) -> Optional[OCRResult]:
        """获取最佳OCR结果"""
        if not results:
            return None
        
        # 按置信度和文本长度综合评分
        def score_result(result: OCRResult) -> float:
            confidence_score = result.confidence * 0.7
            length_score = min(len(result.text) / 100, 1.0) * 0.3
            return confidence_score + length_score
        
        best_result = max(results, key=score_result)
        logger.info(f"选择最佳OCR结果: {best_result.engine}, 置信度: {best_result.confidence:.3f}")
        
        return best_result

# 全局实例
advanced_ocr_service = AdvancedOCRService()
