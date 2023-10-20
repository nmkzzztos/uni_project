import random
from Entity import *
from typing import List

class Cell:
    def __init__(self, content: str = "."):
        self.content = content

class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid: List[List[Cell]] = [[Cell() for _ in range(size)] for _ in range(size)]

    def __getitem__(self, position) -> Cell:
        return self.grid[position.row_index][position.column_index]

    def set_content(self, entities: Entities, num_food: int) -> None:
        x, y = entities.player.position.row_index, entities.player.position.column_index
        self.grid[x][y].content = "P"

        for _ in range(num_food):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.grid[x][y].content = "*"

        for beast in entities.get_beasts():
            x, y = beast.position.row_index, beast.position.column_index
            self.grid[x][y].content = "="
    
    def update_content(self, entities: Entities) -> None:
        x, y = entities.player.position.row_index, entities.player.position.column_index
        self.grid[x][y].content = "P"

        for beast in entities.get_beasts():
            x, y = beast.position.row_index, beast.position.column_index
            if beast.energy < entities.player.energy:
                self.grid[x][y].content = "<"
            elif beast.energy > entities.player.energy:
                self.grid[x][y].content = ">"
            else:
                self.grid[x][y].content = "="

    def print_board(self, player: Entity=None, state: str='gamemode') -> None:
        if state == "gamemode":
            for i in range(player.position.row_index - 2, player.position.row_index + 3):
                for j in range(player.position.column_index - 2, player.position.column_index + 3):
                    x, y = i % self.size, j % self.size
                    print(self.grid[x][y].content, end=" ")
                print()
        elif state == "editor":
            for row in self.grid:
                print(" ".join(cell.content for cell in row))

    def get_board(self, player: Entity) -> List[List[str]]:
        board = []
        for i in range(player.position.row_index - 2, player.position.row_index + 3):
            row = []
            for j in range(player.position.column_index - 2, player.position.column_index + 3):
                x, y = i % self.size, j % self.size
                row.append(self.grid[x][y].content)
            board.append(row)
        return board