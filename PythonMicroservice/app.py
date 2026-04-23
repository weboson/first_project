from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from ocr_processor import OCRProcessor
from text_analyzer import TextAnalyzer
import tempfile
import os

app = FastAPI(title="Document OCR Service")

# Инициализация сервисов
ocr_processor = OCRProcessor()
text_analyzer = TextAnalyzer()

@app.post("/process_document")
async def process_document(file: UploadFile = File(...)):
    """Основной эндпоинт для обработки документов"""
    try:
        # Чтение файла
        contents = await file.read()
        
        # Определение типа файла
        filename = file.filename.lower()
        
        # OCR распознавание
        if filename.endswith('.pdf'):
            raw_text = ocr_processor.process_pdf(contents)
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.tiff', '.bmp')):
            raw_text = ocr_processor.process_image(contents)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Анализ текста
        extracted_data = text_analyzer.extract_entities(raw_text)
        
        # Добавляем raw текст в ответ
        extracted_data["raw_text"] = raw_text[:500]  # первые 500 символов для отладки
        
        return JSONResponse(content=extracted_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)