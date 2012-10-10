#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from dal import *

db = DAL('sqlite://evolution.db')

db.define_table('experiment',
		Field('task'),
		Field('mutate_prob', 'float'))

db.define_table('chromossome',
		Field('score'))

db.define_table('population',
		Field('experiment', db.experiment),
		Field('generation', 'integer'),
		Field('chromossomes', 'list:reference chromossome'),
		Field('max_score', compute=
			lambda r: max([c.score for c in r.chromossomes])))

if __name__=='__main__':
	from Population import F6Population
	p = F6Population(pop_size=50)

	mutate_prob = 0.01

	experiment = db.experiment.insert(task='F6', mutate_prob=mutate_prob)
	db.commit()

	for i in xrange(2000):
		crs_id = []
		for c in p.chromossomes:
			crs_id.append(db.chromossome.insert(score=c.score))

		db.population.insert(experiment=experiment,
				generation=i,
				chromossomes=crs_id)
		db.commit()

		p = p.new_population(mutate_prob)

	db.close()
