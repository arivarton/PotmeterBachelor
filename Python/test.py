import time

start = time.time()

while True:
    if time.time() - start > 5:
        print("5 seconds passed")
        start = time.time()
