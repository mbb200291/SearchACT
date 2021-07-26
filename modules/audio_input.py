import speech_recognition


class audioRecords:
    def __init__(self, recognizer=None, microphone=None):
        self.recognizer = (
            speech_recognition.Recognizer() if recognizer is None else recognizer
        )
        self.microphone = (
            speech_recognition.Microphone() if microphone is None else microphone
        )

        if not isinstance(self.recognizer, speech_recognition.Recognizer):
            raise TypeError(
                f"recognizer must be Recognizer instance, not {type(self.recognizer)}"
            )

        if not isinstance(self.microphone, speech_recognition.Microphone):
            raise TypeError(
                f"microphone must be Microphone instance, not {type(self.microphone)}"
            )

    def recognize_speech_from_microphone(self):
        """
        Transcript your speech to words predict.

        """
        response = {"Success": True, "error": None, "prediction": None}

        try:

            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # self.recognizer.pause_threshold = 0.8
                self.recognizer.phrase_time_limit = 3
                # print("Try to say something!")
                audio = self.recognizer.listen(source, timeout=3)

            record_chinese = self.recognizer.recognize_google(audio, language="zh-TW")
            # record_english = self.recognizer.recognize_google(audio, language ="en-US")

            response["prediction"] = record_chinese
            return response

        except speech_recognition.WaitTimeoutError as e:
            response["Success"] = False
            response[
                "error"
            ] = f"listening timed out while waiting for phrase to start: {e}"
            return response

        except speech_recognition.UnknownValueError as e:
            # cannot recoginize
            response["Success"] = False
            response[
                "error"
            ] = f"Google Speech Recognition could not understand audio: {e}"
            return response

        except speech_recognition.RequestError as e:
            # api end point error
            response["Success"] = False
            response[
                "error"
            ] = f"Could not request results from Google Speech Recognition service: {e}"

            return response

        except OSError as e:
            # OSError
            response["Success"] = False
            response["error"] = f"OSError: {e}"

            return response


if __name__ == "__main__":

    audio_obj = audioRecords()

    response = audio_obj.recognize_speech_from_microphone()

    # print(response)
