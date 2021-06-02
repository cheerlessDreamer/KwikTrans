import random
import socket

import pyperclip
import rumps
from googletrans import Translator

from variables import availableLanguages

translator = Translator()

rumps.debug_mode(True)


# TODO: • Preferences panel to change default language configuration (could use PyQt5)
#       • Before a GUI version is implemented, use a 'preferences.json' file to maintain preferences
#       • Add keybindings
#       • Add a right-click service
#       • Use full name of language ('Detect Language' and 'Random') instead of ISO code (maybe a flag emoji?)
#       • Inform when 'Copy Text' was successful (either change icon to 'Copied!' or use a native notification)
#       • Fix dark mode - still not working for windows and alerts
#       • Remove 'Random' mode?
#       • Implement auto-translate by language (if clipboard is English, translate to Swedish - and vice versa)
#       • Update version number in 'About' window automatically (use a Global Variable?)


def getOnlineStatus():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False


def getClipboard(source=None, destination=None):
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
        rumps.alert(title="KwikTrans", ok="Close",
                    message="© 2021 Danny Taylor\nVersion: 0.3.3\nContact: hello@dannytaylor.se")

    @rumps.clicked("Detect Language")
    def getLanguage(self, _):
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
        rumps.alert(title="Detected language:", message=detectedLanguage.lang)

    @rumps.clicked("🇬🇧 → 🇸🇪")
    def englishToSwedish(self, _):
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
            translation = translator.translate(original, dest=random.choice(availableLanguages))
            while detectedLang == translation.dest:
                translation = translator.translate(original, dest=random.choice(availableLanguages))

            correctAnswer = translation.dest
            choices = random.sample(availableLanguages, 2)
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
                correct = rumps.alert(title="Correct!", cancel="Play again", ok="Great!!",
                                      message="Well done!")
                # print("Well done!")
                if correct:
                    return None
                else:
                    # Play again
                    self.toRandom(_)

            else:
                wrong = rumps.alert(title="Bad luck", cancel="Play again", ok="Close",
                                    message=f"Correct answer = {translation.dest}")
                # print("User gave up")
                if wrong:
                    return None
                else:
                    # Play again
                    self.toRandom(_)


if __name__ == "__main__":
    Kwiktrans().run()
