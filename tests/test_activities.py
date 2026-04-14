from src.app import activities


# ---------------------------------------------------------------------------
# GET /activities
# ---------------------------------------------------------------------------

class TestGetActivities:
    def test_returns_all_activities(self, client):
        # Arrange - no extra setup needed; fixture state is the full seed data

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_activity_has_required_fields(self, client):
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")

        # Assert
        for activity in response.json().values():
            assert required_fields.issubset(activity.keys())


# ---------------------------------------------------------------------------
# GET / (root redirect)
# ---------------------------------------------------------------------------

class TestRootRedirect:
    def test_redirects_to_static_index(self, client):
        # Arrange - no setup needed

        # Act
        response = client.get("/")

        # Assert
        assert response.status_code in (301, 302, 307, 308)
        assert response.headers["location"].endswith("/static/index.html")


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

class TestSignup:
    def test_signup_adds_participant(self, client):
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email},
        )

        # Assert
        assert response.status_code == 200
        assert new_email in activities[activity_name]["participants"]

    def test_signup_returns_confirmation_message(self, client):
        # Arrange
        activity_name = "Chess Club"
        new_email = "another@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email},
        )

        # Assert
        assert "message" in response.json()

    def test_signup_unknown_activity_returns_404(self, client):
        # Arrange
        activity_name = "Unknown Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404

    def test_signup_duplicate_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        existing_email = activities[activity_name]["participants"][0]

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email},
        )

        # Assert
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/participants
# ---------------------------------------------------------------------------

class TestUnregister:
    def test_unregister_removes_participant(self, client):
        # Arrange
        activity_name = "Chess Club"
        existing_email = activities[activity_name]["participants"][0]

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": existing_email},
        )

        # Assert
        assert response.status_code == 200
        assert existing_email not in activities[activity_name]["participants"]

    def test_unregister_returns_confirmation_message(self, client):
        # Arrange
        activity_name = "Chess Club"
        existing_email = activities[activity_name]["participants"][0]

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": existing_email},
        )

        # Assert
        assert "message" in response.json()

    def test_unregister_unknown_activity_returns_404(self, client):
        # Arrange
        activity_name = "Unknown Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404

    def test_unregister_participant_not_enrolled_returns_404(self, client):
        # Arrange
        activity_name = "Chess Club"
        unenrolled_email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": unenrolled_email},
        )

        # Assert
        assert response.status_code == 404
