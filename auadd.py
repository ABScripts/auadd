from googletrans import Translator
import pyperclip
import threading
import requests
import time
import sqlm
import sys
import re


class Dictionary:

    def __init__(self, src = None, dest = None):
        self.src = src
        self.dest = dest
        self.basedata = sqlm.Sqlm('data', src, dest)
        self.detect()

    def detect(self):
        while self.connect():
            time.sleep(1)
            fetched = pyperclip.paste() # data fetched from the buffer
            if self.is_valid(fetched):
                if fetched == 'exit':
                    """TODO: Get rid off this statement by using, mb, threading to allow both
                       working with buffer and typing some commands into the command line"""
                    pyperclip.copy('')
                    sys.exit()
                else:
                    if self.basedata.select({self.src: fetched}) == None:
                        if self.is_origin(fetched):
                            try:
                                translated = Translator().translate(fetched, src=self.src, dest=self.dest)
                            except:
                                continue
                            self.basedata.add_word(fetched, translated.text)
                            print('New word was added!')

    def connect(self):
        alerted = False
        while True:
            try:
                requests.get("https://www.google.com/")
                if alerted:
                    print("The Internet connection was resumed!")
                return True
            except:
                if not alerted:
                    print("Waiting for the Internet connection...")
                    alerted = True
                time.sleep(0.1)

    def show(self):
        items = self.basedata.is_filled()
        # if this table is an empty one, we will inform a user
        # otherwise, this method will return the list with the items
        if not items:
            return print('This dictionary is empty!')
        print("{filename:^30}".format(filename = self.filename()))
        for word, tword in items:
            print("{word:-<15}{tword:->15}".format(word = word, tword = tword))

    def is_valid(self, check):
        reg_word = re.compile('.?[^a-zA-Z]+.?')
        if not reg_word.search(check) and len(check) < 25:
            return True
        return False

    def is_origin(self, check):
        detected = Translator().detect(check)
        if not (detected.lang == self.src):
            print("Watch out, maybe you meant something else\n"
                     "Setted [{setted}] but received [{received}]\nContinue? y/n".format(setted = self.src, received = detected.lang))
            while True:
                res = input()
                if res == 'y':
                    return True
                elif res == 'n':
                    break
                else:
                    print("Input incorrect! Allowed only y/n")

            return False
        return True


    def copy(self):
        items = self.basedata.is_filled()
        if not items:
            return print('This dictionary is empty!')
        file = open(self.filename('.txt'), 'w')
        for word, tword in items:
            file.write(word + '-' + tword + '\n')

    def filename(self, attributes = []):
        filename = '-'.join([self.src, self.dest])
        for attribute in attributes:
            filename += attribute
        return filename

# drive code...
dict = Dictionary(sys.argv[1], sys.argv[2])
dict.basedata.close()


