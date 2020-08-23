
# (c) 2020 Kazuki KOHZUKI

import Cell
import cpu
import ui
from config import GameConfig
from console import alert
from itertools import product
from utils import *


class Score(ui.View):
	def __init__(self, player, *args, **kwargs):
		super().__init__(
			width=160, height=80,
			background_color='white',
			*args, **kwargs
		)
		self.player = ui.Label(
			text=player,
			frame=(10, 10, 60, 60),
			font=('<system>', 50)
		)
		self.add_subview(self.player)

		self.score = ui.Label(
			text='0',
			frame=(70, 10, 80, 60),
			font=('Futura', 48),
			alignment=ui.ALIGN_RIGHT
		)
		self.add_subview(self.score)

	def set_score(self, score):
		self.score.text = str(score)


class Board(ui.View):
	def __init__(self, *args, **kwargs):
		height, width = ui.get_screen_size()
		super().__init__(
			frame=(0, 0, width, height),
			background_color='white',
			name='4-4-4-4',
			*args, **kwargs
		)
		self.sections = [
			[Cell.Cells(z, w) for w in range(4)] for z in range(4)
		]
		for sections_w in self.sections:
			for section in sections_w:
				self.add_subview(section)

		self.player = 1
		self.black, self.white = 0, 0
		self.history = []

		self.scores = [
			Score(player, x=750, y=10+85*i) for i, player in enumerate(['●', '○'])
		]
		for score in self.scores:
			self.add_subview(score)
		self.scores[0].border_width = 1.5

		self.cpu = ui.Switch(
			x=750, y=220,
			value=False,
			action=self.save_config
		)
		self.add_subview(self.cpu)

		self.add_subview(ui.Label(
			text='CPU',
			font=('<system>', 42),
			x=810, y=185
		))

		self.reset = ui.Button(
			tint_color='black',
			frame=(750, 310, 160, 60),
			font=('Source Code Pro', 42),
			action=self.clear,
			border_color='black',
			border_width=1,
			corner_radius=5,
			alignment=ui.ALIGN_CENTER
		)
		self.reset.title = 'Clear'
		self.add_subview(self.reset)
		self.disable(self.reset)

		self.undo = ui.Button(
			background_image=ui.Image('iob:ios7_undo_256'),
			frame=(800, 400, 60, 60),
			action=self.backward
		)
		self.add_subview(self.undo)
		self.disable(self.undo)

		self.saveas = ui.Button(
			tint_color='black',
			frame=(750, 500, 160, 40),
			font=('<system>', 28),
			action=self.write,
			border_width=1,
			corner_radius=5,
			alignment=ui.ALIGN_CENTER
		)
		self.saveas.title = 'Save as'
		self.add_subview(self.saveas)

		self.loadfrom = ui.Button(
			tint_color='black',
			frame=(750, 550, 160, 40),
			font=('<system>', 28),
			action=self.read,
			border_width=1,
			corner_radius=5,
			alignment=ui.ALIGN_CENTER
		)
		self.loadfrom.title = 'Load from'
		self.add_subview(self.loadfrom)

		self.delete = ui.Button(
			tint_color='red',
			frame=(750, 640, 160, 40),
			font=('<system>', 28),
			action=GameConfig.delete,
			border_width=1,
			corner_radius=5,
			alignment=ui.ALIGN_CENTER
		)
		self.delete.title = 'Delete'
		self.add_subview(self.delete)

		self.apply_config(GameConfig().load())
		self.save_config()

	def show(self):
		super().present(style='fullscreen', orientations='landscape')

	def get_label(self):
		return self.scores[int(1/2-self.player/2)]

	def cell_tapped(self, coordinate):
		self.enable(self.reset)
		self.enable(self.undo)
		if len(self.history) > 0:
			self.get_cell(*self.history[-1]).reset_mark()
		self.get_cell(*coordinate).set_disc(self.player)
		self.history.append(coordinate)
		self.get_cell(*coordinate).set_mark()
		self.get_label().border_width = 0
		self.player *= -1
		if self.player == -1 and self.cpu:
			board = [
				[
					[
						[
							self.get_cell(x, y, z, w).player for x in range(4)
						] for y in range(4)
					] for z in range(4)
				] for w in range(4)
			]
			next_coordinate = cpu.next(board, -1)
			self.cell_tapped(int2coordinate(next_coordinate))
		self.get_label().border_width = 1.5
		self.aggregate()
		self.save_config()

	def backward(self, sender):
		if len(self.history) == 0:
			return
		last = self.history.pop(-1)
		self.get_cell(*last).clear()
		self.get_label().border_width = 0
		self.player *= -1
		self.get_label().border_width = 1.5
		if len(self.history) == 0:
			self.disable(self.reset)
			self.disable(self.undo)
		else:
			self.get_cell(*self.history[-1]).set_mark()
		self.aggregate()
		self.save_config()

	def get_section(self, z, w):
		return self.sections[z][w]

	def get_cell(self, x, y, z, w):
		return self.get_section(z, w).get_cell(x, y)

	def get_cells(self):
		for x, y, z, w in product(range(4), range(4), range(4), range(4)):
			yield self.get_cell(x, y, z, w)

	def clear(self, sender=None):
		if sender is not None:
			try:
				alert('Are you sure you want to reset the game?', '', 'Reset')
			except KeyboardInterrupt:
				return
		self.player = 1
		self.black, self.white = 0, 0
		self.history.clear()
		self.disable(self.reset)
		self.disable(self.undo)
		self.scores[0].border_width = 1.5
		self.scores[1].border_width = 0
		self.scores[0].set_score(0)
		self.scores[1].set_score(0)
		for cell in self.get_cells():
			cell.clear()
		self.save_config()

	def aggregate(self):
		def _aggr(vec):
			def start(val):
				if val == 1:
					return [0]
				elif val == -1:
					return [3]
				else:
					return range(4)

			for X, Y, Z, W in vec:
				if (X, Y, Z, W) == (0, 0, 0, 0):
					continue
				for x, y, z, w in product(start(X), start(Y), start(Z), start(W)):
					s = sum(
						self.get_cell(x+X*i, y+Y*i, z+Z*i, w+W*i).player for i in range(4)
					)
					if s == 4:
						self.black += 1
					elif s == -4:
						self.white += 1

		self.black, self.white = 0, 0

		# 1D
		for i in range(4):
			_aggr([[1, 0, 0, 0][i:]+[1, 0, 0, 0][:i]])

		# 2D
		_aggr(product([-1, 1], [1], [0], [0]))  # x-y
		_aggr(product([-1, 1], [0], [1], [0]))  # x-z
		_aggr(product([-1, 1], [0], [0], [1]))  # x-w
		_aggr(product([0], [-1, 1], [1], [0]))  # y-z
		_aggr(product([0], [-1, 1], [0], [1]))  # y-w
		_aggr(product([0], [0], [-1, 1], [1]))  # z-w

		# 3D
		_aggr(product([-1, 1], [-1, 1], [1], [0]))  # x-y-z
		_aggr(product([-1, 1], [-1, 1], [0], [1]))  # x-y-w
		_aggr(product([-1, 1], [0], [-1, 1], [1]))  # x-z-w
		_aggr(product([0], [-1, 1], [-1, 1], [1]))  # y-z-w

		# 4D
		_aggr(product([-1, 1], [-1, 1], [-1, 1], [1]))

		self.scores[0].set_score(self.black)
		self.scores[1].set_score(self.white)

	def apply_config(self, config):
		self.clear()
		for score in self.scores:
			score.border_width = 0
		self.cpu.value = config.cpu
		self.history = config.history
		if len(self.history) > 0:
			self.enable(self.reset)
			self.enable(self.undo)
			self.get_cell(*self.history[-1]).set_mark()
		for coordinate in self.history:
			self.get_cell(*coordinate).set_disc(self.player)
			self.player *= -1
		self.get_label().border_width = 1.5
		self.aggregate()

	def make_config(self):
		board = [0] * 256
		for x, y, z, w in product(range(4), range(4), range(4), range(4)):
			board[w*64+z*16+y*4+x] = self.get_cell(x, y, z, w).player
		return GameConfig(
			history=self.history,
			cpu=self.cpu.value
		)

	def save_config(self, sender=None):
		self.make_config().save()

	def write(self, sender):
		self.make_config().saveas()

	def read(self, sender):
		config = self.make_config().load_from()
		if config is not None:
			self.apply_config(config)

	def disable(self, sender):
		sender.enabled = False
		sender.alpha = .3

	def enable(self, sender):
		sender.enabled = True
		sender.alpha = 1.0
