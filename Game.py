import random
import math
import pickle
from time import sleep as time
from Board import Board
from Entity import Entities, Entity, Position
from Q import Q


class Game:
    """
    Game class that handles the game loop and game settings.
    
    Attributes:
        board_size (int): The size of the board.
        initial_energy (int): The initial energy of the entities.
        num_food (int): The number of food on the board.
        entities_number (int): The number of entities on the board.
        entities (Entities): The entities on the board (player and beasts).
        board (Board): The game board.
        state (str): The game state (gamemode or editor).
        q_for_player (Q): The Q-table for the player.
        q_for_beast (Q): The Q-table for the beast.
        save_mode (bool): Whether or not the game is in save mode.
        auto_settings (bool): Whether or not the game is in auto-settings mode.
        auto_play (bool): Whether or not the game is in auto-play mode.
        play (bool): Whether or not the game is in play mode.
        path_for_player (str): Path to the file where the player Q-table is stored.
        path_for_beast (str): Path to the file where the beast Q-table is stored."""
    def __init__(
        self,
        save_mode: bool = False,
        auto_settings: tuple = True,
        auto_play: bool = False,
        play: bool = False,
        path_for_player: str = "main.pkl",
        path_for_beast: str = "main.pkl",
    ) -> None:
        self.board_size = None
        self.initial_energy = None
        self.num_food = None
        self.entities_number = None
        self.entities = None
        self.board = None
        self.state = None
        self.q_for_player = None
        self.q_for_beast = None

        self.save_mode = save_mode
        self.auto_settings = auto_settings
        self.play = play
        self.auto_play = auto_play
        self.path_for_player = path_for_player
        self.path_for_beast = path_for_beast

    def _get_valid_input(self, prompt: str, valid_inputs: list) -> str:
        """
        Get valid input from user.

        Args:
            prompt (str): Prompt for the user.
            valid_inputs (list): List of valid inputs.
        """
        user_input = input(prompt)
        if user_input in valid_inputs:
            return user_input
        else:
            print("Invalid input. Please try again.")
            return self._get_valid_input(prompt, valid_inputs)

    def _get_numeric_input(self, prompt: str) -> int:
        """
        Get numeric input from user.

        Args:
            prompt (str): Prompt for the user.
        """
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self._get_numeric_input(prompt)

    def _pick_settings(self) -> None:
        """Pick the game settings (default or custom)."""

        settings = self._get_valid_input(
            "Choose settings: 1: default, 2: custom: ", ["1", "2"]
        )

        if settings == "1":
            (
                self.board_size,
                self.initial_energy,
                self.num_food,
                self.entities_number,
                self.state,
            ) = (10, 10, 20, 5, "gamemode")
        elif settings == "2":
            self._custom_settings()
            self._pick_mode()

    def _custom_settings(self) -> None:
        """Get custom settings from user input."""

        self.board_size = self._get_numeric_input("Enter board size: ")
        self.initial_energy = self._get_numeric_input("Enter initial energy: ")
        self.num_food = self._get_numeric_input("Enter number of food: ")
        self.entities_number = self._get_numeric_input("Enter number of beasts: ")

    def _pick_mode(self) -> None:
        """Pick the game mode (gamemode-"5x5" or editor-"full size")."""

        mode = self._get_valid_input(
            "Enter mode: 1: gamemode (map 5x5), 2: editor (map full size): ", ["1", "2"]
        )
        self.state = "gamemode" if mode == "1" else "editor"

    def _initialize_game(self, path_for_player: str, path_for_beast: str) -> None:
        """
        Initialize the game (board, entities, Q-tables).

        Args:
            path_for_player (str): Path to the file where the player Q-table is stored.
            path_for_beast (str): Path to the file where the beast Q-table is stored.
        """

        if self.auto_settings == False:
            self._pick_settings()
        else:
            (
                self.board_size,
                self.initial_energy,
                self.num_food,
                self.entities_number,
                self.state,
            ) = (15, 20, 30, 10, "gamemode")

        self.entities = Entities()
        self.entities.add_players(
            self.board_size, self.initial_energy, self.entities_number
        )

        self.board = Board(self.board_size, self.entities)
        self.board.set_content(self.num_food)

        self.q_for_player = Q(path_for_player)
        self.q_for_beast = Q(path_for_beast)

    def _save_q_tables(self, path) -> None:
        """
        Save the Q-table to a file.

        Args:
            path (str): Path to the file where the Q-table will be saved.
        """

        with open(path, "wb") as f:
            pickle.dump(self.q_for_player.q_table, f)

    def _update_energy(self, dx, dy, entity: Entity) -> None:
        """
        Update the energy of the entity based on the content of the cell it moved to.

        Args:
            dx (int): The change in x (column) position.
            dy (int): The change in y (row) position.
            entity (Entity): The entity whose energy is being updated.
        """
        target_position = Position(
            (entity.position.row_index - dy) % self.board_size,
            (entity.position.column_index + dx) % self.board_size,
        )

        # If the entity doesn't have enough energy to move to the target cell it dies
        if entity.energy < math.sqrt(dx**2 + dy**2):
            entity.energy = 0
            return

        content = self.board[target_position].content
        target_entity = self.entities.get_entity_at_position(target_position)

        FOOD = "*"
        EQUALS = "="
        BEAST_LESS = "<"
        BEAST_GREATER = ">"

        if content == FOOD:
            entity.energy += 10
        elif content == EQUALS:
            entity.energy = 0
        elif content == BEAST_LESS:
            entity.energy += target_entity.energy
            self.entities.remove(target_entity)
        elif content == BEAST_GREATER:
            target_entity.energy += entity.energy
            self.entities.remove(entity)

        # Update energy based on distance moved
        entity.energy -= math.sqrt(dx**2 + dy**2)

    def _game_turn(
        self, all_entities: Entities, main: Entity
    ) -> tuple[int, int, str, str]:
        """
        Run a game turn (move entities, update energy, etc.).

        Args:
            all_entities (Entities): All entities (player and beasts).
            main (Entity): The main entity (player).

        Returns:
            tuple[int, int, str, str]: dx, dy, state, content

            (1, 0, "...*..<.....P*...........", '*')
        """
        dx_player, dy_player = None, None
        state_return = None
        content = None

        for entity in all_entities:
            if entity.energy < 1:
                self.entities.remove(entity)
                self.board.clear_entity_at(entity.position)
                continue

            self.board.update_content(self.entities)

            if main == entity:
                # Print board and entity information for play mode
                if self.play:
                    self.board.print_board(entity, state=self.state)
                    print(entity)
                    dx, dy = self._get_player_move()
                # Print board and entity information for save mode
                else:
                    state = self.q_for_player.get_current_state(entity, self.board)
                    dx, dy = self.q_for_player.choose_action(state)
                    state_return = state
                    dx_player, dy_player = dx, dy

                # Get target position and content of the cell the entity moved to
                target_position = Position(
                    (entity.position.row_index - dy) % self.board_size,
                    (entity.position.column_index + dx) % self.board_size,
                )
                content = self.board[target_position].content

                # Print board and entity information for auto-play mode
                if self.auto_play:
                    self.board.print_board(entity, state=self.state)
                    print(entity)
                    print(
                        f"new position: {target_position.row_index} {target_position.column_index}"
                    )
                    print(f"target: {content}")
                    time(1.5)
            else:
                state = self.q_for_beast.get_current_state(entity, self.board)
                dx, dy = self.q_for_beast.choose_action(state)

            self._update_energy(dx, dy, entity)

            self.board.clear_entity_at(entity.position)

            entity.move(dx, dy, self.board_size)

        return (dx_player, dy_player, state_return, content)

    def _get_player_move(self) -> tuple[int, int]:
        """
        Get player move from user input in interval x: [-2 2], y: [-2 2].

        Returns:
            tuple[int, int]: dx, dy

            (-1, 1) or (0, 1)
        """
        try:
            dx, dy = map(int, input("Enter x y: ").split())
            if -2 <= dx <= 2 and -2 <= dy <= 2:
                return dx, dy
            else:
                print("Invalid input. Coordinates must be between -2 and 2.")
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a space.")
        return self._get_player_move()

    def start(self) -> None:
        """
        Main game loop.

        Returns:
            bool: True if player won, False if player lost.
        """

        # Initialize game parameters (board, entities, Q-tables)
        self._initialize_game(self.path_for_player, self.path_for_beast)

        main_player = self.entities.get_player()

        game_won = False

        while main_player.energy >= 1:
            # Get all entities (player and beasts)
            all_entities = self.entities.get_entities()

            # Check winning condition (only player left)
            if len(all_entities) == 1:
                game_won = True
                break

            # Shuffle the entities to randomize turn order each round
            random.shuffle(all_entities)

            # Run a game turn (move entities, update energy, etc.)
            dx, dy, state, content = self._game_turn(all_entities, main_player)

            # Update Q-tables if in save mode
            if self.save_mode and main_player.energy != 0:
                reward = self.q_for_player.get_reward(content, None)
                self.q_for_player.update_q_value(state, (dx, dy), reward)

        # Update Q-tables if in save mode and player lost
        if game_won == False:
            if self.save_mode and main_player.energy != 0:
                reward = self.q_for_player.get_reward(None, lose=True)
                self.q_for_player.update_q_value(state, (dx, dy), reward)

        if self.save_mode:
            self._save_q_tables(self.path_for_player)
        else:
            if game_won == False:
                print("You lost!")
            else:
                print("You won!")

        return game_won
