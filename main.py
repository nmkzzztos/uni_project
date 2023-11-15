from Game import Game
import sys
import time


def main(save_mode: bool = False, auto_settings: bool = True, play: bool = False, auto_play: bool = False) -> None:
    game = Game(
        save_mode=save_mode,
        auto_settings=auto_settings,
        play=play,
        auto_play=auto_play,
    )

    if auto_play or play:
        game.start()
        return
    else:
        total_win_count = 0
        total_lose_count = 0 
        current_win_count = 0 
        current_lose_count = 0 
        time_start = time.time()
        iterations = 15000

        for i in range(iterations):
            if i % 100 == 0:
                print(f"iteration: {i}")
                print(f"current win: {current_win_count} | current lose: {current_lose_count}")
                current_win_count = 0
                current_lose_count = 0
            win = game.start()
            if win:
                total_win_count += 1
                current_win_count += 1
            else:
                total_lose_count += 1
                current_lose_count += 1

        time_end = time.time()
        print(f"time: {time_end - time_start}")
        print(f"total win: {total_win_count} | total lose: {total_lose_count}")


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        if args[1] == "save": # save mode it will save the q_table in a file 
            main(save_mode=True)
        elif args[1] == "auto-play": # auto-play mode will play the game automatically based on the q_table
            main(save_mode=False, auto_settings=False, auto_play=True)
        elif args[1] == "play": # user can play the game
            main(save_mode=False, auto_settings=False, play=True)
