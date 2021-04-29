# Team Crabs: Karl Hernandez, Arib Chowdhury, Anya Zorin, Saqif Abedin
# Softdev
# P3: ArRESTed Development, JuSt in Time
# 2021-04-23
from requests import get
from random import randint, shuffle
from html import unescape


class PlayerCPU:
    # bossLevel corresponds to the number of questions overall
    # categories will be the categories of trivia questions
    def __init__(self, bossLevel=10, categories=["random"]):  # Start up simulation
        self.bossLevel = bossLevel
        self.player, self.boss = self.generateEntities(bossLevel)
        self.trivia = self.generateTrivia(2 * bossLevel, categories)
        self.question = None
        self.answer = None
        self.choices = None

    def generateEntities(self, hitsRequired):  # Create player and boss objects
        player = get("https://pokeapi.co/api/v2/pokemon/" + str(randint(1, 898))).json()
        playerSprite = player["sprites"]["back_default"]
        boss = get("https://pokeapi.co/api/v2/pokemon/" + str(randint(1, 898))).json()
        bossSprite = boss["sprites"]["front_shiny"]
        player = {"sprite": playerSprite, "health": 1000, "attacks": hitsRequired}
        boss = {"sprite": bossSprite, "health": 1000, "attacks": hitsRequired // 2}
        print("Sprites Successfully Generated!")
        print(playerSprite)
        print(bossSprite)
        return player, boss


    def generateTrivia(
        self, questions, categories
    ):  ##Need better ways of generating triva, possibly give MC or specific categoried trivia
        questionsPerCategory = questions // len(categories) + 1
        openTriviaCategories = [
            0,1,2,3,4,5,6,7,8,"general_knowledge","books","film","music","musicals","television","videogames","boardgames","science_nature",
            "science_computers","science_mathematics","mythology","sports","geography","history","politics","art","celebrities","animals",
            "vehicles","comics","science_gadgets","anime_manga","cartoon_animations",
            ]
        trivia = []
        for category in categories:
            # Handles trivia categories from openTriviaDB as integers from 9 to 32
            if category == "random":
                category = randint(9, 32)
            elif category in openTriviaCategories:
                category = openTriviaCategories.index(category)
            # print(
            #     "Questions for category", openTriviaCategories[category], "generated!"
            # )
            if 9 <= category <= 32:
                rawTrivia = get("https://opentdb.com/api.php?amount="+str(questionsPerCategory)+"&category="+str(category)+"&type=multiple").json()
                for question in rawTrivia["results"]:
                    tmp = [unescape(question["correct_answer"].strip())] + [unescape(choice.strip()) for choice in question["incorrect_answers"]]
                    shuffle(tmp)
                    trivia.append([unescape(question["question"].strip()), unescape(question["correct_answer"].strip()), tmp])
        return trivia


    def newQuestion(self):  ##Need a way of fixing unicode characters
        question, answer, choices = self.trivia.pop()
        self.question = question
        self.answer = answer
        self.choices = choices
        print("Question Successfully Generated!\n",question,"\nThe correct answer is",answer,)
        print("Possible Choices:", str(self.choices))
        return question, answer, self.choices


    def checkAnswer(
        self, yourAnswer
    ):  # Check answer to see if it is correct then apply damage accordingly
        if yourAnswer.strip() == self.answer:
            print("You have gotten the answer correct!")
            self.damageResult(self.boss)
            return True
        else:
            print("You have gotten the answer incorrect")
            self.damageResult(self.player)
            return False


    def damageResult(self, damageTo):  # Apply damage to player/boss
        if damageTo == self.player:
            attLeft = self.boss["attacks"]
            if attLeft != 1:
                damage = randint(900, 1100) / (self.bossLevel // 2)
                self.player["health"] -= damage
                print("Player has taken",damage,"damage and has",self.player["health"],"health remaining")
            elif attLeft == 1:
                print("Player has taken", self.player["health"], "damage")
                self.player["health"] = 0
                print("Player has died")
            self.boss["attacks"] -= 1
        elif damageTo == self.boss:
            attLeft = self.player["attacks"]
            if attLeft != 1:
                damage = randint(900, 1100) / self.bossLevel
                self.boss["health"] -= damage
                print("Boss has taken", damage,"damage and has",self.boss["health"],"health remaining")
            elif attLeft == 1:
                print("Boss has taken", self.boss["health"], "damage")
                self.boss["health"] = 0
                print("Boss has died")
            self.player["attacks"] -= 1


    def healthCheck(self):  # Check health of player and boss
        return (
            str(self.player["health"] // 10) + "%",
            str(self.boss["health"] // 10) + "%",
        )


    def getSprites(self): # Get player sprite and boss sprite
        return self.player["sprite"], self.boss["sprite"]


    def testTerminal(self):  # Here only for testing purposes
        self.newQuestion()
        self.checkAnswer(str(input()))


if __name__ == "__main__":
    x = PlayerCPU()
    while True:
        x.testTerminal()
