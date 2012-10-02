#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import random
import re

class AlleleTypeError(Exception):
	pass

class Allele:
	def __init__(self, allele_type, value=None):
		self.allele_type = allele_type
		if self.allele_type.valid_value(value):
			self.value = value
		else:
			raise AlleleTypeError("Invalid allele '%s'" % value)

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		if not self.allele_type.valid_value(value):
			raise AlleleTypeError("Not a valid allele: '%s'" % value)
		self._value = value

	def cross_over(self, other):
		raise NotImplementedError()

class AlleleType:
	def __init__(self):
		pass

	def random_allele(self):
		raise NotImplementedError()

	def valid_value(self, allele):
		raise NotImplementedError()

class BinaryAlleleType(AlleleType):
	def __init__(self, num_bits):
		self.num_bits = num_bits
		self.maximum = int('1' * self.num_bits, 2)
		AlleleType.__init__(self)

	def random_allele():
		return random.getrandombits(self.num_bits)

	def valid_value(self, allele):
		if not (isinstance(allele, int) or isinstance(allele, long)):
			return False
		return allele <= self.maximum and allele >= 0

class BinaryAllele(Allele):
	def __init__(self, num_bits=None, binary_allele_type=None, value=None):
		if (num_bits is None and
				not isinstance(binary_allele_type, BinaryAlleleType)):
			raise AlleleTypeError("The number of bits or an BinaryAlleleType " +
					"instance must be supplied")
		if binary_allele_type is None:
			binary_allele_type = BinaryAlleleType(num_bits)
		if isinstance(value, str):
			value = int(value, 2)

		Allele.__init__(self, binary_allele_type, value)

	def cross_over(self, other):
		"""One point cross_over"""
		self_str = self.binary_str()
		other_str = other_str.binary_str()

		point = random.randint(0, self.num_bits)
		return BinaryAllele(binary_allele_type=self.binary_allele_type,
				self_str[:point] + other_str[point:])

	def binary_str(self):
		self_str = bin(self.value)[2:]
		#Insert zeros to complement the binary string
		return ('0' * self.binary_allele_type.num_bits - len(self_str) \
				if len(self_str) < self.binary_allele_type.num_bits else '') +\
				self_str
