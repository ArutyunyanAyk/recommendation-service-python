# Recommendation Service Python

Python/FastAPI сервис для проекта **What's for Cooking**.

Сервис отвечает за рекомендации рецептов:
- выбор случайного рецепта;
- сборку meal-комбинации;
- работу со списком рецептов, который может прийти из другого backend-сервиса.

## Стек

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- HTTPX

## Структура проекта

```text
recommendation-service-python/
  app/
    __init__.py
    main.py
    data.py
    schemas.py
    services.py
    routers/
      __init__.py
      system.py
      recipes.py
      recommendations.py

  tests/
    test_api.py

  README.md
  requirements.txt
  pytest.ini
  .gitignore
```

## Что делает каждый файл

```text
app/main.py
```

Главная точка входа FastAPI-приложения.
Создаёт `app = FastAPI()` и подключает routers.

```text
app/routers/system.py
```

System endpoints, например `/health`.

```text
app/routers/recipes.py
```

Endpoints для получения рецептов:

```text
GET /recipes
GET /recipes/{recipe_id}
```

```text
app/routers/recommendations.py
```

Endpoints для рекомендаций рецептов и meal-комбинаций.

```text
app/data.py
```

Временные тестовые данные рецептов.

```text
app/services.py
```

Бизнес-логика сервиса: поиск, фильтрация, подбор случайного рецепта и сборка meal.

```text
app/schemas.py
```

Pydantic-схемы.
Описывают структуру данных: `Recipe`, `Meal`, `RecipeRecommendation`, `MealRecommendation`, request-схемы и допустимые значения `meal_role`.

```text
tests/test_api.py
```

Автотесты для проверки API endpoints.

```text
requirements.txt
```

Список Python-зависимостей проекта.

```text
pytest.ini
```

Настройка pytest, чтобы тесты могли импортировать приложение из папки `app`.

---

## Как запустить проект

### 1. Создать виртуальное окружение

```bash
python -m venv venv
```

### 2. Активировать виртуальное окружение

Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

Если используется обычный cmd:

