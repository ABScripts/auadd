import pyperclip
import requests
import time
import sqlm
import sys
import re

from beeper import Beeper
from googletrans import Translator
from keyboardcontroller import KeyboardController


class Dictionary:

    def __init__(self, src = None, dest = None):
        self.src = src
        self.dest = dest
        """TODO: check the validaty of dest"""
        self.to_exit = False
        self.last_check = ""
        self.alert_sound = Beeper(1000, 100)
        self.database = sqlm.Sqlm('data', src, dest)
        self.keyboard = KeyboardController([['shift', 'E'], 's', 'c'], [self.exit, self.show, self.copy])
        self.detect()

    def detect(self):

        with Listener(on_press=self.keyboard.on_press, on_release=self.keyboard.on_release) as listener:

            while self.connect() and (not self.to_exit):
                # TODO: create a thread for inputting inside this function, without a join method!
                fetched = pyperclip.paste() # data fetched from the buffer
                if self.is_valid(fetched):
                    if fetched == 'exit':
                        pyperclip.copy('')
                    else:
                        if self.database.select({self.src: fetched}) == None:
                            if self.is_origin(fetched):
                                try:
                                    translated = Translator().translate(fetched, src=self.src, dest=self.dest)
                                except:
                                    continue
                                self.database.add_word(fetched, translated.text)
                                print('New word was added!')
                time.sleep(1)

    def connect(self):

        alerted = False
        while True:
            try:
                requests.get("https://www.google.com/")
                if alerted:
                    self.alert_sound.beep()
                    print("/aThe Internet connection was resumed!")
                return True
            except:
                if not alerted:
                    self.alert_sound.beep()
                    print("//aWaiting for the Internet connection...")
                    alerted = True
            time.sleep(1)

    def is_valid(self, check):
        reg_word = re.compile('.?[^a-zA-Z]+.?')
        if not reg_word.search(check) and len(check) < 25:
            return True
        return False

    def is_origin(self, check):
        if not(check == self.last_check ):
            detected = Translator().detect(check)
            if not (detected.lang == self.src):
                self.alert_sound.beep()
                print("Watch out, maybe you meant something else\n"
                         "Setted [{setted}] but received [{received}]\nContinue? y/n".format(setted = self.src, received = detected.lang))

                while True:
                    res = input()
                    if res == 'y':
                        return True # or break
                    elif res == 'n':
                        self.last_check = check
                        return False
                    self.alert_sound.beep()
                    print("Input is incorrect! Allowed only y/n")

            return True
        return False

    def filename(self, attributes = []):
        filename = '-'.join([self.src, self.dest])
        for attribute in attributes:
            filename += attribute
        return filename

    def copy(self):
        items = self.database.is_filled()
        if not items:
            self.alert_sound.beep()
            return print('This dictionary is empty!')

        filename = self.filename('.txt')
        file = open(filename, 'w')
        for word, tword in items:
            file.write(word + '-' + tword + '\n')
        print("Words were copied to the {filename}!".format(filename = filename))

    def show(self):
        items = self.database.is_filled()
        # if this table is an empty one, we will inform a user
        # otherwise, this method will return the list with the items
        if not items:
            self.alert_sound.beep()
            return print('This dictionary is empty!')
        print("{filename:^30}".format(filename = self.filename()))
        for word, tword in items:
            print("{word:-<15}{tword:->15}".format(word = word, tword = tword))
        print("showing!")

    def sound_state(self):
        if self.alert_sound.duration == 0:  # if souund was disabled we turn it on
            self.alert_sound.duration = 100
        else:                               # else if it was not
            self.alert_sound.duration = 0   # we turn it off

    def exit(self):
        self.to_exit = True

# drive code...
dict = Dictionary(sys.argv[1], sys.argv[2])


