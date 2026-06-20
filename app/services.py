import random


def find_recipe_by_id(recipes, recipe_id):
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            return recipe
    return None


def recommend_random_recipe(
    recipes,
    max_time: int = None,
    meal_role: str = None,
    tag=None
):
    filtered_recipes = []
    for recipe in recipes:
        if (
            (max_time is None or recipe["cooking_time"] <= max_time)
            and
            (meal_role is None or recipe["meal_role"] == meal_role)
            and
            (tag is None or tag in recipe.get("tags", []))
        ):
            filtered_recipes.append(recipe)
    if not filtered_recipes:
        return None
    else:
        return random.choice(filtered_recipes)


def recommend_random_meal(recipes):
    proteins = []
    carbs = []
    vegetables = []
    for recipe in recipes:
        if recipe["meal_role"] == "protein":
            proteins.append(recipe)
        elif recipe["meal_role"] == "carbs":
            carbs.append(recipe)
        elif recipe["meal_role"] == "vegetables":
            vegetables.append(recipe)
    if not proteins or not carbs:
        return None
    if vegetables:
        random_vegetable = random.choice(vegetables)
    random_protein = random.choice(proteins)
    random_carbs = random.choice(carbs)
    meal = {
        "protein": random_protein,
        "carbs": random_carbs
    }
    if vegetables:
        meal["vegetables"] = random_vegetable
    return meal


def convert_recipes_to_dicts(recipes):
    recipes_as_dicts = []
    for recipe in recipes:
        recipes_as_dicts.append(recipe.model_dump())
    return recipes_as_dicts
