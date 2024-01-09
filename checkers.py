import tkinter as tk
import tkinter.messagebox as tm
import copy

rules = \
"""\
Доска и начальная расстановка\n\
Доска 8×8 клеток располагается между партнерами таким образом, чтобы слева от \
играющего находилось тёмное угловое поле. В начальной позиции у каждого игрока по 12 шашек, расположенных в \
первых трёх рядах на чёрных клетках.\n\n
Правила ходов и взятия\n\
Первый ход делают чёрные шашки (обычно они \
красного цвета). «Простые» шашки могут ходить по диагонали на одно поле вперёд и бить только вперёд. Дамка может \
ходить на одно поле по диагонали вперёд или назад, при взятии ходит только через одно поле в любую сторону, \
а не на любое поле диагонали, как в русских или международных шашках. Взятие шашки соперника является \
обязательным. При нескольких вариантах взятия игрок выбирает вариант взятия по своему усмотрению, и в выбранном \
варианте необходимо бить все доступные для взятия шашки. При достижении последнего (восьмого от себя) \
горизонтального ряда простая шашка превращается в дамку. Если простая достигла последнего ряда во время взятия, \
то она превращается в дамку и останавливается, даже при возможности продолжить взятие.\n\n 
Окончание игры\n\
Игрок одерживает победу, взяв все шашки соперника, или когда у того не остаётся ходов. Игра заканчивается вничью, \
когда никто не может обеспечить себе победу, или по соглашению (одна сторона предлагает ничью, \
другая - принимает).\
"""

WIDTH = 560
HEIGHT = 560
players = ['x', 'o']
max_value: int = 9999999

