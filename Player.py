from Card import Card
from Deck import Deck

class Player:

	def __init__(self, name):
		self.name = name
		self.hand = []
		self.points = 0
		
	def draw(self, deck):
		self.hand.append(deck.drawCard())
		# return self
		
	def hasCard(self, card):
		for c in self.hand:
			if c.equals(card):
				return True
		return False
		
	def showScore(self):
		print(self.name + " has " + str(self.points) + " points.")
	
	def showHand(self):
		for card in self.hand:
			card.show()
			
	def sortHand(self):
		self.hand = sorted(self.hand, key=lambda card: (card.suit, card.value))
			
	def legalCards(self, leadCard):
		legalCards = []
		for card in self.hand:
			if card.suit == leadCard.suit:
				legalCards.append(card)
		if not legalCards:
			for card in self.hand:
				legalCards.append(card)
		return legalCards
			