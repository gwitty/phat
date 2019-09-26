from Card import Card
from Deck import Deck
from Player import Player
import copy
import random

class Game:
	
	def __init__(self):
		self.deck = Deck()
		self.players = self.playerSetUp()
		self.cardsPlayed = []
		self.dealerChosen = False
		self.startingPlayerIndex = 0
		
	def deal(self):
		while self.deck.cards:
			for player in self.players:
				player.draw(self.deck)
		for player in self.players:
			player.sortHand()
					
	def playerSetUp(self):
		players = []
		for i in range(4):
			if i == 0:
				name = input("Please enter YOUR name: ")
				players.append(Player(name))
			else:
				name = input("Please enter a player name: ")
				players.append(Player(name))
		return players

	def cutForDealer(self):
		cutCards = []
		lowPlayers = []
		for i in range(4):
			d = self.deck.drawCard()
			cutCards.append(d)
			print(self.players[i].name + " drew the " + d.name())
		lowestCard = Card("Plops",99)
		for i in range(4):
			if cutCards[i].value < lowestCard.value:
				lowestCard = cutCards[i]
		lowestCard.show()
		for i in range(4):
			if cutCards[i].value <= lowestCard.value:
				lowPlayers.append(i)
		print(lowPlayers)
		if len(lowPlayers) != 1:
			print("Low players are:")
			print(lowPlayers)
			print("Equal lowest cards. Try again!")
		else:
			print(self.players[lowPlayers[0]].name + " drew the lowest card so they will pitch.")
			self.startingPlayerIndex = lowPlayers.copy()[0]
			self.dealerChosen = True
			return self.startingPlayerIndex

		
	def round(self):
		self.trick(self.startingPlayerIndex)
		
	def trick(self, leadPlayerIndex):
		trick = []
		for i in range(4):
			if i == 0:
				leadCard = Card("Plops", 99)
			else:
				leadCard = trick[0]
			currentPlayerIndex = (leadPlayerIndex + i) % 4
			if currentPlayerIndex == 0:
				print("Your legal cards are: ")
				for c in self.players[0].legalCards(leadCard):
					c.show()
				# self.players[0].legalCards(leadCard,self.heartsBroken).show()
				number = int(input("Input number of card you want: "))
				try:
					card = self.players[0].legalCards(leadCard)[number]
				except:
					print("NOT GOOD")
			else:
				rand = random.randint(0,len(self.players[currentPlayerIndex].legalCards(leadCard,self.heartsBroken))-1)
				card = self.players[currentPlayerIndex].legalCards(leadCard)[rand]
			self.players[currentPlayerIndex].hand.remove(card)
			trick.append(card)
			self.cardsPlayed.append(card)
			# print(self.players[currentPlayerIndex].name + " played the " + str(card.value) + " of " + card.suit)
			print(self.players[currentPlayerIndex].name + " played the " + card.name())
		winningValue = 0
		for c in trick:
			if c.suit == leadCard.suit and c.value > winningValue:
				winningCard = c
				winningValue = c.value
		winner = self.players[(self.startingPlayerIndex + trick.index(winningCard)) % 4]
		print(winner.name + " won the trick.")
		for c in trick:
			if c.suit == "Hearts":
				winner.points += 1
			if c.equals(Card("Spades", 12)):
				winner.points += 13
		self.startingPlayerIndex = self.players.index(winner)	
		
	def run(self):
		if self.deck.cards == []:
			self.deck = Deck()
		self.deck.shuffle()
		while self.dealerChosen == False:
			self.startingPlayerIndex = self.cutForDealer()
			self.deck = Deck()
			self.deck.shuffle()
		self.deal()
		print("Your starting hand is: ")
		self.players[0].showHand()
		while len(self.cardsPlayed) != 52:
			self.round()
		for p in self.players:
			p.showScore()
		self.cardsPlayed = []

if __name__ == "__main__":
	game = Game()
	keepPlaying = True
	while keepPlaying == True:
		game.run()