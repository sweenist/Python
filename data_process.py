import os, sys

class DataProcess:
    def __init__(self, filename = None):
        self.filename = filename or ""
        self.data = {}
        self.is_valid_file = os.path.exists(self.filename)
        if self.is_valid_file:
            self.process()

    def process(self):
        fp = open(self.filename)
        for line in fp:
            self.data[line.split(':')[0]] = line.split(':')[1]
        fp.close()
