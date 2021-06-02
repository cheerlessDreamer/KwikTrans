# KwikTrans

###### Image coming soon!

> A menubar app for macOS that provides quick translations of short snippets of text into a desired language.

I'm a Brit living in Sweden and although I'm comfortable reading Swedish, occasionally a new word or phrase crops up that I can't understand. **Enter KwikTrans!**

Previously, I would manually copy and paste the text into Google Translate, but it always felt cumbersome to fire up a whole browser session just to translate a single word or idiom. KwikTrans takes the contents of the clipboard translates the text much faster than manually using Google Translate! 

As an interesting beginners test for myself, I also implemented a 'Random' function, where you can guess the correct language out of a choice of three, just for fun.

###### Current todos and problems include: 

- [ ] Preferences panel to change default language configuration (could use PyQt5)
- [ ] Before a GUI version is implemented, use a 'preferences.json' file to maintain preferences
- [ ] Add keybindings
- [ ] Add a right-click service
- [ ] Use full name of language ('Detect Language' and 'Random') instead of ISO code (maybe a flag emoji?)
- [ ] Inform when 'Copy Text' was successful (either change icon to 'Copied!' or use a native notification)
- [ ] Fix dark mode - still not working for windows and alerts
- [ ] Remove 'Random' mode?
- [ ] Implement auto-translate by language (if clipboard is English, translate to Swedish - and vice versa)
- [ ] Update version number in 'About' window automatically (use a Global Variable?)
