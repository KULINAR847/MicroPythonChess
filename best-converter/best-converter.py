import os

class King:
	def __init__(self, position, figure, area):
		self.id = 0
		self.area = area
		self.position = position
		self.color = 'b' if figure == 'k' else 'w'
		self.next_positions = []
		self.figure = figure
		self.moves = []
		self.castle = False
	
	def can_move(self, is_castling=False):
		self.next_positions = []
		y = int(self.position[1])
		x = int(self.position[0])
		
		mas = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		for e in mas:
			if x + e[0] > 0 and x + e[0] < 9:
				if y + e[1] > 0 and y + e[1] < 9:
					if (self.area[x + e[0]][y + e[1]] == '.') or (self.area[x + e[0]][y + e[1]].color != self.color):
						self.next_positions.append((x + e[0], y + e[1]))
		
		if len(self.moves) == 0:
			self.next_positions.append((x + 2, y))
			self.next_positions.append((x - 2, y))

	def __repr__(self):
		return self.figure

class Queen:
	def __init__(self, position, figure, area):
		self.id = 0
		self.area = area
		self.position = position
		self.color = 'b' if figure == 'q' else 'w'
		self.next_positions = []
		self.figure = figure
		self.moves = []
	
	def can_move(self, is_castling=False):
		self.next_positions = []
		y = int(self.position[1])
		x = int(self.position[0])
		
		mas = []
		mas.append(list((x+i, y+i) for i in range(1,8) if x + i < 9 and y + 1 < 9))
		mas.append(list((x-i, y-i) for i in range(1,8) if x - i > 0 and y - 1 > 0))
		mas.append(list((x+i, y-i) for i in range(1,8) if x + i < 9 and y - 1 > 0))
		mas.append(list((x-i, y+i) for i in range(1,8) if x - i > 0 and y + 1 < 9))
		mas.append(list((x+i, y) for i in range(1,8) if x + i < 9))
		mas.append(list((x-i, y) for i in range(1,8) if x - i > 0))
		mas.append(list((x, y+i) for i in range(1,8) if y + i < 9))
		mas.append(list((x, y-i) for i in range(1,8) if y - i > 0))
		for line in mas:
			for e in line:
				if e[0] > 0 and e[0] < 9:
					if e[1] > 0 and e[1] < 9:
						if (self.area[e[0]][e[1]] == '.'):
							self.next_positions.append((e[0], e[1]))
						if (self.area[e[0]][e[1]] != '.'): 
							if (self.area[e[0]][e[1]].color != self.color):
								self.next_positions.append((e[0], e[1]))
							break

	def __repr__(self):
		return self.figure

class Elephant:
	def __init__(self, position, figure, area):
		self.id = 0
		self.area = area
		self.position = position
		self.color = 'b' if figure == 'b' else 'w'
		self.next_positions = []
		self.figure = figure
		self.moves = []
	
	def can_move(self, is_castling=False):
		self.next_positions = []
		y = int(self.position[1])
		x = int(self.position[0])
		
		mas = []
		mas.append(list((x+i, y+i) for i in range(1,8) if x + i < 9 and y + 1 < 9))
		mas.append(list((x-i, y-i) for i in range(1,8) if x - i > 0 and y - 1 > 0))
		mas.append(list((x+i, y-i) for i in range(1,8) if x + i < 9 and y - 1 > 0))
		mas.append(list((x-i, y+i) for i in range(1,8) if x - i > 0 and y + 1 < 9))
		
		for line in mas:
			for e in line:
				if e[0] > 0 and e[0] < 9:
					if e[1] > 0 and e[1] < 9:
						if (self.area[e[0]][e[1]] == '.'):
							self.next_positions.append((e[0], e[1]))
						if (self.area[e[0]][e[1]] != '.'): 
							if (self.area[e[0]][e[1]].color != self.color):
								self.next_positions.append((e[0], e[1]))
							break
				else:
					break

	def __repr__(self):
		return self.figure

class Horse:
	def __init__(self, position, figure, area):
		self.id = 0
		self.area = area
		self.position = position
		self.color = 'b' if figure == 'n' else 'w'
		self.next_positions = []
		self.figure = figure
		self.moves = []
	
	def can_move(self, is_castling=False):
		self.next_positions = []
		y = int(self.position[1])
		x = int(self.position[0])
		
		mas = [(-2,1),(-2,-1),(-1,2),(-1,-2),(1,2),(1,-2),(2,1),(2,-1)]
		for e in mas:
			if x + e[0] > 0 and x + e[0] < 9:
				if y + e[1] > 0 and y + e[1] < 9:
					if (self.area[x + e[0]][y + e[1]] == '.') or (self.area[x + e[0]][y + e[1]].color != self.color):
						self.next_positions.append((x + e[0], y + e[1]))

	def __repr__(self):
		return self.figure

