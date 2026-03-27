from fastapi.testclient import TestClient

from app.main import app
from app.repository import ExerciseRepository
from app.routes import get_repository


NOT_FOUND_DETAIL = "Exercise not found"


def exercise_payload(**overrides):
    payload = {
        "name": "Push Up",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["triceps", "shoulders"],
        "equipment": "bodyweight",
        "difficulty": "beginner",
        "instructions": "Keep your body in a straight line.",
        "media_url": "https://example.com/push-up",
    }
    payload.update(overrides)
    return payload


def create_test_client() -> TestClient:
    repository = ExerciseRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    return TestClient(app)


def request_with_fresh_client(method: str, path: str, **kwargs):
    with create_test_client() as client:
        response = getattr(client, method)(path, **kwargs)
    app.dependency_overrides.clear()
    return response


def test_create_valid_exercise_successfully():
    response = request_with_fresh_client("post", "/exercises", json=exercise_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Push Up"
    assert data["primary_muscles"] == ["chest"]


def test_reject_invalid_muscle_group():
    response = request_with_fresh_client(
        "post",
        "/exercises",
        json=exercise_payload(primary_muscles=["wings"]),
    )

    assert response.status_code == 422


def test_reject_blank_name():
    response = request_with_fresh_client("post", "/exercises", json=exercise_payload(name="   "))

    assert response.status_code == 422


def test_reject_empty_primary_muscles():
    response = request_with_fresh_client("post", "/exercises", json=exercise_payload(primary_muscles=[]))

    assert response.status_code == 422


def test_reject_overlap_between_primary_and_secondary_muscles():
    response = request_with_fresh_client(
        "post",
        "/exercises",
        json=exercise_payload(primary_muscles=["chest"], secondary_muscles=["chest"]),
    )

    assert response.status_code == 422


def test_reject_invalid_media_url():
    response = request_with_fresh_client(
        "post",
        "/exercises",
        json=exercise_payload(media_url="not-a-valid-url"),
    )

    assert response.status_code == 422


def test_get_all_exercises():
    with create_test_client() as client:
        client.post("/exercises", json=exercise_payload())
        client.post(
            "/exercises",
            json=exercise_payload(
                name="Squat",
                primary_muscles=["quadriceps"],
                secondary_muscles=["glutes", "hamstrings"],
            ),
        )
        response = client.get("/exercises")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Push Up"
    assert data[1]["name"] == "Squat"


def test_get_one_exercise_by_id():
    with create_test_client() as client:
        create_response = client.post("/exercises", json=exercise_payload())
        exercise_id = create_response.json()["id"]
        response = client.get(f"/exercises/{exercise_id}")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["name"] == "Push Up"


def test_return_404_for_non_existent_id():
    response = request_with_fresh_client("get", "/exercises/999")

    assert response.status_code == 404
    assert response.json()["detail"] == NOT_FOUND_DETAIL


def test_update_existing_exercise():
    with create_test_client() as client:
        create_response = client.post("/exercises", json=exercise_payload())
        exercise_id = create_response.json()["id"]
        response = client.put(
            f"/exercises/{exercise_id}",
            json=exercise_payload(
                name="Incline Push Up",
                difficulty="intermediate",
                instructions="Place your hands on an elevated surface.",
            ),
        )
    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == exercise_id
    assert data["name"] == "Incline Push Up"
    assert data["difficulty"] == "intermediate"


def test_update_non_existent_exercise():
    response = request_with_fresh_client(
        "put",
        "/exercises/999",
        json=exercise_payload(name="Updated Push Up"),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == NOT_FOUND_DETAIL


def test_delete_existing_exercise():
    with create_test_client() as client:
        create_response = client.post("/exercises", json=exercise_payload())
        exercise_id = create_response.json()["id"]
        delete_response = client.delete(f"/exercises/{exercise_id}")
        get_response = client.get(f"/exercises/{exercise_id}")
    app.dependency_overrides.clear()

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_delete_same_exercise_twice_second_time_should_fail():
    with create_test_client() as client:
        create_response = client.post("/exercises", json=exercise_payload())
        exercise_id = create_response.json()["id"]
        first_delete = client.delete(f"/exercises/{exercise_id}")
        second_delete = client.delete(f"/exercises/{exercise_id}")
    app.dependency_overrides.clear()

    assert first_delete.status_code == 204
    assert second_delete.status_code == 404
