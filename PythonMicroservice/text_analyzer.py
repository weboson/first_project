import ollama
import re
import json
import asyncio
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextAnalyzer:
    def __init__(self, use_ollama: bool = True):
        self.use_ollama = use_ollama
        self.model = "qwen2:7b"  # или "qwen:7b" для меньшей версии
        self.ollama_available = False
        
        if use_ollama:
            self._check_ollama()
    
    def _check_ollama(self):
        """Проверка доступности Ollama сервера"""
        try:
            # Пытаемся получить список моделей
            response = ollama.list()
            self.ollama_available = True
            logger.info(f"Ollama доступен. Доступные модели: {response}")
            
            # Проверяем наличие нужной модели
            models = [model['name'] for model in response.get('models', [])]
            if self.model not in models:
                logger.warning(f"Модель {self.model} не найдена. Используйте: ollama pull {self.model}")
        except Exception as e:
            logger.warning(f"Ollama не доступен: {e}. Будет использован fallback на regex")
            self.ollama_available = False
    
    def extract_entities(self, text: str) -> dict:
        """Извлечение ИНН, ФИО, контрагентов с помощью LLM или regex"""
        
        if self.use_ollama and self.ollama_available:
            return self._extract_with_llm(text)
        else:
            logger.info("Используем резервный метод извлечения (regex)")
            return self._fallback_extraction(text)
    
    def _extract_with_llm(self, text: str) -> dict:
        """Извлечение через Ollama"""
        
        prompt = f"""
        Ты - эксперт по извлечению данных из российских документов.
        Извлеки из текста следующие поля:
        - ИНН (российский, 10 или 12 цифр)
        - ФИО (фамилия, имя, отчество человека)
        - Контрагенты (список названий организаций или ИП)
        
        Текст документа:
        {text[:3000]}  # Ограничиваем длину
        
        Ответь ТОЛЬКО в формате JSON без дополнительного текста:
        {{
            "inn": "найденный ИНН или null",
            "full_name": "найденное ФИО или null",
            "counterparties": ["контрагент1", "контрагент2"]
        }}
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt, options={
                'temperature': 0.1,  # Минимум творчества для точности
                'num_predict': 500
            })
            
            # Очищаем ответ от возможных маркдаун-оберток
            clean_response = response['response'].strip()
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:]
            if clean_response.startswith('```'):
                clean_response = clean_response[3:]
            if clean_response.endswith('```'):
                clean_response = clean_response[:-3]
            
            result = json.loads(clean_response)
            return result
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return self._fallback_extraction(text)
    
    def _fallback_extraction(self, text: str) -> dict:
        """Резервное извлечение через regex (улучшенный)"""
        
        # Поиск ИНН (10 или 12 цифр)
        inn_pattern = r'\b(\d{10}|\d{12})\b'
        inn_match = re.search(inn_pattern, text)
        inn = inn_match.group(1) if inn_match else None
        
        # Поиск ФИО (разные варианты написания)
        fio_patterns = [
            r'([А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+)',  # Иванов Иван Иванович
            r'([А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.\s*[А-ЯЁ]\.)',  # Иванов И. И.
            r'(ФИО|Ф\.И\.О\.)\s*:?\s*([А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+)',  # ФИО: Иванов Иван Иванович
        ]
        
        full_name = None
        for pattern in fio_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                full_name = match.group(2) if len(match.groups()) > 1 else match.group(1)
                break
        
        # Поиск организаций (расширенный список)
        org_patterns = [
            r'(ООО|ИП|ЗАО|ОАО|ПАО|АО|ФГУП|ГУП|МУП)\s+[А-ЯЁ][а-яё\s\-""]+',
            r'([А-ЯЁ][а-яё]+(?:компания|фирма|корпорация|холдинг))',
            r'\"([А-ЯЁ][а-яё\s]+)\"',
        ]
        
        counterparties = []
        for pattern in org_patterns:
            matches = re.findall(pattern, text)
            counterparties.extend(matches)
        
        # Убираем дубликаты и очищаем
        counterparties = list(set([c.strip() for c in counterparties if len(c.strip()) > 3]))[:5]
        
        return {
            "inn": inn,
            "full_name": full_name,
            "counterparties": counterparties
        }

    async def extract_entities_async(self, text: str) -> dict:
        """Асинхронная версия для лучшей производительности"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.extract_entities, text)