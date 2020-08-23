
# (c) 2020 Kazuki KOHZUKI

import random
from itertools import product
from utils import *

def next(board, next_player):
	lines3_opp = get_3lines(board, next_player*-1)
	if len(lines3_opp) > 0:
		return random.choice(lines3_opp)

	lines3 = get_3lines(board, next_player)
	if len(lines3) > 0:
		return random.choice(lines3)

	lines2_opp = get_2lines(board, next_player*-1)
	if len(lines2_opp) > 0:
		dict2_opp = {i: 0 for i in range(4**4)}
		for coordinate in lines2_opp:
			dict2_opp[coordinate] += 1
		m2_opp = max(dict2_opp.values())
		filtered2_opp = [k for k, v in dict2_opp.items() if v == m2_opp]
		return random.choice(filtered2_opp)

	lines2 = get_2lines(board, next_player)
	if len(lines2) > 0:
		dict2 = {i: 0 for i in range(4**4)}
		for coordinate in lines2:
			dict2[coordinate] += 1
		m2 = max(dict2.values())
		filtered2 = [k for k, v in dict2.items() if v == m2]
		return random.choice(filtered2)

	empty = []
	for coordinate in range(4**4):
		x, y, z, w = int2coordinate(coordinate)
		if board[w][z][y][x] == 0:
			empty.append(coordinate)

	return random.choice(empty)

def get_3lines(board, player):
	def func(vec):
		l = []
		for X, Y, Z, W in vec:
			if (X, Y, Z, W) == (0, 0, 0, 0):
				continue
			for x, y, z, w in product(start(X), start(Y), start(Z), start(W)):
				s = sum(
					board[w+W*i][z+Z*i][y+Y*i][x+X*i] == player for i in range(4)
				)
				if s == 3:
					for i in range(4):
						if board[w+W*i][z+Z*i][y+Y*i][x+X*i] == 0:
							l.append(coordinate2int((x+X*i, y+Y*i, z+Z*i, w+W*i)))
							break
		return l

	return iter_all(func)

def get_2lines(board, player):
	def func(vec):
		l = []
		for X, Y, Z, W in vec:
			if (X, Y, Z, W) == (0, 0, 0, 0):
				continue
			for x, y, z, w in product(start(X), start(Y), start(Z), start(W)):
				s = sum(
					board[w+W*i][z+Z*i][y+Y*i][x+X*i] == player for i in range(4)
				)
				s_opp = sum(
					board[w+W*i][z+Z*i][y+Y*i][x+X*i] == player*-1 for i in range(4)
				)
				if s_opp > 0:
					continue
				if s == 2:
					for i in range(4):
						if board[w+W*i][z+Z*i][y+Y*i][x+X*i] == 0:
							l.append(coordinate2int((x+X*i, y+Y*i, z+Z*i, w+W*i)))
		return l

	return iter_all(func)

def iter_all(func):
	l = []

	# 1D
	for i in range(4):
		l += func([[1, 0, 0, 0][i:]+[1, 0, 0, 0][:i]])

	# 2D
	l += func(product([-1, 1], [1], [0], [0]))  # x-y
	l += func(product([-1, 1], [0], [1], [0]))  # x-z
	l += func(product([-1, 1], [0], [0], [1]))  # x-w
	l += func(product([0], [-1, 1], [1], [0]))  # y-z
	l += func(product([0], [-1, 1], [0], [1]))  # y-w
	l += func(product([0], [0], [-1, 1], [1]))  # z-w

	# 3D
	l += func(product([-1, 1], [-1, 1], [1], [0]))  # x-y-z
	l += func(product([-1, 1], [-1, 1], [0], [1]))  # x-y-w
	l += func(product([-1, 1], [0], [-1, 1], [1]))  # x-z-w
	l += func(product([0], [-1, 1], [-1, 1], [1]))  # y-z-w

	# 4D
	l += func(product([-1, 1], [-1, 1], [-1, 1], [1]))

	return l

def start(val):
	if val == 1:
		return [0]
	elif val == -1:
		return [3]
	else:
		return range(4)
