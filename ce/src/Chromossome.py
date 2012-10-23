#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import random

from scipy import sin, sqrt

from util import flip_coin

class ChromossomeValueError(Exception):
	pass

class Chromossome(object):
	def __init__(self, alleles):
		self.alleles = alleles 
		self._score = None

	def mutate(self, mutate_prob):
		return NotImplementedError

	def cross_over(self, other):
		"""Return a list of generated chromossomes"""
		raise NotImplementedError()

	def _evaluate(self):
		return NotImplementedError()

	@property
	def score(self):
		if self._score is None:
			score = self._evaluate()
			if score < 0:
				raise ChromossomeValueError("Invalid score (negative) '%s'" %
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

class Trab1ChromossomeError(Exception):
	pass

class F6Func(object):
	def calc(self):
		x2y2 = self.x**2 + self.y**2
		return 999.5 - (sin(sqrt(x2y2))**2-0.5) / (1+0.001*(x2y2))**2

class Trab1BinaryChromossome(F6Func, Chromossome):
	def __init__(self, min_x, max_x, num_bits_x, num_bits_y, min_y=None,
			max_y=None, x=None, y=None, alleles=None):

		self.min_x = min_x
		self.max_x = max_x

		self.min_y = min_y or self.min_x
		self.max_y = max_y or self.max_x

		self.num_bits_x = num_bits_x
		self.num_bits_y = num_bits_y

		self.size = num_bits_x + num_bits_y
		if alleles is not None and self.size != len(alleles):
			raise Trab1ChromossomeError(
					"self.size (%d) does not match alleles size (%d)" % (
						self.size, len(alleles)))

		self.zero_complete = lambda value, size: ('0' * (size - len(value))) + value

		x = x or random.getrandbits(self.num_bits_x)
		y = y or random.getrandbits(self.num_bits_y)

		if isinstance(x, (int, long)):
			x = self.zero_complete(bin(x)[2:], self.num_bits_x)
		if isinstance(y, (int, long)):
			y = self.zero_complete(bin(y)[2:], self.num_bits_y)

		if alleles is None:
			alleles = []
			alleles += list(x) + list(y)

		self.db_id = None
		self.point = None

		Chromossome.__init__(self, alleles)

	def copy(self):
		return Trab1BinaryChromossome(self.min_x, self.max_x, self.num_bits_x,
				self.num_bits_y, self.min_y, self.max_y, alleles=self.alleles)

	def mutate(self, mutate_prob):
		for idx, value in enumerate(self.alleles):
			if flip_coin(mutate_prob):
				self.alleles[idx] = '0' if value == '1' else '1'

	@property
	def x(self):
		return self.x_int * \
				float(self.max_x-self.min_x)/(2**self.num_bits_x-1) + self.min_x

	@property
	def y(self):
		return self.y_int * \
				float(self.max_y-self.min_y)/(2**self.num_bits_y-1) + self.min_y

	def bit_str(self):
		return ''.join(self.alleles)

	def x_bit_str(self):
		return ''.join(self.alleles[:self.num_bits_x])

	def y_bit_str(self):
		return ''.join(self.alleles[-self.num_bits_y:])

	@property
	def x_int(self):
		return int(self.x_bit_str(), 2)

	@property
	def y_int(self):
		return int(self.y_bit_str(), 2)

	@property
	def num_bits(self):
		return self.num_bits_x + self.num_bits_y

	def _evaluate(self):
		return self.calc()

	def copy_alleles(self):
		return list(self.alleles)

	def cross_over(self, other, mutate_prob, cross_prob):
		self_alleles = self.copy_alleles()
		other_alleles = other.copy_alleles()

		cross = flip_coin(cross_prob)

		point = random.randint(0, len(self.alleles)) if cross else 0
		#point = self.num_bits_x if cross else 0

		son = self.copy()
		son.alleles = self_alleles[:point] + other_alleles[point:]
		son.father = self
		son.mother = other
		son.point = point if cross else None

		daughter = self.copy()
		daughter.alleles = other_alleles[:point] + self_alleles[point:]
		daughter.father = other
		daughter.mother = self
		daughter.point = point if cross else None

		if cross:
			son.mutate(mutate_prob)
			daughter.mutate(mutate_prob)

		return son, daughter

	def __str__(self):
		s = ""
		if self.point is not None:
			bs = self.bit_str()
			s += "Alleles: %s %s\n" % (bs[:self.point], bs[self.point:])
		else:
			s += "Alleles: %s\n" % self.bit_str()
		s += "X: %s (%.6f)\n" % (self.x_bit_str(), self.x)
		s += "Y: %s (%.6f)\n" % (self.y_bit_str(), self.y)
		s += "Score: %.6f\n" % self.score
		if self.point is not None:
			s += "Cross Point: %d\n" % self.point
			s += "Father:\n"
			bs = self.father.bit_str()
			s += "\t Alleles: %s %s\n" % (bs[:self.point], bs[self.point:])
			s += "\t Score: %.6f\n" % self.father.score
			s += "Mother:\n"
			bs = self.mother.bit_str()
			s += "\t Alleles: %s %s\n" % (bs[:self.point], bs[self.point:])
			s += "\t Score: %.6f\n" % self.mother.score
		return s
