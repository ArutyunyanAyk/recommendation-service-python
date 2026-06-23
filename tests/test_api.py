from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_recipes():
    response = client.get("/recipes")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "title" in data[0]
    assert "cooking_time" in data[0]
    assert "meal_role" in data[0]


def test_get_recipe_by_id():
    response = client.get("/recipes/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Омлет"


def test_get_recipe_not_found():
    response = client.get("/recipes/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_random_recipe():
    response = client.get("/recommend/random-recipe")

    assert response.status_code == 200

    data = response.json()

    assert "recipe" in data
    assert "id" in data["recipe"]
    assert "title" in data["recipe"]
    assert "cooking_time" in data["recipe"]
    assert "meal_role" in data["recipe"]


def test_random_recipe_with_max_time():
    response = client.get("/recommend/random-recipe?max_time=20")

    assert response.status_code == 200

    data = response.json()

    assert data["recipe"]["cooking_time"] <= 20


def test_random_recipe_not_found_by_time():
    response = client.get("/recommend/random-recipe?max_time=1")

    assert response.status_code == 404


def test_random_meal():
    response = client.get("/recommend/random-meal")

    assert response.status_code == 200

    data = response.json()

    assert "meal" in data
    assert "protein" in data["meal"]
    assert "carbs" in data["meal"]


def test_post_random_recipe_from_list():
    payload = {
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
            },
            {
                "id": 3,
                "title": "Макароны",
                "cooking_time": 15,
                "meal_role": "carbs"
            }
        ]
    }

    response = client.post("/recommend/random-recipe/from-list", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "recipe" in data
    assert "id" in data["recipe"]
    assert "title" in data["recipe"]
    assert "cooking_time" in data["recipe"]
    assert "meal_role" in data["recipe"]


def test_post_random_recipe_from_list_with_meal_role_filter():
    payload = {
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
            },
            {
                "id": 3,
                "title": "Макароны",
                "cooking_time": 15,
                "meal_role": "carbs"
            }
        ]
    }

    response = client.post(
        "/recommend/random-recipe/from-list?meal_role=protein",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recipe"]["meal_role"] == "protein"


def test_post_random_recipe_from_list_with_max_time_filter():
    payload = {
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
            },
            {
                "id": 3,
                "title": "Макароны",
                "cooking_time": 15,
                "meal_role": "carbs"
            }
        ]
    }

    response = client.post(
        "/recommend/random-recipe/from-list?max_time=20",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recipe"]["cooking_time"] <= 20


def test_post_random_recipe_from_list_not_found():
    payload = {
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

    response = client.post(
        "/recommend/random-recipe/from-list?max_time=1",
        json=payload
    )

    assert response.status_code == 404
    expected = (
        "No matching recipe found in the "
        "provided list"
    )
    assert response.json()["detail"] == expected


def test_post_random_meal_from_list():
    payload = {
        "recipes": [
            {
                "id": 1,
                "title": "Котлеты",
                "cooking_time": 40,
                "meal_role": "protein"
            },
            {
                "id": 2,
                "title": "Макароны",
                "cooking_time": 15,
                "meal_role": "carbs"
            },
            {
                "id": 3,
                "title": "Овощной салат",
                "cooking_time": 10,
                "meal_role": "vegetables"
            }
        ]
    }

    response = client.post("/recommend/random-meal/from-list", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "meal" in data
    assert "protein" in data["meal"]
    assert "carbs" in data["meal"]
    assert data["meal"]["protein"]["meal_role"] == "protein"
    assert data["meal"]["carbs"]["meal_role"] == "carbs"


def test_post_random_meal_from_list_not_enough_recipes():
    payload = {
        "recipes": [
            {
                "id": 1,
                "title": "Котлеты",
                "cooking_time": 40,
                "meal_role": "protein"
            },
            {
                "id": 2,
                "title": "Овощной салат",
                "cooking_time": 10,
                "meal_role": "vegetables"
            }
        ]
    }

    response = client.post("/recommend/random-meal/from-list", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "No complete meal could be recommended "
        "from the provided list"
    )


def test_post_random_recipe_from_list_invalid_meal_role():
    payload = {
        "recipes": [
            {
                "id": 1,
                "title": "Странный рецепт",
                "cooking_time": 10,
                "meal_role": "wrong_role"
            }
        ]
    }

    response = client.post("/recommend/random-recipe/from-list", json=payload)

    assert response.status_code == 422


def test_random_recipe_with_meal_role_filter():
    response = client.get("/recommend/random-recipe?meal_role=protein")

    assert response.status_code == 200

    data = response.json()

    assert data["recipe"]["meal_role"] == "protein"


def test_random_recipe_with_tag_filter():
    response = client.get("/recommend/random-recipe?tag=quick")

    assert response.status_code == 200

    data = response.json()

    assert "recipe" in data
    assert "quick" in data["recipe"]["tags"]


def test_random_recipe_with_unknown_tag():
    response = client.get("/recommend/random-recipe?tag=unknown_tag")

    assert response.status_code == 404
    assert response.json()["detail"] == "No matching recipe found"


def test_post_random_recipe_from_list_with_tag_filter():
    payload = {
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

    response = client.post(
        "/recommend/random-recipe/from-list?tag=quick",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "recipe" in data
    assert "quick" in data["recipe"]["tags"]


def test_post_random_recipe_by_request():
    payload = {
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
            },
            {
                "id": 3,
                "title": "Макароны",
                "cooking_time": 15,
                "meal_role": "carbs",
                "tags": ["cheap", "quick"]
            }
        ],
        "max_time": 20,
        "tag": "quick"
    }

    response = client.post(
        "/recommend/random-recipe/by-request",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "recipe" in data
    assert data["recipe"]["cooking_time"] <= 20
    assert "quick" in data["recipe"]["tags"]


def test_post_random_meal_by_request():
    payload = {
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
            }
        ]
    }

    response = client.post(
        "/recommend/random-meal/by-request",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "meal" in data
    assert "protein" in data["meal"]
    assert "carbs" in data["meal"]
    assert data["meal"]["protein"]["meal_role"] == "protein"
    assert data["meal"]["carbs"]["meal_role"] == "carbs"


def test_post_random_meal_by_request_not_enough_recipes():
    payload = {
        "recipes": [
            {
                "id": 1,
                "title": "Котлеты",
                "cooking_time": 40,
                "meal_role": "protein",
                "tags": ["high_protein"]
            }
        ]
    }

    response = client.post(
        "/recommend/random-meal/by-request",
        json=payload
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "No complete meal could be recommended "
        "from the provided request"
    )


def test_post_random_recipe_by_request_with_required_tags():
    payload = {
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
            },
            {
                "id": 3,
                "title": "Макароны",
                "cooking_time": 15,
                "meal_role": "carbs",
                "tags": ["cheap", "quick"]
            }
        ],
        "required_tags": ["quick", "high_protein"]
    }

    response = client.post(
        "/recommend/random-recipe/by-request",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "recipe" in data
    assert "quick" in data["recipe"]["tags"]
    assert "high_protein" in data["recipe"]["tags"]


def test_post_random_recipe_by_request_with_unknown_required_tag():
    payload = {
        "recipes": [
            {
                "id": 1,
                "title": "Омлет",
                "cooking_time": 10,
                "meal_role": "full_meal",
                "tags": ["breakfast", "quick", "high_protein"]
            }
        ],
        "required_tags": ["quick", "unknown_tag"]
    }

    response = client.post(
        "/recommend/random-recipe/by-request",
        json=payload
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "No matching recipe found in the "
        "provided request"
    )


def test_post_random_recipe_by_request_with_excluded_tags():
    payload = {
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
                "title": "Острые макароны",
                "cooking_time": 15,
                "meal_role": "carbs",
                "tags": ["cheap", "quick", "spicy"]
            }
        ],
        "required_tags": ["quick"],
        "excluded_tags": ["spicy"]
    }

    response = client.post(
        "/recommend/random-recipe/by-request",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "recipe" in data
    assert "quick" in data["recipe"]["tags"]
    assert "spicy" not in data["recipe"]["tags"]


def test_post_random_recipe_by_request_all_recipes_excluded():
    payload = {
        "recipes": [
            {
                "id": 1,
                "title": "Острый омлет",
                "cooking_time": 10,
                "meal_role": "full_meal",
                "tags": ["breakfast", "quick", "spicy"]
            }
        ],
        "required_tags": ["quick"],
        "excluded_tags": ["spicy"]
    }

    response = client.post(
        "/recommend/random-recipe/by-request",
        json=payload
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "No matching recipe found in the "
        "provided request"
    )


def test_post_random_recipe_by_request_with_preferred_tags():
    payload = {
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
                "title": "Котлеты",
                "cooking_time": 40,
                "meal_role": "protein",
                "tags": ["dinner", "high_protein"]
            }
        ],
        "required_tags": ["quick"],
        "preferred_tags": ["high_protein", "breakfast"]
    }
    rsponse = client.post(
        "/recommend/random-recipe/by-request",
        json=payload
    )

    assert rsponse.status_code == 200

    data = rsponse.json()

    assert "recipe" in data
    assert data["recipe"]["title"] == "Омлет"
    assert "quick" in data["recipe"]["tags"]
    assert "high_protein" in data["recipe"]["tags"]
    assert "breakfast" in data["recipe"]["tags"]
