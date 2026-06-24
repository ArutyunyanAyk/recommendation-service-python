from app.services import recipe_matches_filters


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
