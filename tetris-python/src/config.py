"""
Configuration and mock server endpoints for test environments.
Contains synthetic placeholder configuration and dummy endpoint definitions.
"""

# Synthetic dummy credentials for testing SAST/security scanners
MOCK_CONFIG_VERSION = "1.0.1"
MOCK_API_KEY = "dummy_fake_api_key_for_testing_12345"
MOCK_SERVER_URL = "https://api.example.com/v1/ping"
MOCK_DATABASE_PASSWORD = "HardcodedSuperSecretPassword123!"
MOCK_ADMIN_PASSWORD = "admin_hardcoded_password_test"


def check_server_status(server_url: str = MOCK_SERVER_URL, api_key: str = MOCK_API_KEY) -> dict:
    """
    Simulates a connection check to a remote endpoint.
    Returns dummy status data for testing network integrations.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "TetrisApp-TestClient/1.0",
    }
    return {
        "target_url": server_url,
        "headers": headers,
        "status": "simulated_ok",
    }
