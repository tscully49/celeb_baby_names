import threading
from queue import Queue
import pandas as pd
import us
import time


class RateChangeWorker:

    def __init__(self):
        names1 = pd.read_csv('data/stateNames1.csv')
        names2 = pd.read_csv('data/stateNames2.csv')
        self.df = pd.concat([names1, names2])
        self.q = Queue()
        self.num_threads = 20
        self.lock = threading.Lock()
        self.change = {}

    def calculate_range(self, row):
        print("Doing work...")
        year = row['Year']
        name = row['Name']
        state = row['State']
        gender = row['Gender']
        change = 'NA'
        prev = self.df[(self.df.Year == (year - 1)) & (self.df.Name == name) & (self.df.State == state.abbr)
                       & (self.df.Gender == gender)]
        if len(prev) > 0:
            change = row['count'] - prev['count']
        row['change'] = change
        with self.lock:
            print('Calculating: ' + str(name) + ", " + str(year) + ", " + str(name) + ", " + str(state) +
                  ", change=" + str(change))
            self.change[row['Id']] = change

    def do_work(self, item):
        time.sleep(.1)
        with self.lock:
            print(threading.current_thread().name, item)

    def worker(self):
        while True:
            job = self.q.get()
            self.do_work(job)
            self.q.task_done()

    def spawn_threads(self):
        for i in range(self.num_threads):
            t = threading.Thread(target=self.do_work)
            t.daemon = True
            t.start()

    def generate_work(self):
        for i in range(100):
            print("Adding work..." + str(i))
            self.q.put(i)

    def setup(self):
        self.generate_work()
        self.spawn_threads()
        self.q.join()

rate_calc = RateChangeWorker()
rate_calc.setup()


