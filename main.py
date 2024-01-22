from gamestate import GameState


def main():
    game = GameState(num_players=3)

    while not game.is_over():
        player = game.get_player()
        print(f"Current turn: {player.id},  chips: {player.chips}")
        print(f"Card: {game.get_card()}, chips: {game.get_chips()}")
        action = input("Select action <Take/Skip> or <Hand> to see cards.\n")
        if action.lower() == "take":
            game.take_card()
        elif action.lower() == "skip":
            if player.can_skip():
                game.skip_card()
            else:
                print("Player has no chips!")
        elif action.lower() == "hand":
            print(player.cards)
        else:
            print("Invalid option")

    print("Game over")
    for player in game.players:
        print(f"Player {player.id} has {player.score()} points")


if __name__ == "__main__":
    main()
