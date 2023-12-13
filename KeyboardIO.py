"""
This moudle is used to control the keyboard's input and output.
"""
from queue import Queue
from pynput import keyboard
from pynput.keyboard import KeyCode, Controller
import logging
from time import sleep

ctr = Controller()
KeyboardEventQueue = Queue(100)

def send_keys(keys):
    for char in keys:
        if char=='\b':
            char = keyboard.Key.backspace
        ctr.press(char)
        ctr.release(char)
    


class KeyboardReader():
    def __init__(self):
        self.active = False
        self.inputs = ""
    
    def run(self):
        logging.info("KeyboardReader is started")
        lsn1 = keyboard.GlobalHotKeys({"<alt>+f": self.on_commend})
        lsn1.start()
        with keyboard.Listener(on_press=self.on_press) as lsn2:
            lsn2.join()

    def on_press(self, key):
        if self.active:
            if isinstance(key, KeyCode):
                self.inputs += key.char
            else:
                if (key.name=="space"):
                    self.inputs += " "
                elif (key.name=="backspace") and (self.inputs):
                    self.inputs = self.inputs[:-1]
            KeyboardEventQueue.put(self.inputs)
            logging.debug("Hand in TextEvent: " + self.inputs)

            if (len(self.inputs)>=15):
                self._clear()
                self.active = False
                logging.info("Quit waiting mode")
                
    def on_commend(self):
        logging.info("Receive Alt+f, the program will send a :) emotion")
        ctr.release("f")
        ctr.release(keyboard.Key.alt)
        send_keys(":)")
        self.active = True
        self.inputs = ""
        logging.info("Receive Alt+f, enter waiting mode")
    
    def _clear(self):
        send_keys("\b"*(len(self.inputs)+2))



if __name__ == "__main__":
    from threading import Thread

    logging.basicConfig(level=logging.DEBUG)
    Thread(target=KeyboardReader().run, daemon=False).start()

    while True:
        if not KeyboardEventQueue.empty():
            logging.debug("Receive TextEvent: "+KeyboardEventQueue.get())
        else:
            sleep(0.1)