import random
from time import sleep

sleep(2)
for line in open("tests/data/swift-test-error.txt"):
    sleep(random.choice((0.02, 0.03, 0.035, 0.04, 0.045, 0.05, 0.1)))
    print(line)
