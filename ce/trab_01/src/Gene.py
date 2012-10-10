#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import random

class Gene:
	def __init__(self, allele):
		self.allele = allele

	def mutate(self):
		"""mutate the gene in-place"""
		raise NotImplementedError()

	def cross_over(self, other):
		"""coross_over self and gene and return the generated gene"""
		raise NotImplementedError()

class RealGene(Gene):
	def __init__(self, allele):
		Gene.__init__(self, allele)

	def mutate(self):
		"""change allele to a random one"""
		self.allele.value = self.allele.allele_type.random_allele()

	def cross_over(self, other):
		return RealGene(self.allele.cross_over(other.allele))
