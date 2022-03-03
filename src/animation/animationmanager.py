import numpy as np
from os import walk
import time
import pandas as pd
from colormath.color_objects import sRGBColor

### Data types
Vector = list[int]


### Constants
ANIMATIONS_PATH = './matrices/'
PITCH_COLORS_FILE = 'pitch_colors.txt'
PITCH_COLORS = []


### Global variables
animations = []
current_animation = []
global_animation_counter = 0
current_animation_counter = 0



def load_matrices() -> None:
    """
    Loads all animation-matrices into the global animations list
    """

    try:
        print('Importing animations...')

        for file in next(walk(ANIMATIONS_PATH))[2]:
            animations.append(np.loadtxt(ANIMATIONS_PATH + file, dtype='str'))

        print(str(len(animations)) + ' animation(s) imported.')
    except IOError:
        print('No animations found.')
        raise



def load_pitch_colors() -> None:
    """
        Loads the pitch color mapping matrix and sets it to the global constant
    """

    global PITCH_COLORS_FILE
    global PITCH_COLORS

    try:
        print('Importing pitch color matrix...')

        PITCH_COLORS = pd.read_csv(PITCH_COLORS_FILE, dtype='str', sep=' ', header=None).to_numpy()
    except IOError:
        print('Pitch color mappings could not be loaded.')
        raise



def convert_pitch_to_rbg(pitch) -> sRGBColor:
    """
        Converts the pitch to a color based on the Newton Color principle.
        The pitch is a string as 'Em' or 'F#'.
        The first row contains the Major Chords.
        The second row contains the Minor Chords.
        Rows 3, 4, 5 contain the R, G, B Value of the Chord
        The returned Vector is a sRGBColor
    """

    global PITCH_COLORS

    index = 0

    if (pitch[-1] != 'm'):
        index = np.where(PITCH_COLORS[0] == pitch)[0][0]
    else:
        index = np.where(PITCH_COLORS[1] == pitch)[0][0]
    
    return sRGBColor(PITCH_COLORS[2][index], PITCH_COLORS[3][index], PITCH_COLORS[4][index])




def read_music_extractors() -> Vector:
    """
        Imports the music extractors from the cache.
        Returns [vol: int, bpm: int, pitch: str]
    """

    # TODO: implement

    return (255, 120, 'C')



def show_leds(led_config = []) -> None:
    """
        Shows the passed configuration on the hardware.
        The length of the configuration has to be the size of the LED strip.
    """

    # TODO: implement
    print(led_config)




def add_extractors_to_animation_state(vol, pitch, animation_state = []) -> list:
    """
        Adds the extractors to the animation state.
        The pitch is a Vector of three values (r, g, b) with values from 0 to 255
        Returns the converted animation state
    """

    converted_animation_state = []
    rel_vol = vol / 255

    current_color = convert_pitch_to_rbg(pitch)

    for state in animation_state:
        rgb_state = sRGBColor.new_from_rgb_hex(state)
        rgb_state.rgb_r = current_color.rgb_r *  (rgb_state.rgb_r / 255 ) * rel_vol
        rgb_state.rgb_g = current_color.rgb_g *  (rgb_state.rgb_g / 255 ) * rel_vol
        rgb_state.rgb_b = current_color.rgb_b *  (rgb_state.rgb_b / 255 ) * rel_vol
        converted_animation_state.append(rgb_state)


    return converted_animation_state


def pause_animation(bpm) -> None:
    """
        Pauses the execution based on the passed bpm
    """

    try:
        time.sleep(60 / bpm / len(current_animation))
    except:
        print('No BPM passed.')
        pass



def main():
    global current_animation_counter, current_animation, global_animation_counter, animations

    load_matrices()
    load_pitch_colors()

    while True:

        current_animation = animations[global_animation_counter]

        while current_animation_counter < len(current_animation):
            vol, bpm, pitch = read_music_extractors()
            current_state = current_animation[current_animation_counter]
            adapted_current_state = add_extractors_to_animation_state(vol, pitch, current_state)
            show_leds(adapted_current_state)

            current_animation_counter += 1
            if (current_animation_counter >= len(current_animation)):
                current_animation_counter = 0

            pause_animation(bpm)
            

        global_animation_counter += 1
        if (global_animation_counter >= len(animations)):
            global_animation_counter = 0
        









if __name__ == "__main__":
    main()