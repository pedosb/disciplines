#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import sys

from stats import db
from scipy import array, zeros

if __name__=='__main__':

	out = sys.stdout

	exp = 102
	pops = db(db.population.experiment==exp)\
			.select(orderby=db.population.generation)

	ma = zeros(len(pops))
	mi = zeros(len(pops))
	me = zeros(len(pops))
	st = zeros(len(pops)) 
	for idx, pop in enumerate(pops):
		ma[idx] = pop.max_score
		mi[idx] = pop.min_score
		me[idx] = pop.mean
		st[idx] = pop.std
		if not idx % 50:
			out.write("""
					\\begin{table}
					\\begin{tabular}{|l|l|l|l|}
					Representaç~ao Bin´aria & x & y & score \\\\\hline\n
					""")
			for c in pop.chromossomes:
				print c.x
				out.write('%s & %.6f & %.6f & %.6f\\\\\hline\n' % (
					c.bits,
					c.x,
					c.y,
					c.score))
			out.write(r"""
					\end{tabular}
					\label{Tabela da populaço %d}
					\end{table}
					""" % idx)
