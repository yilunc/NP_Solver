#multiple_iterator.py
#Code to run the a function mulptiple times on the data sets
import os

NUM_TIMES_TO_RUN = 1000
FUNCTION_TO_RUN = "solve_tom.py"

for i in range(0,NUM_TIMES_TO_RUN):
	# os.system("python " + FUNCTION_TO_RUN)
	os.system("python test.py sid 600")