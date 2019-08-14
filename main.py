import random
import os
import time
import sys

from dice import dice_frames, pig_art


TURNS = 1
TURN_SCORE = 0
TOTAL_SCORE = 0


def roll_dice():
    return random.randint(1, 6)


def print_dice_roll_animation(n):
    start_time = time.time()

    while True:
        sys.stdout.write("\033[32m" + dice_frames[random.randint(0, 5)] + "\033[0m")
        sys.stdout.flush()

        # Adjust the delay as needed for each dice face frame
        time.sleep(0.1)

        # Move the cursor up 6 line (6 is the line the dice takes to print)
        sys.stdout.write("\033[{}A".format(6))

        # Run the animation till 1.5s
        if time.time() - start_time > 1.5:
            break

    print_dice(n)


def reset_score():
    global TOTAL_SCORE
    global TURN_SCORE
    global TURNS

    TOTAL_SCORE = 0
    TURN_SCORE = 0
    TURNS = 1


def print_dice(n):
    dice_art = dice_frames[n]
    rolled_message = f"You rolled {n + 1}\n"
    print(f"\033[32m{dice_art.rstrip()}  \033[3m{rolled_message}\033[0m")


def print_banner():
    print("=*" * 30)
    print(pig_art)
    print(
        """
        \033[1m\t\033[4mWelcome to the game of Pig!\033[0m\n
        \033[1mTo restart the game, put 's' and press enter
        To quit the game put 'q' and press enter\033[0m
        """
    )
    print("=*" * 30)
    print()


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def show_score_and_turn():
    global TOTAL_SCORE
    global TURN_SCORE
    global TURNS

    print("┌" + "─" * 9 + "┐")
    print(f"| \033[1mTURN: {TURNS}\033[0m |")
    print("└" + "─" * 9 + "┘")
    # print("┌" + "─" * 58 + "┐")
    print(
        f"\nYour turn score is \033[36m\033[4m{TURN_SCORE}\033[0m and your total score is \033[36m{TOTAL_SCORE}\033[0m"
    )
    print(f"If you hold, you will have {TURN_SCORE + TOTAL_SCORE}")
    # print("└" + "─" * 58 + "┘")


def game():
    global TOTAL_SCORE
    global TURN_SCORE
    global TURNS

    print("\n\033[1mPress enter to roll or enter 'h' to hold.\033[0m\n")
    choice = input("▶ ").lower()

    if choice == "":
        rolled = roll_dice()
        print_dice_roll_animation(rolled - 1)

        if rolled == 1:
            print(
                f"Turn over. No score from this turn.\nYour total score is {TOTAL_SCORE}"
            )
            TURN_SCORE = 0
            TURNS += 1
            input("\nPress enter to start the new turn")
            clear()
            return "s"

        TURN_SCORE += rolled

        if (TOTAL_SCORE + TURN_SCORE) >= 20:
            print(
                f"Your turn score was {TURN_SCORE} and added to your total score is {TOTAL_SCORE + TURN_SCORE}\n"
            )
            print(
                f"\033[31m~~ 🏆 ৻(  •̀ ᗜ •́  ৻) You won! You finished the game in {TURNS} turns. ~~\033[0m"
            )
            print("\n1. Press 'q' to quit game.\n2. Press 's' to start new game.\n")
            reset_score()
            return input("▶ ")

    elif choice == "h":
        if TURN_SCORE == 0:
            print("\nNothing to hold. Roll and then try to hold")
            time.sleep(2)
            return "s"

        TOTAL_SCORE += TURN_SCORE
        TURN_SCORE = 0
        TURNS += 1

        print(
            f"\nYour turn score is now added to total score. TOTAL SCORE: {TOTAL_SCORE}"
        )
        input("\nPress enter to start the new turn")
        clear()

        return "s"

    elif choice in ["s", "q"]:
        action = "quit" if choice == "q" else "restart"
        confirm = input(
            "Do you really want to " + action + "?\n'Y' or 'N'?\n▶ "
        ).lower()
        if confirm == "y":
            # Reset the scoring vars
            reset_score()
            return choice
        elif confirm == "n":
            print("Action cancelled. Continuing game.")
            time.sleep(1)
            return "s"
        else:
            print("\nInvalid input. Continuing game...")
            time.sleep(1)
            return "s"
    else:
        print("\nInvalid choice.")
        print("\nhint: Press 's' to restart or 'q' to quit the game\n")

    time.sleep(1)
    return "s"


def main():
    global TURNS

    after = "s"

    while True:
        # Start or quit input
        if after == "":
            print("Invalid input.")
            after = input("Press 's' to start the game or 'q' to quit\n▶ ").lower()
            continue

        # Start or restart logic for game
        elif after == "s":
            clear()
            print_banner()
            show_score_and_turn()

        # Quitting logic for game
        elif after == "q":
            clear()
            print(pig_art)
            print("""
            \033[34m~~ Thanks for playing ٩(｡•́‿•̀｡)۶ ~~\033[0m
            """)
            print()
            time.sleep(3)
            break

        after = game()


if __name__ == "__main__":
    main()
