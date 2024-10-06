from pi5neo import Pi5Neo
import time

def rainbow_cycle(neo, delay=0.1):
    colors = [
        (255, 0, 0),  # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (75, 0, 130),  # Indigo
        (148, 0, 211),  # Violet
        (0,0,0), # OFF
    ]
    for color in colors:
        neo.fill_strip(*color)
        neo.update_strip()
        time.sleep(delay)

def loading_bar(neo):
    for i in range(neo.num_leds):
        neo.set_led_color(i, 0, 255, 0)  # Green loading bar
        neo.update_strip()
        time.sleep(0.2)
    neo.clear_strip()
    neo.update_strip()




COLORS = {
    "RED": (255, 0, 0),
    "ORANGE": (255, 127, 0),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "INDIGO": (75, 0, 130),
    "VIOLET": (148, 0, 211),
    "OFF": (0, 0, 0),
    }

class LEDColor:
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def __eq__(self, other):
        if isinstance(other, LEDColor):
            return self.red == other.red and \
                    self.green == other.green and \
                    self.blue == other.blue
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def isOff(self):
        self.red == 0 and self.green == 0 and self.blue == 0

    def get_color(self):
        return (self.red, self.green, self.blue)

class LEDStripController:
    OFF = LEDColor()
    def __init__(self, neo: Pi5Neo, delay=0.2):
        self.neo: Pi5Neo = neo
        self.num_leds: int = neo.num_leds
        self.delay: float = delay
        self.layers: list[LEDLayer] = []
        self.render_layer = LEDLayer(self.num_leds, "render") 

    def add_layer(self, layer: list[LEDColor], layer_name):
        pass

    def flatten_layers(self):
        flattened_layer = LEDLayer(self.num_leds, "flattened")
        for layer in self.layers:
            flattened_layer += layer
        return flattened_layer

    def render_strip(self):
        new_render_layer = self.flatten_layers()
        for i in range(self.num_leds):
            self.neo.set_led_color(i, *(new_render_layer.get_color(i)))
        neo.update_strip()


class LEDLayer:
    def __init__(self, num_leds: int, name: str = ""):
        self.name = name
        self.num_leds = num_leds
        this.leds: list[LEDColor]
        self.clear()

    def clear(self):
        self.leds = self._clear_layer()
    
    def _clear_layer(self) -> list[LEDColor]:
        return [LEDColor() for _ in range(self.num_leds)]

    def set_color(self, color):
        self.set_color(color, 0, self.num_leds)

    def set_color(self, color, index):
        self.set_color(color, index, index+1)

    def get_color(self, index):
        return self.leds[index].get_color()

    def set_color(color, start, end):
        if not isinstance(color, LEDColor):
            raise TypeError("color is not of type LEDColor")
        if start < 0 or start > self.num_leds or end < 0 or end > self.num_leds:
            raise IndexError("Index out of bounds")
        
        for i in range(start, end):
            self.leds[i] = color

    def set_leds(self, leds):
        self.leds = leds

    def get_leds(self):
        return self.leds

    def __add__(self, other) -> "LEDLayer":
        combined = []
        for i in range(self.num_leds):
            if other.leds[i].isOff():
                combined.append(self.leds[i])
            else:
                combined.append(other.leds[i])

        combinedLayer = LEDLayer(self.num_leds, self.name)
        combinedLayer.set_leds(combined)

        return combinedLayer

    def __iadd__(self, other) -> "LEDLayer":
        combinedLayer = self.__add__(other)
        self.set_leds(combinedLayer.get_leds())
        return self


neo = Pi5Neo('/dev/spidev0.0', 150, 1000)
rainbow_cycle(neo)
loading_bar(neo)
neo.clear_strip()
neo.update_strip()
