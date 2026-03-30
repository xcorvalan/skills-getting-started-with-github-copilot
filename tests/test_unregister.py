"""Tests for DELETE /activities/{activity_name}/unregister endpoint"""


def test_unregister_successful(client):
    """Test successful unregistration from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert email in data["message"]


def test_unregister_not_registered_fails(client):
    """Test that unregister for non-registered student fails"""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@test.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"].lower()


def test_unregister_nonexistent_activity_fails(client):
    """Test that unregister from non-existent activity fails with 404"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@test.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_unregister_removes_email_from_participants(client):
    """Test that successful unregister removes email from participants list"""
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act - unregister
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert - verify unregister success
    assert response.status_code == 200

    # Verify - check via GET request
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity_name]["participants"]
