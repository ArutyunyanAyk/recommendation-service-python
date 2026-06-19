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

## Структура проекта

```text
recommendation-service-python/
  main.py
  data.py
  services.py
  schemas.py
  requirements.txt
  README.md
```

## Что делает каждый файл

```text
main.py
```

Главный файл FastAPI-приложения.  
Здесь находятся endpoints.

```text
data.py
```

Временные тестовые данные.  
Пока здесь хранится список рецептов.

```text
services.py
```

Логика сервиса.  
Здесь находятся функции поиска, фильтрации и подбора рецептов.

```text
schemas.py
```

Pydantic-схемы.  
Описывают структуру данных: Recipe, Meal, RecipeRecommendation и другие.

```text
requirements.txt
```

Список Python-библиотек, которые нужны для запуска проекта.

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
uvicorn main:app --reload
```

После запуска сервер будет доступен по адресу:

```text
http://127.0.0.1:8000
```

Документация API:

```text
http://127.0.0.1:8000/docs
```

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

Возвращает список тестовых рецептов из `data.py`.

```text
GET /recipes/{recipe_id}
```

Возвращает один рецепт по id.

---

### Recommendations

```text
GET /recommend/random-recipe
```

Возвращает случайный рецепт из локального списка `data.py`.

Поддерживает фильтры:

```text
max_time
meal_role
```

Пример:

```text
GET /recommend/random-recipe?max_time=20&meal_role=full_meal
```

---

```text
GET /recommend/random-meal
```

Собирает meal-комбинацию из локального списка `data.py`.

Пример ответа:

```json
{
  "meal": {
    "protein": {
      "id": 2,
      "title": "Котлеты",
      "cooking_time": 40,
      "meal_role": "protein"
    },
    "carbs": {
      "id": 3,
      "title": "Макароны",
      "cooking_time": 15,
      "meal_role": "carbs"
    },
    "vegetables": {
      "id": 4,
      "title": "Овощной салат",
      "cooking_time": 10,
      "meal_role": "vegetables"
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

Пример body:

```json
{
  "recipes": [
    {
      "id": 1,
      "title": "Омлет",
      "cooking_time": 10,
      "meal_role": "full_meal"
    },
    {
      "id": 2,
      "title": "Котлеты",
      "cooking_time": 40,
      "meal_role": "protein"
    }
  ]
}
```

Пример ответа:

```json
{
  "recipe": {
    "id": 1,
    "title": "Омлет",
    "cooking_time": 10,
    "meal_role": "full_meal"
  }
}
```

---

```text
POST /recommend/random-meal/from-list
```

Принимает список рецептов в body и пытается собрать meal-комбинацию.

Для успешной сборки нужны минимум:

```text
protein
carbs
```

Если есть `vegetables`, они добавляются дополнительно.

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

## Зачем нужен этот сервис

В будущем основной backend, например Java/Spring Boot, сможет отправлять сюда список рецептов.

Схема работы:

```text
Java backend
↓
отправляет список рецептов
↓
Python FastAPI service
↓
выбирает рецепт или meal-комбинацию
↓
возвращает результат Java backend
```

## Текущий статус

Сейчас сервис умеет:

- запускаться через FastAPI;
- отдавать тестовые рецепты;
- искать рецепт по id;
- выбирать случайный рецепт;
- фильтровать рецепты по времени и роли;
- собирать meal-комбинацию;
- принимать список рецептов через POST-запрос.