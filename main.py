from Game import Game
import time

def main() -> None:
    game = Game()
    win_count = 0
    lose_count = 0
    time_start = time.time()
    for i in range(1000):
        if i % 100 == 0:
            print(f'iteration: {i}')
        win = game.start()
        if win:
            win_count += 1
        else:
            lose_count += 1
    time_end = time.time()
    print(f'time: {time_end - time_start}')
    print(f'win: {win_count} | lose: {lose_count}')

if __name__ == "__main__":
    main()