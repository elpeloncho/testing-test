"""
Synthetic test fixtures for static analysis (SAST) and secret detection tools.
All tokens and keys in this file are dummy mock values for testing scanner detection rules.
"""

TEST_SYNTHETIC_API_KEY = "AKIAIOSFODNN7EXAMPLE"
TEST_DUMMY_SECRET_TOKEN = "fake_test_token_1234567890abcdef"
TEST_MOCK_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-ID1PhMogZqSpA28L7C_733AIerA-m_R0GkWQgM3y8"


def test_secrets_fixture_contains_mock_data():
    assert TEST_SYNTHETIC_API_KEY.startswith("AKIA")
    assert "fake_test_token" in TEST_DUMMY_SECRET_TOKEN
