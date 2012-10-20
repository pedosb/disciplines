#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from scipy import std, mean

from dal import *

db = DAL('sqlite://evolution.db', folder='databases')

db.define_table('experiment',
		Field('task'),
		Field('mutate_prob', 'float'),
		Field('cross_prob', 'float'))

db.define_table('chromossome',
		Field('bits'),
		Field('x', 'float'),
		Field('y', 'float'),
		Field('score', 'float'),
		Field('father', 'reference chromossome'),
		Field('mother', 'reference chromossome'),
		Field('cross_point', 'integer'))

db.define_table('population',
		Field('experiment', db.experiment),
		Field('generation', 'integer'),
		Field('chromossomes', 'list:reference chromossome'),
		Field('max_score', compute=
			lambda r: max([c.score for c in r.chromossomes])),
		Field('min_score', compute=
			lambda r: min([c.score for c in r.chromossomes])),
		Field('mean', compute=
			lambda r: mean([c.score for c in r.chromossomes])),
		Field('std', compute=
			lambda r: std([c.score for c in r.chromossomes])),
		)

if __name__=='__main__':
	from Population import F6Population
	p = F6Population(pop_size=50)

	mutate_prob = 0.3
	cross_prob = 0.7

	experiment = db.experiment.insert(task='F6Binary', mutate_prob=mutate_prob,
			cross_prob=cross_prob)
	db.commit()

	for i in xrange(500):
		crs_id = []
		for c in p.chromossomes:
			crs_id.append(db.chromossome.insert(score=c.score,
				bits=c.bit_str(),
				x=c.x,
				y=c.y
				))
			c.db_id = crs_id[-1]

		db.population.insert(experiment=experiment,
				generation=i,
				chromossomes=crs_id)
		if not i % 50:
			db.commit()
		p = p.new_population(mutate_prob, cross_prob)

	print p
	db.commit()

	db.close()