```bash
venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Запустить сервер

```bash
uvicorn app.main:app --reload
```

После запуска сервер будет доступен по адресу:

```text
http://127.0.0.1:8000
```

Документация API:

```text
http://127.0.0.1:8000/docs
```

---

## Как запустить тесты

```bash
pytest
```

Подробный вывод:

```bash
pytest -v
```

Тесты проверяют основные endpoints, фильтры, ошибки `404/422` и POST-запросы с body.

---

## Endpoints

### System

```text
GET /health
```

Проверяет, что сервис работает.

Пример ответа:

```json
{
  "status": "ok"
}
```

---

### Recipes

```text
GET /recipes
```

Возвращает список тестовых рецептов из `app/data.py`.

```text
GET /recipes/{recipe_id}
```

Возвращает один рецепт по `id`.

Если рецепт не найден, возвращает `404`.

---

### Recommendations from local data

```text
GET /recommend/random-recipe
```

Возвращает случайный рецепт из локального списка `app/data.py`.

Поддерживает фильтры:

```text
max_time
meal_role
tag
```

Примеры:

```text
GET /recommend/random-recipe?max_time=20
GET /recommend/random-recipe?meal_role=protein
GET /recommend/random-recipe?tag=quick
GET /recommend/random-recipe?max_time=20&tag=quick
```

---

```text
GET /recommend/random-meal
```

Собирает meal-комбинацию из локального списка `app/data.py`.

Минимально нужны:

```text
protein
carbs
```

Если есть `vegetables` или `sauce`, они добавляются дополнительно.

Пример ответа:

```json
{
  "meal": {
    "protein": {
      "id": 2,
      "title": "Котлеты",
      "cooking_time": 40,
      "meal_role": "protein",
      "tags": ["dinner", "high_protein"]
    },
    "carbs": {
      "id": 3,
      "title": "Макароны",
      "cooking_time": 15,
      "meal_role": "carbs",
      "tags": ["cheap", "quick"]
    },
    "vegetables": {
      "id": 4,
      "title": "Овощной салат",
      "cooking_time": 10,
      "meal_role": "vegetables",
      "tags": ["vegetables", "quick", "low_calorie"]
    },
    "sauce": {
      "id": 10,
      "title": "Томатный соус",
      "cooking_time": 5,
      "meal_role": "sauce",
      "tags": ["sauce", "quick"]
    }
  }
}
```

---

### Recommendations from provided list

```text
POST /recommend/random-recipe/from-list
```

Принимает список рецептов в body и возвращает случайный рецепт из этого списка.

Фильтры передаются через query parameters:

```text
max_time
meal_role
tag
```

Пример body:

```json
{
  "recipes": [
    {
      "id": 1,
      "title": "Омлет",
      "cooking_time": 10,
      "meal_role": "full_meal",
      "tags": ["breakfast", "quick", "high_protein"]
    },
    {
      "id": 2,
      "title": "Котлеты",
      "cooking_time": 40,
      "meal_role": "protein",
      "tags": ["dinner", "high_protein"]
    }
  ]
}
```

Пример запроса:

```text
POST /recommend/random-recipe/from-list?tag=quick
```

---

```text
POST /recommend/random-meal/from-list
```

Принимает список рецептов в body и пытается собрать meal-комбинацию.

Пример body:

```json
{
  "recipes": [
    {
      "id": 1,
      "title": "Котлеты",
      "cooking_time": 40,
      "meal_role": "protein",
      "tags": ["dinner", "high_protein"]
    },
    {
      "id": 2,
      "title": "Макароны",
      "cooking_time": 15,
      "meal_role": "carbs",
      "tags": ["cheap", "quick"]
    }
  ]
}
```

---

### Request-based recommendations

Эти endpoints удобнее для будущей связки с Java backend, потому что все данные передаются одним JSON body.

```text
POST /recommend/random-recipe/by-request
```

Принимает список рецептов и фильтры в body.

Пример body:

```json
{
  "recipes": [
    {
      "id": 1,
      "title": "Омлет",
      "cooking_time": 10,
      "meal_role": "full_meal",
      "tags": ["breakfast", "quick", "high_protein"]
    },
    {
      "id": 2,
      "title": "Макароны",
      "cooking_time": 15,
      "meal_role": "carbs",
      "tags": ["cheap", "quick"]
    },
    {
      "id": 3,
      "title": "Острые котлеты",
      "cooking_time": 40,
      "meal_role": "protein",
      "tags": ["dinner", "high_protein", "spicy"]
    }
  ],
  "max_time": 20,
  "required_tags": ["quick"],
  "excluded_tags": ["spicy"],
  "preferred_tags": ["high_protein", "breakfast"]
}
```

Поддерживаемые фильтры в body:

- `max_time` — максимальное время приготовления;
- `meal_role` — нужная роль блюда;
- `tag` — один обязательный тег;
- `required_tags` — список тегов, которые обязательно должны быть у рецепта;
- `excluded_tags` — список тегов, которых не должно быть у рецепта;
- `preferred_tags` — список желательных тегов. Они не обязательны, но увеличивают score рецепта.

Логика подбора:

1. Сначала сервис отфильтровывает рецепты по `max_time`, `meal_role`, `tag`, `required_tags` и `excluded_tags`.
2. Если `preferred_tags` не переданы, сервис выбирает случайный рецепт из подходящих.
3. Если `preferred_tags` переданы, сервис считает score для каждого подходящего рецепта.
4. Рецепты с большим количеством совпадений по `preferred_tags` считаются более подходящими.
5. Если несколько рецептов имеют одинаковый лучший score, сервис выбирает случайный среди них.

Пример ответа:

В этом примере лучше всего подходит `Омлет`, потому что он:
- проходит `required_tags`: `quick`;
- не содержит `excluded_tags`: `spicy`;
- имеет оба желательных тега из `preferred_tags`: `high_protein` и `breakfast`.

```json
{
  "recipe": {
    "id": 1,
    "title": "Омлет",
    "cooking_time": 10,
    "meal_role": "full_meal",
    "tags": ["breakfast", "quick", "high_protein"]
  }
}
```

---

```text
POST /recommend/random-meal/by-request
```

Принимает список рецептов в body и возвращает meal-комбинацию.

Дополнительно можно управлять необязательными частями meal:

```json
{
  "recipes": [
    {
      "id": 1,
      "title": "Котлеты",
      "cooking_time": 40,
      "meal_role": "protein",
      "tags": ["dinner", "high_protein"]
    },
    {
      "id": 2,
      "title": "Макароны",
      "cooking_time": 15,
      "meal_role": "carbs",
      "tags": ["cheap", "quick"]
    },
    {
      "id": 3,
      "title": "Овощной салат",
      "cooking_time": 10,
      "meal_role": "vegetables",
      "tags": ["vegetables", "quick", "low_calorie"]
    },
    {
      "id": 4,
      "title": "Томатный соус",
      "cooking_time": 5,
      "meal_role": "sauce",
      "tags": ["sauce", "quick"]
    }
  ],
  "include_vegetables": true,
  "include_sauce": false
}
```

---

## Пример ролей блюда

```text
full_meal   — полноценное блюдо
protein     — белковая часть
carbs       — гарнир / углеводы
vegetables  — овощи / салат
sauce       — соус
dessert     — десерт
snack       — перекус
drink       — напиток
```

`meal_role` в Pydantic-схемах ограничен через `Literal`, поэтому рецепты в request body проходят проверку только с разрешёнными значениями.

---

## Пример тегов рецептов

```text
quick         — быстрое блюдо
high_protein  — много белка
cheap         — недорогое
breakfast     — завтрак
dinner        — ужин
low_calorie   — низкокалорийное
comfort_food  — сытное / домашнее
healthy       — более полезное
```

Теги используются для фильтрации рекомендаций:

```text
GET /recommend/random-recipe?tag=quick
POST /recommend/random-recipe/by-request
```

---

## Зачем нужен этот сервис

В будущем основной backend, например Java/Spring Boot, сможет отправлять сюда список рецептов и фильтры.

Схема работы:

```text
Java backend
↓
отправляет список рецептов и фильтры
↓
Python FastAPI recommendation service
↓
выбирает рецепт или meal-комбинацию
↓
возвращает результат Java backend
```

---

## Текущий статус

Сейчас сервис умеет:

* запускаться через FastAPI;
* использовать структуру `app/`, `routers`, `services.py`, `schemas.py`;
* отдавать тестовые рецепты;
* искать рецепт по id;
* выбирать случайный рецепт;
* фильтровать рецепты по времени, роли и тегу;
* собирать meal-комбинацию;
* принимать список рецептов через POST-запрос;
* принимать request body с рецептами и фильтрами;
* валидировать `meal_role`;
* возвращать ошибки `404` и `422`;
* проверяться автотестами через `pytest`.
