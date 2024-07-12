# Given a directory - assume everything in directory is a file
# Open every file in that directory
# Spit out lines until there are no more lines in files
import logging
import os


class DirectoryReader:
    def __init__(self, directory):
        self.directory = directory

    def read(self):
        for filename in os.listdir(self.directory):
            with open(self.directory + "/" + filename) as f:
                yield from f


if __name__ == "__main__":
    reader = DirectoryReader("../../data")
    for line in reader.read():
        logging.info(line)
