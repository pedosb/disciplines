#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from matplotlib import pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
rc('text.latex', unicode=True)
rc('font', family='serif', serif='Computer Modern Roman')

states = ((0.7, 0.1), (0.9,0.007), (0.7,0.2), 
		(0.9, 0.02), (0.7,0.02), (0.8,0.3),
		(0.9,0.001), (0.7, 0.02), (0.7,0.08),
		(0.7, 0.02))

x = range(0,500)
y1 = []
y2 = []

j = -1
for i in xrange(500):
		j = 9 if j > 9 else j
		y1.append(states[j][0])
		y2.append(states[j][1])
		if not i % 50:
			print i,j
			if len(states) > j:
				j += 1

plt.figure(figsize=(9,6), dpi=1200)
plt.plot(x, y1, label='Taxa de Cruzamento')
plt.plot(x, y2, label='Taxa de Mutação')
plt.grid()
plt.legend(loc='best')
plt.xlabel('Geração')
plt.ylabel('Taxa')
plt.ylim(0,1)

plt.savefig('varia.eps')
