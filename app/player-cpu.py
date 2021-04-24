from requests import get
from random import randint

class PlayerCPU:

    def __init__(self, bossLevel = 10): #Start up simulation
        self.bossLevel = bossLevel
        self.player, self.boss = self.generateEntities(bossLevel)
        self.trivia = self.generateTrivia(2*bossLevel)
        self.question = None
        self.answer = None

    def generateEntities(self, hitsRequired): #Create player and boss objects
        player = get("https://pokeapi.co/api/v2/pokemon/"+str(randint(1,898))).json()
        playerSprite = player['sprites']['front_shiny']
        boss = get("https://pokeapi.co/api/v2/pokemon/"+str(randint(1,898))).json()
        bossSprite = boss['sprites']['front_shiny']
        player = {"sprite": playerSprite, "health": 1000, "attacks": hitsRequired}
        boss = {"sprite": bossSprite, "health": 1000, "attacks": hitsRequired//2}
        print("Sprites Successfully Generated!")
        print(playerSprite)
        print(bossSprite)
        return player, boss

    def generateTrivia(self, questions): ##Need better ways of generating triva, possibly give MC or specific categoried trivia
        rawTrivia = get("https://opentdb.com/api.php?amount="+str(questions)).json()
        trivia = []
        for question in rawTrivia['results']:
            trivia.append([question["question"].strip(), question["correct_answer"].strip().upper()])
        return trivia

    def newQuestion(self): ##Need a way of fixing unicode characters
        question, answer = self.trivia.pop()
        self.question = question
        self.answer = answer
        print("Question Successfully Generated!\n",question,"\nThe correct answer is",answer)
        return question, answer

    def checkAnswer(self, yourAnswer): #Check answer to see if it is correct then apply damage accordingly
        if yourAnswer.strip().upper() == self.answer:
            print("You have gotten the answer correct!")
            self.damageResult(self.boss)
        else:
            print("You have gotten the answer incorrect")
            self.damageResult(self.player)

    def damageResult(self, damageTo): #Apply damage to player/boss
        if damageTo == self.player:
            attLeft = self.boss['attacks']
            if attLeft != 1:
                damage = randint(900,1100)/(self.bossLevel//2)
                self.player['health'] -= damage
                print("Player has taken",damage,"damage and has",self.player['health'],"health remaining")
            else:
                print("Player has taken",self.player['health'],"damage")
                self.player['health'] = 0
                print("Player has died")
        elif damageTo == self.boss:
            attLeft = self.player['attacks']
            if attLeft != 1:
                damage = randint(900,1100)/self.bossLevel
                self.boss['health'] -= damage
                print("Boss has taken",damage,"damage and has",self.boss['health'],"health remaining")
            else:
                print("Boss has taken",self.boss['health'],"damage")
                self.boss['health'] = 0
                print("Boss has died")

    def healthCheck(self): #Check health of player and boss
        return self.player['health'], self.boss['health']
        
    def testTerminal(self): #Here only for testing purposes
        self.newQuestion()
        self.checkAnswer(str(input()))
x = PlayerCPU()
while True:
    x.testTerminal()