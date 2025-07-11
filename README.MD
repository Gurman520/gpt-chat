[English ver.](./README_en.md)

---

# Чат-приложение с Llama 3 🦙✨

<!-- <div align="center">
  <img src="https://i.imgur.com/JZk6bE0.png" width="300" alt="Llama Chat Demo">
</div> -->

## 📖 Содержание
- [О проекте](#-о-проекте)
- [Возможности](#-возможности)
- [Технологии](#-технологии)
- [Установка](#-установка)
- [Запуск Llama локально](#-запуск-llama-локально)
- [Разработчикам](#-разработчикам)

## 🌟 О проекте
Интерактивный чат с поддержкой нейросети Llama 3.1. Приложение предоставляет интерфейс для общения с AI с сохранением истории диалогов и Markdown-форматированием ответов.

## 🚀 Возможности
- 💬 Диалоги с сохранением истории
- ✨ Поддержка Markdown и подсветка кода
- ⚡ Быстрые ответы через FastAPI
- 📱 Адаптивный интерфейс
- 🔄 Анимация набора текста

## 🛠 Технологии
- **Backend**: Python + FastAPI
- **Frontend**: HTML/CSS/JS
- **AI**: Llama 3.1 (Docker)
- **DB**: SQLite

## ⚙️ Установка

### Требования
- Python 3.9+
- Docker (опционально)

```bash
# Клонировать репозиторий
git clone https://github.com/ваш-репозиторий/llama-chat.git
cd llama-chat

# Установить зависимости
pip install -r requirements.txt

# Инициализировать БД
python -c "from app.models import init_db; init_db()"
```

## 🐋 Запуск Llama локально

Для запуска Llama используется оригинальный образ Docker Llama

[Ссылка на официальную страницу проекта](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image)

Выполнить в консоли:
``` bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

docker exec -it ollama ollama run llama3:8b
```

## 👨‍💻 Разработчикам

### Запуск приложения
```bash
uvicorn app.main:app --reload
```

<!-- ### Сборка Docker
```bash
docker-compose up -d --build
``` -->


---