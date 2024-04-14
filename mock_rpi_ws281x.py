# mock_rpi_ws281x.py

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __eq__(self, other):
        if isinstance(other, Color):
            return self.r == other.r and self.g == other.g and self.b == other.b
        return False


class PixelStrip(object):
    def __init__(self, led_count, pin, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0, strip_type=None):
        self.led_count = led_count
        self.pin = pin
        self.freq_hz = freq_hz
        self.dma = dma
        self.invert = invert
        self.brightness = brightness
        self.channel = channel
        self.strip_type = strip_type
        self.pixels = [Color(0, 0, 0) for _ in range(led_count)]

    def begin(self):
        print("Mock PixelStrip initialized")

    def show(self):
        print("Displaying Mock LED colors")

    def setPixelColor(self, i, color):
        if 0 <= i < self.led_count:
            self.pixels[i] = color

    def setBrightness(self, brightness):
        self.brightness = brightness

    def numPixels(self):
        return self.led_count
