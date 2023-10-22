import random
from typing import List, Optional


class Position:
    def __init__(self, row_index: int, column_index: int):
        self.row_index = row_index
        self.column_index = column_index

    def __str__(self) -> str:
        return f"({self.row_index}, {self.column_index})"


class Entity:
    def __init__(self, position: Position):
        self.position = position

    def get_position(self) -> Position:
        return self.position

    def set_position(self, position: Position) -> None:
        self.position = position


class MoveableEntity(Entity):
    def __init__(self, position: Position, energy: int):
        super().__init__(position)
        self.energy = energy
        self.id_counter = 0
        self.id = self.get_next_id()

    def __str__(self) -> str:
        return f"Position: {self.position}, Energy: {self.energy}, ID: {self.id}"
    
    def get_next_id(self):
        self.id_counter += 1
        return self.id_counter

    def get_energy(self) -> int:
        return self.energy

    def set_energy(self, energy: int) -> None:
        self.energy = energy

    def move(self, dx: int, dy: int, board_size: int) -> None:
        new_position = self.get_new_position(dx, dy, board_size)
        if new_position:
            self.set_position(new_position)

    def get_new_position(self, dx: int, dy: int, board_size: int) -> Optional[Position]:
        new_row_index = (self.position.row_index - dy) % board_size
        new_column_index = (self.position.column_index + dx) % board_size

        if 0 <= new_row_index < board_size and 0 <= new_column_index < board_size:
            return Position(new_row_index, new_column_index)

        return None

class Food(Entity):
    def __init__(self, position: Position):
        super().__init__(position)

class Player(MoveableEntity):
    def __init__(self, position: Position, energy: int):
        super().__init__(position, energy)

class Entities:
    def __init__(self):
        self.players: List[Player] = []

    def __str__(self) -> str:
        return f"Player: {self.player}, Beasts: {self.beasts}"

    def add_players(self, board_size: int, initial_energy: int = 10, num_players: int = 1) -> None:
        for _ in range(num_players):
            position = Position(
                random.randint(0, board_size - 1), random.randint(0, board_size - 1)
            )
            self.players.append(Player(position, initial_energy))

    def remove_player(self, player: Player) -> None:
        self.players.remove(player)

    def get_entities(self) -> List[Player]:
        return self.players

    def get_player(self) -> Player:
        for player in self.players:
            # print(player)
            if player.id == 1:
                return player
    
    def get_entity_at_position(self, position: Position) -> Optional[Entity]:
        for entity in self.players:
            if entity.position.row_index == position.row_index and entity.position.column_index == position.column_index:
                return entity
        return None