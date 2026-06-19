from fastapi import FastAPI, HTTPException
from services import (
    find_recipe_by_id,
    recommend_random_recipe,
    recommend_random_meal,
    convert_recipes_to_dicts,
)
from data import recipes
from schemas import (
    Recipe,
    RecipeRecommendation,
    MealRecommendation,
    RecipeListRequest,
)

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/hello")
def hello_check():
    return {"message": "Hello, World!"}


@app.get("/recipes", response_model=list[Recipe])
def get_recipes():
    return recipes


@app.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int):
    recipe = find_recipe_by_id(recipes, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe


@app.get("/recommend/random-recipe", response_model=RecipeRecommendation)
def get_recommend_random_recipe(max_time: int = None, meal_role: str = None):
    recipe = recommend_random_recipe(recipes, max_time, meal_role)
    if recipe is None:
        raise HTTPException(status_code=404, detail="No matching recipe found")
    return {"recipe": recipe}


@app.get("/recommend/random-meal", response_model=MealRecommendation)
def get_recommend_random_meal():
    meal = recommend_random_meal(recipes)
    if meal is None:
        raise HTTPException(
            status_code=404,
            detail="No complete meal could be recommended",
        )
    return {"meal": meal}


@app.post("/recommend/random-recipe/from-list",
          response_model=RecipeRecommendation)
def random_recipes_from_list(request: RecipeListRequest, max_time: int = None,
                             meal_role: str = None):
    recipes_from_request = convert_recipes_to_dicts(request.recipes)
    recipe = recommend_random_recipe(recipes_from_request, max_time, meal_role)
    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail="No matching recipe found in the provided list",
        )
    return {"recipe": recipe}


@app.post("/recommend/random-meal/from-list",
          response_model=MealRecommendation)
def random_meal_from_list(request: RecipeListRequest):
    recipes_from_request = convert_recipes_to_dicts(request.recipes)
    meal = recommend_random_meal(recipes_from_request)
    if meal is None:
        raise HTTPException(
            status_code=404,
            detail="No complete meal could be recommended from"
                   " the provided list",
        )
    return {"meal": meal}
