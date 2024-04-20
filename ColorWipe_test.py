import sys
sys.path.append('C:/Users/17344/Desktop/djangotest')
from unittest import TestCase
from unittest.mock import patch, MagicMock, call  
from Unit_Testing_Functions import colorWipe

class TestColorWipe(TestCase):

    @patch('Unit_Testing_Functions.time.sleep')  
    def test_color_wipe(self, mock_sleep):
        # Create a mock strip object
        mock_strip = MagicMock()
        mock_strip.setPixelColor = MagicMock()
        mock_strip.show = MagicMock()
        mock_strip.numPixels.return_value = 10  
        color = MagicMock()  
        wait_ms = 50
        colorWipe(mock_strip, color, wait_ms)
        calls = [call(i, color) for i in range(10)]  
        mock_strip.setPixelColor.assert_has_calls(calls, any_order=True)
        self.assertEqual(mock_strip.show.call_count, 10)
        self.assertEqual(mock_sleep.call_count, 10)
        mock_sleep.assert_called_with(wait_ms / 1000.0)

if __name__ == '__main__':
    import unittest
    unittest.main()
