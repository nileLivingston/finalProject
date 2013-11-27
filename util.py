# Represents a single card object with rank, suit, and wildness.
class Card:

	# Initializes the rank, suit, and wildness of the Card.
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		if self.rank == 2 or self.rank == 3 or self.rank == 10:
			self.wild = True
		else:
			self.wild = False

	def getRank(self):
		return self.rank

	def getSuit(self):
		return self.suit

	def isWild(self):
		return self.wild

	# Returns a String representation of the Card.
	def toString(self):
		translatedRank = ""
		if self.rank == 11:
			translatedRank = "J"
		elif self.rank == 12:
			translatedRank = "Q"
		elif self.rank == 13:
			translatedRank = "K"
		elif self.rank == 14:
			translatedRank = "A"
		else:
			translatedRank = str(self.rank)

		return translatedRank + str(self.suit)

	# Returns True iff this card is playable (by Scheisskopf rules) on otherCard.
	def isPlayableOn(self, otherCard):
		# Pile is empty.
		if otherCard == None:
			return True
		# Wild cards are playable on anything.
		elif self.wild:
			return True
		# 7's case.
		elif otherCard.rank == 7:
			if self.rank <= 7:
				return True
			else:
				return False
		# Normal case.
		else:
			if self.rank >= otherCard.getRank():
				return True
			else:
				return False

	# Returns True iff card is more valuable than otherCard.
	# Value order:
	# 3 > 10 > 2 > A > K > ... > 4
	def isBetterThan(self, otherCard):
		if otherCard.getRank() == 3:
			return False
		elif otherCard.getRank() == 10:
			if self.rank == 3:
				return True
			else:
				return False
		elif otherCard.getRank() == 2:
			if self.rank == 3 or self.rank == 10:
				return True
			else:
				return False
		else:
			if self.wild:
				return True
			else:
				if self.rank > otherCard.getRank():
					return True
				else:
					return False

# A general purpose, last in first out (LIFO) data structure.
# In our implementation, used for representing stacks of Cards.
class Stack:

	# Elements of the stack are stored in a list, where the last element of the list
	# is topmost in the stack.
	def __init__(self):
		self.list = []

	# Removes the topmost element from the stack and returns it.
	def pop(self):
		if not self.list == []:
			return self.list.pop()

	# Adds item to the stack, making it the new topmost element.
	def push(self, item):
		self.list.append(item)

	# Push an entire list onto the stack. Note that the last element of the list
	# becomes the new topmost element of the stack.
	def pushList(self, list):
		for item in list:
			self.list.append(item)

	# Returns the number of elements in the stack.
	def size(self):
		return len(self.list)

	# Returns True iff stack is empty.
	def isEmpty(self):
		return self.size() == 0

	# Returns the item topmost in the stack.
	def peek(self):
		if self.isEmpty():
			return None
		index = self.size() - 1
		return self.list[index]

	# Returns a String representation of the stack.
	def toString(self):
		output = "["
		for item in self.list:
			output += item.toString() + " "
		output += "]"
		return output