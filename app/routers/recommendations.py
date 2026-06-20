from fastapi import APIRouter, HTTPException

from app.data import recipes
from app.schemas import (
    RecipeRecommendation,
    MealRecommendation,
    RecipeListRequest,
)
from app.services import (
    recommend_random_recipe,
    recommend_random_meal,
    convert_recipes_to_dicts,
)

router = APIRouter(prefix="/recommend", tags=["recommendations"])


@router.get("/random-recipe", response_model=RecipeRecommendation)
def get_recommend_random_recipe(max_time: int = None, meal_role: str = None,
                                tag: str = None):
    recipe = recommend_random_recipe(recipes, max_time, meal_role, tag)
    if recipe is None:
        raise HTTPException(status_code=404, detail="No matching recipe found")
    return {"recipe": recipe}


@router.get("/random-meal", response_model=MealRecommendation)
def get_recommend_random_meal():
    meal = recommend_random_meal(recipes)
    if meal is None:
        raise HTTPException(
            status_code=404,
            detail="No complete meal could be recommended",
        )
    return {"meal": meal}


@router.post("/random-recipe/from-list",
             response_model=RecipeRecommendation)
def random_recipes_from_list(request: RecipeListRequest, max_time: int = None,
                             meal_role: str = None, tag: str = None):
    recipes_from_request = convert_recipes_to_dicts(request.recipes)
    recipe = recommend_random_recipe(recipes_from_request, max_time, meal_role,
                                     tag)
    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail="No matching recipe found in the provided list",
        )
    return {"recipe": recipe}


@router.post("/random-meal/from-list",
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
