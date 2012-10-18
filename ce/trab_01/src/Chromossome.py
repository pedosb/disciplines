#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import random

from scipy import sin, sqrt

from util import flip_coin
from Allele import BinaryListAllele, BinaryAllele
from Gene import RealGene, Gene

class ChromossomeValueError(Exception):
	pass

class Chromossome(object):
	def __init__(self, genes):
		self.genes = genes
		self._score = None

	def mutate(self, mutate_prob):
		for gene in self.genes:
			if flip_coin(mutate_prob):
				gene.mutate()

	def cross_over(self, other):
		"""Return a list of generated chromossomes"""
		raise NotImplementedError()
		new_genes = []
		for self_gene, other_gene in zip(self.genes, other.genes):
			new_genes.append(self_gene.cross_over(other_gene))
		return Chromossome(new_genes)

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
		return 0.5 - (sin(sqrt(x2y2))**2-0.5) / (1+0.001*(x2y2))**2

class Trab1BinaryChromossome(F6Func, Chromossome):
	def __init__(self, min_value, max_value, num_bits_x, num_bits_y,
			x=None, y=None, genes=None):

		self.min_v = min_value
		self.max_v = max_value

		self.size = num_bits_x + num_bits_y
		if genes is not None and self.size != len(genes):
			raise Trab1ChromossomeError(
					"self.size (%d) does not match genes size (%d)" % (
						self.size, len(genes)))

		self.zero_complete = lambda value, size: ('0' * (size - len(value))) + value

		if isinstance(x, int):
			x = self.zero_complete(bin(x)[2:], num_bits_x)
		if isinstance(y, int):
			y = self.zero_complete(bin(y)[2:], num_bits_y)

		if num_bits_x is None and x is not None:
			num_bits_x = len(x)
		if num_bits_y is None and x is not None:
			num_bits_y = len(y)
		self.num_bits_x = num_bits_x
		self.num_bits_y = num_bits_y

		if genes is None:
			if x is not None:
				genes = [Gene(BinaryAllele(int(i))) for i in x]
			else:
				genes = [Gene(BinaryAllele()) for i in xrange(self.num_bits_x)]
			if y is not None:
				genes += [Gene(BinaryAllele(int(i))) for i in y]
			else:
				genes += [Gene(BinaryAllele()) for i in xrange(self.num_bits_y)]

		self.db_id = None
		self.point = None

		Chromossome.__init__(self, genes)

	def mutatea(self, mutate_prob):
		if flip_coin(mutate_prob):
			self.genes[:self.num_bits_x] = [Gene(BinaryAllele(int(i)))
					for i in
					self.zero_complete(bin(random.getrandbits(self.num_bits_x))[2:],
						self.num_bits_x)]
		if flip_coin(mutate_prob):
			self.genes[-self.num_bits_y:] = [Gene(BinaryAllele(int(i)))
					for i in
					self.zero_complete(bin(random.getrandbits(self.num_bits_y))[2:],
						self.num_bits_y)]

	@property
	def x(self):
		return float(int(self.bit_str()[:self.num_bits_x], 2)) * \
				float((self.max_v-self.min_v))/(2**self.num_bits_x-1) + \
				self.min_v

	@property
	def y(self):
		return float(int(self.bit_str()[-self.num_bits_y:], 2)) * \
				float((self.max_v-self.min_v))/(2**self.num_bits_y-1) + \
				self.min_v

	def bit_str(self):
		return ''.join([str(g.value) for g in self.genes])

	def _evaluate(self):
		return self.calc()

	def copy_genes(self):
		return [Gene(BinaryAllele(g.value)) for g in self.genes]

	def cross_over(self, other, mutate_prob, cross_prob):
		self_genes = self.copy_genes()
		other_genes = other.copy_genes()

		cross = flip_coin(cross_prob)

		point = random.randint(0, len(self.genes)) if cross else 0
		#point = self.num_bits_x if cross else 0

		son = Trab1BinaryChromossome(self.min_v, self.max_v, self.num_bits_x,
				self.num_bits_y, genes=self_genes[:point] + other_genes[point:])
		son.father = self
		son.mother = other
		son.point = point if cross else None
		daughter = Trab1BinaryChromossome(self.min_v, self.max_v, self.num_bits_x,
				self.num_bits_y, genes=other_genes[:point] + self_genes[point:])
		daughter.father = other
		daughter.mother = self
		daughter.point = point if cross else None

		if cross:
			son.mutate(mutate_prob)
			daughter.mutate(mutate_prob)

		if not cross:
			if self.best:
				print self.score
			elif other.best:
				print other.score
			else:
				print "pass"

		return son, daughter

	def __str__(self):
		s = ""
		if self.point is not None:
			bs = self.bit_str()
			s += "Alleles: %s %s\n" % (bs[:self.point], bs[self.point:])
		else:
			s += "Alleles: %s\n" % self.bit_str()
		s += "X: %s (%.6f)\n" % (self.bit_str()[:self.num_bits_x], self.x)
		s += "Y: %s (%.6f)\n" % (self.bit_str()[-self.num_bits_y:], self.y)
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

class Trab1Chromossome(Chromossome):
	def __init__(self, num_bits_x=None, num_bits_y=None, x=None, y=None,
			max_value=None, min_value=None):
		if max_value is None and min_value is None:
			raise Trab1ChromossomeError("min and max value required to create" +
					" a Trab1Chromossome instance")
		self.max_v = max_value
		self.min_v = min_value
		self._x = self._gene_instance(num_bits_x, x)
		self._y = self._gene_instance(num_bits_y, y)
		Chromossome.__init__(self, [self._x, self._y])

	def _gene_instance(self, num_bits, value):
		if isinstance(value, RealGene):
			return value
		elif num_bits is not None:
			return RealGene(BinaryListAllele(num_bits, value=value))
		else:
			raise Trab1ChromossomeError("num_bits or Allele instance required to " +
					"create a Gene")

	@property
	def x(self):
		return float(self._x.allele.value) * \
				float((self.max_v-self.min_v))/(2**self._x.allele.allele_type.num_bits-1) + \
				self.min_v

	@property
	def y(self):
		return float(self._y.allele.value) * \
				float((self.max_v-self.min_v))/(2**self._y.allele.allele_type.num_bits-1) + \
				self.min_v

	def cross_over(self, other):
		#point = random.randint(0, len(self.genes))
		return Trab1Chromossome(x=self._x, y=other._y, min_value=self.min_v, max_value=self.max_v), \
				Trab1Chromossome(x=other._x, y=self._y, min_value=self.min_v, max_value=self.max_v)

	def _evaluate(self):
		x2y2 = self.x**2 + self.y**2
		return 0.5 - (sin(sqrt(x2y2))**2-0.5) / (1+0.001*(x2y2))**2

	def __str__(self):
		s = ""
		s += "X: %s (%.6f)\n" % (self._x.allele.binary_str(), self.x)
		s += "Y: %s (%.6f)\n" % (self._y.allele.binary_str(), self.y)
		s += "Score: %.6f\n" % self.score
		return s
