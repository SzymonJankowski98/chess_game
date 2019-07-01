import tkinter
import random
import os

path = os.path.dirname(__file__)
os.chdir(path)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800


class WrongPlayerException(Exception):
    """"Wrong player number"""
    pass


class Figure:
    def __init__(self, player=1):
        if player == 1 or player == 2:
            self.player = player
        else:
            raise WrongPlayerException()

    def possible_moves_direction(self, x, y, board, *directions):
        dict = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0), 'NE': (1, -1), 'NW': (-1, -1), 'SE': (1, 1), 'SW': (-1, 1)}
        moves = []
        for i in directions:
            moves += self.__possible_moves_direction_helper(x, y, board, dict[i])
        return moves

    def __possible_moves_direction_helper(self, x, y, board, direction):
        moves = []
        try:
            if x + direction[0] < 0 or y + direction[1] < 0:
                return moves
            while board[x + direction[0]][y + direction[1]] is None:
                moves.append((x + direction[0], y + direction[1]))
                x += direction[0]
                y += direction[1]
            if board[x + direction[0]][y + direction[1]].player != self.player:
                moves.append((x + direction[0], y + direction[1]))
            return moves
        except IndexError:
            return moves

    @staticmethod
    def possible_moves_with_check(moves, x, y, board, player):
        result = []
        for i in moves:
            king_cords = King.find_king(board, player)
            tempboard = [list(p2) for p2 in board]
            tempboard[i[0]][i[1]] = tempboard[x][y]
            tempboard[x][y] = None
            if x == king_cords[0] and y == king_cords[1]:
                king_cords = i
            if not King.check_for_check(tempboard, player, king_cords):
                result.append(i)
        return result


class King(Figure):
    def __init__(self, player):
        super().__init__(player)
        self.is_checked = False
        if self.player == 1:
            self.image = tkinter.PhotoImage(file=path+"\\images\\king_white.png")
        else:
            self.image = tkinter.PhotoImage(file=path+"\\images\\king_black.png")

    @staticmethod
    def find_king(board, player):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if type(board[i][j]) == King:
                    if board[i][j].player == player:
                        return tuple((i, j))
        return tuple((-1, -1))

    @staticmethod
    def check_for_check(board, player, king_cord):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] is not None and board[i][j].player != player:
                    if king_cord in board[i][j].possible_moves(i, j, board):
                        return True
        return False

    def possible_moves(self, x, y, board):
        shifts = [(1, 1), (-1, -1), (1, -1), (-1, 1), (1, 0), (0, 1), (-1, 0), (0, -1)]
        moves = []
        for (i, j) in shifts:
            if x + i < 0 or y + j < 0:
                continue
            try:
                if board[x + i][y + j] is None:
                    moves.append((x + i, y + j))
                elif board[x + i][y + j].player != self.player:
                    moves.append((x + i, y + j))
            except IndexError:
                pass
        return moves


class Queen(Figure):
    def __init__(self, player):
        super().__init__(player)
        if self.player == 1:
            self.image = tkinter.PhotoImage(file=path+"\\images\\queen_white.png")
        else:
            self.image = tkinter.PhotoImage(file=path+"\\images\\queen_black.png")

    def possible_moves(self, x, y, board):
        return self.possible_moves_direction(x, y, board, "N", "W", "S", "E", "NE", "NW", "SE", "SW")


class Bishop(Figure):
    def __init__(self, player):
        super().__init__(player)
        if self.player == 1:
            self.image = tkinter.PhotoImage(file=path+"\\images\\Bishop_white.png")
        else:
            self.image = tkinter.PhotoImage(file=path+"\\images\\Bishop_black.png")

    def possible_moves(self, x, y, board):
        return self.possible_moves_direction(x, y, board, "NE", "NW", "SE", "SW")


class Knight(Figure):
    def __init__(self, player):
        super().__init__(player)
        if self.player == 1:
            self.image = tkinter.PhotoImage(file=path+"\\images\\knight_white.png")
        else:
            self.image = tkinter.PhotoImage(file=path+"\\images\\knight_black.png")

    def possible_moves(self, x, y, board):
        shifts = [(-2, 1), (-1, 2), (-2, -1), (-1, -2), (2, 1), (1, 2), (2, -1), (1, -2)]
        moves = []
        for (i, j) in shifts:
            if x + i < 0 or y + j < 0:
                continue
            try:
                if board[x + i][y + j] is None:
                    moves.append((x + i, y + j))
                elif board[x + i][y + j].player != self.player:
                    moves.append((x + i, y + j))
            except IndexError:
                pass
        return moves


