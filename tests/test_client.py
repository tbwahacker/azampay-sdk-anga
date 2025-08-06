# tests/client_test.py

import os
import unittest
from unittest.mock import patch
from azampay.core import AzamPay

class TestAzamPayClient(unittest.TestCase):

    @patch('azampay.core.requests.post')
    def test_get_auth_token_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {
                "accessToken": "mocked_token_123"
            }
        }

        token = AzamPay.get_auth_token()
        self.assertEqual(token, "mocked_token_123")

    @patch('azampay.core.requests.post')
    def test_get_auth_token_failure(self, mock_post):
        mock_post.return_value.status_code = 401
        mock_post.return_value.text = "Unauthorized"

        with self.assertRaises(Exception) as context:
            AzamPay.get_auth_token()

        self.assertIn("Auth failed", str(context.exception))

    @patch('azampay.core.requests.post')
    def test_mno_checkout_success(self, mock_post):
        # Mock token call
        with patch('azampay.core.AzamPay.get_auth_token', return_value='mock_token'):
            # Mock checkout API response
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"status": "success", "message": "Transaction accepted"}

            response, external_id = AzamPay.mno_checkout(
                mobile_number="255712345678",
                amount=5000,
                currency="TZS",
                provider="Tigo",
                external_id="REF123456"
            )

            self.assertEqual(response['status'], "success")
            self.assertEqual(external_id, "REF123456")

if __name__ == '__main__':
    unittest.main()
