# Team Crabs: Karl Hernandez, Arib Chowdhury, Anya Zorin, Saqif Abedin
# Softdev
# P3: ArRESTed Development, JuSt in Time
# 2021-04-23
from requests import get
from random import randint
from .marvel import *
from .player import *


class PlayerVsPlayer:
    # level corresponds to the number of questions overall
    # categories will be the categories of trivia questions
    def __init__(self, level=10):  # Start up simulation
        self.level = level
        # self.player_id = None  # session id for player
        # self.opponent_id = None  # session id for opponent
        # self.players = {}  # spectators and session ids
        self.player, self.opponent = self.generateEntities(level)
        self.trivia = self.generateTrivia(level)
        self.img = None
        self.answer = None
        self.answer_len = None
        self.player_health = "100%"
        self.opponent_health = "100%"

    # game states
    # def add_player(self, session_id):
    #     assert session_id is not None
    #     assert session_id not in self.players
    #     self.players[session_id] = Player(session_id)

    # def remove_player(self, session_id):
    #     assert session_id is not None
    #     assert session_id in self.players
    #     self.players.pop(session_id, None)

    # def count_players(self):
    #     return len(self.players)

    # def is_player(self, sid):
    #     assert sid is not None
    #     return self.player_id == sid

    # def is_opponent(self, sid):
    #     assert sid is not None
    #     return self.opponent_id == sid

    # def is_player_set(self):
    #     return self.player_id != None

    # def is_opponent_set(self):
    #     return self.opponent_id != None

    # def set_player(self, sid, name):
    #     self.player_id = sid
    #     if sid == None:
    #         return
    #     self.players[sid].change_type(PlayerType.PLAYER_TYPE)
    #     self.players[sid].set_name(name)

    # def set_opponet(self, sid, name):
    #     self.opponent_id = sid
    #     if sid == None:
    #         return
    #     self.players[sid].change_type(PlayerType.OPPONENT_TYPE)
    #     self.players[sid].set_name(name)

    # def set_spectator(self, sid):
    #     self.players[sid].change_type(PlayerType.SPECTATOR_TYPE)

    # def get_player_type(self, sid):
    #     return self.players[sid].get_type()

    # def get_opposite_player_type(self, sid):
    #     if self.is_player(sid):
    #         return PlayerType.PLAYER_TYPE
    #     elif self.is_opponent(sid):
    #         return PlayerType.OPPONENT_TYPE
    #     else:
    #         return PlayerType.NO_TYPE

    # def players_ready(self):
    #     return self.is_player_set() and self.is_opponent_set()

    # def swap_players(self):
    #     self.players[self.player_id].player_type = PlayerType.PLAYER_TYPE
    #     self.players[self.opponent_id].player_type = PlayerType.OPPONENT_TYPE
    #     temp_player_sid = self.player_id
    #     self.player_id = self.opponent_id
    #     self.opponent_id = temp_player_sid

    def generateEntities(self, hitsRequired):  # Create player and opponent objects
        player = get("https://pokeapi.co/api/v2/pokemon/" + str(randint(1, 898))).json()
        playerSprite = player["sprites"]["back_default"]
        opponent = get(
            "https://pokeapi.co/api/v2/pokemon/" + str(randint(1, 898))
        ).json()
        bossSprite = opponent["sprites"]["front_default"]
        player = {"sprite": playerSprite, "health": 1000, "attacks": hitsRequired}
        opponent = {"sprite": bossSprite, "health": 1000, "attacks": hitsRequired}
        print("Sprites Successfully Generated!")
        print(playerSprite)
        print(bossSprite)
        return player, opponent

    def generateTrivia(self, questions):
        trivia = getChars()
        ## get all characters of the name + some
        print("Trivia Generated")
        return trivia[: questions * 2 - 1]

    def newQuestion(self):  ##Need a way of fixing unicode characters
        answer, img, answer_len = self.trivia.pop()
        self.answer = answer
        self.img = img
        self.answer_len = answer_len
        # print("Question Successfully Generated!\n" + str(answer_len) + "\nThe len of the answer is",answer,)
        # print("Possible Choices:", str(self.answer_len))
        return answer, img, answer_len

    def checkAnswer(
        self, yourAnswer
    ):  # Check answer to see if it is correct then apply damage accordingly
        if yourAnswer.strip() == self.answer:
            print("You have gotten the answer correct!")
            self.damageResult(self.opponent)
            return (True, self.player)
        else:
            print("You have gotten the answer incorrect")
            self.damageResult(self.player)
            return (False, self.opponent)

    def damageResult(self, damageTo):  # Apply damage to player/opponent
        if damageTo == self.player:
            attLeft = self.opponent["attacks"]
            if attLeft != 1:
                damage = randint(900, 1100) / (self.level // 2)
                self.player["health"] -= damage
                print(
                    "Player has taken",
                    damage,
                    "damage and has",
                    self.player["health"],
                    "health remaining",
                )
            else:
                print("Player has taken", self.player["health"], "damage")
                self.player["health"] = 0
                print("Player has died")
        elif damageTo == self.opponent:
            attLeft = self.player["attacks"]
            if attLeft != 1:
                damage = randint(900, 1100) / self.level
                self.opponent["health"] -= damage
                print(
                    "opponent has taken",
                    damage,
                    "damage and has",
                    self.opponent["health"],
                    "health remaining",
                )
            else:
                print("opponent has taken", self.opponent["health"], "damage")
                self.opponent["health"] = 0
                print("opponent has died")

    def healthCheck(self):  # Check health of player and boss
        return (
            str(self.player["health"] // 10) + "%",
            str(self.opponent["health"] // 10) + "%",
        )

    def getSprites(self):  # Get player sprite and boss sprite
        return self.player["sprite"], self.opponent["sprite"]

    def testTerminal(self):  # Here only for testing purposes
        self.newQuestion()
        self.checkAnswer(str(input()))


if __name__ == "__main__":
    x = PlayerVsPlayer()
    while True:
        x.testTerminal()
