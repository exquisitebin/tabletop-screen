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
        (148, 0, 211)  # Violet
    ]
    for color in colors:
        neo.fill_strip(*color)
        neo.update_strip()
        time.sleep(delay)




#Breathing Effect for a Single LED (LED slowly fades in and out)

def breathing_led(neo, led_index, color, steps=50, delay=0.05):
    for i in range(steps):
        intensity = int(255 * (i / steps))  # Gradually increase intensity
        neo.set_led_color(led_index, *(intensity if c > 0 else 0 for c in color))  # Adjust brightness
        neo.update_strip()
        time.sleep(delay)
    for i in range(steps, 0, -1):
        intensity = int(255 * (i / steps))  # Gradually decrease intensity
        neo.set_led_color(led_index, *(intensity if c > 0 else 0 for c in color))
        neo.update_strip()
        time.sleep(delay)



neo = Pi5Neo('/dev/spidev0.0', 150, 1000)
rainbow_cycle(neo)
while True:
    breathing_led(neo, 0, (255, 125, 0))
