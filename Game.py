import random
import math
from Board import Board
from Entity import Entities, Entity, Player, Beast, Position


class Game:
    def __init__(self):
        self.board_size = None
        self.initial_energy = None
        self.num_food = None
        self.entities_number = None
        self.entities = None
        self.board = None
        self.state = None

    def get_valid_input(self, prompt: str, valid_inputs: list) -> str:
        user_input = input(prompt)
        if user_input in valid_inputs:
            return user_input
        else:
            print("Invalid input. Please try again.")
            return self.get_valid_input(prompt, valid_inputs)

    def get_numeric_input(self, prompt: str) -> int:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self.get_numeric_input(prompt)

    def pick_settings(self) -> None:
        settings = self.get_valid_input(
            "Choose settings: 1: default, 2: custom: ", ["1", "2"]
        )

        if settings == "1":
            (
                self.board_size,
                self.initial_energy,
                self.num_food,
                self.entities_number,
            ) = (20, 10, 20, 3)
        elif settings == "2":
            self.custom_settings()

    def custom_settings(self) -> None:
        self.board_size = self.get_numeric_input("Enter board size: ")
        self.initial_energy = self.get_numeric_input("Enter initial energy: ")
        self.num_food = self.get_numeric_input("Enter number of food: ")
        self.entities_number = self.get_numeric_input("Enter number of beasts: ")

    def pick_mode(self) -> None:
        mode = self.get_valid_input(
            "Enter mode: 1: gamemode (map 5x5), 2: editor (map full size): ", ["1", "2"]
        )
        self.state = "gamemode" if mode == "1" else "editor"

    def get_entity(self, position: Position) -> Entity:
        for beast in self.entities.get_beasts():
            if (
                beast.position.row_index == position.row_index
                and beast.position.column_index == position.column_index
            ):
                return beast
        return None

    def update_energy(self, dx, dy, entity: Entity) -> None:
        target_position = Position(
            (entity.position.row_index - dy) % self.board_size,
            (entity.position.column_index + dx) % self.board_size,
        )

        content = self.board[target_position].content
        target_entity = self.get_entity(target_position)

        FOOD = "*"
        EQUALS = "="
        LESS = "<"
        GREATER = ">"

        if content == FOOD:
            entity.energy += 10
        elif content == EQUALS:
            entity.energy = 0
        elif content == LESS:
            entity.energy += target_entity.energy
            self.entities.remove_beast(target_entity)
        elif content == GREATER:
            target_entity.energy += entity.energy
            self.entities.remove_beast(entity)

        entity.energy -= math.sqrt(dx**2 + dy**2)

    def move_entity(self, entity: Entity) -> None:
        dx, dy = self.get_entity_move(entity)
        self.update_energy(dx, dy, entity)
        self.board[entity.position].content = "."
        entity.move(dx, dy, self.board_size)

    def get_entity_move(self, entity: Entity) -> tuple[int, int]:
        if isinstance(entity, Player):
            return self.get_player_move()
        elif isinstance(entity, Beast):
            return random.randint(-2, 2), random.randint(-2, 2)

    def get_player_move(self) -> tuple[int, int]:
        try:
            dx, dy = map(int, input("Enter x y: ").split())
            if -2 <= dx <= 2 and -2 <= dy <= 2:
                return dx, dy
            else:
                print("Invalid input. Coordinates must be between -2 and 2.")
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a space.")
        return self.get_player_move()

    def start(self) -> None:
        # Choose settings
        self.pick_settings()

        # Create entities
        self.entities = Entities()
        self.entities.add_player(self.board_size, self.initial_energy)
        self.entities.add_beast(self.board_size, 7, self.initial_energy)

        # Create board
        self.board = Board(self.board_size)
        self.board.set_content(self.entities, self.num_food)

        self.pick_mode()

        while self.entities.player.energy > 0:
            all_entities = self.entities.get_beasts() + [self.entities.player]

            random.shuffle(all_entities)

            for entity in all_entities:
                if entity.energy <= 1:
                    print(f"Unable to move {entity}")
                    continue
                if type(entity) == Player:
                    self.board.update_content(self.entities)
                    self.board.print_board(self.entities.player, self.state)
                    print(f"Player: {entity}")
                elif type(entity) == Beast:
                    print(f"Beast: {entity}")
                self.move_entity(entity)
