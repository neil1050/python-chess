# Copyright 2025 Neil Li
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# base piece class

class piece:
    def __init__(self, boardIndex: int, colour: str) -> None:
        """Initialises a chess piece

        :self: piece - the piece type and its location
        :boardIndex: int - where the piece is on the board
        
        This constructor emulates placing a piece on a certain tile of the chess board
        """
        self.position = boardIndex
        self.colour = colour
    
    def getMoves(self, obstacles: list[bool], sideLength: int = 8) -> list[int]:
        """Returns the valid moves of a piece

        :self: piece - the piece type and its location
        :obstacles: list[bool] - the potential blocking pieces
        :sideLength: - the side length of the board
        :return: list[int] - the squares the given piece can move on to

        piece.getMoves takes a list of obstacles, and using the self.position variable, determines all valid moves for the piece (using sideLength as a bounding check)
        """
        return []
    
    def move(self, newBoardIndex: int) -> None:
        """Emulates the movement of a piece

        :self: piece - the piece type and its location
        :newBoardIndex: int - where the piece is moving to

        piece.move takes a new index and emulates moving there"""

        self.position = newBoardIndex
