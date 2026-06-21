from pydantic import BaseModel, Field
from typing import Literal, Optional


MealRole = Literal[
    "full_meal",
    "protein",
    "carbs",
    "vegetables",
    "sauce",
    "dessert",
    "snack",
    "drink",
]


class Recipe(BaseModel):
    id: int
    title: str
    cooking_time: int
    meal_role: MealRole
    tags: list[str] = Field(default_factory=list)


class RecipeRecommendation(BaseModel):
    recipe: Recipe


class Meal(BaseModel):
    protein: Recipe
    carbs: Recipe
    vegetables: Recipe | None = None


class MealRecommendation(BaseModel):
    meal: Meal


class RecipeListRequest(BaseModel):
    recipes: list[Recipe]


class RecipeRecommendationRequest(BaseModel):
    recipes: list[Recipe]
    max_time: Optional[int] = None
    MealRole: Optional[MealRole] = None
    tag: Optional[str] = None
