from src.config import (
    check_server_status,
    send_mock_c2_beacon,
    MOCK_SERVER_URL,
    MOCK_API_KEY,
    MOCK_DATABASE_PASSWORD,
    MOCK_ADMIN_PASSWORD,
    MOCK_CONFIG_VERSION,
    MOCK_C2_SERVER_URL,
)


def test_check_server_status():
    result = check_server_status()
    assert result["target_url"] == MOCK_SERVER_URL
    assert result["headers"]["Authorization"] == f"Bearer {MOCK_API_KEY}"
    assert result["status"] == "simulated_ok"


def test_mock_credentials_defined():
    assert MOCK_DATABASE_PASSWORD == "HardcodedSuperSecretPassword123!"
    assert MOCK_ADMIN_PASSWORD == "admin_hardcoded_password_test"


def test_send_mock_c2_beacon():
    res = send_mock_c2_beacon()
    assert res["beacon_url"] == MOCK_C2_SERVER_URL
    assert res["status"] == "simulation_only"
