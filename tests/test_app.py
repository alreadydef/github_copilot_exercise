import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_contains_chess_club(reset_activities):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data


def test_signup_and_remove_participant(reset_activities):
    # Arrange
    email = "tester@mergington.edu"
    activity = "Chess Club"

    # Act - sign up
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert signup_response.status_code == 200

    # Act - verify participant was added
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]

    # Act - remove participant
    remove_response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": email},
    )

    # Assert
    assert remove_response.status_code == 200
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]
