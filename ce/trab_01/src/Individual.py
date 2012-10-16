#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from scipy import sin, sqrt

from util import flip_coin, binary_to_real
from Chromossome import RealChromossome

class Individual(object):
	def __init__(self, chromossomes=None):
		if chromossomes is None:
			chromossomes = list()
		self._chromossomes = chromossomes

		self._score = None

	@property
	def chromossomes(self):
		return self._chromossomes

	def cross_over(self, other, cross_prob, mutate_prob):
		return NotImplementedError()

	def add_chromossome(self, chromossome):
		self._chromossomes.append(chromossome)

	def mutate(self, mutate_prob):
		for cr in self.chromossomes:
			cr.mutate(mutate_prob)

	def _evaluate(self):
		return NotImplementedError()

	@property
	def score(self):
		if self._score is None:
			score = self._evaluate()
			if score < 0:
				raise ValueError("Invalid score (negative) '%s'" %
						score)
			self._score = score
		return self._score

	@score.deleter
	def score(self):
		self._score = None

	def __lt__(self, other):
		return self.score.__lt__(other.score)

	def __le__(self, other):
		return self.score.__le__(other.score)

	def __gt__(self, other):
		return self.score.__gt__(other.score)

	def __ge__(self, other):
		return self.score.__ge__(other.score)

	def __eq__(self, other):
		return self.score.__eq__(other.score)

	def __ne__(self, other):
		return self.score.__ne__(other.score)

class F6Individual(Individual, object):
	def __init__(self, num_bits_x, num_bits_y, min_x, max_x, min_y=None,
			max_y=None, x=None, y=None):
		if min_y is None:
			min_y = min_x
		if max_y is None:
			max_y = max_x

		Individual.__init__(self, (RealChromossome(min_x, max_x, num_bits_x, x),
			RealChromossome(min_y, max_y, num_bits_y, y)))

	@property
	def x(self):
		return self.chromossomes[0].real

	@property
	def y(self):
		return self.chromossomes[1].real

	def _evaluate(self):
		x2y2 = self.x**2 + self.y**2
		return 0.5 - (sin(sqrt(x2y2))**2-0.5) / (1+0.001*(x2y2))**2

	def cross_over(self, other, cross_prob, mutate_prob):
		if flip_coin(cross_prob):
			x1, x2, = self.chromossomes[0].cross_over(other.chromossomes[0])
			y1, y2, = self.chromossomes[1].cross_over(other.chromossomes[1])

			sun = F6Individual(x1.num_bits, y1.num_bits, x1.min, x1.max, y1.min,
					y1.max, x1.bit_str(), y1.bit_str())
			daughter = F6Individual(x2.num_bits, y2.num_bits, x2.min, x2.max, y2.min,
					y2.max, x2.bit_str(), y2.bit_str())

			map(lambda c: c.mutate(mutate_prob), (sun, daughter))
		else:
			sun = self
			daughter = other

		return sun, daughter

	def __str__(self):
		s = ""
		s += "X: %s (%.6f)\n" % (self.chromossomes[0].bit_str(), self.x)
		s += "Y: %s (%.6f)\n" % (self.chromossomes[1].bit_str(), self.y)
		s += "Score: %.6f\n" % self.score
		return s
