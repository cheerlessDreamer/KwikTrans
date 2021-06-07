import random
import socket

import pyperclip
import rumps
from googletrans import Translator

from variables import availableLanguages

translator = Translator()


# rumps.debug_mode(True)

def getOnlineStatus():
    """Return online status as a boolean"""
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False


def getClipboard(source=None, destination=None):
    """Get clipboard contents and check length"""
    original = pyperclip.paste()
    if not getOnlineStatus():
        rumps.alert(title="No Connection…", ok="Close",
                    message="We are having trouble connecting to the internet. Please try again later.")
        return None

    if len(original) > 500:
        original = original[0:500]
        translation = translator.translate(original, src=source, dest=destination)
        result = rumps.Window(title="Character limit exceeded…",
                              message="Maximum length is 500 characters. Here are the first 500 characters, "
                                      "translated…",
                              cancel="Copy", default_text=translation.text, dimensions=(320, 320))
        response = result.run()
        if not response.clicked:
            pyperclip.copy(translation.text)
            print("User clicked 'Copy'")
        return None

    if len(original) == 0:
        rumps.alert(title="Empty clipboard!",
                    message="Copy text to the clipboard to translate.")
        return None

    return original


class Kwiktrans(rumps.App):
    """The Kwiktrans object is a rumps application that houses all of the language functions."""

    def __init__(self):
        super(Kwiktrans, self).__init__(name="TestName")
        self.template = True
        self.icon = "icon.png"
        self.menu = ["About KwikTrans", "Preferences – Coming soon!", None, "Detect Language", "Random", "🇬🇧 → 🇸🇪",
                     "🇸🇪 → 🇬🇧", None]
        # self.nativeLanguage = pass
        # self.foreignLanguage = pass

    @rumps.clicked("About KwikTrans")
    def aboutWindow(self, _):
        """Show a simple 'about' window."""
        rumps.alert(title="KwikTrans", ok="Close",
                    message="© 2021 Danny Taylor\nVersion: 0.4.0\nContact: hello@dannytaylor.se")

    @rumps.clicked("Detect Language")
    def getLanguage(self, _):
        """Displays the language of text on the clipboard."""
        if not getOnlineStatus():
            rumps.alert(title="No Connection…", ok="Close",
                        message="We are having trouble connecting to the internet. Please try again later.")
            return None

        original = pyperclip.paste()

        if len(original) > 500:
            rumps.alert(title="Character-Limit Exceeded", cancel=None,
                        message="Please try again with less than 500 characters.")
            return None

        elif len(original) == 0:
            rumps.alert(title="Empty clipboard!",
                        message="Copy text to the clipboard to translate.")
            return None

        detectedLanguage = translator.detect(original)
        fullLanguage = availableLanguages[detectedLanguage.lang]
        rumps.alert(title="Detected language:", message=fullLanguage.title())

    @rumps.clicked("🇬🇧 → 🇸🇪")
    def englishToSwedish(self, _):
        """Translates text on the clipboard from English into Swedish."""
        original = getClipboard(source="en", destination="sv")
        if not original:
            return

        translation = translator.translate(original, src="en", dest="sv")
        result = rumps.Window(title="English to Swedish…", cancel="Copy", default_text=translation.text,
                              dimensions=(320, 320))
        response = result.run()
        if not response.clicked:
            pyperclip.copy(translation.text)
            # print("User clicked 'Copy'")

    @rumps.clicked("🇸🇪 → 🇬🇧")
    def swedishToEnglish(self, _):
        """Translates text on the clipboard from Swedish into English."""
        original = getClipboard(source="sv", destination="en")
        if not original:
            return

        translation = translator.translate(original, src="sv", dest="en")
        result = rumps.Window(title="Swedish to English…", cancel="Copy", default_text=translation.text,
                              dimensions=(320, 320))
        response = result.run()
        if response.clicked:
            pass
            # print("User clicked 'OK'")
        else:
            pyperclip.copy(translation.text)
            # print("User clicked 'Copy'")

    @rumps.clicked("Random")
    def toRandom(self, _):
        """Starts a super fun quiz session and presents three possible language choices."""
        if not getOnlineStatus():
            rumps.alert(title="No Connection…", ok="Close",
                        message="We are having trouble connecting to the internet. Please try again later.")
            return None

        original = pyperclip.paste()

        if len(original) > 500:
            rumps.alert(title="Character-Limit Exceeded", cancel=None,
                        message="Please try again with less than 500 characters.")
            return None

        elif len(original) == 0:
            rumps.alert(title="Empty clipboard!",
                        message="Copy text to the clipboard to translate.")
            return None
        else:
            detectedLang = translator.detect(original)
            detectedLang = detectedLang.lang
            translation = translator.translate(original, dest=random.choice(list(availableLanguages.keys())))
            while detectedLang == translation.dest:
                translation = translator.translate(original, dest=random.choice(list(availableLanguages.keys())))

            correctAnswer = translation.dest
            correctLanguage = availableLanguages[correctAnswer]
            choices = random.sample(list(availableLanguages.keys()), 2)
            choices.append(correctAnswer)
            random.shuffle(choices)
            choice1 = choices[0]
            choice2 = choices[1]
            choice3 = choices[2]

            correctChoice = choices.index(correctAnswer) + 1
            # print("Correct choice:", correctChoice)
            correctResponse = correctChoice + 1
            # print("Correct response value:", correctResponse)

            quiz = rumps.Window(title="What language is this:", cancel=None, ok="Admit Defeat",
                                default_text=translation.text, dimensions=(320, 320))
            quiz.add_buttons(choice1, choice2, choice3)

            response = quiz.run()

            if response.clicked == correctResponse:
                correct = rumps.alert(title="Correct!", cancel="Play again", ok="Great!",
                                      message="Well done!")
                # print("Well done!")
                if correct:
                    return None
                else:
                    # Play again
                    self.toRandom(_)

            else:
                wrong = rumps.alert(title="Bad luck", cancel="Play again", ok="Close",
                                    message=f"Correct answer:\n\n{correctLanguage.title()}")
                # print("User gave up")
                if wrong:
                    return None
                else:
                    # Play again
                    self.toRandom(_)


if __name__ == "__main__":
    Kwiktrans().run()
