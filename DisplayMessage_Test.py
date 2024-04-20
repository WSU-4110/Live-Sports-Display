import sys
sys.path.append('C:/Users/17344/Desktop/djangotest')
from unittest import TestCase
from unittest.mock import MagicMock, patch
from Unit_Testing_Functions import displayMessage

class TestDisplayMessage(TestCase):

    @patch('Unit_Testing_Functions.time.sleep')  
    @patch('Unit_Testing_Functions.getLedIndex', side_effect=lambda x, y, height: (x + y) % height)  
    def test_display_message(self, mock_get_led_index, mock_sleep):
        mock_strip = MagicMock()
        mock_strip.setPixelColor = MagicMock()
        mock_strip.numPixels.return_value = 768  
        char_map = {
            'A': [
                [0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 1, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1],
                [0, 0, 0, 0, 0],  
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ], 
            ' ': [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ]
        }
        message = "A A"
        wait_ms = 100
        displayMessage(mock_strip, message, wait_ms, char_map)
        self.assertTrue(mock_strip.setPixelColor.called)
        self.assertTrue(mock_strip.show.called)
        mock_sleep.assert_called_with(wait_ms / 10000.0)

if __name__ == '__main__':
    import unittest
    unittest.main()
