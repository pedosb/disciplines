#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import sys
import os
import argparse
import threading

from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, \
		ProcessEvent
from scipy import *
from matplotlib import pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
rc('text.latex', unicode=True)
rc('font', family='serif', serif='Computer Modern Roman')

from stats import *

class RealTimePlot(ProcessEvent):
	def __init__(self, experiment, ax):
		self.experiment = experiment
		self.last_generation = 0
		self.ax = ax
		self.max = 0
		ProcessEvent.__init__(self)

	def process_IN_MODIFY(self, event):
		result = db(
				(db.population.experiment==self.experiment) &
				(db.population.generation>self.last_generation))\
						.select(orderby=db.population.generation)
		x = zeros(len(result))
		best = zeros(len(result))
		worst = zeros(len(result))
		mmean = zeros(len(result))
		mstd = zeros(len(result))
		idx = None
		for idx, p in enumerate(result):
			x[idx] = p.generation
			best[idx] = p.max_score
			worst[idx] = p.min_score
			mmean[idx] = p.mean
			mstd[idx] = p.std
		self.max = self.max if self.max > max(best) else max(best)
		print self.max
		self.last_generation += idx or 0
		self.ax.plot(x, best, 'b')
		self.ax.plot(x, worst, 'g')
		self.ax.errorbar(x, mmean, yerr=mstd, fmt='c')
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
	parser.add_argument('-s', '--save-fig',
			help='Save fig with the given name')
	args = parser.parse_args()

	#4 F6
	#10 F6e
	#16 alpha 3

	f = plt.figure(figsize=(9, 6), dpi=1200) if args.save_fig is not None \
			else plt.figure()
	f.hold(True)
	ax = f.add_subplot(111)

	experiment = args.experiment_id or db(db.experiment).select().last().id
	wm = WatchManager()
	plotter = RealTimePlot(experiment, ax)
	plotter.process_IN_MODIFY(None)
	plt.legend(('Melhor', 'Pior', u'Média e desvio padrão'), loc='upper left',
			prop=dict(size=10))
	plt.xlabel(u'Gerações')
	plt.ylabel(u'Score (não para o desvio padrão)')
	if args.save_fig is not None:
		plt.savefig(args.save_fig)
		sys.exit(0)
	notifier = Notifier(wm, plotter, timeout=10)
	wd = wm.add_watch('databases/', EventsCodes.ALL_FLAGS['IN_MODIFY'])

	f.canvas.new_timer(interval=500,
			callbacks=((check_notify, (notifier,), {}),)).start()

	plt.show()
