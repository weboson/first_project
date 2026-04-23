#Run microservice 'PythonMicroservice' for read images or pdf documents with use AI (Ollama) qwen2:7b:

1. cd PythonMicroservice

2. docker-compose up -d
(waiting 5-10 minutes)

3. docker-compose exec ollama ollama pull qwen2:7b

4. In Postman:

Тестирование Python микросервиса через Postman
Шаг 1: Убедитесь, что сервис запущен
Перед отправкой запроса проверьте, что сервис работает:

Откройте в браузере: http://localhost:8000/health

Или в Postman отправьте GET запрос на http://localhost:8000/health

Шаг 2: Настройка POST запроса в Postman
Метод: POST

URL: http://localhost:8000/process_document

Вкладка: Body

Тип: form-data

Key: file (обязательно точно так, как в коде)

Value: выберите ваш файл (нажмите на выпадающий список и выберите "File")