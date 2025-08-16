# Copyright 2025 Neil Li
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class piece:
    def __init__(self, boardIndex: int) -> None:
        """Initialises a chess piece

        :self: piece - the piece type and its location
        :boardIndex: int - where the piece is on the board
        
        This constructor emulates placing a piece on a certain tile of the chess board
        """
        self.position = boardIndex
    
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

class board:
    boardSideLength = 8  # default chess board

    pieceMappings = {
            }
    
    def __init__(self, startingFen: str) -> None:
        """Initialises a chess board

        :self: board - the board the game will take place on
        :startingFen: str - the associated FEN code for the chess game

        This constructor takes a FEN code and parses it into a board object"""
        self.boardPieces = []
    
    def checkMove(self, origin: int, target: int) -> bool:
        """Validates a move based on an origin point and a target square
        
        :self: board - a board of pieces
        :origin: int - the index of the piece
        :target: int - the target index of the piece (the new location)
        :return: bool - if the piece can move to the target square
        """
        return target in self.boardPieces[origin].getMoves([x != None for x in self.boardPieces])

    def move(self, origin: int, target: int) -> None:
        """Moves a piece based on an origin point and a target square

        :self: board - a board of pieces
        :origin: int """
        self.boardPieces[target] = self.boardPieces[origin]
        self.boardPieces[origin] = None
        self.boardPieces[target].move(target)
