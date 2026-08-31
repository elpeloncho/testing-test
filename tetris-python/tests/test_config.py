from src.config import check_server_status, MOCK_SERVER_URL, MOCK_API_KEY


def test_check_server_status():
    result = check_server_status()
    assert result["target_url"] == MOCK_SERVER_URL
    assert result["headers"]["Authorization"] == f"Bearer {MOCK_API_KEY}"
    assert result["status"] == "simulated_ok"
