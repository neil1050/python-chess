# Copyright 2025 Neil Li
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from base import piece

# standard chess pieces definitions

class king(piece):
    def getMoves(self, obstacles: list[bool], sideLength: int = 8) -> list[int]:
        super().getMoves(obstacles, sideLength)

        legalMoves = []
        # king can move one square in any of the 8 ordinal directions
        flags = {"up": self.position - sideLength >= 0,
                 "down": self.position + sideLength < sideLength * sideLength,
                 "left": self.position % sideLength >= 1,
                 "right": self.position % sideLength <= 6}  # which basic directions the king can move in

        # THIS DOES NOT CONSIDER POTENTIAL ISSUES DUE TO CHECKS

        if flags["up"] and flags["left"]:
            legalMoves.append(self.position - sideLength - 1)
        
        if flags["up"]:
            legalMoves.append(self.position - sideLength)

        if flags["up"] and flags["right"]:
            legalMoves.append(self.position - sideLength + 1)

        if flags["right"]:
            legalMoves.append(self.position + 1)

        if flags["down"] and flags["right"]:
            legalMoves.append(self.position + sideLength + 1)

        if flags["down"]:
            legalMoves.append(self.position + sideLength)

        if flags["down"] and flags["left"]:
            legalMoves.append(self.position + sideLength - 1)

        if flags["left"]:
            legalMoves.append(self.position - 1)

        return legalMoves

class queen(piece):
    def getMoves(self, obstacles: list[bool], sideLength: int = 8) -> list[int]:
        super().getMoves(obstacles, sideLength)

        # queen can move any number of squares in the 8 ordinal directions (equivalent to a rook and a bishop)
        rookEquivalent = rook(self.position, self.colour)
        bishopEquivalent = bishop(self.position, self.colour)
        
        # get the rook and bishop moves and combine them to form the queen's moves
        return (rookEquivalent.getMoves(obstacles, sideLength)
                + bishopEquivalent.getMoves(obstacles, sideLength))

class rook(piece):
    def getMoves(self, obstacles: list[bool], sideLength: int = 8) -> list[int]:
        super().getMoves(obstacles, sideLength)

        # rook can move any number of squares in a straight line

        currentIndex = self.position
        obstacles[currentIndex] = False

        legalMoves = []

        # moving right
        while not (obstacles[currentIndex] or (currentIndex % sideLength >= sideLength - 1)):
            currentIndex += 1
            legalMoves.append(currentIndex)

        # reset between iterations
        
        currentIndex = self.position

        # move left
        while not (obstacles[currentIndex] or (currentIndex % sideLength <= 0)):
            currentIndex -= 1
            legalMoves.append(currentIndex)

        # move up
        currentIndex = self.position
        while not (obstacles[currentIndex] or (currentIndex - sideLength <= 0)):
            currentIndex -= sideLength
            legalMoves.append(currentIndex)

        # move down
        currentIndex = self.position
        while not (obstacles[currentIndex] or (currentIndex + sideLength >= sideLength * sideLength)):
            currentIndex += sideLength
            legalMoves.append(currentIndex)

        return legalMoves

class bishop(piece):
    def getMoves(self, obstacles: list[bool], sideLength: int = 8) -> list[int]:
        super().getMoves(obstacles, sideLength)

        # bishop can move any number of squares diagonally

        currentIndex = self.position
        obstacles[currentIndex] = False

        legalMoves = []

        # moving north east
        while not (currentIndex % sideLength >= sideLength - 1 or
                   currentIndex - sideLength < 0 or
                   obstacles[currentIndex]):
            currentIndex = currentIndex - sideLength + 1  # move one rank up and one file east
            legalMoves.append(currentIndex)
        
        # reset index to prevent duplicate items
        currentIndex = self.position

        # moving south east
        while not (currentIndex % sideLength >= sideLength - 1 or
                   currentIndex + sideLength >= sideLength * sideLength or
                   obstacles[currentIndex]):
            currentIndex = currentIndex + sideLength + 1  # move one rank down and one file east
            legalMoves.append(currentIndex)

        currentIndex = self.position

        # moving south west
        while not (currentIndex % sideLength <= 0 or
                   currentIndex + sideLength >= sideLength * sideLength or
                   obstacles[currentIndex]):
            currentIndex = currentIndex + sideLength - 1  # move one rank down and one file east
            legalMoves.append(currentIndex)

        currentIndex = self.position

        # moving north west
        while not (currentIndex % sideLength <= 0 or
                   currentIndex - sideLength < 0 or
                   obstacles[currentIndex]):
            currentIndex = currentIndex - sideLength - 1  # move one rank up and one file west
            legalMoves.append(currentIndex)

        return legalMoves

