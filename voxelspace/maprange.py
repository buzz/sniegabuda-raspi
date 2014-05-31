def maprange(a, b, s):
	(a0, a1), (b0, b1) = a, b
	return  b0 + ((s - a0) * (b1 - b0) / (a1 - a0))
