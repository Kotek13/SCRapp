class DataLogger:
    def __init__(self):
        self.log_file = None

    def log(self, data):
        if self.log_file is not None and not self.log_file.closed:
            self.log_file.write("\n" + data)
            return True
        else:
            return False

    def start(self, file = "data.log"):
        self.log_file = open(file, "a")

    def stop(self):
        if self.log_file is not None:
            self.log_file.close()


if __name__ == "__main__":
    log = DataLogger()
    log.start()
    for i in range(1,10):
        log.log("test" + i.__str__())
    log.stop()