# Some if this is from http://nullege.com/codes/show/src@e@i@einstein-HEAD@Python25Einstein@Lib@subprocess.py/380/win32api.GetStdHandle
# and
# http://nullege.com/codes/show/src@v@i@VistA-HEAD@Python@Pexpect@winpexpect.py/901/win32console.GetStdHandle.PeekConsoleInput

from ctypes import *
import time
import threading

from win32api import STD_INPUT_HANDLE, STD_OUTPUT_HANDLE

from win32console import GetStdHandle, KEY_EVENT, ENABLE_WINDOW_INPUT, ENABLE_MOUSE_INPUT, ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT

import keyPress


class CaptureLines():
    def __init__(self):
        self.stopLock = threading.Lock()

        self.isCapturingInputLines = False

        self.inputLinesHookCallback = CFUNCTYPE(c_int)(self.inputLinesHook)
        self.pyosInputHookPointer = c_void_p.in_dll(pythonapi, "PyOS_InputHook")
        self.originalPyOsInputHookPointerValue = self.pyosInputHookPointer.value

        self.readHandle = GetStdHandle(STD_INPUT_HANDLE)
        self.readHandle.SetConsoleMode(ENABLE_LINE_INPUT|ENABLE_ECHO_INPUT|ENABLE_PROCESSED_INPUT)

    def inputLinesHook(self):

        self.readHandle.SetConsoleMode(ENABLE_LINE_INPUT|ENABLE_ECHO_INPUT|ENABLE_PROCESSED_INPUT)
        inputChars = self.readHandle.ReadConsole(10000000)
        self.readHandle.SetConsoleMode(ENABLE_LINE_INPUT|ENABLE_PROCESSED_INPUT)

        if inputChars == "\r\n":
            keyPress.KeyPress("\n")
            return 0

        inputChars = inputChars[:-2]

        inputChars += "\n"

        for c in inputChars:
            keyPress.KeyPress(c)

        self.inputCallback(inputChars)

        return 0


    def startCapture(self, inputCallback):
        self.stopLock.acquire()

        try:
            if self.isCapturingInputLines:
                raise Exception("Already capturing keystrokes")

            self.isCapturingInputLines = True
            self.inputCallback = inputCallback

            self.pyosInputHookPointer.value = cast(self.inputLinesHookCallback, c_void_p).value
        except Exception as e:
            self.stopLock.release()
            raise

        self.stopLock.release()

    def stopCapture(self):
        self.stopLock.acquire()

        try:
            if not self.isCapturingInputLines:
                raise Exception("Keystrokes already aren't being captured")

            self.readHandle.SetConsoleMode(ENABLE_LINE_INPUT|ENABLE_ECHO_INPUT|ENABLE_PROCESSED_INPUT)

            self.isCapturingInputLines = False
            self.pyosInputHookPointer.value = self.originalPyOsInputHookPointerValue

        except Exception as e:
            self.stopLock.release()
            raise

        self.stopLock.release()