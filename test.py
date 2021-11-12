import unittest
import json
import kwiktrans
from kwiktrans import *
from variables import availableLanguages


class ClipboardTests(unittest.TestCase):
    def test_pyperclipModule(self):
        """
        Test that the Pyperclip copy/paste functions work as expected
        """
        randomText = "Lorem Ipsum Dolor Sit Amet"
        pyperclip.copy(randomText)
        copiedText = pyperclip.paste()
        self.assertEqual(copiedText, randomText)

    def test_limitExceeded(self):
        """
        Test that the clipbaord is limited to 500 characters
        """
        # oversizedText is 700 characters long
        tooLongText = "Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Curabitur blandit " \
                      "tempus porttitor. Aenean lacinia bibendum nulla sed consectetur. Donec sed odio dui. Donec " \
                      "sed odio dui. Maecenas sed diam eget risus varius blandit sit amet non magna. Duis mollis, " \
                      "est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Donec " \
                      "ullamcorper nulla non metus auctor fringilla. Vivamus sagittis lacus vel augue laoreet " \
                      "rutrum faucibus dolor auctor. Aenean eu leo quam. Pellentesque ornare sem lacinia quam " \
                      "venenatis vestibulum. Curabitur blandit tempus porttitor. Nullam quis risus eget urna mollis " \
                      "ornare vel eu leo. Nullam quis risus eget urna mollis ornare vel eu leo. "
        pyperclip.copy(tooLongText)
        self.assertEqual(len(getClipboard()), 500)

    def test_noClipboard(self):
        """
        Test that a clipboard with no content returns None
        """
        noText = ""
        pyperclip.copy(noText)
        self.assertIsNone(getClipboard())

    def test_getClipboard(self):
        """
        Test that the getClipboard function works as expected by copying some provided dummy text
        """
        text = "Lorem Ipsum"
        pyperclip.copy(text)
        self.assertEqual(getClipboard(), text)


class SetLanguagePreferenceTests(unittest.TestCase):
    def test_readCurrentDefaultForeignLanguage(self):
        """
        Test that Kwiktrans identifies the foreign language found in preferences.json
        """
        self.assertEqual(defaultForeignLanguage, preferences['default_foreign_language'])
        print()
        print("Detected foreign language code: " + defaultForeignLanguage)
        print("Foreign language name: " + availableLanguages[defaultForeignLanguage].title())

    def test_readCurrentNativeLanguage(self):
        """
        Test that Kwiktrans identifies the native language found in preferences.json
        """
        self.assertEqual(nativeLanguage, preferences['native_language'])
        print()
        print("Detected native language code: " + nativeLanguage)
        print("Native language name: " + availableLanguages[nativeLanguage].title())


if __name__ == '__main__':
    unittest.main()
