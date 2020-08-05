from machine import Pin
import os
import pyb
import micropython
import random
from time import sleep
micropython.alloc_emergency_exception_buf(100)

# 3 Pin Board in  - входы стола для выбора линии (эмулятор)
bd_ins = [Pin('X11'),Pin('X12'),Pin('Y11')]
# 3 Pin microcontroller out  - выходы микроконтроллера для выбора линии
mc_outs = [Pin('X18', Pin.OUT),Pin('X19', Pin.OUT),Pin('X20', Pin.OUT)]

# 8 Pin microcontroller in  - входы данных на микроконтроллере X1 .. X8
mc_data = [ Pin('X' + str(i) ) for i in range(1,9) ]
# 8 Pin microcontroller out  - выходы данных на столе (эмулятор)
#bd_data = [ Pin('Y' + str(i), Pin.OUT) for i in range(1,9) ]
# Установим в IN для реального стенда
bd_data = [ Pin('Y' + str(i)) for i in range(1,9) ]

# Проверка одной линии (только вместе с эмулятором)
def check_pins(inn, out):    
    if inn.value() != 0:
        return False
    out.high()
    if inn.value() != 1:
        return False
    out.low()
    if inn.value() != 0:
        return False
    return True

# Проверка всех линий (только вместе с эмулятором)
def check_all_pins():
    print('\nChecking...\n')    
    res = [check_pins(bd_ins[i], mc_outs[i]) for i in range(0,3)]
    for r in res:
        if not r:
            return False
    res = [check_pins(mc_data[i], bd_data[i]) for i in range(0,8)]
    for r in res:
        if not r:
            return False
    return True

# Микроконтроллер
class Board:
    def __init__(self):        
        global u     

        # Буквы и цифры на доске
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        
        # Создадим доску 8x8
        self.area = []
        for j in range(0,8):
            self.area.append([])
            for i in range(0,8):
                self.area[j].append('.')

        # Обозначим массивы белых и чёрных фигур        
        self.w_figures = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'R', 'R', 'N', 'N', 'B', 'B', 'Q', 'K']
        self.b_figures = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'r', 'r', 'n', 'n', 'b', 'b', 'q', 'k']
        self.figures = self.w_figures + self.b_figures
        
        # Расставим фигуры на доске
        self.put_chess()
        # Для запоминания первой поднятой фигуры
        self.chess = '.'        
        self.tups_move = []
        self.bittaked = True
        # Список сделанных ходов ( хранится глобально )
        self.records = u        
        # Распечатаем доску
        print(self)
    
    # Провека на совпадение положения выключателя на доске и в памяти микроконтроллера
    def is_changed(self, i,j, state):
        is_figure = self.area[j][i] in self.figures
        if is_figure == state:
            return False
        else:
            return True
    
    # Расставим один ряд фигур списком 
    def put_list(self, l, j):
        for i, e in enumerate(l):
            self.area[j][i] = e

    # Расставим все фигуры
    def put_chess(self):
        self.put_list(list('rnbqkbnr'), self.numbers.index('8'))
        self.put_list(list('pppppppp'), self.numbers.index('7'))
        self.put_list(list('PPPPPPPP'), self.numbers.index('2'))
        self.put_list(list('RNBQKBNR'), self.numbers.index('1'))

    # Функция анализа поля
    def read_bits(self, i):
        bits = [not p.value() for p in mc_data ]
        for j, bit in enumerate(bits):
            if self.is_changed(i, j, bit):                
                # Первое взятие фигуры
                if self.bittaked and bit == 0:
                    #self.write_log('первое взятие' , 1)
                    self.chess = self.area[j][i]
                    self.area[j][i] = '.'
                    self.bittaked = False
                    self.tups_move.append((self.chess, i, j))
                # Недостижимая ситуация
                elif self.bittaked and bit == 1:
                    #self.write_log('едостижимая ситуация' , 1)
                    self.area[j][i] = self.chess
                    print('bad situation')
                    self.records.append(['bad situation', 'self.bittaked and bit == 1'])
                    #self.write_log('bad situation', bit)
                # Поднятие второй фигуры
                elif not self.bittaked and bit == 0:
                    self.area[j][i] = '.'
                # Ставим первую фигуру на новое место
                elif not self.bittaked and bit == 1:
                    self.area[j][i] = self.chess
                    self.bittaked = True
                    if len(self.tups_move) == 1:
                        if self.tups_move[0] != (self.chess, i, j):
                            c, ii, jj = self.tups_move[0]
                            self.records.append([str(self.letters[ii]) + str(self.numbers[jj]), str(self.letters[i]) + str(self.numbers[j])])
                            
                            # Закомментировать блок если нужно запоминать все ходы
                            if len(self.records) > 1:
                                if self.records[-1][0] == self.records[-2][1]:
                                    in_one = [ self.records[-2][0], self.records[-1][1] ]
                                    self.records.pop()
                                    self.records.pop()
                                    self.records.append(in_one)
                            
                            print(self)
                    else:
                        print('bad len(self.tups_move) !!!!!!!!!!!!!!!!')
                    self.tups_move = []
                    
                else:
                    print('bad else situation')
                    self.records.append(['bad else situation', 'else'])

    # Установим значение 0 или 1 на определённой ноге    
    def set_pin(self, pin, value):
        if value:
            pin.high()
        else:
            pin.low()

    # Расставим сигнал 0 .. 7 на выходы микроконтроллера
    def send_signal(self, i):
        self.set_pin(mc_outs[0], i & 1)                     # Pin X18 (младший)
        self.set_pin(mc_outs[1], int((i & 2) / 2))          # Pin X19
        self.set_pin(mc_outs[2], int((i & 4) / 4))          # Pin X20 (старший)

    # Распечатка доски
    def __repr__(self):
        s = ''
        for j in range(7,-1,-1):
            s += str(self.numbers[j]) + '| ' 
            for i in range(0,8):
                s += self.area[j][i] + ' '
            s += '\n'
        
        for i in range(0,18):
            s += '-'
        s += '\n   '
        for i in range(0,8):
            s += self.letters[i] + ' '
        s += '\n'
        return s

