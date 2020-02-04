import winsound


class Beeper:

    def __init__(self, frequensy, duration):
        self.frequensy = frequensy
        self.duration = duration

    def beep(self):
        winsound.Beep(self.frequensy, self.duration)
