import logging
import threading
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

# Define the functions to be executed by each thread
def function_one():
    logging.info("Executing Function One")
    time.sleep(50)
    logging.info("Function One completed")

def function_two():
    logging.info("Executing Function Two")
    time.sleep(55)
    logging.info("Function Two completed")

def function_three():
    logging.info("Executing Function Three")
    time.sleep(60)
    logging.info("Function Three completed")

def function_four():
    logging.info("Executing Function Four")
    time.sleep(65)
    logging.info("Function Four completed")

# Create a dictionary to map index values to functions
index_to_function = {
    0: function_one,
    1: function_two,
    2: function_three,
    3: function_four
}

# Create threads for each function using the provided snippet
threads = list()
for index in range(4):
    logging.info("Main    : create and start thread %d.", index)
    x = threading.Thread(target=index_to_function[index], name=f'Thread-{index + 1}')
    threads.append(x)
    x.start()

# Wait for all threads to complete using the second part of the provided snippet
for index, thread in enumerate(threads):
    logging.info("Main    : before joining thread %d.", index)
    thread.join()
    logging.info("Main    : thread %d done", index)

logging.info("All threads have completed")
