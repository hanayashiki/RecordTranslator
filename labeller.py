class Labeller:
    count = 0

    def __init__(self):
        self.count = 0

    def generate(self):
        self.count +=  1
        return "label_"+str(self.count)