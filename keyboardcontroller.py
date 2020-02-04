from pynput.keyboard import Key, KeyCode
from keys import Keys


class KeyboardController:

    def __init__(self, key_combinations: tuple, fs_to_call: tuple):
        self.current_keys = []
        self.combinations = {}
        for keys, f_to_call in zip(key_combinations, fs_to_call):  # fs_to_call - functions to call
            combination = []
            for key in keys:
                if key in Keys.keys.keys():
                    combination.append(Keys.keys[key])
                else:
                    combination.append(KeyCode(char=key))

            self.combinations[frozenset(combination)] = f_to_call

    def on_press(self, key):
        self.current_keys.append(key)
        if frozenset(self.current_keys) in self.combinations.keys():
            self.combinations[frozenset(self.current_keys)]()

    def on_release(self, key):
        self.current_keys.remove(key)