board = \
    [
        ['-', 'o', '-', 'o', '-', 'o', '-', 'o'],
        ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
        ['-', 'o', '-', 'o', '-', 'o', '-', 'o'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
        ['-', 'x', '-', 'x', '-', 'x', '-', 'x'],
        ['x', '-', 'x', '-', 'x', '-', 'x', '-']
    ]

max_depth = 5

def is_enemy_piece(tile_1, tile_2):
    t1, t2 = tile_1.lower(), tile_2.lower()
    return (t1 == 'o' and t2 == 'x') or (t1 == 'x' and t2 == 'o')

def show_help(_):
    tm.showinfo('Правила игры:', rules)

class Game:
    def __init__(self, visible=False):  # visible - признак видимости объекта, по умолчанию - нет

        # self.game_board = board_0  # начальная расстановка шашек ('x' - человек, 'o' - компьютер, 'X' и 'O' - дамки)
        # self.game_board = board_1
        # self.game_board = board_2
        self.game_board = copy.deepcopy(board)

        self.visible = visible
        self.cols = len(self.game_board[0])  # количество столбцов игровой доски
        self.rows = len(self.game_board)  # количество строк игровой доски
        self.last_row = self.rows - 1  # номер последней строки
        self.square_size = 70  # экранный размер клетки

        self.first_move = False  # выбор того, за кем ход, False - человек, True- компьютер
        self.turn = self.first_move  # текущий игрок (аналогично)
        self.sel_row, self.sel_col = None, None  # выбранная клетка доски
        self.jumping = False  # признак того, что выполнятся взятие

        if self.visible:
            self.width = self.cols * self.square_size
            self.height = self.rows * self.square_size

            self.startup = tk.Tk()
            self.startup.title("Английские шашки (правила игры - F1)")

            self.canvas = tk.Canvas(self.startup, height=self.height, width=self.width)
            self.canvas.pack()
            # Устанавливаем окно по центру экрана:
            positionRight = int(self.startup.winfo_screenwidth() / 2 - self.width / 2)
            positionDown = int(self.startup.winfo_screenheight() / 2 - self.height / 2)
            self.startup.geometry(f"+{positionRight}+{positionDown}")

            self.draw()

            self.startup.bind('<Button-1>', self.evaluate_click)
            self.startup.bind('<KeyPress-F1>', show_help)

            self.startup.mainloop()

    def current_player(self):
        return players[self.turn]

    def get_tile(self, loc):
        row, col = loc[0], loc[1]
        if row is None or col is None or row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            return '#'
        return self.game_board[row][col]

    def get_moves(self, row, col):
        moves = []
        jumps = []
        piece = self.get_tile((row, col))
        if piece != '-':
            if piece == 'x':
                options = [[-1, -1], [-1, 1]]
            elif piece == 'o':
                options = [[1, -1], [1, 1]]
            elif piece == 'O' or piece == 'X':
                options = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
            else:
                options = []
            for i in options:
                new_loc = (row + i[0], col + i[1])
                new_tile = self.get_tile(new_loc)

                if new_tile == '-':
                    moves.append(new_loc)

                if is_enemy_piece(piece, new_tile):
                    new_loc = (new_loc[0] + i[0], new_loc[1] + i[1])
                    if self.get_tile(new_loc) == '-':
                        jumps.append(new_loc)
        return (True, jumps) if jumps else (False, moves)

    def get_all_moves(self):
        all_moves = {}
        all_jumps = {}
        current_player = self.current_player()
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.get_tile((row, col)).lower()
                if tile == current_player:
                    is_jump, moves = self.get_moves(row, col)
                    if moves:
                        if is_jump:
                            all_jumps[(row, col)] = moves
                        else:
                            all_moves[(row, col)] = moves
        return all_jumps if all_jumps else all_moves

    def evaluate_click(self, mouse_pos):
        #f"{['Ваш ход...', 'Думаю...'][self.turn]}"
        if not self.turn:
            row, col = get_clicked_coord(mouse_pos.y), get_clicked_coord(mouse_pos.x)
            moves = self.get_all_moves()
            moves_to = moves.get((self.sel_row, self.sel_col), None)
            tile = self.get_tile((row, col)).lower()
            # msg = 'Английские шашки'
            if not self.jumping and tile == self.current_player() and \
                    moves.get((row, col), None) is not None:
                self.sel_row, self.sel_col = row, col
            if moves_to is not None and (row, col) in moves_to:
                self.play(row, col)
            if is_enemy_piece(tile, self.current_player()):
                 msg = f"{['Ваш ход...', ][self.turn]}"
        msg = 'Думаю...'
        self.startup.title(msg)
        self.draw()
        self.make_ai_move()

        msg = 'Ваш ход...'
        self.startup.title(msg)
        self.draw()

    def play(self, to_row, to_col):
        from_row, from_col = self.sel_row, self.sel_col
        tile_char = self.get_tile((from_row, from_col))
        moves = self.get_moves(from_row, from_col)
        self.game_board[to_row][to_col] = tile_char
        self.game_board[from_row][from_col] = '-'
        became_king = ((tile_char == 'x' and to_row == 0) or (tile_char == 'o' and to_row == self.last_row))
        if became_king:
            self.game_board[to_row][to_col] = tile_char.upper()
        jump = moves[0]
        if jump:
            self.game_board[(from_row + to_row) // 2][(from_col + to_col) // 2] = '-'
            self.sel_row, self.sel_col = to_row, to_col
            self.jumping = self.get_moves(to_row, to_col)[0]
            if became_king:
                self.jumping = False

        if not self.jumping:
            self.next_turn()

    def next_turn(self):
        if self.jumping:
            return
        self.turn = not self.turn
        self.jumping = False
        self.sel_row, self.sel_col = None, None
        msg = self.check_winner()
        if msg is not None:
            self.draw()
            tm.showinfo('Игра окончена', msg)
            self.restart()

    def check_winner(self):
        if self.heuristic_value() == -max_value:
            return 'Вы победили!'
        elif self.heuristic_value() == max_value:
            return 'Вы проиграли...'
        return None

    def restart(self):
        self.turn = self.first_move
        self.sel_row, self.sel_col = None, None
        self.jumping = False
        self.game_board = copy.deepcopy(board)
        self.visible = True

    def draw(self):
        if self.jumping:
            self.startup.after(1000)
        for i in range(self.rows):
            for j in range(self.cols):

                x1 = j * self.square_size
                y1 = i * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = 'green' if (i + j) % 2 else 'lightgreen'
                if self.sel_row == i and self.sel_col == j:
                    color = 'white'

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        for r in range(self.rows):
            for c in range(self.cols):
                mark = self.game_board[r][c]
                if mark != '-':
                    x = WIDTH / 8 * c + WIDTH / 16
                    y = HEIGHT / 8 * r + HEIGHT / 16
                    fill, outline = ('darkgreen', 'black') if self.game_board[r][c].lower() == players[0] else (
                        'black', 'darkgreen')
                    width = 8 if mark.isupper() else 2
                    self.canvas.create_oval(x + 25, y + 25, x - 25, y - 25, fill=fill, outline=outline, width=width)

    def get_ai_move(self):
        move = minimax(self, max_depth, True)
        return move

    def make_ai_move(self):
        if self.current_player() != 'o':
            return
        move = self.get_ai_move()
        if (move == max_value) or (move == -max_value) or (move is None):
            self.restart()
            return
        self.sel_row, self.sel_col = move[0]
        row, col = move[1]
        self.play(row, col)
        if self.jumping:
            self.make_ai_move()

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__init__()
        memo[id(self)] = result

        for k, v in self.__dict__.items():
            if k not in ['square_size', 'width', 'height', 'startup', 'canvas']:
                setattr(result, k, copy.deepcopy(v, memo))
        setattr(result, 'visible', False)
        return result

    def heuristic_value(self):
        value_x, value_o = 0, 0
        for i in range(self.rows):
            for j in range(self.cols):
                match self.get_tile((i, j)):
                    case 'x':
                        value_x += 50
                    case 'X':
                        value_x += 150
                    case 'o':
                        value_o += 50
                    case 'O':
                        value_o += 150
                    case _:
                        pass
        if value_o == 0:
            return -max_value
        if value_x == 0:
            return max_value
        return value_o - value_x


def get_clicked_coord(mouse_pos):
    def ceil(x: float) -> int:
        return int(x) if x - int(x) <= 0 else int(x) + 1

    return ceil(8 * mouse_pos / WIDTH) - 1


def minimax(game: Game, depth: int, root: bool = True):
    strategy = {'x': lambda x, y: x > y, 'o': lambda x, y: x < y}
    start_value = {'x': max_value, 'o': -max_value}

    first_copy = copy.deepcopy(game)
    player = first_copy.current_player()
    moves = first_copy.get_all_moves()
    if not moves and not root:
        return [-max_value, max_value][player == 'x']
    if depth == 0:  # node is a terminal node then
        heuristic_value = first_copy.heuristic_value()
        return heuristic_value

    value = start_value[player]
    optimal_move = None
    any_move = None
    for start, moves_list in moves.items():
        second_copy = copy.deepcopy(first_copy)
        second_copy.sel_row = start[0]
        second_copy.sel_col = start[1]
        for to_row, to_col in moves_list:
            player = second_copy.current_player()
            new_value = minimax(second_copy, depth - 1, False)
            any_move = ((start[0], start[1]), (to_row, to_col))
            if strategy[player](value, new_value):
                value = new_value
                optimal_move = ((start[0], start[1]), (to_row, to_col))
    if not root:
        return value
    if optimal_move:
        return optimal_move
    return any_move

Game(True)
