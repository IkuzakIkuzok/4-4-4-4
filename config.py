
# (c) 2020 Kazuki KOHZUKI

import dialogs
from configparser import ConfigParser
from hashlib import sha512
from os import remove
from utils import *

FILENAME = './history'
DIRNAME = './records'


class GameConfig(ConfigParser):
	def __init__(
		self,
		history=[],
		cpu=False,
		*args, **kwargs
	):
		super().__init__(*args, **kwargs)
		self.history = [coordinate2int(coordinate) for coordinate in history]
		self.cpu = cpu

	def get_all_records():
		with open(f'{DIRNAME}/_index', 'r') as f:
			files = f.read().splitlines()

		data = {}
		for file in files:
			if not file:
				continue
			hash, name = file.split('=', 1)
			data[name] = hash

		return data

	def save(self, path=FILENAME):
		self.add_section('game')
		self.set('game', 'history', str(self.history))
		self.set('game', 'cpu', str(self.cpu))

		with open(path, 'w', encoding='utf-8') as f:
			self.write(f)

	def saveas(self):
		try:
			name = dialogs.input_alert('Game title').strip()
		except KeyboardInterrupt:
			return

		if name == '':
			dialogs.alert(
				'The name cannot be empty.', '', 'OK', hide_cancel_button=True
			)
			return

		hash = sha512(name.encode('utf-8')).hexdigest()
		records = GameConfig.get_all_records()
		if hash in records.values():
			dialogs.alert(
				f'Record \'{name}\' already exists.', '', hide_cancel_button=True
			)
			return

		with open(f'{DIRNAME}/_index', 'a', encoding='utf-8') as f:
			f.write(f'{hash}={name}\n')

		self.save(f'{DIRNAME}/{hash}')

	def load(self, path=FILENAME):
		self.read(path, encoding='utf-8')
		if self.has_section('game'):
			_history = eval(self['game']['history'])
			self.history = [int2coordinate(val) for val in _history]
			self.cpu = eval(self['game']['cpu'])

		return self

	def load_from(self):
		records = GameConfig.get_all_records()
		if len(records) == 0:
			return

		file = dialogs.list_dialog('Select record', list(records.keys()))
		if file is None:
			return
		hash = records[file]
		return self.load(f'{DIRNAME}/{hash}')

	def delete(sender):
		records = GameConfig.get_all_records()
		if len(records) == 0:
			return

		file = dialogs.list_dialog('Select record', list(records.keys()))
		if file is None:
			return

		hash = records[file]
		remove(f'{DIRNAME}/{hash}')

		del records[file]
		with open(f'{DIRNAME}/_index', 'w') as f:
			for name, hash in records.items():
				f.write(f'{hash}={name}\n')

		dialogs.alert(
			f'Record \'{file}\' deleted.', '', 'OK', hide_cancel_button=True
		)
