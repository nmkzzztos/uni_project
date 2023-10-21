import random
import numpy as np
import pickle
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
    _id_counter = 0

    def __init__(self, position: Position, energy: int):
        super().__init__(position)
        self.energy = energy
        self.entity_id = self._get_next_id_()
    
    @classmethod
    def _get_next_id_(cls):
        cls._id_counter = cls._id_counter + 1
        return cls._id_counter

    def __str__(self) -> str:
        return f"Position: {self.position}, Energy: {self.energy}, ID: {self.entity_id}"

    def get_energy(self) -> int:
        return self.energy

    def set_energy(self, energy: int) -> None:
        self.energy = energy

    def move(self, dx: int, dy: int, board_size: int) -> None:
        new_position = self.get_new_position(dx, dy, board_size)
        # print(f'position {self.position.row_index} {self.position.column_index}, new position {new_position.row_index} {new_position.column_index}')
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
        try:
            with open("q_table.pkl", "rb") as f:
                self.q_table = pickle.load(f)
        except:
            self.q_table = {}  # Initialize an empty Q-table if the file doesn't exist

    def update_q_value(self, state, action, reward, alpha=0.1):
        current_q = self.q_table.get((state, action), 0)
        self.q_table[(state, action)] = current_q + alpha * (reward - current_q)

    def get_possible_actions(self):
        return [(dx, dy) for dx in range(-2, 2) for dy in range(-2, 2)]

    def choose_action(self, state, epsilon=0.1):
        possible_actions = self.get_possible_actions()
        if np.random.random() < epsilon:
            return random.choice(possible_actions)
        else:
            q_values = [self.q_table.get((state, action), 0) for action in possible_actions]
            print(f'q_values: {q_values}')
            return possible_actions[np.argmax(q_values)]

class Beast(MoveableEntity):
    def __init__(self, position: Position, energy: int):
        super().__init__(position, energy)
        try:
            with open("q_table.pkl", "rb") as f:
                self.q_table = pickle.load(f)
        except:
            self.q_table = {}  # Initialize an empty Q-table if the file doesn't exist

    def get_possible_actions(self):
        return [(dx, dy) for dx in range(-2, 2) for dy in range(-2, 2)]

    def choose_action(self, state, epsilon=0.1):
        possible_actions = self.get_possible_actions()
        if np.random.random() < epsilon:
            return random.choice(possible_actions)
        else:
            q_values = [self.q_table.get((state, action), 0) for action in possible_actions]
            # print(f'q_values: {q_values}')
            return possible_actions[np.argmax(q_values)]

class Entities:
    def __init__(self):
        self.player: Player = None
        self.beasts: List[Beast] = []

    def __str__(self) -> str:
        return f"Player: {self.player}, Beasts: {self.beasts}"

    def add_player(self, board_size: int, initial_energy: int = 10) -> None:
        y, x = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
        player = Player(Position(x, y), initial_energy)
        self.player = player

    def add_beast(
        self, board_size: int, num_beasts: int = 1, initial_energy: int = 10
    ) -> None:
        for _ in range(num_beasts):
            y, x = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
            beast = Beast(Position(x, y), initial_energy)
            self.beasts.append(beast)

    def remove_beast(self, beast: Beast) -> None:
        self.beasts.remove(beast)

    def get_beasts(self) -> List[Beast]:
        return self.beasts
    
    def get_entity(self, position: Position) -> Optional[Entity]:
        if self.player.position.row_index == position.row_index and self.player.position.column_index == position.column_index:
            return self.player
        for beast in self.beasts:
            if beast.position.row_index == position.row_index and beast.position.column_index == position.column_index:
                return beast
        return None

    def get_player(self) -> Player:
        return self.player