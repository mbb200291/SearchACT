from os import path
from sys import argv

from pynput import keyboard
from pynput.keyboard import Controller
from pynput.keyboard import Key

from modules.audio_input import audioRecords
from modules.search import SearchACT

# default value if there is no **kwargs
PATH_OF_SCRIPT = path.dirname(argv[0])
PATH_DICT_DATA = path.join(PATH_OF_SCRIPT, "_dict_data.pkl")

# The key combination to check

flag = False


class keyboardCatcher(keyboard.Listener):
    """
    Keyboard class inherit from keyboard.Listener
    Use to catch on special keyboard press
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            on_press=self.on_press, on_release=self.on_release, *args, **kwargs
        )

        self.SearchACT = kwargs.pop("SearchACT", SearchACT)
        self.contact = kwargs.pop("contact")
        self.audio = kwargs.pop("audio", audioRecords())
        self.controller = Controller()

    def on_press(self, key):
        global flag
        # Use this to monitor event of keyboard pressing
        if key == keyboard.Key.esc:

            self.controller.press("e")
            self.controller.release("e")
            self.controller.press("x")
            self.controller.release("x")

            self.controller.press(Key.enter)
            self.controller.release(Key.enter)

        elif key == keyboard.Key.media_volume_up:
            if not flag:
                flag = True
                self.enter_audio_mode()

    def on_release(self, key):
        global flag
        # Use this when you want to Stop listener
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    def enter_audio_mode(self):
        global flag
        # print("Try to say something!", flush=True)
        print("\nMicrophone >>> ", end="")

        response = self.audio.recognize_speech_from_microphone()

        if response["Success"] is True:
            input_text = response["prediction"]
            searchact = self.SearchACT(self.contact.DICT_MAPPING_DATA)
            print(input_text, flush=True)
            ls_persons = searchact.get_person(input_text)
            if ls_persons:
                for person in ls_persons:
                    print("\n", ">" + "\t".join(person))
            else:
                print(f'\n "{input_text}" not found. Retry or type "exit" to exit.')

        else:
            print(f'\n{response["error"]}')

        print("Seach >>> ", end="", flush=True)
        flag = False


def main():

    KC = keyboardCatcher()
    KC.start()


if __name__ == "__main__":

    main()
