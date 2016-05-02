import threading
from queue import Queue
import time
import pandas as pd

# lock to serialize console output
lock = threading.Lock()

names1 = pd.read_csv('data/stateNames1.csv')
names2 = pd.read_csv('data/stateNames2.csv')
df = pd.concat([names1, names2])
changes = []


def do_work(row):
    year = row['Year']
    name = row['Name']
    state = row['State']
    gender = row['Gender']
    count = row['Count']

    prev = df[(df.Year == (year - 1)) & (df.Name == name) & (df.State == state) & (df.Gender == gender)]

    with lock:
        if len(prev) > 0:
            c = {
                'Id': row['Id'],
                'change': int(count) - int(prev['Count'])
            }
            changes.append(c)
        print(threading.current_thread().name, row['Id'])


# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

# Create the queue and thread pool.
q = Queue()
for i in range(15):
     t = threading.Thread(target=worker)
     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
     t.start()

# stuff work items on the queue (in this case, just a number).
start = time.perf_counter()
count = 0
for i, task in df.iterrows():
    q.put(task)

q.join()

for change in changes:
    df.loc[df['Id'] == change['Id'], 'Change'] = change['change']

df.to_csv('output/NameRateChange.csv')