# Эмулятор - не трогать
class Emulator:
    def __init__(self):
        self.area = []
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        #self.numbers = ['8', '7', '6', '5', '4', '3', '2', '1']
        for j in range(0,8):
            self.area.append([])
            for i in range(0,8):
                self.area[j].append(0)
        self.put_chesses_on_board()
    
    def put_list(self, l, j):
        for i, e in enumerate(l):
            self.area[j][i] = int(e)
        
    def put_chesses_on_board(self):
        self.put_list(list('11111111'), 7)
        self.put_list(list('11111111'), 6)
        self.put_list(list('11111111'), 1)
        self.put_list(list('11111111'), 0)
        pass
    
    def get_list_coords_for_bit(self, bit):
        l = []
        for j in range(0,8):
            for i in range(0,8):
                if self.area[j][i] == bit:
                    l.append((i,j))
        return l
    
    
    def getRandCoord(self, zero_one = None, exclude = None):
        if zero_one is None:
            i = random.randint(0, 7)
            j = random.randint(0, 7)
            if exclude is not None:
                while i == exclude[0] and j == exclude[1]:
                    i = random.randint(0, 7)
                    j = random.randint(0, 7)
            return (i,j)
        elif zero_one == 1 or zero_one == 0:
            l = self.get_list_coords_for_bit(zero_one)
            return l[random.randint(0, len(l)-1)]
        else:
            #raise 'bad coordinate'
            print('bad getRandCoord')
            return (-1,-1)
            
    
    def take_chess(self, i, j):
        self.area[j][i] = 0
        return i, j
    
    def take_chess_random(self):
        i, j = self.getRandCoord(zero_one = 1)
        self.take_chess(i,j)
        return i, j
    
    def prepare_to_put(self, coord, gen = None):
        if gen is None:
            i, j = coord
        else:
            i, j = self.getRandCoord(exclude = coord)
        #print((i,j))
        if self.area[j][i] == 1:
            for _ in range(0,5):
                self.take_chess(i, j)
                sleep(0.0001)
                self.put_chess(i, j)
                sleep(0.0001)
                self.take_chess(i, j)
                sleep(0.0001)
            #self.take_chess(i, j)
        return (i,j)
        
    def put_chess(self, i, j):
        self.area[j][i] = 1
        #print((i,j))
        
    def __repr__(self):
        s = ''
        for j in range(0,8):
            for i in range(0,8):
                s += str(self.area[j][i]) + ' '
            s += '\n'
        return s
    
    def parse_str(self, s):
        s = s.upper()
        return self.letters.index(s[0]), self.numbers.index(s[1])
    
    def generate_move(self):
        i, j = self.getRandCoord(zero_one = 1)
        inext, jnext = self.getRandCoord( exclude = (i,j) )
        return str(self.letters[i]) + str(self.numbers[j]) + str(self.letters[inext]) + str(self.numbers[jnext])
    
    def make_move_1(self, str):
        ist, jst = self.parse_str(str)
                
        sleep(0.01)
        for i in range(0,5):
            self.take_chess(ist, jst)
            sleep(0.0001)
            self.put_chess(ist, jst)
            sleep(0.0001)
            self.take_chess(ist, jst)
            sleep(0.0001)
    
    def make_move_2(self, str):            
        ien, jen = self.parse_str(str)
        sleep(0.01)
        ien, jen = self.prepare_to_put( coord = (ien, jen) )
    
    def make_move_3(self, str):
        ien, jen = self.parse_str(str)
        sleep(0.01)
        for i in range(0,5):
            self.put_chess(ien, jen)
            sleep(0.0001)
            self.take_chess(ien, jen)
            sleep(0.0001)
            self.put_chess(ien, jen)
            sleep(0.0001)
    
    def get_signal(self):
        r = 0
        for i, p in enumerate(bd_ins):
            r += p.value() * (2 ** i)        
        self.setLine(r)
        return r
    
    def set_pin(self, pin, value):
        if value:
            pin.high()
        else:
            pin.low()

    def setLine(self, i):        
        for j in range(0,8):
            self.set_pin(bd_data[j], self.area[j][i])

