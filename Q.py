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
            self.path = path
            # print(f'path: {path}')
            with open(path, "rb") as f:
                self.q_table = pickle.load(f)
                # f.close()
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

    def get_reward(self, content: None, lose: None) -> int:
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
        
        positive = ["*", "<"]
        negative = [">", "="]	

        if content in positive:
            return 30
        elif content in negative:
            return -10
        else:
            return -1

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
        # print(f'state: {state} | action: {action} | reward: {reward}')
        current_q = self.q_table.get((state, action), 0)
        self.q_table[(state, action)] = current_q + alpha * (reward - current_q)

    def get_possible_actions(self) -> list[tuple[int, int]]:
        """
        Get the list of possible actions the entity can take.

        Returns:
            list[tuple[int, int]]: List of possible actions as (dx, dy) tuples.

            [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
            (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
            ( 0, -2), ( 0, -1), ( 0, 0), ( 0, 1), ( 0, 2),
            ( 1, -2), ( 1, -1), ( 1, 0), ( 1, 1), ( 1, 2),
            ( 2, -2), ( 2, -1), ( 2, 0), ( 2, 1), ( 2, 2)]
        """
        return [(dx, dy) for dx in range(-2, 2) for dy in range(-2, 2)]

    def choose_action(self, state, epsilon=0.1) -> tuple[int, int]:
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
        if random.uniform(0, 1) < epsilon:
            return random.choice(possible_actions)
        else:
            q_values = []
            for action in possible_actions:
                q_values.append(self.q_table.get((state, action), 0))
            print(f'q_values: {q_values}')
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
