from Board import Board
from Entity import Position, Entity
import random
import numpy as np
import pickle

class Q:
    def __init__(self, path) -> None:
        try:
            with open(path, "rb") as f:
                self.q_table = pickle.load(f)
                f.close()
        except:
            self.q_table = {}  # Initialize an empty Q-table if the file doesn't exist

    def get_current_state(self, entity: Entity, board: Board) -> str:
        grid_5x5 = board.get_board(entity)
        current_state = ''.join([cell for row in grid_5x5 for cell in row])
        return current_state
    
    def get_reward(self, dx: int, dy: int, board: Board, entity: Entity) -> int:
        target = Position(
            (entity.position.row_index - dy) % board.size,
            (entity.position.column_index + dx) % board.size,
        )

        content = board[target].content

        # print(f'content: {content}')

        negative_content = ["=", ">"]

        if content in '*':
            return 10
        elif content == '<':
            return 1000
        elif content in negative_content:
            return -10
        else:
            return -1
        
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
            # print(f'q_values: {q_values}')
            return possible_actions[np.argmax(q_values)]