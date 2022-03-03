import numpy as np
from os import walk
import time
import colormath as cm

ANIMATIONS_PATH = './matrices/'

animations = []
current_animation = []
global_animation_counter = 0
current_animation_counter = 0
Vector = list[int]


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


def read_music_extractors() -> Vector:
    """
        Imports the music extractors from the cache.
        Returns (vol, bpm, pitch)
    """

    # TODO: implement

    return (0, 0, 0)


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
        Returns the calculated animation state
    """

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