class Rock:
	def __init__(self, position, figure, area):
		self.id = 0
		self.area = area
		self.position = position
		self.color = 'b' if figure == 'r' else 'w'
		self.can_rockery = False
		self.next_positions = []
		self.figure = figure
		self.moves = []
	
	def can_move(self, is_castling=False):
		self.next_positions = []
		y = int(self.position[1])
		x = int(self.position[0])
		
		if not is_castling:
			mas = []
			mas.append(list((x+i, y) for i in range(1,8) if x + i < 9))
			mas.append(list((x-i, y) for i in range(1,8) if x - i > 0))
			mas.append(list((x, y+i) for i in range(1,8) if y + i < 9))
			mas.append(list((x, y-i) for i in range(1,8) if y - i > 0))
			for line in mas:
				for e in line:
					if e[0] > 0 and e[0] < 9:
						if e[1] > 0 and e[1] < 9:
							if (self.area[e[0]][e[1]] == '.'):
								self.next_positions.append((e[0], e[1]))
							if (self.area[e[0]][e[1]] != '.'): 
								if (self.area[e[0]][e[1]].color != self.color):
									self.next_positions.append((e[0], e[1]))
								break
		else:
			if self.position == (1,1):
				self.next_positions.append((4, 1))
			if self.position == (8,1):
				self.next_positions.append((6, 1))
			if self.position == (1,8):
				self.next_positions.append((4, 8))
			if self.position == (8,8):
				self.next_positions.append((6, 8))

		
		

	def __repr__(self):
		return self.figure

class Pawn:
	def __init__(self, position, figure, area):
		self.id = 0
		self.area = area
		self.position = position
		self.color = 'b' if figure == 'p' else 'w'
		self.direction = -1 if self.color == 'b' else 1
		self.next_positions = []
		self.figure = figure
		self.moves = []

	def can_move(self, is_castling=False):
		self.next_positions = []
		y = int(self.position[1])
		x = int(self.position[0])
		d = self.direction
		c = self.color
		
		if len(self.moves) == 0 and self.area[x][y+d] == '.' and self.area[x][y+2*d] == '.':
			self.next_positions.append((x, y+2*d ))
		if y < 8 and y > 1 and self.area[x][y+d] == '.':
			self.next_positions.append((x, y+d ))
		if x-1 >=1 and y < 8 and y > 1 and self.area[x-1][y+d] != '.' and self.area[x-1][y+d].color != c:
			self.next_positions.append((x-1, y+d ))
		if x+1 <= 8 and y < 8 and y > 1 and self.area[x+1][y+d] != '.' and self.area[x+1][y+d].color != c:
			self.next_positions.append((x+1, y+d ))
		
		#print(str(self.position) + '   ' + str(self.next_positions) )
		'''	
		self.next_positions = []
		y = self.position[1] + self.direction
		x = self.position[0]
		if y < 8 and y > 1:
			if x - 1 > 0 and self.area[x - 1][y] != '.' and self.area[x - 1][y].color != self.color:
				self.next_positions.append((x - 1, y))
			if x + 1 < 9 and self.area[x + 1][y] != '.' and self.area[x + 1][y].color != self.color:
				self.next_positions.append((x + 1, y))
			if self.area[x][y] == '.':
				self.next_positions.append((x,y))
			if ((self.position[1] == 2 and self.color == 'w') or (self.position[1] == 7 and self.color == 'b')) and self.area[x][y + self.direction] == '.':
				self.next_positions.append((x,y + self.direction))
		'''

	def __repr__(self):
		return self.figure

