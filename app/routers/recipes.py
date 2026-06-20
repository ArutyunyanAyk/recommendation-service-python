from fastapi import APIRouter, HTTPException
from app.data import recipes
from app.schemas import Recipe
from app.services import find_recipe_by_id


router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("", response_model=list[Recipe])
def get_recipes():
    return recipes


@router.get("/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int):
    recipe = find_recipe_by_id(recipes, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe
