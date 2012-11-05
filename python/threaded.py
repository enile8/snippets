#!/usr/bin/env python

import Queue
import threading

class Fetcher(threading.Thread):
  def __init__(self, in_queue, out_queue):
    threading.Thread.__init__(self)
    self.in_queue = in_queue
    self.out_queue = out_queue

  def run(self):
    while True:
      # pull job off the queue
      data = self.in_queue.get()

      # do work

      # signal to queue job is done
      self.in_queue.task_done()

class Writer(threading.Thread):
  def __init__(self, out_queue):
    threading.Thread.__init__(self)
    self.out_queue = out_queue

  def run(self):
    while True:
      # pull job off the queue
      data = self.out_queue.get()

      # do work
      
      # signal to queue job is done
      self.out_queue.task_done()

def main():
  num_threads = 8
  in_queue = Queue.Queue()
  out_queue = Queue.Queue()

  # start worker threads
  for i in range(num_threads):
    t = Fetcher(in_queue, out_queue)
    t.setDaemon(True)
    t.start()

  # add 5000 jobs to work queue
  for combo in range(5000):
    in_queue.put(combo)

  # start output/writer thread
  dt = Writer(out_queue)
  dt.setDaemon(True)
  dt.start()

  # wait for work to finish
  in_queue.join()
  out_queue.join()

if __name__ == "__main__":
  main()
