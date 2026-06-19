from pydantic import BaseModel


class Recipe(BaseModel):
    id: int
    title: str
    cooking_time: int
    meal_role: str


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