class Rook(Figure):
    def __init__(self, player):
        super().__init__(player)
        if self.player == 1:
            self.image = tkinter.PhotoImage(file=path+"\\images\\rook_white.png")
        else:
            self.image = tkinter.PhotoImage(file=path+"\\images\\rook_black.png")

    def possible_moves(self, x, y, board):
        return self.possible_moves_direction(x, y, board, "N", "W", "S", "E")


class Pawn(Figure):
    def __init__(self, player):
        super().__init__(player)
        self.first_move = True
        if self.player == 1:
            self.image = tkinter.PhotoImage(file=path+"\\images\\pawn_white.png")
        else:
            self.image = tkinter.PhotoImage(file=path+"\\images\\pawn_black.png")

    def possible_moves(self, x, y, board):
        moves = []
        if self.player == 1:
            if y - 1 >= 0:
                try:
                    if board[x][y - 1] is None:
                        moves.append((x, y - 1))
                        if self.first_move and board[x][y - 2] is None:
                            moves.append((x, y - 2))
                except IndexError:
                    pass
                try:
                    if x - 1 >= 0 and board[x - 1][y - 1].player is not self.player:
                        moves.append((x - 1, y - 1))
                except (IndexError, AttributeError):
                    pass
                try:
                    if board[x + 1][y - 1].player is not self.player:
                        moves.append((x + 1, y - 1))
                except (IndexError, AttributeError):
                    pass
        else:
            try:
                if board[x][y + 1] is None:
                    moves.append((x, y + 1))
                    if self.first_move and board[x][y + 2] is None:
                        moves.append((x, y + 2))
            except IndexError:
                pass
            try:
                if x - 1 >= 0 and board[x - 1][y + 1].player is not self.player:
                    moves.append((x - 1, y + 1))
            except (IndexError, AttributeError):
                pass
            try:
                if board[x + 1][y + 1].player is not self.player:
                    moves.append((x + 1, y + 1))
            except (IndexError, AttributeError):
                pass

        return moves


