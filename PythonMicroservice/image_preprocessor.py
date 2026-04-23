import cv2
import numpy as np
from PIL import Image

class ImagePreprocessor:
    @staticmethod
    def enhance_for_ocr(image: np.ndarray) -> np.ndarray:
        """Улучшение плохих изображений для OCR"""
        # Конвертация в контраст если нужно
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Денойзинг
        denoised = cv2.fastNlMeansDenoising(enhanced, h=30)
        
        # Бинаризация (адаптивная для разных условий освещения)
        binary = cv2.adaptiveThreshold(
            denoised, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        return binary