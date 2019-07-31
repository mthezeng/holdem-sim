import game

def main():
    print("Texas hold'em simulator")
    print("Originally developed by Michael Zeng")
    print("-----")
    num_players = int(input("How many players?: "))
    g = game.Game(num_players)
    g.start_game()

if __name__ == '__main__':
    main()