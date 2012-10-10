#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from scipy import sin, sqrt

from util import flip_coin
from Allele import BinaryAllele, BinaryAlleleType
from Gene import RealGene

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
			return RealGene(BinaryAllele(num_bits, value=value))
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
