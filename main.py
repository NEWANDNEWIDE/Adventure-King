from game_master.game import Game


def stop(o: Game):
    o.running = False


if __name__ == "__main__":
    g = Game()
    g.run()
    