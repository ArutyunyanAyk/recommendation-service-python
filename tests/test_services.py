from app.services import (
    recipe_matches_filters,
    recommend_random_meal,
    calculate_recipe_score,
)


def test_recipe_matches_filters_with_required_tags():
    recipe = {
        "id": 1,
        "title": "Омлет",
        "cooking_time": 10,
        "meal_role": "full_meal",
        "tags": ["breakfast", "quick", "high_protein"],
    }

    result = recipe_matches_filters(
        recipe,
        required_tags=["quick", "high_protein"],
    )

    assert result is True


def test_recipe_does_not_match_excluded_tags():
    recipe = {
        "id": 1,
        "title": "Острый омлет",
        "cooking_time": 10,
        "meal_role": "full_meal",
        "tags": ["breakfast", "quick", "spicy"],
    }

    result = recipe_matches_filters(
        recipe,
        required_tags=["quick"],
        excluded_tags=["spicy"],
    )

    assert result is False


def test_recommend_random_meal_with_required_parts():
    recipes = [
        {
            "id": 1,
            "title": "Котлеты",
            "cooking_time": 40,
            "meal_role": "protein",
            "tags": ["high_protein"],
        },
        {
            "id": 2,
            "title": "Макароны",
            "cooking_time": 15,
            "meal_role": "carbs",
            "tags": ["quick"],
        },
    ]

    meal = recommend_random_meal(recipes)

    assert meal is not None
    assert meal["protein"]["meal_role"] == "protein"
    assert meal["carbs"]["meal_role"] == "carbs"


def test_recommend_random_meal_returns_none_without_carbs():
    recipes = [
        {
            "id": 1,
            "title": "Котлеты",
            "cooking_time": 40,
            "meal_role": "protein",
            "tags": ["high_protein"],
        }
    ]

    meal = recommend_random_meal(recipes)

    assert meal is None


def test_recommend_random_meal_without_sauce():
    recipes = [
        {
            "id": 1,
            "title": "Котлеты",
            "cooking_time": 40,
            "meal_role": "protein",
            "tags": ["high_protein"],
        },
        {
            "id": 2,
            "title": "Макароны",
            "cooking_time": 15,
            "meal_role": "carbs",
            "tags": ["quick"],
        },
        {
            "id": 3,
            "title": "Томатный соус",
            "cooking_time": 5,
            "meal_role": "sauce",
            "tags": ["sauce", "quick"],
        },
    ]

    meal = recommend_random_meal(
        recipes,
        include_sauce=False,
        include_vegetables=True,
    )

    assert meal is not None
    assert "protein" in meal
    assert "carbs" in meal
    assert "sauce" not in meal


def test_recommend_random_meal_without_vegetables():
    recipes = [
        {
            "id": 1,
            "title": "Котлеты",
            "cooking_time": 40,
            "meal_role": "protein",
            "tags": ["high_protein"],
        },
        {
            "id": 2,
            "title": "Макароны",
            "cooking_time": 15,
            "meal_role": "carbs",
            "tags": ["quick"],
        },
        {
            "id": 3,
            "title": "Овощной салат",
            "cooking_time": 10,
            "meal_role": "vegetables",
            "tags": ["vegetables", "quick"],
        },
    ]

    meal = recommend_random_meal(
        recipes,
        include_vegetables=False,
        include_sauce=True,
    )

    assert meal is not None
    assert "protein" in meal
    assert "carbs" in meal
    assert "vegetables" not in meal


def test_calculate_recipe_score_with_matching_preferred_tags():
    recipe = {
        "id": 1,
        "title": "Омлет",
        "cooking_time": 10,
        "meal_role": "full_meal",
        "tags": ["breakfast", "quick", "high_protein"],
    }

    score = calculate_recipe_score(
        recipe,
        preferred_tags=["high_protein", "breakfast"],
    )

    assert score == 2


def test_calculate_recipe_score_without_matching_preferred_tags():
    recipe = {
        "id": 1,
        "title": "Макароны",
        "cooking_time": 15,
        "meal_role": "carbs",
        "tags": ["cheap", "quick"],
    }

    score = calculate_recipe_score(
        recipe,
        preferred_tags=["high_protein", "breakfast"],
    )

    assert score == 0


def test_recommend_random_meal_with_required_tags():
    recipes = [
        {
            "id": 1,
            "title": "Куриная грудка",
            "cooking_time": 25,
            "meal_role": "protein",
            "tags": ["high_protein", "quick"],
        },
        {
            "id": 2,
            "title": "Рис",
            "cooking_time": 20,
            "meal_role": "carbs",
            "tags": ["carbs", "quick"],
        },
        {
            "id": 3,
            "title": "Котлеты",
            "cooking_time": 40,
            "meal_role": "protein",
            "tags": ["high_protein", "dinner"],
        },
    ]

    meal = recommend_random_meal(
        recipes,
        required_tags=["quick"],
    )

    assert meal is not None
    assert "quick" in meal["protein"]["tags"]
    assert "quick" in meal["carbs"]["tags"]


def test_recommend_random_meal_with_excluded_tags():
    recipes = [
        {
            "id": 1,
            "title": "Куриная грудка",
            "cooking_time": 25,
            "meal_role": "protein",
            "tags": ["high_protein", "quick"],
        },
        {
            "id": 2,
            "title": "Рис",
            "cooking_time": 20,
            "meal_role": "carbs",
            "tags": ["carbs", "quick"],
        },
        {
            "id": 3,
            "title": "Острый соус",
            "cooking_time": 5,
            "meal_role": "sauce",
            "tags": ["sauce", "quick", "spicy"],
        },
        {
            "id": 4,
            "title": "Томатный соус",
            "cooking_time": 5,
            "meal_role": "sauce",
            "tags": ["sauce", "quick"],
        },
    ]

    meal = recommend_random_meal(
        recipes,
        include_sauce=True,
        required_tags=["quick"],
        excluded_tags=["spicy"],
    )

    assert meal is not None
    assert meal["sauce"] is not None
    assert "spicy" not in meal["sauce"]["tags"]
