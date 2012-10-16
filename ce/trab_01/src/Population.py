#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import random
import re

from Chromossome import RealChromossome
from Individual import F6Individual

class Population(object):
	def __init__(self, individuals):
		self.individuals = individuals

	@property
	def individuals(self):
		return self._individuals

	@individuals.setter
	def individuals(self, individuals):
		self._individuals = sorted(individuals)

	def __len__(self):
		return len(self.individuals)

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
	def best_individual(self):
		return self.individuals[-1]

	@property
	def best_score(self):
		return self.best_individual.score

	def __str__(self):
		s = ""
		s += "Size: %s\n" % len(self)
		s += "Best score: %.4f\n" % self.individuals[-1].score
		for i, c in enumerate(self.individuals):
			s += "Individual: %d\n\t" % i
			s += re.sub('\n(?!$)', '\n\t', str(c))
			s += '\n'
		return s

class F6Population(Population):
	def __init__(self, individuals=None, pop_size=None):
		"""
		Initialize with chromossomes or a random population of size pop_size
		"""
		if individuals is not None:
			Population.__init__(self, individuals)
		else:
			Population.__init__(self,
					[F6Individual(21, 25, -100, 100) for i in xrange(pop_size)])

	def select(self):
		"""Roullet wheel selection"""
		scores = [c.score for c in self.individuals]
		n_scores = scores / sum(scores)

		number = random.random()

		acc = 0
		for idx, value in enumerate(n_scores):
			acc += value
			if acc > number:
				return self.individuals[idx]

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

		#offsprint.append(self.best_chromossome)

		return F6Population(offsprint)

if __name__=='__main__':
	p = F6Population(pop_size=5)
