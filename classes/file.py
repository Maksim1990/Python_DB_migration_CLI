class File:

    def __init__(self, file):
        self.file=file

    def log(self, message):
        f = open("storage/"+self.file, "a")
        f.write(message)
        f.close()
