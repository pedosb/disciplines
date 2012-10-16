#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from scipy import std, mean

from dal import *

db = DAL('sqlite://evolution.db')

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
		Field('max_score', 'float'),
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

	mutate_prob = 0.05
	cross_prob = 0.9

	experiment = db.experiment.insert(task='F6Binary', mutate_prob=mutate_prob,
			cross_prob=cross_prob)
	db.commit()

	for i in xrange(500):
		print p
		crs_id = []
		db.population.insert(experiment=experiment,
				generation=i,
				max_score=p.best_score)
		print p.best_score
		db.commit()

		p = p.new_population(mutate_prob, cross_prob)

	db.close()
