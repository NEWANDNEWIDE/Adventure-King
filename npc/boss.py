import game_master


class Boss(game_master.gameObject.GameNpc):
    def __init__(self, pos, group, name="Boss"):
        super().__init__(pos, group, name)
