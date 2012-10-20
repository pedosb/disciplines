#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import argparse
import threading

from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, \
		ProcessEvent
from scipy import *
from matplotlib import pyplot as plt

from stats import *

class RealTimePlot(ProcessEvent):
	def __init__(self, experiment, ax):
		self.experiment = experiment
		self.last_generation = 0
		self.ax = ax
		ProcessEvent.__init__(self)

	def process_IN_MODIFY(self, event):
		result = db(
				(db.population.experiment==self.experiment) &
				(db.population.generation>self.last_generation))\
						.select(orderby=db.population.generation)
		x = zeros(len(result))
		y = zeros(len(result))
		idx = None
		for idx, p in enumerate(result):
			x[idx] = p.generation
			y[idx] = p.max_score
		self.last_generation += idx or 0
		self.ax.plot(x, y, 'b')
		self.ax.figure.canvas.draw()

def check_notify(notifier):
	notifier.process_events()
	if notifier.check_events():
		notifier.read_events()

if __name__=='__main__':
	parser = argparse.ArgumentParser(
			description='Plot AG statistics in Real-time')
	parser.add_argument('-e', '--experiment-id',
			help='The ID of the monitored experiment')
	args = parser.parse_args()

	f = plt.figure()
	f.hold(True)
	ax = f.add_subplot(111)

	experiment = args.experiment_id or db(db.experiment).select().last().id
	wm = WatchManager()
	plotter = RealTimePlot(experiment, ax)
	notifier = Notifier(wm, plotter, timeout=10)
	wd = wm.add_watch('databases/', EventsCodes.ALL_FLAGS['IN_MODIFY'])

	f.canvas.new_timer(interval=200,
			callbacks=((check_notify, (notifier,), {}),)).start()

	plt.show()
