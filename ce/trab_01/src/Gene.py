#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import random

class Gene:
	def __init__(self, allele):
		self.allele = allele

	def mutate(self):
		"""mutate the gene in-place
		change allele to a random one"""
		self.allele.value = self.allele.allele_type.random_allele()

	@property
	def value(self):
		return self.allele.value

	@value.setter
	def value(self, value):
		self.allele.value = value

	def __str__(self):
		return str(self.value)

class RealGene(Gene):
	def __init__(self, allele):
		Gene.__init__(self, allele)

	def cross_over(self, other):
		return RealGene(self.allele.cross_over(other.allele))