class Board:
	def __init__(self, filename):
		
		self.letters = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
		self.numbers = [' ', '1', '2', '3', '4', '5', '6', '7', '8']
		self.list_moves = []
		
		self.filename = filename
		self.pawns = []
		self.rocks = []
		self.horses = []
		self.elephants = []
		self.queens = []
		self.kings = []
		self.allfig = []
		self.chess = '.'
		self.make_castling = False
		self.castle = 'O-O'
		self.res = []
		self.score = '1/2-1/2'
		self.capture = False
		self.last_color = 'b'
		self.rfig = '123'
		self.skip_count = 0
		
		self.area = []
		for i in range(0,9):
			self.area.append([])
			for j in range(0,9):
				self.area[i].append('.')

		self.push_figures()
		self.exchange_on_objects()
		self.allfig = self.pawns + self.rocks + self.horses + self.elephants + self.queens + self.kings
		
		self.get_list_moves()
		
		print(self)
	
	def get_list_moves(self):
		with open(self.filename, 'r') as f:
			self.list_moves = f.read().split('\n')
		if self.list_moves[-1] == '':
			self.list_moves.pop()
	
	def push_line(self, line, j):
		for i, e in enumerate(line):
			self.area[i][j] = e
	
	def push_figures(self):
		#p = Pawn()
		self.push_line('.rnbqkbnr', 8)
		self.push_line('.pppppppp', 7)
		self.push_line('.PPPPPPPP', 2)
		self.push_line('.RNBQKBNR', 1)
	
	def exchange_on_objects(self):
		for i in range(0,9):
			for j in range(0,9):
				if self.area[i][j] != '.':
					if self.area[i][j] == 'p' or self.area[i][j] == 'P':
						self.area[i][j] = Pawn((i,j), self.area[i][j], self.area)
						self.pawns.append(self.area[i][j])
					elif self.area[i][j] == 'r' or self.area[i][j] == 'R':
						self.area[i][j] = Rock((i,j), self.area[i][j], self.area)
						self.rocks.append(self.area[i][j])
					elif self.area[i][j] == 'n' or self.area[i][j] == 'N':
						self.area[i][j] = Horse((i,j), self.area[i][j], self.area)
						self.horses.append(self.area[i][j])
					elif self.area[i][j] == 'b' or self.area[i][j] == 'B':
						self.area[i][j] = Elephant((i,j), self.area[i][j], self.area)
						self.elephants.append(self.area[i][j])
					elif self.area[i][j] == 'k' or self.area[i][j] == 'K':
						self.area[i][j] = King((i,j), self.area[i][j], self.area)
						self.kings.append(self.area[i][j])
					elif self.area[i][j] == 'q' or self.area[i][j] == 'Q':
						self.area[i][j] = Queen((i,j), self.area[i][j], self.area)
						self.queens.append(self.area[i][j])
					else:
						print('bad symbol')
	
	def check_shah(self, f):
		figures = [ e for e in self.allfig if e.color == f.color ]
		#print(figures)
		#print(f.color)
		
		r = [ e.can_move() for e in figures ]
		king = [ e for e in self.allfig if e.color != f.color and e.figure.upper() == 'K' ][0]
		#print(king)
		if king is None or king == '':
			print('Не смог найти короля')
			input()
		for e in figures:
			if king.position in e.next_positions:
				print(e)
				#input()
				return e
		return False

	def check_shah_position(self, color, posXY):
		figures = [ e for e in self.allfig if e.color != color ]
		r = [ e.can_move() for e in figures ]
		#king = [ e for e in self.allfig if e.color != f.color and e.figure.upper() == 'K' ][0]
		for e in figures:
			if posXY in e.next_positions:
				return True
		return False
			
		
	def check_pat(self, f):
		figures = [ e for e in self.allfig if e.color != f.color ]
		r = [ e.can_move() for e in figures ]
		reslist = []
		for e in figures:
			reslist += e.next_positions
		if reslist == []:
			return True
		else:
			return False
	
	def check_mat(self, f):
		figures = [ e for e in self.allfig if e.color == f.color ]
		figures2 = [ e for e in self.allfig if e.color != f.color and e.figure.upper() != 'K']
		r = [ e.can_move() for e in figures ]
		king = [ e for e in self.allfig if e.color != f.color and e.figure.upper() == 'K' ][0]
		king.can_move()
		r = []
		for e in figures:
			r += e.next_positions
		
		# Проверка на возможность убежать королём
		for e in king.next_positions:
			if e not in r:
				return False
		
		# Проверка на возможность заблокировать короля
		a = f.position
		k = king.position
		
		n = max(abs(a[0] - k[0]), abs(a[1] - k[1]) )
		x = [ a[0] + i * int(abs(k[0] - a[0])/(k[0] - a[0]) if k[0] - a[0] != 0 else 0)  for i in range(0, n) ]
		y = [ a[1] + i * int(abs(k[1] - a[1])/(k[1] - a[1]) if k[1] - a[1] != 0 else 0)  for i in range(0, n) ]
		series = list(zip(x, y))
		r = [ e.can_move() for e in figures2 ]
		r = []
		for e in figures2:
			r += e.next_positions
		for e in series:
			if e in r:
				return False
		return True

	
	def check_next_move(self, index):
		s = self.list_moves[index]
		cmd = list(s.upper())
		_from = (self.letters.index(cmd[0]), self.numbers.index(cmd[1]))
		_to = (self.letters.index(cmd[2]), self.numbers.index(cmd[3]))
		temp = self.area[_from[0]][_from[1]]
		return (temp, _from, _to)
	
	def move(self, s, index):
		cmd = list(s.upper())
		
		_from = (self.letters.index(cmd[0]), self.numbers.index(cmd[1]))
		_to = (self.letters.index(cmd[2]), self.numbers.index(cmd[3]))
		
		if self.area[_from[0]][_from[1]] == '.':
			print('Ход не с фигуры ' + str(s))
			input()
			return False
		# Получаем фигуру
		temp = self.area[_from[0]][_from[1]]

		if not self.make_castling and temp.color == self.last_color:
			print('Ошибка цвета')
			input()
			return False
		
		# Будет ли взятие
		self.capture = self.area[_to[0]][_to[1]] != '.'
		
		# Проверяем рокировку
		if temp.figure.upper() == 'R' and len(temp.moves) == 0:
			if _to[0] == 6:
				if index + 1 < len(self.list_moves):
					f2, _from2, _to2 = self.check_next_move(index + 1)
					self.rfig = f2
					if f2.figure.upper() == 'K' and len(f2.moves) == 0 and abs(_from2[0] - _to2[0]) == 2:
						if self.check_shah_position(f2.color, _to2):
							print('Нельзя провести рокировку, фигура под боем')
							input()
							return False
						if (_from[0] > _from2[0]) and (_to[0] > _to2[0]):
							print('Рокировка сделана не правильно')
							input()
							return False
						self.make_castling = True
						self.castle = 'O-O'

			if _to[0] == 4:
				if index + 1 < len(self.list_moves):
					f2, _from2, _to2 = self.check_next_move(index + 1)
					self.rfig = f2
					if f2.figure.upper() == 'K' and len(f2.moves) == 0 and abs(_from2[0] - _to2[0]) == 2:
						if self.check_shah_position(f2.color, _to2):
							print('Нельзя провести рокировку, фигура под боем')
							input()
							return False
						if (_from[0] > _from2[0]) and (_to[0] > _to2[0]):
							print('Рокировка сделана не правильно')
							input()
							return False
						self.make_castling = True
						self.castle = 'O-O-O'
				

		elif not self.make_castling and temp.figure.upper() == 'K':
			if abs(_from[0] - _to[0]) == 2:
				if _to[0] - _from[0] > 0:
					self.castle = 'O-O'
				else:
					self.castle = 'O-O-O'
				self.make_castling = True
				if index + 1 < len(self.list_moves):
					f2, _from2, _to2 = self.check_next_move(index + 1)
					self.rfig = f2
					if f2.figure.upper() != 'R':
						print('Сейчас должна сходить ладья')
						input()
						return False
					else:
						f2.can_move(False)
						if len(f2.moves) != 0:
							print('Ладья уже ходила')
							input()
							return False
						
				if len(temp.moves) > 0:
					print('Ошибка движения короля')
					input()
					return False
				if self.check_shah_position(temp.color, _to):
					print('Ошибка король под боем')
					input()
					return False
		
		
		# Делаем проверку куда могла двигаться фигура
		temp.can_move(self.make_castling)
		# Снимаеи рокировку если была
		if self.make_castling and temp.position == self.rfig.position:
			self.make_castling = False
		
		
		# Блок для формирования записи
		figures = [ e for e in self.allfig if e.figure == temp.figure and e.color == temp.color ]
		r = [ e.can_move(self.make_castling) for e in figures ]
		r = sum([ 1 for e in figures if (_to[0], _to[1]) in e.next_positions])
		#if self.make_castling:
		#	self.res.append('make')
		if self.make_castling:
			self.skip_count += 1
			if self.skip_count == 1 or self.skip_count == 3:
				self.res.append([temp.color, self.castle, self.make_castling])
		else:
			self.skip_count = 0
			
			if r > 1:
				self.res.append([temp.color, str(str(temp).upper() if temp.figure.upper() != 'P' else '') + cmd[0].lower() + str('x' if self.capture else '') + cmd[2].lower() + cmd[3].lower(), self.make_castling])
			elif r == 1:
				self.res.append([temp.color, str(str(temp).upper() if temp.figure.upper() != 'P' else '') + str(cmd[0].lower() if temp.figure.upper() == 'P' and self.capture else '') +  str('x' if self.capture else '') + cmd[2].lower() + cmd[3].lower(), self.make_castling])
			else:
				print('Нет ни одного хода для данных фигур')
				input()
				return False

		# Поднимаем фигуру
		self.area[_from[0]][_from[1]] = '.'
		
		
		# Делаем проверку на возможный ход
		if (_to[0], _to[1]) in temp.next_positions:
			# Если был захват
			if self.capture:
				# Получаем фигуру, которая будет взята
				delfig = self.area[_to[0]][_to[1]]
				# Изымаем её из списка фигур
				self.allfig = self.del_figure(delfig)
			# Ставим фигуру на новое место
			self.area[_to[0]][_to[1]] = temp
			
			# Добавляем старые координаты в историю
			temp.moves.append(s)
			
			# Перезаписываем новые координаты
			temp.position = (_to[0], _to[1])
			
			# Проверка на шах
			if self.check_shah(temp):
				print('Шах')
				elem = self.res.pop()
				elem[1] += '+'
				self.res.append(elem)
				
				# Проверка на мат
				fatack = self.check_shah(temp)
				if self.check_mat(fatack):
					print('Мат')
					input()
					if temp.color == 'w':
						self.score = '1-0'
					if temp.color == 'b':
						self.score = '0-1'
					return False
			# Проверка на пат
			if not self.check_shah(temp) and self.check_pat(temp):
				print('Пат')
				input()
				return False
			
		else:
			print(temp.next_positions)
			print('Неразрешённый ход ' + s)
			input()
			return False
		print(self)
		self.last_color = temp.color
		return True

	def del_figure(self, fig):
		new_mas = []
		for e in self.allfig:
			if e == fig:
				continue
			new_mas.append(e)
		return new_mas

	def __repr__(self):
		s = ''
		for j in range(8,-1,-1):
			for i in range(0,9):
				if i == 0:
					s += str(j) + '|'
					continue
				if j == 0:
					s += self.letters[i] + ' '
					continue
				s += str(self.area[i][j]) + ' '
			
			if j > 0:
				s += '\n'
		return s
		
		return s


