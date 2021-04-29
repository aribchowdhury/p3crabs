import enum


class PlayerType(enum.Enum):
    PLAYER_TYPE = "player"
    OPPONENT_TYPE = "opponent"
    SPECTATOR_TYPE = "spectator"
    NO_TYPE = "none"


class Player:
    def __init__(self, sid):
        self.sid = sid
        self.player_type = PlayerType.SPECTATOR_TYPE
        self.name = None
        self.score = 0

    def is_player(self):
        return self.player_type == PlayerType.PLAYER_TYPE

    def is_opponent(self):
        return self.player_type == PlayerType.OPPONENT_TYPE

    def is_spectator(self):
        return self.player_type == PlayerType.SPECTATOR_TYPE

    def get_type(self):
        return self.player_type

    def change_type(self, new_type: PlayerType):
        self.player_type = new_type

    def set_name(self, name):
        self.name = name

    def reset_name(self):
        self.name = None

    def get_score(self):
        return self.score

    def full_reset(self):
        self.change_type(PlayerType.SPECTATOR_TYPE)
        self.reset_name()
