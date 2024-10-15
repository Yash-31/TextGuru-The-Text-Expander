# TextGuru: The Text Expander

> TextGuru is a versatile text expansion tool aimed at enhancing your typing efficiency. It allows users to create custom shortcuts that automatically expand into pre-defined phrases, sentences, or even commands. Running seamlessly in the background, it helps reduce repetitive typing, making it ideal for professionals and anyone seeking to optimize their workflow and save time.

**_Check the Release for TextGuru.exe for the tool. The `shortcuts.txt` file is necessary to run the tool._**

**DO NOT OPEN OR DELETE THE JSON FILE**

## How to Store Shortcuts:

1. The `shortcuts.txt` file is your friend. Use the text file to store all your shortcuts.
2. Each `Short` word and `Expansion` text is stored as a pair separated by colon "`:`". 
Example: `check:This is a test`. 
Here "`check`" is the short word and "`This is a test`" is corresponding Expansion text.
3. No numbering or quotes("") needed, and space is not recommended after the "`:`"
4. Each shortcut is stored on new line. Kindly follow it for best experience.

## How to use the Tool:
1. Double clicking the Application file will run the script.
2. Consider putting some `shortcuts` in the text file before running the script.
3. After you double click the application a GUI or a small window will appear on the screen.
4. Don't worry. It means the application is now running perfectly.
5. On the window there are two buttons "`Pause`" and "`End`". One to pause the tool but not end the script completely. the other button to end the tool. Pausing will stop the tool from listening to input and expand it immediately. So just pause the script when you don't want to use the tool and resume anytime.
6. Now open any text editor like MS Word to test the tool. 
7. Type the short word that you stored in text file. Considering my above example (`check:This is a test`). So type "`check`" and see the magic. It's case sensitive.
8. The word "`check`" will be replaced by is corresponding big text that is "`This is a test`".
9. The tool works with any application where you can type.

### IMPORTANT THINGS TO REMEMBER
1. There should be `no line gap` between two shortcuts defined in your text file `shortcuts.txt`
2. The short word that will be defined are case sensitive i.e. "`Hi`" is not same as "`hi`".
3. When the tool is running and you decide to add new shortcuts in the text file, please close/end the tool for changes to reflect before you start using the new shortcuts.


### Congratulations!!! Now you can use tool without problems.

### Happy Expanding!

## About the Tool
**TextGuru** is a text expander tool built using `Python`. It primarily utilizes the `pynput` library to listen to `keyboard inputs`, expanding user-defined shortcuts into full text phrases. The `PyQt5` library is employed to create a graphical user interface (GUI) where users can toggle between play/pause modes and stop the script. The expansion logic relies on continuously monitoring typed sequences, matching them with predefined shortcuts stored in external files (`.txt` and `.json`), and expanding them into longer phrases.

The tool handles expansion by tracking user input with `pynput.keyboard.Listener`, and when a shortcut is detected, the input is replaced with the expanded text. The `keyboard listener` is paused during the expansion to avoid interference, and shortcut configurations are loaded from files. The code also integrates password detection logic to prevent storage of passwords in the `.txt` file.

In summary, **TextGuru** works by combining keyboard event monitoring, text expansion logic, and a simple, interactive GUI for user control, ensuring smooth, controlled expansions.
