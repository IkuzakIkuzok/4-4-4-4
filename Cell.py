
# (c) 2020 Kazuki KOHZUKI

import ui

CELL_SIZE = 40


class Cell(ui.View):
	def __init__(self, coordinate, *args, **kwargs):
		x, y, z, w = coordinate
		self.frame = (x*CELL_SIZE+.1, y*CELL_SIZE+.1, CELL_SIZE, CELL_SIZE)
		self._button = ui.Button(
			frame=(0, 0, CELL_SIZE, CELL_SIZE),
			action=self.tapped,
			tint_color='black',
			font=('<system>', CELL_SIZE*.8),
			border_color='black',
			border_width=1
		)
		self.add_subview(self._button)
		self._button.bring_to_front()
		self.coordinate = coordinate
		self.player = 0
	
	def tapped(self, sender):
		self.superview.superview.cell_tapped(self.coordinate)

	def set_disc(self, player):
		if not abs(player) == 1:
			return
		self._button.title = '●' if player == 1 else '◯'
		self.player = player
		self._button.touch_enabled = False
		self._button.action = None
	
	def set_mark(self):
		self._button.background_color = '#99bcff'
	
	def reset_mark(self):
		self._button.background_color = 'white'
	
	def clear(self):
		self.player = 0
		self._button.title = ''
		self._button.touch_enabled = True
		self._button.action = self.tapped
		self._button.background_color = 'white'


class Cells(ui.View):
	def __init__(self, z, w, *args, **kwargs):
		super().__init__(
			frame=(z*CELL_SIZE*4.2+20, w*CELL_SIZE*4.2+20, CELL_SIZE*4, CELL_SIZE*4),
			background_color='white',
			*args, **kwargs
		)
		self.border_color = 'black'
		self.border_width = 2.5
		
		self.cells = [
			[Cell(coordinate=(x, y, z, w)) for y in range(4)] for x in range(4)
		]
		for cells_y in self.cells:
			for cell in cells_y:
				self.add_subview(cell)
				cell.bring_to_front()
	
	def get_cell(self, x, y):
		return self.cells[x][y]