header = '''[Event ""]
[Site ""]
[Date "2020.3.21"]
[Round ""]
[White "Иван"]
[Black "Иван"]
[TimeControl "-"]
[Result "*"]
[ECO " "]

'''

##############################
# Печать на экране
##############################

files = [e for e in os.listdir() if 'chess' in e and '.txt' in e]
print(files)


for file in files:
	
	print(file[:-3] + 'pgn')
	#exit(0)
	b = Board(file)
	print(b.list_moves)
	for i, e in enumerate(b.list_moves):
		print('\n')
		print('----------------------')
		print(str(' '*(3-len(str(i+1))) + str(i+1)) + ' | ' + str(e))
		print('----------------------')
		if not b.move(e,i):
			break

	##############################
	# Формирование ходов
	##############################

	color = 'b'
	resstr = ''
	s = ''
	count_moves = 0
	for i, e in enumerate(b.res):
		if e[0] == color:
			print('Ошибка цвета при постобработке')
			input()
			break
		
		if i % 2 == 0:
			count_moves += 1
			s += str(count_moves) + '.'
		s += e[1] + ' '
		
		print(e)
		if len(s) > 125:
			if e[0] == 'b':
				s = s[:-1]
			resstr += s + '\n'
			s = ''
		
		color = e[0]

	if len(s) > 0:
		resstr += s


	##############################
	# Запись файла 
	##############################
	print(resstr)

	with open(file[:-3] + 'pgn', 'w') as f:
		f.write(str(header.replace('*', b.score) if b.score != '1/2-1/2' else header) + resstr + str('*' if b.score == '1/2-1/2' else '') + '\n\n' + str(b.score if b.score != '1/2-1/2' else ''))

	b.allfig = b.pawns + b.rocks + b.horses + b.elephants + b.queens + b.kings
	for e in b.allfig:
		print(str(e) + ' ' + str(e.position) + ' ' + str(e.moves))