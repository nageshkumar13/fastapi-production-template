def test_signup_success(client, make_email):
    response = client.post(
        "/auth/signup",
        json={"email": make_email(), "password": "strongpass123"},
    )

    body = response.json()

    assert response.status_code == 201
    assert body["email"].endswith("@example.com")
    assert body["is_active"] is True
    assert "id" in body
    assert "created_at" in body
    assert "password_hash" not in body


def test_duplicate_signup_returns_conflict(client, make_email):
    email = make_email()

    first_response = client.post(
        "/auth/signup",
        json={"email": email, "password": "strongpass123"},
    )
    second_response = client.post(
        "/auth/signup",
        json={"email": email, "password": "strongpass123"},
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "success": False,
        "error": "Email is already registered",
    }


def test_login_success_returns_access_token(client, create_user):
    email, password, signup_response = create_user()

    response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    body = response.json()

    assert signup_response.status_code == 201
    assert response.status_code == 200
    assert body["message"] == "Login credentials verified successfully"
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["access_token"]
    assert body["user"]["email"] == email
    assert body["user"]["is_active"] is True
    assert "password_hash" not in body["user"]


def test_login_wrong_password_returns_unauthorized(client, create_user):
    email, _, signup_response = create_user()

    response = client.post(
        "/auth/login",
        json={"email": email, "password": "wrongpass123"},
    )

    assert signup_response.status_code == 201
    assert response.status_code == 401
    assert response.json() == {
        "success": False,
        "error": "Invalid email or password",
    }


def test_login_unknown_email_returns_unauthorized(client, make_email):
    response = client.post(
        "/auth/login",
        json={"email": make_email(), "password": "strongpass123"},
    )

    assert response.status_code == 401
    assert response.json() == {
        "success": False,
        "error": "Invalid email or password",
    }


def test_protected_route_returns_current_user(client, create_user):
    email, password, signup_response = create_user()
    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    token = login_response.json()["access_token"]
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

    body = response.json()

    assert signup_response.status_code == 201
    assert login_response.status_code == 200
    assert response.status_code == 200
    assert body["email"] == email
    assert body["is_active"] is True
    assert "id" in body
    assert "created_at" in body
    assert "password_hash" not in body


def test_protected_route_without_token_returns_unauthorized(client):
    response = client.get("/users/me")

    assert response.status_code == 401
    assert response.json() == {
        "success": False,
        "error": "Authentication credentials were not provided",
    }


def test_protected_route_with_invalid_token_returns_unauthorized(client):
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401
    assert response.json() == {
        "success": False,
        "error": "Invalid authentication token",
    }
