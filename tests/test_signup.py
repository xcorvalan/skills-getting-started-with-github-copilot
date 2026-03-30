"""Tests for POST /activities/{activity_name}/signup endpoint"""


def test_signup_successful(client):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@test.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_duplicate_registration_fails(client):
    """Test that duplicate signup is rejected"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_fails(client):
    """Test that signup to non-existent activity fails with 404"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@test.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_includes_email_in_participants(client):
    """Test that successful signup adds email to participants list"""
    # Arrange
    activity_name = "Programming Class"
    email = "newprogrammer@test.edu"

    # Act - signup
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert - verify signup success
    assert response.status_code == 200

    # Verify - check via GET request
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]