# Для работы микроконтроллера и эмулятора (а также микроконтроллера без эмулятора)
class WorkerReader():
    def __init__(self):
        print("worker reader created")
        # Создаём микроконтроллер
        self.b = Board()
        # Создаём эмулятор
        self.e = Emulator()

    # Если используется эмулятор сделаем правильно ход
    def make_move(self, str):
        self.e.make_move_1(str[:2])
        self.read_desk()
        self.e.make_move_2(str[2:])
        self.read_desk()
        self.e.make_move_3(str[2:])
        self.read_desk()
    
    # Прочитаем все состояния выключателей на доске
    def read_desk(self):
        # С эмулятором
        # Пробежим по всем столбцам на шахматной доске от 0 .. 7
        #for i in range(0,8):
        #    self.b.send_signal(i)
        #    i = self.e.get_signal()
        #    self.b.read_bits(i)

        # С реальным стендом
        # Пробежим по всем столбцам на шахматной доске от 0 .. 7
        for i in range(0,8):
            # Установим положения на выходах микроконтроллера
            self.b.send_signal(i) 
            # Считаем все входы микроконтроллера           
            self.b.read_bits(i)

###########################################################
### --- Основная логика программы ----------------- #######
###########################################################

# Список записанных ходов 
u = []
# Счётчик файлов для проверки 000 - 100
counterfiles = 0
# Имя файла по умолчанию ( где 000 это значение счётчика файлов)
filename = 'chess_000.txt'
# Формат записи одного хода  
record = ['E2','E4']
# Сформируем имя файла для записи партии, которого нет на диске
for counterfiles in range(0,100):
    filename = 'chess_' + '0' * (3 - len(str(counterfiles))) + str(counterfiles) + '.txt'
    if filename not in os.listdir(os.getcwd()):
        break
    
# Делаем запись партии в файл через обработчик прерываний
def record_match():
    # Включим красный(1) светодиод
    pyb.LED(1).on()
    print('Начинаю запись в файл...')    
    # Получим глобальные переменные
    global u
    global counterfiles
    global filename
    global record   

    # Разблокируем кучу иначе впадём в нехватку памяти
    micropython.heap_unlock()
    # Откроем файл и запишем данные
    with open(filename, 'w') as f:
        for record in u:
            f.write(record[0] + record[1] + '\n')
    print('Запись в файл ' + filename + ' успешно завершена!')
    # Заблокируем кучу как и было
    micropython.heap_lock()
    
    # Выключим красный(1) светодиод
    pyb.LED(1).off()

# Запись режима ( Режим записи партии / Режим простоя ) в файл
def write_command(text):
    with open ('data.bin', 'w') as f:
        f.write(text)

# Читает какое будет состояние ( Режим записи партии / Режим простоя ) из файла 
def read_write_state():
    if 'data.bin' in os.listdir(os.getcwd()):    
        s = ''
        with open ('data.bin', 'r') as f:
            s = f.read()
        if s == 'idle':
            write_command('recording')
            return True
        else:
            write_command('idle')
    else:
        write_command('idle')
    return False

if __name__ == "__main__":
    # Прочитаем режим работы
    state = read_write_state()
    
    if state:
        print('Режим записи партии')        
        # Включим синий(4) светодиод
        pyb.LED(4).on()

        # Создадим прогрммно кнопку USR для записи в файл
        sw = pyb.Switch()
        # Привяжем к ней функцию записи в файл
        sw.callback(record_match)

        # Создаём рабочий объект 
        w = WorkerReader()      
        # Здесь выполняем бесконечное чтение поля
        # Для схемы без эмулятора
        while True:
            w.read_desk()

        # Для схемы с эмулятором
        #for i in range(0,200):
        #    w.make_move(w.e.generate_move())
    else:
        print('Режим простоя')
        # Выключим синий(4) светодиод
        pyb.LED(4).off()
