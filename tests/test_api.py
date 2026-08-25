from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    # Arrange
    root_path = "/"

    # Act
    response = client.get(root_path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_catalog(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in payload
    assert "participants" in payload[expected_activity]


def test_signup_for_activity_succeeds(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"



def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"



def test_signup_duplicate_student_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"



def test_unregister_from_activity_succeeds(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"



def test_unregister_from_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"



def test_unregister_student_not_signed_up_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "notenrolled@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
