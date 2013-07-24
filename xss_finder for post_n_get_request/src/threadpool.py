#!/usr/bin/env python

from Queue import Queue
from threading import Thread

# -------------------------------------
class ThreadPoolWorker(Thread):
# -------------------------------------

	tasks_queue = None

	# -------------------------------------
	def __init__(self, tasks_queue):
	# -------------------------------------

		# Init
		Thread.__init__(self)

		self.tasks_queue = tasks_queue

		# Start daemon thread
		self.daemon = True
		self.start()

	# -------------------------------------
	def __del__(self):
	# -------------------------------------	

		pass

	# -------------------------------------
	def run(self):
	# -------------------------------------

		# Endless loop
		while True:
			# Fetch item from queue
			func, args, kargs = self.tasks_queue.get()

			# Execute task
			#func(*args, **kargs)
			try:
				func(*args, **kargs)
			except Exception, e:
				print 'Args',func, args, kargs
				print 'Exception',e

			# Mark task as completed (remove from queue)
			self.tasks_queue.task_done()

# -------------------------------------
class ThreadPool:
# -------------------------------------

	num_threads = None
	tasks_queue = None

	DEFAULT_NUM_THREADS = 5

	# -------------------------------------
	def __init__(self, num_threads=DEFAULT_NUM_THREADS):
	# -------------------------------------

		# Init
		self.num_threads = num_threads
		self.tasks_queue = Queue(num_threads)

		# Create 'num_threads' worker threads
		for i in range(num_threads):
			ThreadPoolWorker(self.tasks_queue)

	# -------------------------------------
	def enqueue(self, func, *args, **kargs):
	# -------------------------------------

		# Add a task to the queue
		self.tasks_queue.put((func, args, kargs))

	# -------------------------------------
	def wait(self):
	# -------------------------------------

		# Wait for completion of all the tasks in the queue
		self.tasks_queue.join()

# -------------------------------------
if __name__ == '__main__':
# -------------------------------------

	print 'Error : This python script cannot be run as a standalone program.'
