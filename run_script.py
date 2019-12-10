import os
import time
import json

with open("script.txt") as fp:
   lines = fp.read().splitlines()

execution_times = dict()

for line in lines:
    print("-- Running:", line)
    start = time.time()
    os.system(line)
    end = time.time()
    print("\n-- Elapsed:", end - start)
    execution_times[line] = end - start

    with open("execution_times.csv", 'a+') as fp:
        fp.write("'{}',{}\n".format(line, end - start))

with open("execution_times.json", 'w+') as fp:
        json.dump(execution_times, fp)