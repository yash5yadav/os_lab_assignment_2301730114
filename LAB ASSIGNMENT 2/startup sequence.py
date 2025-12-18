### Sub-Task 1: Initialize Logging Configuration

import logging

logging.basicConfig(
    filename='process_log.txt',   # log file name
    level=logging.INFO,           # log level
    format='%(asctime)s - %(processName)s - %(message)s'
)


### Sub-Task 2: Define a Function That Simulates a Process Task

import logging
import time

# Sub-Task 1: Setup logger
logging.basicConfig(
    filename='process_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s'
)
def system_process(task_name):
    logging.info(f"{task_name} started")
    time.sleep(2)  # Simulate task delay
    logging.info(f"{task_name} ended")


### Sub-Task 3: Create at least two processes and run them concurrently


import logging
import time
import multiprocessing

logging.basicConfig(
    filename='process_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s'
)
def system_process(task_name):
    logging.info(f"{task_name} started")
    time.sleep(2)
    logging.info(f"{task_name} ended")

if __name__ == '__main__':
    print("System Starting...")

    p1 = multiprocessing.Process(target=system_process, args=('Process-1',))
    p2 = multiprocessing.Process(target=system_process, args=('Process-2',))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("All processes finished.")


###  Sub-Task 4: Ensure proper termination and verify logs

import logging
import time
import multiprocessing

logging.basicConfig(
    filename='process_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s'
)
def system_process(task_name):
    logging.info(f"{task_name} started")
    time.sleep(2)
    logging.info(f"{task_name} ended")

if __name__ == '__main__':
    print("System Starting...")

    p1 = multiprocessing.Process(target=system_process, args=('Process-1',))
    p2 = multiprocessing.Process(target=system_process, args=('Process-2',))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("System Shutdown.")
