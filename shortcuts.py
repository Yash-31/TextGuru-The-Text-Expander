import os
from pynput import keyboard
import time
import json
import threading
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

typed_sequence = ""
running = True
expansion_mode = False
expanding = False
paused=False

app = QApplication(sys.argv)

def pause_input(duration):
    global paused
    paused = True
    print(f"Pausing input for {duration} seconds.")
    t = threading.Timer(duration, resume_input)
    t.start()

def resume_input():
    global paused
    paused = False
    print("Resuming input.")

def toggle_play_pause():
    global expansion_mode
    expansion_mode = not expansion_mode
    play_pause_button.setText("Play" if expansion_mode else "Pause")

def end_script():
    global running
    running = False
    app.quit()

def show_alert(value):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(f"A password is not allowed. This is a password: {value}")
    msg.setDetailedText("Please remove the shortcut that contains the password from the text file and run the tool again.")
    msg.setWindowTitle("Password Alert")
    msg.exec_()

def cal_space(x):
    c=0
    for i in x:
       if(i.isspace()):
            c+=1
    return c

def cal_len(x):
    return len(str(x))

def cal_capL(x):
    x=str(x)
    cnt=0
    for i in x:
        if(i.isupper()):
            cnt+=1
    return cnt

def cal_smL(x):
    x=str(x)
    cnt=0
    for i in x:
        if(i.islower()):
            cnt+=1
    return cnt

def cal_spc(x):
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~\\"
    x=str(x)
    cnt=0
    for c in x:
        if c in special_characters:
            cnt+=1
    return cnt

def cal_num(x):
    x=str(x)
    cnt=0
    for i in x:
        if(i.isnumeric()):
            cnt+=1
    return cnt

def is_password(value):
    spc = cal_space(value)
    
    if spc>=1:
        return False
    
    return 6 <= cal_len(value)<=16 and cal_capL(value)>=1 and cal_num(value)>=1 and cal_smL(value)>=1 and cal_spc(value)>=1

def read_shortcuts_from_text_file(file_path, delimiter=':'):
    global running
    sh = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(delimiter)
            value = value.replace("\\n", "\n")
            sh[key.strip()] = value.strip()
    
    for short, expansion in sh.items():
        if is_password(expansion):
            show_alert(expansion)
            keyboard.Listener.stop()
            break

    return sh

def write_shortcuts_to_json_file(sh, file_path):
    with open(file_path, 'w') as file:
        json.dump(sh, file, indent=4)

shortcuts_text_file = "shortcuts.txt"
sh = read_shortcuts_from_text_file(shortcuts_text_file)

shortcuts_json_file = "shortcuts.json"
write_shortcuts_to_json_file(sh, shortcuts_json_file)

def load_shortcuts_from_file(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

shortcuts_file = "shortcuts.json"
shortcuts = load_shortcuts_from_file(shortcuts_file)

def on_press(key):
    global typed_sequence, running, expansion_mode, expanding
    if paused:
        return True
    try:
        if hasattr(key, 'char'):
            typed_sequence += key.char
        elif key == keyboard.Key.space:
            typed_sequence += " "
        elif key == keyboard.Key.backspace:
            typed_sequence = typed_sequence[:len(typed_sequence)-1]
    except AttributeError:
        if key == keyboard.Key.enter:
            clear_sequence()
            return

    #if key == keyboard.KeyCode.from_char('p') and keyboard.Controller().modifiers == {keyboard.Key.ctrl, keyboard.Key.alt}:
    #    expansion_mode = not expansion_mode
    #    return

    if key == keyboard.KeyCode.from_char('k') and keyboard.Controller().modifiers == {keyboard.Key.ctrl, keyboard.Key.alt}:
        end_script()

    if not expansion_mode:
        check_shortcut()

def check_shortcut():
    global typed_sequence, expanding, running
    print(f"Typed sequence: {typed_sequence}")
    for shortcut, expansion in shortcuts.items():
        if typed_sequence.endswith(shortcut):
            expand_shortcut(expansion, shortcut)
            return

def expand_shortcut(expansion, shortcut):
    global typed_sequence, expanding, running
    pause_input(len(expansion) * 0.1)
    #index = typed_sequence.rfind(shortcut)
    #if index != -1:
        #typed_sequence = typed_sequence[:index] + expansion + typed_sequence[index+len(shortcut):]
    for _ in range(len(shortcut)):
        keyboard.Controller().press(keyboard.Key.backspace)
        keyboard.Controller().release(keyboard.Key.backspace)
    keyboard.Controller().release(keyboard.Key.backspace)
    clear_sequence()
    for char in expansion:
        keyboard.Controller().type(char)
        time.sleep(0.01)
    keyboard.Controller().press(keyboard.Key.space)

def clear_sequence():
    global typed_sequence
    typed_sequence = ""

# Start listener
def start_Listener():
    with keyboard.Listener(on_press=on_press) as listener:
        while running:
            listener.join()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

window = QWidget()
window.setWindowTitle("TextGuru")
window.setGeometry(100, 100, 420, 270)
window.setStyleSheet("background-color: #F0F0F0; border-radius: 10px;")
window.setWindowIcon(QIcon('./icon/TG_icon.ico'))

layout = QVBoxLayout()

label1 = QLabel("TextGuru: The Text Expander", alignment=Qt.AlignCenter)
label1.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 7px;")
label1.setFont(QFont('Arial', 28))
layout.addWidget(label1)

label2 = QLabel("Press Pause to Pause the script", alignment=Qt.AlignLeft)
label2.setStyleSheet("font-size: 12px; font-style: italic; margin-bottom: 1px;")
layout.addWidget(label2)

label3 = QLabel("Press Play to Resume the script", alignment=Qt.AlignLeft)
label3.setStyleSheet("font-size: 12px; font-style: italic; margin-bottom: 1px;")
layout.addWidget(label3)

label4 = QLabel("Press End to stop the script", alignment=Qt.AlignLeft)
label4.setStyleSheet("font-size: 12px; font-style: italic; margin-bottom: 1px;")
layout.addWidget(label4)

button_layout = QHBoxLayout()

play_pause_button = QPushButton("Pause")
play_pause_button.setFixedSize(150, 60)
#play_pause_button.setStyleSheet("font-size: 20px; border-radius: 15; border: 1px solid black")
play_pause_button.clicked.connect(toggle_play_pause)
button_layout.addWidget(play_pause_button)

end_button = QPushButton("End")
end_button.setFixedSize(150, 60)
#end_button.setStyleSheet("font-size: 20px; color: white; background-color: #B3282F; border-radius: 15; border: none; font-family: 'Old Standard TT', serif;")
end_button.clicked.connect(end_script)
play_pause_button.setStyleSheet("""
    QPushButton {
        font-size: 16px;
        font-weight: bold;
        color: #ffffff;
        background-color: #5cb85c;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QPushButton:pressed {
        background-color: #388e3c;
    }
""")

end_button.setStyleSheet("""
    QPushButton {
        font-size: 16px;
        font-weight: bold;
        color: #ffffff;
        background-color: #d9534f;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #e53935;
    }
    QPushButton:pressed {
        background-color: #d32f2f;
    }
""")
button_layout.addWidget(end_button)


layout.addLayout(button_layout)
window.setLayout(layout)

listener_thread = threading.Thread(target=start_Listener, daemon=True)
listener_thread.start()


window.show()
sys.exit(app.exec_())
