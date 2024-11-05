from game_master import game


def stop(o: game.Game):
    o.set_running_state(False)


if __name__ == "__main__":
    g = game.Game()
    g.run()
    