import random
import socket
import json
import pyperclip
import rumps
from googletrans import Translator

from variables import availableLanguages

translator = Translator()


# rumps.debug_mode(True)

limitExceeded = False

with open('preferences.json', 'r') as preferencesFile:
    preferencesData = preferencesFile.read()
preferences = json.loads(preferencesData)
nativeLanguage = preferences['native_language']
defaultForeignLanguage = preferences['default_foreign_language']
nativeLanguageName = availableLanguages[nativeLanguage].title()
defaultForeignLanguageName = availableLanguages[defaultForeignLanguage].title()


def getOnlineStatus():
    """Return online status as a boolean"""
    try:
        socket.setdefaulttimeout(5)
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False


def getClipboard():
    """Get clipboard contents and check length"""
    global limitExceeded
    original = pyperclip.paste()
    limitExceeded = False
    if not getOnlineStatus():
        rumps.alert(title="Connection Error", ok="Close",
                    message="Please check that you are connected to the internet and try again.")
        return None

    if len(original) > 500:
        limitExceeded = True
        original = original[0:500]

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
        self.icon = "icon.icns"
        self.menu = [
            rumps.MenuItem(title="About KwikTrans"),
            None,
            rumps.MenuItem(title="Translate", icon='icon.icns', template=True, dimensions=(18, 18), key="T"),
            None,
            rumps.MenuItem(title="Detect Language", key="D"),
            rumps.MenuItem(title="Random", key="R"),
            None,
            # rumps.MenuItem(title="Preferences", callback=None)
        ]
        global nativeLanguage
        global defaultForeignLanguage

    @rumps.clicked("About KwikTrans")
    def aboutWindow(self, _):
        """Show a simple 'about' window."""
        rumps.alert(title="KwikTrans", ok="Close",
                    message="© 2021 Danny Taylor\nVersion: 1.0.1\nContact: hello@dannytaylor.se")

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

    @rumps.clicked("Translate")
    def autoTranslate(self, _):
        """Automatically translate text between native language and a default foreign language, based on source text
        language. """
        original = getClipboard()

        if not original:
            return

        if limitExceeded:
            windowMessage = "Character limit exceeded – only the first 500 characters are shown below:"
        else:
            windowMessage = ""

        translation = translator.translate(original, src=nativeLanguage, dest=defaultForeignLanguage)
        detectedLang = translator.detect(original)
        detectedLang = detectedLang.lang
        if detectedLang == nativeLanguage:
            windowTitle = str(nativeLanguageName + ' to ' + defaultForeignLanguageName)
            result = rumps.Window(title=windowTitle, cancel="Copy", default_text=translation.text,
                                  dimensions=(320, 320), message=windowMessage)
            response = result.run()
            if not response.clicked:
                pyperclip.copy(translation.text)
        elif detectedLang == defaultForeignLanguage:
            windowTitle = str(defaultForeignLanguageName + ' to ' + nativeLanguageName)
            translation = translator.translate(original, src=defaultForeignLanguage, dest=nativeLanguage)
            result = rumps.Window(title=windowTitle, cancel="Copy", default_text=translation.text,
                                  dimensions=(320, 320), message=windowMessage)
            response = result.run()
            if not response.clicked:
                pyperclip.copy(translation.text)
        else:
            translation = translator.translate(original, dest=nativeLanguage)
            windowTitle = str('To ' + nativeLanguageName)
            result = rumps.Window(title=windowTitle, cancel="Copy", default_text=translation.text,
                                  dimensions=(320, 320), message=windowMessage)
            response = result.run()
            if not response.clicked:
                pyperclip.copy(translation.text)

    @rumps.clicked("Random")
    def toRandom(self, _):
        """Starts a *super fun* quiz session and presents three possible language choices."""
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
            choices = random.sample(list(availableLanguages.values()), 2)
            choices.append(correctLanguage)
            random.shuffle(choices)
            choice1 = choices[0]
            choice2 = choices[1]
            choice3 = choices[2]
            correctChoice = choices.index(correctLanguage) + 1
            correctResponse = correctChoice + 1

            quiz = rumps.Window(title="What language is this:", cancel=None, ok="Admit Defeat",
                                default_text=translation.text, dimensions=(320, 320))
            quiz.add_buttons(choice1.title(), choice2.title(), choice3.title())

            response = quiz.run()

            if response.clicked == correctResponse:
                correct = rumps.alert(title="Correct!", cancel="Play again", ok="Close",
                                      message="Well done!")
                if correct:
                    return None
                else:
                    # Play again
                    self.toRandom(_)

            else:
                wrong = rumps.alert(title="Bad luck", cancel="Play again", ok="Close",
                                    message=f"Correct answer:\n\n{correctLanguage.title()}")
                if wrong:
                    return None
                else:
                    # Play again
                    self.toRandom(_)


if __name__ == "__main__":
    Kwiktrans().run()
