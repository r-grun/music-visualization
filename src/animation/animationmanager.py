import numpy as np
from os import walk
import time
from colormath.color_objects import sRGBColor

### Data types
Vector = list[int]


### Constants
ANIMATIONS_PATH = './matrices/'
PITCH_COLORS_FILE = 'pitch_colors.txt'
PITCH_COLORS = []

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



def load_pitch_colors() -> None:
    """
        Loads the pitch color mapping matrix and sets it to the global constant
    """

    try:
        PITCH_COLORS = np.loadtxt(PITCH_COLORS_FILE, dtype='str')
    except IOError:
        print('Pitch color mappings could not be loaded.')



def convert_pitch_to_rbg(pitch) -> sRGBColor:
    """
        Converts the pitch to a color based on the Newton Color principle.
        The pitch is a string as 'Em minor' or 'F# major'.
        The returned Vector is a sRGBColor
    """
    


def read_music_extractors() -> Vector:
    """
        Imports the music extractors from the cache.
        Returns [vol: int, bpm: int, pitch: str]
    """

    # TODO: implement

    return [0, 0, 'str']


def show_leds(led_config = []) -> None:
    """
        Shows the passed configuration on the hardware.
        The length of the configuration has to be the size of the LED strip.
    """

    # TODO: implement

    pass



def add_extractors_to_animation_state(vol, pitch, animation_state = []) -> list:
    """
        Adds the extractors to the animation state.
        The pitch is a Vector of three values (r, g, b) with values from 0 to 255
        Returns the calculated animation state
    """

    rel_vol = vol / 255

    for state in animation_state:
        rgb_state = sRGBColor.new_from_rgb_hex(current_animation[current_animation_counter])
        rgb_state.rgb_r = rgb_state.rgb_r * rel_vol

    # TODO: implement

    pass


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
    load_matrices()

    while True:

        current_animation = animations[global_animation_counter]

        while current_animation_counter < len(current_animation):
            vol, bpm, pitch = read_music_extractors()
            current_state = current_animation[current_animation_counter]
            adapted_current_state = add_extractors_to_animation_state(vol, pitch, current_state)
            show_leds(adapted_current_state)

            current_animation_counter += 1
            if (current_animation_counter > len(current_animation)):
                current_animation_counter = 0

            pause_animation(bpm)
            

        animation_counter += 1
        if (animation_counter > len(animations)):
            animation_counter = 0
        









if __name__ == "__main__":
    main()