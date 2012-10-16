#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import random
import re

from Chromossome import Trab1Chromossome, Trab1BinaryChromossome

class Population(object):
	def __init__(self, chromossomes):
		self._chromossomes = None
		self.chromossomes = chromossomes

	@property
	def chromossomes(self):
		return self._chromossomes

	@chromossomes.setter
	def chromossomes(self, chromossomes):
		self._chromossomes = sorted(chromossomes)

	def __len__(self):
		return len(self.chromossomes)

	def select(self):
		"""Return a chromossome from the population"""
		return NotImplementedError()

	def new_population(self, mutate_prob, size=None):
		"""Create a new_population from the current one

		The cross over rate is 100%

		if size is None (default) the new_population size will be the lenght of
		the current one
		"""
		return NotImplementedError()

	@property
	def best_chromossome(self):
		return self.chromossomes[-1]

	@property
	def best_score(self):
		return self.best_chromossome.score

	def __str__(self):
		s = ""
		s += "Size: %s\n" % len(self)
		s += "Best score: %.4f\n" % self.chromossomes[-1].score
		for i, c in enumerate(self.chromossomes):
			s += "Chromossome: %d\n\t" % i
			s += re.sub('\n(?!$)', '\n\t', str(c))
			s += '\n'
		return s

class F6Population(Population):
	def __init__(self, chromossomes=None, pop_size=None):
		"""
		Initialize with chromossomes or a random population of size pop_size
		"""
		if chromossomes is not None:
			Population.__init__(self, chromossomes)
		else:
			Population.__init__(self,
					[Trab1BinaryChromossome(-100, 100, 21, 25) for i in xrange(pop_size)])
		self.chromossomes = sorted(self.chromossomes)

	def select(self):
		"""Roullet wheel selection"""
		scores = [c.score for c in self.chromossomes]
		n_scores = scores / sum(scores)

		number = random.random()

		acc = 0
		for idx, value in enumerate(n_scores):
			acc += value
			if acc > number:
				return self.chromossomes[idx]

	def new_population(self, mutate_prob, cross_prob, size=None):
		size = size or len(self)# - 1
		offsprint = []

		while True:
			if len(offsprint) >= size:
				break
			else:
				offsprint.extend(self.select().cross_over(self.select(),
					mutate_prob,
					cross_prob))

		if len(offsprint) > size:
			offsprint = sorted(offsprint)[:len(self)]

		#[c.mutate(mutate_prob) for c in offsprint]
		#offsprint.append(self.best_chromossome)
		#print len(offsprint)

		return F6Population(offsprint)

if __name__=='__main__':
	p = F6Population(pop_size=5)
	print p
