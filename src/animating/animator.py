import numpy as np
from os import walk
import time
import pandas as pd
from colormath.color_objects import sRGBColor
import redis
from rpi_ws281x import PixelStrip, Color

### Data types
Vector = list[int]


### Constants
ANIMATIONS_PATH = './matrices/'
KEY_COLORS_FILE = 'key_colors.txt'
KEY_COLORS = []
LED_COUNT = 44          # Number of LED pixels.
LED_PIN = 18            # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10            # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False      # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0         # set to '1' for GPIOs 13, 19, 41, 45 or 53




def load_matrices() -> list:
    """
    Loads all animation-matrices into the global animations list
    """

    animations = []

    try:
        print('Importing animations...')

        for file in next(walk(ANIMATIONS_PATH))[2]:
            animations.append(np.loadtxt(ANIMATIONS_PATH + file, dtype='str'))

        print(str(len(animations)) + ' animation(s) imported.')
        return animations
    except IOError:
        print('No animations found.')
        raise



def load_key_colors() -> None:
    """
        Loads the key color mapping matrix and sets it to the global constant
    """

    global KEY_COLORS_FILE
    global KEY_COLORS

    try:
        print('Importing key color matrix...')

        KEY_COLORS = pd.read_csv(KEY_COLORS_FILE, dtype='str', sep=' ', header=None).to_numpy()
        print('Key color matrix imported.')
    except IOError:
        print('Key color mappings could not be loaded.')
        raise



def convert_key_to_rbg(key) -> sRGBColor:
    """
        Converts the key to a color based on the Newton Color principle.
        The key is a string as 'Em', 'F#' or 'Gbm'.
        Row 1 contains the Major Chords, written with '#'.
        Row 2 contains the Minor Chords, written with '#'.
        Row 3 contains the Major Chords, written with 'b'.
        Row 4 contains the Minor Chords, written with 'b'.
        Rows 5, 6, 7 contain the R, G, B Value of the Chord
        The returned Vector is a sRGBColor
    """

    global KEY_COLORS

    index = 0

    if (len(key) > 1 and key[1] == 'b'): # Chord is written as 'Gb' or 'Gbm'
        if (key[-1] == 'm'):
            index = np.where(KEY_COLORS[3] == key)[0][0]
        else:
            index = np.where(KEY_COLORS[2] == key)[0][0]
    else: # Chord is written as 'F#' or 'F#m'
        if (key[-1] == 'm'):
            index = np.where(KEY_COLORS[1] == key)[0][0]
        else:
            index = np.where(KEY_COLORS[0] == key)[0][0]
    
    return sRGBColor(float(KEY_COLORS[4][index]), float(KEY_COLORS[5][index]), float(KEY_COLORS[6][index]), is_upscaled=True)



def read_music_extractors(cache) -> Vector:
    """
        Imports the music extractors from the cache.
        Maps the values to fit to further computations.
        Returns [vol: int, bpm: int, key: str]
    """

    bpm_cached = int(float(cache.get('bpm'))) # bpm values
    vol_cached = int(float(cache.get('vol'))) # values from 0 to 15
    key_cached = (cache.get('key')).decode('utf-8')
    scale_cached = (cache.get('scale')).decode('utf-8')
    
    # Re-map cached volume value to 0 - 255
    vol_cached_min = 0
    vol_cached_max = 15
    vol_min = 0
    vol_max = 255
    vol = ((vol_cached - vol_cached_min) / (vol_cached_max - vol_cached_min)) * (vol_max - vol_min) + vol_min
    vol = 255 if vol > 255 else int(vol)

    # Re-map key and scale to suit the shortened version
    key = key_cached + ('m' if scale_cached == 'minor' else '')


    return (vol, bpm_cached, key)



def colorWipe(strip, color, wait_ms=50):
    """
        Wipe color across display a pixel at a time.
    """
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        
    strip.show()



def show_leds(strip, led_config = []) -> None:
    """
        Shows the passed configuration on the hardware.
        The length of the configuration has to be the size of the LED strip.
    """
    for i in range(strip.numPixels()):
        color = Color(int(led_config[i].rgb_r), int(led_config[i].rgb_g), int(led_config[i].rgb_b))
        strip.setPixelColor(i, color)
        
    strip.show()




def add_extractors_to_animation_state(vol, key, animation_state = []) -> list:
    """
        Adds the extractors to the animation state.
        The key is a Vector of three values (r, g, b) with values from 0 to 255
        Returns the converted animation state
    """

    converted_animation_state = []
    rel_vol = vol / 255

    current_color_tuple = convert_key_to_rbg(key).get_upscaled_value_tuple() # (r, g, b)

    for state in animation_state:
        rgb_downscaled = sRGBColor.new_from_rgb_hex(state)
        rgb_state_tuple = rgb_downscaled.get_upscaled_value_tuple() # (r, g, b)
        rgb_state = sRGBColor(rgb_state_tuple[0], rgb_state_tuple[1], rgb_state_tuple[2], is_upscaled=True)
        rgb_state.rgb_r = current_color_tuple[0] *  (rgb_state_tuple[0] / 255 ) * rel_vol
        rgb_state.rgb_g = current_color_tuple[1] *  (rgb_state_tuple[1] / 255 ) * rel_vol
        rgb_state.rgb_b = current_color_tuple[2] *  (rgb_state_tuple[2] / 255 ) * rel_vol
        converted_animation_state.append(rgb_state)


    return converted_animation_state


def pause_animation(bpm, begin_animation_time, current_animation_length) -> None:
    """
        Pauses the execution based on the passed bpm and begin_animation_time.
        begin_animation_time is a timestamp in nanoseconds
    """

    try:
        end_animation_time = time.time_ns()
        animation_time_diff = (end_animation_time - begin_animation_time)  / (10 ** 9) # convert to seconds
        time.sleep(60 / bpm / current_animation_length + animation_time_diff)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        print('Could not pause properly.')
    



def main():
    current_animation = []
    global_animation_counter = 0
    current_animation_counter = 0

    # Create redis instance
    cache = redis.Redis(host='172.28.1.4', port=6379, db=0)

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    animations = load_matrices()
    load_key_colors()

    try:

        while True:

            current_animation = animations[global_animation_counter]
            current_animation_counter = 0

            print('New animation started.')

            while current_animation_counter < len(current_animation):
                t1 = time.time_ns() # time before animation calculation in ns
                vol, bpm, key = read_music_extractors(cache)
                # TODO: remove
                # vol, bpm, key = (140, 124, 'C')
                current_state = current_animation[current_animation_counter]
                adapted_current_state = add_extractors_to_animation_state(vol, key, current_state)
                show_leds(strip, adapted_current_state)

                current_animation_counter += 1

                pause_animation(bpm, t1, len(current_animation))
                
            
            print('Animation ended.')
       
            global_animation_counter += 1
            if (global_animation_counter >= len(animations)):
                global_animation_counter = 0

    except KeyboardInterrupt:
        colorWipe(strip, Color(0, 0, 0), 10)
        exit()
        









if __name__ == "__main__":
    main()