class knight(piece):
    def getMoves(self, obstacles: list[bool], sideLength: int = 8) -> list[int]:
        super().getMoves(obstacles, sideLength)

        legalMoves = []

        # knight moves 2 squares in a straight line (strictly), then moves one in the other axis
        # if the position is not further than the final index after moving down twice
        
        # knight moves 2 squares down
        if self.position + (2 * sideLength) < sideLength * sideLength:
            # if the left and right side don't exceed the edge (to NOT provide incorrect indexes)...
            if self.position % sideLength != 0:
                legalMoves.append(self.position + (2 * sideLength) - 1)

            if self.position % sideLength != 7:
                legalMoves.append(self.position + (2 * sideLength) + 1)

        # knight moves 2 squares up
        if self.position - (2 * sideLength) >= 0:
            # same code as the left and right side checks
            if self.position % sideLength != 0:
                legalMoves.append(self.position - (2 * sideLength) - 1)

            if self.position % sideLength != 7:
                legalMoves.append(self.position - (2 * sideLength) + 1)

        # knight moves 2 squares left
        if not self.position % sideLength <= 1:
            if self.position - sideLength >= 0:
                legalMoves.append(self.position - 2 - sideLength)
                
            if self.position + sideLength < sideLength * sideLength:
                legalMoves.append(self.position - 2 + sideLength)

        # knight moves 2 squares right
        if not self.position % sideLength >= 6: 
            if self.position - sideLength >= 0:
                legalMoves.append(self.position + 2 - sideLength)

            if self.position + sideLength < sideLength * sideLength:
                legalMoves.append(self.position + 2 + sideLength)

        return legalMoves

class pawn(piece):
    def getMoves(self, obstacles: list[bool], sideLength: int = 8) -> list[int]:
        super().getMoves(obstacles, sideLength)

        # pawns can move 1 square forward (2 if it hasn't moved yet (ie on second or sixth rank)),
        # can capture 1 square diagonally (only forwards, never backwards),
        # and en passant (not accounted for here, will be up to the implementation of board class)
        # colour is important here

        legalMoves = []

        if self.colour == "w":
            if not (self.position - sideLength < 0 or 
                    obstacles[self.position - sideLength]):  # if the next row doesn't contain a piece NOR is it out of bounds
                legalMoves.append(self.position - sideLength)

            if obstacles[self.position - sideLength] and (
                    not (self.position - sideLength < 0 or
                         self.position % sideLength <= 0)):  # if there is a piece to the top left, and we aren't going out of bounds
                    legalMoves.append(self.position - sideLength - 1)
            
            if obstacles[self.position - sideLength] and (
                    not (self.position - sideLength < 0 or
                         self.position % sideLength >= sideLength - 1)):  # if there is a piece to the top right, and we aren't going out of bounds
                    legalMoves.append(self.position - sideLength + 1)

            return legalMoves

        # if colour == "b"
        if not (self.position + sideLength >= sideLength * sideLength or 
                obstacles[self.position + sideLength]):  # if the next row doesn't contain a piece NOR is it out of bounds
            legalMoves.append(self.position + sideLength)

        if obstacles[self.position + sideLength] and (
                not (self.position + sideLength >= sideLength * sideLength or
                     self.position % sideLength <= 0)):  # if there is a piece to the top left, and we aren't going out of bounds
                legalMoves.append(self.position + sideLength - 1)
            
        if obstacles[self.position + sideLength] and (
                not (self.position + sideLength >= sideLength * sideLength or
                     self.position % sideLength >= sideLength - 1)):  # if there is a piece to the top right, and we aren't going out of bounds
                legalMoves.append(self.position + sideLength + 1)
        return legalMoves
