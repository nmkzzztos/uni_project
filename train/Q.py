from Board import Board
from Entity import Entity
import random
import pickle


class Q:
    """
    Q-Learning class that handles Q-table, action selection, and Q-value updates.
    """

    def __init__(self, path) -> None:
        """
        Initialize the Q-table.
        
        Parameters:
            path (str): Path to the file where the Q-table is stored.
        """
        try:
            with open(path, "rb") as f:
                self.q_table = pickle.load(f)
                f.close()
        except:
            self.q_table = {}  # Initialize an empty Q-table if the file doesn't exist

    def get_current_state(self, entity: Entity, board: Board) -> str:
        """
        Get the current state of the game by observing the 5x5 grid around the entity.

        Parameters:
            entity (Entity): The entity whose state we are observing.
            board (Board): The game board.

        Returns:
            str: A string representation of the current state 5x5 grid.
            
            ["...*..<.....P*..........."]
        """
        grid_5x5 = board.get_board(entity)
        current_state = "".join([cell for row in grid_5x5 for cell in row])
        return current_state

    def get_reward(self, content: str, lose: bool, energy: int) -> int:
        """
        Calculate the reward based on the current action outcome.

        Parameters:
            content (None): Content of the cell that was moved to.
            lose (None): Whether or not the game was lost.

        Returns:
            int: Reward for the current state.
        """
        if lose:
            return -10
        
        rewards = {
            "*": 5,
            "<": 30,
            "=": -20,
            ">": -20,
            '.': -1,
            "P": -2,
        }

        return rewards[content] + energy

    def update_q_value(
        self, state: str, action: tuple[int, int], reward: int, alpha: float = 0.1
    ) -> None:
        """
        Update the Q-value for a given state-action pair.

        Parameters:
            state (str): The current state.
            action (tuple[int, int]): The action taken.
            reward (int): The reward received.
            alpha (float, optional): The learning rate. Default is 0.1.
        """
        current_q = self.q_table.get((state, action), 0)
        self.q_table[(state, action)] = current_q + alpha * (reward - current_q)

    def get_possible_actions(self) -> list[tuple[int, int]]:
        """
        Get the list of possible actions the entity can take.

        Returns:
            list[tuple[int, int]]: List of possible actions as (dx, dy) tuples.
            
            [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (0, -2), (0, -1), (0, 0), (0, 1), (1, -2), (1, -1), (1, 0), (1, 1)]
        """
        return [(dx, dy) for dx in range(-2, 2) for dy in range(-2, 2)]
    
    def get_food_actions(self, state: str) -> list[tuple[int, int]]:
        """
        Get the list of actions that will lead to food.

        Parameters:
            state: The current state.

        Returns:
            list[tuple[int, int]]: List of actions that will lead to food as (dx, dy) tuples.

            [(0, 0), (0, 1), (1, -2), (1, -1), (1, 0), (1, 1)]
        """
        grid = [state[i:i+5] for i in range(0, len(state), 5)]
        food_positions = []
        low_enemies = []
        for i in range(5):
            for j in range(5):
                if grid[i][j] == "<":
                    low_enemies.append((j-2, -i+2))
                if grid[i][j] == "*":
                    food_positions.append((j-2, -i+2))
        if len(low_enemies) > 0:
            return low_enemies
        return food_positions
    
    def get_enemies(self, state: str) -> list[tuple[int, int]]:
        """
        Get the list of actions that will lead to enemies.

        Parameters:
            state: The current state.

        Returns:
            list[tuple[int, int]]: List of actions that will lead to enemies as (dx, dy) tuples.

            [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-1, -2), (-1, -1), (-1, 0), (-1, 1)]
        """
        grid = [state[i:i+5] for i in range(0, len(state), 5)]
        enemy_actions = []
        for i in range(5):
            for j in range(5):
                if grid[i][j] == ">":
                    enemy_actions.append((j-2, -i+2))
        return enemy_actions


    def choose_action(self, state, epsilon=0.01) -> tuple[int, int]:
        """
        Choose an action based on the current state and epsilon-greedy strategy.
        
        Parameters:
            state: The current state.
            epsilon (float, optional): The exploration factor. Default is 0.1.
        
        Returns:
            tuple[int, int]: The chosen action as a (dx, dy) tuple.

            (1, -2)
        """
        possible_actions = self.get_possible_actions()
        food_actions = self.get_food_actions(state)
        enemies = self.get_enemies(state)
        if random.uniform(0, 1) < epsilon:
            return random.choice(possible_actions)
        elif len(food_actions) > 0 and len(enemies) < 1:
            q_values = [
                self.q_table.get((state, action), 0) for action in food_actions
            ]
            max_q_value = max(q_values)
            if q_values.count(max_q_value) > 1:
                best_actions = [
                    i
                    for i in range(len(food_actions))
                    if q_values[i] == max_q_value
                ]
                i = random.choice(best_actions)
            else:
                i = q_values.index(max_q_value)
            return food_actions[i]
        else:
            q_values = [
                self.q_table.get((state, action), 0) for action in possible_actions
            ]
            max_q_value = max(q_values)
            if q_values.count(max_q_value) > 1:
                best_actions = [
                    i
                    for i in range(len(possible_actions))
                    if q_values[i] == max_q_value
                ]
                i = random.choice(best_actions)
            else:
                i = q_values.index(max_q_value)
            return possible_actions[i]