"""Tests for GET /activities endpoint"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities with correct structure"""
    # Arrange - client fixture provides TestClient

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_get_activities_includes_required_fields(client):
    """Test that activities include all required fields"""
    # Arrange

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, details in activities.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)


def test_get_activities_participant_count_valid(client):
    """Test that participant counts are within valid range"""
    # Arrange

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, details in activities.items():
        participant_count = len(details["participants"])
        max_participants = details["max_participants"]
        assert participant_count <= max_participants
        assert participant_count >= 0
