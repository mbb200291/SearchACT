import speech_recognition as sr


def recognize_speech_from_microphone(recognizer, microphone):
    """
    Transcript your speech to words predict.

    """
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError(
            f"recognizer must be Recognizer instance, not {type(recognizer)}"
        )

    if not isinstance(microphone, sr.Microphone):
        raise TypeError(
            f"microphone must be Microphone instance, not {type(microphone)}"
        )

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 0.8
        recognizer.phrase_time_limit = 8
        audio = recognizer.listen(source, timeout=3)

    response = {"Success": True, "error": None, "prediction": None}

    try:
        response["prediction"] = recognizer.recognize_google(audio, language="zh-TW")

    except sr.WaitTimeoutError as e:
        response["success"] = False
        response[
            "error"
        ] = f"listening timed out while waiting for phrase to start: {e}"

    except sr.UnknownValueError as e:
        # cannot recoginize
        response["success"] = False
        response["error"] = f"Google Speech Recognition could not understand audio: {e}"

    except sr.RequestError as e:
        # api end point error
        response["success"] = False
        response[
            "error"
        ] = f"Could not request results from Google Speech Recognition service: {e}"

    return response


if __name__ == "__main__":

    recognizer = sr.Recognizer()

    microphone = sr.Microphone()

    response = recognize_speech_from_microphone(recognizer, microphone)

    print(response)
