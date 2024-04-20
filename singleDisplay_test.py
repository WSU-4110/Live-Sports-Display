import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock
from Unit_Testing_Functions import run_single_display  

sys.path.append('C:/Users/17344/Desktop/djangotest')

class TestRunSingleDisplay(TestCase):

    @patch('Unit_Testing_Functions.paramiko.SSHClient')
    @patch('Unit_Testing_Functions.JsonResponse')
    def test_run_single_display_post_success(self, mock_json_response, mock_ssh_client):
        mock_ssh_instance = MagicMock()
        mock_ssh_client.return_value = mock_ssh_instance
        stdout_mock = MagicMock()
        stdout_mock.read.return_value = 'Success'.encode('utf-8')
        stderr_mock = MagicMock()
        stderr_mock.read.return_value = ''.encode('utf-8')
        mock_ssh_instance.exec_command.return_value = (MagicMock(), stdout_mock, stderr_mock)
        mock_request = MagicMock()
        mock_request.method = "POST"
        mock_request.body = '{"players": "Player1, Player2"}'.encode('utf-8')
        response = run_single_display(mock_request)
        mock_ssh_client.assert_called_once()
        mock_ssh_instance.connect.assert_called_with(hostname='us2.pitunnel.com', port=36471, username='jordan', password='CSC4110LSD')
        assert mock_ssh_instance.exec_command.call_count == 3, "exec_command should be called three times."
        mock_json_response.assert_called_once_with({"message": "Single display command executed successfully."})

if __name__ == '__main__':
    import unittest
    unittest.main()