class Game:
    def __init__(self):
        self.player_turn = random.randint(1, 2)

        self.clicked = (-1, -1)
        self.moves = []

        self.gameboard = tkinter.Canvas(root, borderwidth=0)
        self.figures = self.create_figures()
        self.gameboard.bind("<Button-1>", self.click_event)
        self.create_board()

        self.info1 = tkinter.Frame(root)
        self.info2 = tkinter.Frame(root)
        self.info1.place(relx=0.5, rely=0.05, anchor="center")
        self.info2.place(relx=0.5, rely=0.95, anchor="center")
        dict = {1: "białego", 2: "czarnego"}
        self.label = tkinter.Label(self.info1, text="Ruch gracza {}".format(dict[self.player_turn]), pady=5, font=("Open Sans", 22))
        self.label.pack()
        button_img = tkinter.PhotoImage(file=path+"\\images\\button_new_game.png")
        restart_button = tkinter.Button(self.info2, image=button_img, command=self.new_game, borderwidth= 0)
        restart_button.pack()

        root.bind('<Configure>', self.create_board)

        root.mainloop()

    def set_info(self, win=False):
        if win:
            dict = {1: "czarny", 2: "biały"}
            self.label.config(text="Gracza {} wygrał!".format(dict[self.player_turn]), fg="#800303")
        else:
            dict = {1: "białego", 2: "czarnego"}
            self.label.config(text="Ruch gracza {}".format(dict[self.player_turn]), fg="black")

    def new_game(self):
        self.figures = self.create_figures()
        self.create_board()
        self.player_turn = random.randint(1, 2)
        self.set_info()

    def actual_height_and_width(self):
        return root.winfo_height(), root.winfo_width()

    def check_for_win(self):
        for i in range(8):
            for j in range(8):
                if self.figures[j][i] is not None and self.figures[j][i].player == self.player_turn:
                    moves = self.figures[j][i].possible_moves(j, i, self.figures)
                    if King.possible_moves_with_check(moves, j, i, self.figures, self.player_turn):
                        return False
        return True

    def click_event(self, event):
        picked = None
        if self.clicked is not (-1, -1):
            picked = self.clicked
        height, width = self.actual_height_and_width()
        size = (min(height, width) * 0.8) / 8
        self.clicked = (int(event.x / size), int(event.y / size))
        if picked is not None and self.clicked in self.moves:
            if type(self.figures[picked[0]][picked[1]]) == Pawn:
                self.figures[picked[0]][picked[1]].first_move = False
            self.figures[self.clicked[0]][self.clicked[1]] = self.figures[picked[0]][picked[1]]
            self.figures[picked[0]][picked[1]] = None
            self.clicked = (-1, -1)
            self.moves = []
            if self.player_turn == 1:
                self.player_turn = 2
            else:
                self.player_turn = 1
            self.create_board()
            if self.check_for_win():
                self.set_info(True)
            else:
                self.set_info()
        else:
            self.create_board()

    def create_board(self, event=0):
        self.gameboard.delete("all")
        height, width = self.actual_height_and_width()
        size = min(height, width)*0.8
        self.gameboard.place(relx=0.5, rely=0.5, width=size, height=size, anchor="center")
        for i in range(0, 8):
            for j in range(0, 8):
                if i % 2 == 0:
                    if j % 2 == 0:
                        self.gameboard.create_rectangle(size / 8 * j, size / 8 * i, size / 8 * (j + 1), size / 8 * (i + 1), fill='#800303')
                    else:
                        self.gameboard.create_rectangle(size / 8 * j, size / 8 * i, size / 8 * (j + 1), size / 8 * (i + 1), fill='white')
                else:
                    if j % 2 == 0:
                        self.gameboard.create_rectangle(size / 8 * j, size / 8 * i, size / 8 * (j + 1), size / 8 * (i + 1), fill='white')
                    else:
                        self.gameboard.create_rectangle(size / 8 * j, size / 8 * i, size / 8 * (j + 1), size / 8 * (i + 1), fill='#800303')

                #highlighting picked figure
                if i == self.clicked[1] and j == self.clicked[0]:
                    self.moves = []
                    if self.figures[self.clicked[0]][self.clicked[1]] is not None and self.figures[self.clicked[0]][self.clicked[1]].player == self.player_turn:
                        self.moves = self.figures[j][i].possible_moves(j, i, self.figures)
                        self.moves = King.possible_moves_with_check(self.moves, j, i, self.figures, self.player_turn)
        if self.moves:
            self.gameboard.create_rectangle(size / 8 * self.clicked[0], size / 8 * self.clicked[1], size / 8 * (self.clicked[0] + 1), size / 8 * (self.clicked[1] + 1), fill='#2d48e0')
            for x in self.moves:
                self.gameboard.create_rectangle(size / 8 * x[0], size / 8 * x[1], size / 8 * (x[0] + 1), size / 8 * (x[1] + 1), fill='#1cc766')
        else:
            self.clicked = (-1, -1)

        self.set_figures()

    def create_figures(self):
        figures = [[None for _ in range(8)] for _ in range(8)]

        figures[0][0] = Rook(2)
        figures[7][0] = Rook(2)
        figures[0][7] = Rook(1)
        figures[7][7] = Rook(1)

        figures[1][0] = Knight(2)
        figures[6][0] = Knight(2)
        figures[1][7] = Knight(1)
        figures[6][7] = Knight(1)

        figures[2][0] = Bishop(2)
        figures[5][0] = Bishop(2)
        figures[2][7] = Bishop(1)
        figures[5][7] = Bishop(1)

        figures[3][0] = Queen(2)
        figures[4][0] = King(2)
        figures[3][7] = Queen(1)
        figures[4][7] = King(1)
        for i in range(8):
            figures[i][1] = Pawn(2)
            figures[i][6] = Pawn(1)

        return figures

    def set_figures(self):
        height, width = self.actual_height_and_width()
        size = min(height, width) * 0.8
        position = size / 16
        for i in range(len(self.figures)):
            for j in range(len(self.figures[0])):
                if self.figures[i][j] is not None:
                    self.gameboard.create_image((i*position*2)+position, (j*position*2)+position, image=self.figures[i][j].image, anchor="center")


root = tkinter.Tk()
root.minsize(700, 700)
root.title("Szachy")
root.iconbitmap(path+"\\images\\favicon.ico")
g = Game()