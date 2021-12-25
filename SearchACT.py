"""
To lookup the contact info by query the name or other info.
"""
import os
import sys
import time
from os import path

from dotenv import load_dotenv

import modules.calculator as cal
from modules.audio_input import audioRecords
from modules.contact import Contact
from modules.help_info import help_
from modules.keyboardCatcher import keyboardCatcher
from modules.search import SearchACT


load_dotenv()

__author__ = os.getenv("AUTHOR", ["Ben Lin", "Bruce Chen", "Kuan Hang Lin"])
__license__ = os.getenv("LICENSE", "MIT 2.0")
__maintainer__ = os.getenv("MAINTAINER", ["Ben Lin", "Bruce Chen", "Kuan Hang Lin"])
__contact__ = os.getenv("CONTACT", "brucechen@actgenomics.com")
__email__ = os.getenv("EMAIL", "brucechen@actgenomics.com")
__status__ = os.getenv("STATUS", "Production")
__copyright__ = os.getenv("COPYRIGHT", "Copyright 2021, ACT Genomics Co., LTD.")
__deprecated__ = os.getenv("DEPRECATED", False)
__version__ = os.getenv("VERSION", "2.0.0")

PATH_OF_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PATH_DICT_DATA = path.join(PATH_OF_SCRIPT, "_dict_data.pkl")
LI_EXIST_WORDS = ["exit", "bye", "ex", "quit"]


def main():
    print(
        """Type part of name to search ACT contact.
        Type "*help" to get detail instruction.
        Type *cal to enter caculation mode.
        Type *mic or press media_volume_up to enter microphone mode.
        Type "exit" or press ESC to leave.
        """
    )

    if getattr(sys, "frozen", False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    while True:
        try:
            contact = Contact(application_path)
        except Exception as e:
            print(e)
            time.sleep(10)
        else:
            break

    calculator = cal.Calculator(cal.names, cal.ops)
    audio = audioRecords()

    while True:
        KC = keyboardCatcher(SearchACT=SearchACT, contact=contact, audio=audio)
        KC.start()

        str_input = input("\nSeach >>> ")

        # re-build contact dictionary
        if str_input in ["*update"]:
            print(contact.check_version())

        elif str_input in ["clear"]:
            os.system("cls" if os.name == "nt" else "clear")

        # add search term
        elif str_input in ["*addterm", "*add1"]:
            print("into adding mode")
            str_input_key = input(
                'Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit. >>> '
            ).lower()
            if str_input_key in LI_EXIST_WORDS:
                break
            elif not contact.key_exist(str_input_key):
                print("*** The ID not exist. ***")
                continue
            str_input_term = input(
                'Type the new search term or type "exit" to exit.\n>>> '
            ).lower()
            if str_input_term in LI_EXIST_WORDS:
                break
            ans = contact.add_searchTerm_to_key(str_input_term, str_input_key)
            if ans == 0:
                pass
            else:
                break

        # add contact info to key
        elif str_input in ["*addinfo", "*add2"]:
            str_input_key = input(
                'Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit.\n>>> '
            ).lower()
            if str_input_key in LI_EXIST_WORDS:
                break
            elif not contact.key_exist(str_input_key):
                print("*** The ID not exist. ***")
                continue
            str_add_info = input(
                'Type the new info of the person or type "exit" to exit.\n>>> '
            ).lower()
            if str_add_info in LI_EXIST_WORDS:
                break
            ans = contact.add_contact_info(str_input_key, str_add_info)
            if ans == 0:
                pass
            else:
                break

        # remove contact info function
        elif str_input in ["*rminfo", "*rm2"]:
            pass
            # contact.rm_ifno()

        # exit
        elif str_input in LI_EXIST_WORDS:
            break

        # say hello
        elif str_input in ["hi", "hello"]:
            print("HI")

        # calculator
        elif str_input in ["*cal", "*c", "$"]:
            print("Caculation_mode:")
            while True:
                str_input = input("\nCalculator >>> ")
                if str_input in LI_EXIST_WORDS:
                    break
                else:
                    try:
                        print("answer: ", str(calculator.cal(str_input)))
                    except Exception:
                        print("formula error !")
                        pass

        # audio input
        elif str_input in ["*microphone", "*mic"]:
            print("Try to say something!", flush=True)
            print("\nMicrophone >>> ", end="", flush=True)
            response = audio.recognize_speech_from_microphone()
            if response["prediction"] is not None:
                input_text = response["prediction"]
                searchact = SearchACT(contact.data)
                print(input_text, flush=True)
                ls_persons = searchact.get_person(input_text)
                if ls_persons:
                    for person in ls_persons:
                        print("\n", ">" + "\t".join(person))
                else:
                    print(f'\n "{input_text}" not found. Retry or type "exit" to exit.')

        # help info
        elif str_input in ["*help", "*h"]:
            print()
            print(f"    version: {__version__}")
            print(f'    contact version: {contact.data.get("*version")}')
            print(help_())

        # get version info
        elif str_input in ["*version", "*ver"]:
            print()
            print(f"    version: {__version__}")
            print(f'    contact version: {contact.data.get("*version")}')
        else:
            try:
                searchact = SearchACT(contact.data)
                ls_persons = searchact.get_person(str_input)
                if ls_persons:
                    for person in ls_persons:
                        print("\n", ">" + "\t".join(person))
                else:
                    print(f'\n "{str_input}" not found. Retry or type "exit" to exit.')
            # except error:
            except Exception:
                print("formula error !")
                pass


if __name__ == "__main__":
    main()
