from threading import Thread
from time import time, sleep


class SpeedCounter:
    def __init__(self):
        self.data_queue = []
        self.data_sum = 0
        self.averaging_time = 1
        self.average_speed = []
        self.worker = Thread(target=self.worker, name="SpeedCounter")
        self.running = False
        self.buffor_size = 60

    def worker(self):
        curr_time = time() - self.averaging_time
        while self.running:
            prev_time = curr_time
            curr_time = time()
            while len(self.data_queue) > 0 and self.data_queue[0][0] < prev_time:
                self.pop_data()
            average = self.data_sum/(curr_time-prev_time)
            self.average_speed.append((prev_time, average))
            while len(self.average_speed) > self.buffor_size:
                self.average_speed.pop(0)
            timespan = (time()*1000-curr_time*1000)
            print("timespan:",timespan,"ms")
            #print(self.average_speed)
            sleep(self.averaging_time-timespan)

    def pop_data(self):
        _time, length = self.data_queue.pop(0)
        self.data_sum -= length

    def add_data(self, length):
        self.data_queue.append((time(), length))
        self.data_sum += length

    def get_speed(self):
        return self.average_speed

    def start(self):
        self.running = True
        self.worker.daemon = True
        self.worker.start()

    def stop(self):
        self.running = False
        self.worker.join()

if __name__ == "__main__":
    counter = SpeedCounter()
    counter.start()
    start_time = time()
    try:
        while True:
            counter.add_data(10)
            sleep(1)
    except KeyboardInterrupt:
        pass
    counter.stop()
