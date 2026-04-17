## Image Classification (Django + PyTorch)

Одностраничное веб-приложение для загрузки изображения и получения предсказания модели (класс + вероятность).

### Стек
- Python 3.10+
- Django (latest stable)
- PyTorch + torchvision (предобученная `resnet18`)
- Bootstrap 5 (CDN)
- Docker

### Структура
- `image_classifier_project/` — Django-проект (settings/urls/wsgi/asgi)
- `main/` — рендерит единственную страницу (`/`)
- `predictor/` — ML-логика + API (`/api/predict/`) внутри Django
- `templates/main/index.html` — фронтенд (preview, spinner, AJAX)

---

## Запуск локально (без Docker)

1) Создайте виртуальное окружение и установите зависимости:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Запустите Django:

```bash
python3 manage.py runserver 0.0.0.0:8000
```

3) Откройте в браузере `http://127.0.0.1:8000/`.

> Первый запуск может занять больше времени: torchvision может скачать веса модели автоматически.

---

## Запуск через Docker Compose

```bash
docker compose up --build
```

Откройте `http://127.0.0.1:8000/`.

---

## Настройка модели (как заменить на свою)

Сейчас demo-модель (случайное число 1..10) находится в `predictor/ml_model.py`.

Чтобы подключить свою модель:
1) В `predictor/ml_model.py` в классе `ImageClassifierModel`:
   - загрузите модель/веса в `warmup()` или в конструкторе,
   - в `predict(...)` сделайте preprocess + inference,
   - верните `{label: ..., probability: ...}`.
2) Пересоберите контейнер:
   ```bash
   docker compose up --build
   ```

---

## Деплой (пример: Railway)

Ниже — типовой вариант. Конкретные шаги в UI Railway могут немного отличаться.

1) Закоммитьте проект в GitHub.
2) В Railway: **New Project → Deploy from GitHub repo**.
3) Укажите переменные окружения:
   - `DJANGO_DEBUG=0`
   - `DJANGO_SECRET_KEY=<случайная_строка>`
   - `DJANGO_ALLOWED_HOSTS=<ваш домен или *>`
4) Команда запуска (Start Command):

```bash
python3 manage.py runserver 0.0.0.0:$PORT
```

> Railway обычно выставляет переменную `PORT`. Для production лучше использовать gunicorn, но по ТЗ допускается `runserver`.

После деплоя Railway выдаст публичный URL — его и отправьте проверяющему.

