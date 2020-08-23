
# (c) 2020 kazuki KOHZUKi

def coordinate2int(coordinate):
	x, y, z, w = coordinate
	return (w << 6) | (z << 4) | (y << 2) | (x << 0)

def int2coordinate(value):
	x = (value & 0x03) >> 0
	y = (value & 0x0c) >> 2
	z = (value & 0x30) >> 4
	w = (value & 0xc0) >> 6
	return x, y, z, w
