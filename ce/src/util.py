#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import random
random=random.Random(3)

def flip_coin(prob=0.5):
	return True if random.random() < prob else False
