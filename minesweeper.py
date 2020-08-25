import random
from string import ascii_lowercase

class Cell:
    def __init__(self):
        self.value = 0
        self.found = False
        self.flagged = False

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return ("F" if self.flagged else self.value) if self.found else " "

    def flag(self):
        if self.flagged:
            self.flagged = False
            self.found = False
            return -1
        else:
            self.flagged = True
            self.found = True
            return 1

class Game:
    def __init__(self):
        dimensions = {"a": {"rows": 16, "columns": 30, "mines": 99},
        "i": {"rows": 13, "columns": 15, "mines": 40},
        "b": {"rows": 8, "columns": 9, "mines": 1}
        }
        size = input("select level (b for beginnger, i for intermediate, a for advanced): ")
        while size[0].lower() not in "bia":
            size = input("couldn't read input.  Enter b for beginnger, i for intermediate, a for advanced: ")
        rows, cols = dimensions[size[0].lower()]["rows"], dimensions[size[0].lower()]["columns"]
        self.game_phase = "not_started"
        self.grid_rows = rows
        self.grid_columns = cols
        self.mines = dimensions[size[0].lower()]["mines"]
        self.grid = [[Cell() for i in range(cols)] for j in range(rows)]
        self.mines_marked = 0
        self.cells_found = 0

    def print_grid(self):
        header = "\n      "
        for i in range(self.grid_columns):
            header += "  {0}".format(i)
            if i < 10:
                header += " "
        print(header)
        divider = "      " + "-" * (self.grid_columns * 4 + 1)
        for i in range(self.grid_rows):
            print(divider)
            row = "    " + ascii_lowercase[i] + " "
            for j in range(self.grid_columns):
                row += "| {0} ".format(self.grid[i][j].get_value())
            row += "|"
            print(row)
        print(divider, "\n")

    def do_turn(self, move):
        row, col, action = ascii_lowercase.index(move.strip()[0].lower()), int(move.strip()[1:-1]), move.strip()[-1].lower()
        if self.game_phase == "not_started":
            self.initialize_board(row, col)
            self.game_phase = "in_process"
            return
        self.click_cell(row, col, action)

    def initialize_board(self, start_row, start_col):
        self.generate_mines(start_row, start_col)
        self.generate_numbers()
        self.click_cell(start_row, start_col, "r")

    def generate_mines(self, start_row, start_col):
        mines_hash = dict()
        for i in range(self.mines):
            r_idx = random.randint(0, self.grid_rows - 1)
            c_idx = random.randint(0, self.grid_columns - 1)
            id = ascii_lowercase[r_idx] + str(c_idx)
            while (r_idx == start_row and c_idx == start_col) or id in mines_hash:
                r_idx = random.randint(0, self.grid_rows - 1)
                c_idx = random.randint(0, self.grid_columns - 1)
                id = ascii_lowercase[r_idx] + str(c_idx)
            mines_hash[id] = True
            self.grid[r_idx][c_idx].set_value("X")

    def generate_numbers(self):
        for i in range(self.grid_rows):
            for j in range(self.grid_columns):
                if self.grid[i][j].value != "X":
                    adjacent = 0
                    for a in range(i - 1, i + 2):
                        for b in range(j - 1, j + 2):
                            adjacent += self.is_mine(a, b)
                    self.grid[i][j].set_value(adjacent)

    def click_cell(self, row, col, act):
        if act == "f":
            inc = self.grid[row][col].flag()
            self.mines_marked += inc
            self.cells_found += inc

        else:
            self.reveal(row, col)
        if self.game_phase == "lost":
            self.game_over()
        if self.cells_found == self.grid_rows * self.grid_columns:
            self.eval_game()

    def reveal(self, row, col):
        if self.grid[row][col].value == "X":
            self.game_phase = "lost"
        elif not self.grid[row][col].found:
            self.cells_found += 1
            self.grid[row][col].found = True
            if self.grid[row][col].value == 0:
                for i in range(row - 1, row + 2):
                    for j in range(col - 1, col + 2):
                        if i >= 0 and i < self.grid_rows and j >= 0 and j < self.grid_columns:
                            self.reveal(i, j)

    def game_over(self):
        for i in range(self.grid_rows):
            for j in range(self.grid_columns):
                if self.grid[i][j].value == "X":
                    self.grid[i][j].found = True
                    self.grid[i][j].flagged = False

        self.print_grid()
        print("      GAME OVER!\n")

    def win_game(self):
        for i in range(self.grid_rows):
            for j in range(self.grid_columns):
                self.grid[i][j].set_value("!")
        self.print_grid()
        print("      CONGRADULATIONS: YOU'VE WON!!\n")

    def eval_game(self):
        if self.mines_marked != self.mines:
            self.game_phase = "lost"
            self.game_over()
        else:
            self.game_phase = "won"
            self.win_game()

    def is_mine(self, row, col):
        if row >= 0 and row < self.grid_rows and col >= 0 and col < self.grid_columns:
            return 1 if self.grid[row][col].value == "X" else 0
        return 0


class Menu:
    def __init__(self):
        self.game = Game()

    def run(self):
        while self.game.game_phase != "lost" and self.game.game_phase != "won":
            self.manage_turn()
        choice = input("Play again? (y/n) ").lower()[0]
        while choice not in "yn":
            choice = input("Play again? (y/n) ").lower()[0]
        if choice == "y":
            self.game = Game()
            self.run()

    def manage_turn(self):
        self.game.print_grid()
        message = """enter row letter, column number and either 'f' for 'flag' or 'r' for 'reveal'
(no spaces, e.g. 'b5f' or 'c3r' and first turn must use 'r'): """
        move = input(message)
        while not self.is_valid(move):
            print("invalid entry")
            move = input(message)
        self.game.do_turn(move)

    def is_valid(self, move):
        if len(move.strip()) < 3:
            return False
        r, c, a = move.strip()[0], move.strip()[1:-1], move.strip()[-1]
        if r.lower() not in ascii_lowercase[:self.game.grid_rows]:
            return False
        if int(c) not in range(self.game.grid_columns):
            return False
        if a.lower() != "f" and a.lower() != "r":
            return False
        if a.lower() == "f" and self.game.game_phase == "not_started":
            return False
        return True

def main():
    m = Menu()
    m.run()


if __name__ == '__main__':
    main()
