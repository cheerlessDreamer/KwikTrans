import unittest
from kwiktrans import *


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
        text = "Lorem Ipsum"
        pyperclip.copy(text)
        self.assertEqual(getClipboard(), text)


if __name__ == '__main__':
    unittest.main()
