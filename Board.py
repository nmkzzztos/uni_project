import random
from Entity import *
from typing import List

class Cell:
    def __init__(self, content: str = "."):
        self.content = content

class Board:
    def __init__(self, size: int, entities: Entities):
        self.size = size
        self.grid: List[List[Cell]] = [[Cell() for _ in range(size)] for _ in range(size)]
        self.entities = entities

    def __getitem__(self, position) -> Cell:
        return self.grid[position.row_index][position.column_index]
    
    def _get_grid_with_enemies(self, player: Entity) -> List[List[Cell]]:
        grid = self.grid.copy()
        for entity in self.entities.get_entities():
            if entity == player:
                continue
            else:
                x, y = entity.position.row_index, entity.position.column_index
                if player.energy < entity.energy:
                    grid[x][y].content = ">"
                elif player.energy > entity.energy:
                    grid[x][y].content = "<"
                elif player.energy == entity.energy:
                    grid[x][y].content = "="
        return grid

    def set_content(self, num_food: int) -> None:
        for _ in range(num_food):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.grid[x][y].content = "*"

        for entity in self.entities.get_entities():
            x, y = entity.position.row_index, entity.position.column_index
            self.grid[x][y].content = "P"
    
    def update_content(self, entities: Entities) -> None:
        for entity in entities.get_entities():
            x, y = entity.position.row_index, entity.position.column_index
            self.grid[x][y].content = "P"

    def print_board(self, player: Entity=None, state: str='gamemode') -> None:
        if state == "gamemode":
            grid = self._get_grid_with_enemies(player)
            for i in range(player.position.row_index - 2, player.position.row_index + 3):
                for j in range(player.position.column_index - 2, player.position.column_index + 3):
                    x, y = i % self.size, j % self.size
                    print(grid[x][y].content, end=" ")
                print()
        elif state == "editor":
            grid = self._get_grid_with_enemies(player)
            for row in grid:
                print(" ".join(cell.content for cell in row))

    def get_board(self, player: Entity) -> List[List[str]]:
        board = []
        grid = self._get_grid_with_enemies(player)
        for i in range(player.position.row_index - 2, player.position.row_index + 3):
            row = []
            for j in range(player.position.column_index - 2, player.position.column_index + 3):
                x, y = i % self.size, j % self.size
                row.append(grid[x][y].content)
            board.append(row)
        return board
    
    def clear_entity_at(self, position: Position) -> None:
        self[position].content = "."