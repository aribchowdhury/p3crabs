# Team Crabs: Karl Hernandez, Arib Chowdhury, Anya Zorin, Saqif Abedin
# Softdev
# P3: ArRESTed Development, JuSt in Time
# 2021-04-23
from requests import get
from random import randint, shuffle
from .marvel import getChars


class PlayerVsPlayer:
    # level corresponds to the number of questions overall
    # categories will be the categories of trivia questions
    def __init__(self, level=10):  # Start up simulation
        self.level = level
        self.player, self.opponent = self.generateEntities(level)
        self.trivia = self.generateTrivia(level)
        self.img = None
        self.answer = None
        self.choices = None

    def generateEntities(self, hitsRequired):  # Create player and opponent objects
        player = get("https://pokeapi.co/api/v2/pokemon/" + str(randint(1, 898))).json()
        playerSprite = player["sprites"]["front_shiny"]
        opponent = get(
            "https://pokeapi.co/api/v2/pokemon/" + str(randint(1, 898))
        ).json()
        bossSprite = opponent["sprites"]["front_shiny"]
        player = {"sprite": playerSprite, "health": 1000, "attacks": hitsRequired}
        opponent = {"sprite": bossSprite, "health": 1000, "attacks": hitsRequired}
        print("Sprites Successfully Generated!")
        print(playerSprite)
        print(bossSprite)
        return player, opponent

    def generateTrivia(self, questions):
        trivia = getChars()
        return trivia[:questions]

    def newQuestion(self):  ##Need a way of fixing unicode characters
        questionTuple = self.trivia.pop()
        self.answer = questionTuple[0]
        self.img = questionTuple[1]
        wordLength = len(self.answer)

        # self.question = question
        # self.answer = answer
        # self.choices = choices + [answer]
        # shuffle(self.choices)
        # print(
        #     "Question Successfully Generated!\n",
        #     question,
        #     "\nThe correct answer is",
        #     answer,
        # )
        # print("Possible Choices:", str(self.choices))
        # return question, answer, self.choices

    def checkAnswer(
        self, yourAnswer
    ):  # Check answer to see if it is correct then apply damage accordingly
        if yourAnswer.strip().upper() == self.answer:
            print("You have gotten the answer correct!")
            self.damageResult(self.opponent)
        else:
            print("You have gotten the answer incorrect")
            self.damageResult(self.player)

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

    def healthCheck(self):  # Check health of player and opponent
        return self.player["health"], self.opponent["health"]

    def testTerminal(self):  # Here only for testing purposes
        self.newQuestion()
        self.checkAnswer(str(input()))


if __name__ == "__main__":
    x = PlayerVsPlayer()
    while True:
        x.testTerminal()
