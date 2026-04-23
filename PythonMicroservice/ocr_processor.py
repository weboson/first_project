from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
from image_preprocessor import ImagePreprocessor
import io
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self):
        logger.info("Инициализация OCRProcessor...")
        try:
            # Согласно официальной документации PaddleOCR 3.x
            self.ocr = PaddleOCR(
                use_textline_orientation=True,  # Новая опция в 3.x
                lang='ru',           # Русский язык
                show_log=False,
                use_gpu=False,       # Для CPU, если есть GPU - True
                det_db_thresh=0.3,
                det_db_box_thresh=0.3,
                rec_db_thresh=0.3,
                # Дополнительные настройки для лучшего распознавания
                det_limit_side_len=960,  # Увеличиваем для больших изображений
                det_limit_type='max',
                rec_batch_num=6,
                drop_score=0.5
            )
            self.preprocessor = ImagePreprocessor()
            logger.info("OCRProcessor успешно инициализирован")
        except Exception as e:
            logger.error(f"Ошибка инициализации PaddleOCR: {e}")
            raise
    
    def process_image(self, image_bytes: bytes) -> str:
        """Распознавание текста из изображения"""
        try:
            # Конвертация bytes в PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Конвертация в RGB если нужно
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            
            # Конвертация в numpy array для opencv
            image_np = np.array(image)
            
            # Предобработка
            enhanced = self.preprocessor.enhance_for_ocr(image_np)
            
            # OCR
            result = self.ocr.ocr(enhanced, cls=True)
            
            # Извлечение текста с координатами для отладки
            text_lines = []
            if result and result[0]:
                for line in result[0]:
                    text = line[1][0]  # Текст
                    confidence = line[1][1]  # Уверенность
                    if confidence > 0.5:  # Фильтруем низкую уверенность
                        text_lines.append(text)
                        logger.debug(f"Распознано: '{text}' (conf: {confidence:.2f})")
            
            full_text = ' '.join(text_lines)
            logger.info(f"Распознано символов: {len(full_text)}")
            return full_text
            
        except Exception as e:
            logger.error(f"Ошибка OCR обработки изображения: {e}")
            raise
    
    def process_pdf(self, pdf_bytes: bytes) -> str:
        """Распознавание из PDF (конвертация страниц в изображения)"""
        try:
            from pdf2image import convert_from_bytes
            
            logger.info("Конвертация PDF в изображения...")
            images = convert_from_bytes(
                pdf_bytes, 
                dpi=200,  # Уменьшил DPI для скорости, для качества можно 300
                fmt='PNG'
            )
            logger.info(f"PDF содержит {len(images)} страниц")
            
            all_text = []
            for i, image in enumerate(images):
                logger.info(f"Обработка страницы {i+1}/{len(images)}")
                
                # Конвертация PIL в bytes
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                text = self.process_image(img_byte_arr)
                if text.strip():
                    all_text.append(f"--- Page {i+1} ---\n{text}")
            
            result = '\n'.join(all_text)
            logger.info(f"PDF обработан. Всего текста: {len(result)} символов")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка обработки PDF: {e}")
            raise