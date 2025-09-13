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

# board class

class board:
    boardSideLength = 8  # default chess board

    pieceMappings = {
            "k": king,
            "q": queen,
            "r": rook,
            "b": bishop,
            "n": knight,
            "p": pawn
            }
    
    def convertSquareToIndex(self, square: str) -> int:
        """Converts a square on the chess board to a list index

        :self: board - the board the square index is wanted from
        :square: str - the corresponding board square string (like a1)

        board.convertSquareToIndex takes a SAN square and converts it to an index on the board itself."""
        square = square.strip()
        if not len(square) >= 2:
            raise Exception("Square is invalid")
        # ord square[0] - 97 converts the letter into an index of the alphabet
        return ((self.sideLength * (self.sideLength - int(square[1 : ]))) + 
                (ord(square[0].casefold()) - 97))

    def convertIndexToSquare(self, square: int):
        """Converts a list index into a square on the chess board

        :self: board - the board the square string is wanted from
        :square: int - the index of the square on the board

        board.convertIndexToSquare takes an index on the board and converts it to a SAN square."""
        return chr((square % self.sideLength) + 97) + str(self.sideLength - (square // self.sideLength))

    def __init__(self, startingFen: str) -> None:
        """Initialises a chess board

        :self: board - the board the game will take place on
        :startingFen: str - the associated FEN code for the chess game

        This constructor takes a FEN code and parses it into a board object"""
        # variable declarations
        self.boardPieces = []
        self.castling = []
        self.sideLength = board.boardSideLength
        self.playerTurn = None
        self.enPassantSquare = None
        self.fiftyMovesClock = 0
        self.fullMoveClock = 1

        # process the FEN code
        startingFen = startingFen.strip()
        startingFen = startingFen.replace("/", " ")

        # split into the "components"
        components = [component for component in startingFen.split(" ") if not component.isspace()]
        # clean up the original startingFen variable
        del startingFen

        # validate number of components
        if len(components) != self.sideLength + 5:
            raise Exception("FEN is not long enough (potential missing info)")

        for componentsIndex in range(self.sideLength):
            chessLineSum = 0
            for pieceLetter in components[componentsIndex]:
                if pieceLetter.isdecimal():
                    chessLineSum += int(pieceLetter)
                    for _ in pieceLetter:
                        self.boardPieces.append(None)
                    continue  # ignore interpreting the letter as a piece
                if pieceLetter.isupper():
                    pieceColour = "w"
                else:
                    pieceColour = "b"

                try:
                    self.boardPieces.append((board.pieceMappings[pieceLetter.casefold()])(len(self.boardPieces), pieceColour))
                except KeyError:
                    raise Exception("Invalid Piece in FEN (may be caused by invalid side length)")
                
                chessLineSum += 1
            if chessLineSum != self.sideLength:
                raise Exception("Incorrect number of pieces")
        
        # sideLength coincides with the index of the colour (colour comes straight after pieces, and pieces end at self.sideLength)
        if components[self.sideLength] not in ("w", "b"):
            raise Exception("Invalid colour turn")
        self.playerTurn = components[self.sideLength]

        for castlingRight in components[self.sideLength + 1]:
            if castlingRight.casefold() in ("q", "k"):
                self.castling.append(castlingRight)

        if components[self.sideLength + 2] != "-":
            self.enPassantSquare = self.convertSquareToIndex(components[self.sideLength + 2])

        self.fiftyMovesClock = int(components[self.sideLength + 3])
        self.fullMoveClock = int(components[self.sideLength + 4])
    
    def checkMove(self, origin: int, target: int) -> bool:
        """Validates a move based on an origin point and a target square
        
        :self: board - a board of pieces
        :origin: int - the index of the piece
        :target: int - the target index of the piece (the new location)
        :return: bool - if the piece can move to the target square (excluding exceptions, which are handled only in move with completeAdminTasks = True)
        """
        return target in self.boardPieces[origin].getMoves([x != None for x in self.boardPieces])

    def move(self, origin: int, target: int, completeAdminTasks: bool = True) -> bool:
        """Moves a piece based on an origin point and a target square

        :self: board - a board of pieces
        :origin: int - the index of the piece
        :target: int - the target index of the piece (the new location)
        :completeAdminTasks: bool - if the move is to complete all admin (switch turns, and deal with exceptions)"""
        def _move(origin: int, target: int) -> None:
            # if we are allowing a move to occur
            self.boardPieces[target] = self.boardPieces[origin]
            self.boardPieces[origin] = None
            self.boardPieces[target].move(target)

        if not completeAdminTasks:
            _move(origin, target)
            return True
        
        # we need to deal with admin, like checking legal moves, and exceptions to standard rules
        def _checkCastlingRights(colour) -> None:
            # we won't be adding already removed castling rights
            # look at current castling rights
            rights = self.castling
            if colour == "w":
                colourRights = [right for right in rights if right.isupper()]
            else:
                colourRights = [right for right in rights if right.islower()]
            del rights
            
            kingIndex = -1
            for index, piece in self.boardPieces:
                if piece != None:
                    if isinstance(piece, king) and piece.colour == colour:
                        kingIndex = index
                        break  # there should only be one king
            if kingIndex == -1:
                # do not attempt to check if there is no king
                return
            
            kingInCorrectRank = False
            if ((colour == "w" and kingIndex // self.sideLength == self.sideLength - 1) or
                (colour == "b" and kingIndex // self.sideLength == 0)):
                kingInCorrectRank = True
            
            for right in colourRights:  # colour specific rights
                if not (kingIndex % self.sideLength == 4 and kingInCorrectRank):  # if king isn't in e file or in the correct rank
                    # can't castle if king has moved
                    self.castling.remove(right)
                    continue

                currentIndex = kingIndex
                rookDetected = False
                if right.casefold() == "k":
                    # kingside rook needs to be there
                    while currentIndex % self.sideLength < self.sideLength - 1:
                        currentIndex += 1
                        if isinstance(self.boardPieces[currentIndex], rook) and self.boardPieces[currentIndex].colour == colour:
                            if currentIndex - kingIndex >= 2:
                                rookDetected = True
                                break

                    if not rookDetected:
                        self.castling.remove(right)
                    continue
                
                currentIndex = kingIndex
                rookDetected = False
                if right.casefold() == "q":
                    while currentIndex % self.sideLength > 0:
                        currentIndex -= 1
                        if isinstance(self.boardPieces[currentIndex], rook) and self.boardPieces[currentIndex].colour == colour:
                            if kingIndex - currentIndex >= 2:
                                rookDetected = True
                                break

                    if not rookDetected:
                        self.castling.remove(right)
                    continue

        def _checkForCheck(colour) -> None:
            pass

        if self.boardPieces[origin] == None:
            return False  # moving nothing

        if self.boardPieces[origin].colour == self.boardPieces[target].colour:
            return False  # capturing own colour
        
        originalBoard = self.boardPieces  # in case we need to revert due to check

        # castling flag will be used for check detection
        hasCastled = False

        # check if the move is in the getMoves list
        if self.checkMove(origin, target):
            _move(origin, target)
        elif isinstance(pawn, self.boardPieces[origin]):
            # check move using en passant
            # this just allows a pawn to "move" into an en passant square
            if target in self.boardPieces[origin].getMoves([index == self.enPassantSquare or piece != None
                                               for index, piece in enumerate(self.boardPieces)]):
                _move(origin, target)

                # capture the en-passanted piece
                if self.boardPieces[target].colour == "w":
                    self.boardPieces[target + self.sideLength] = None
                else:
                    self.boardPieces[target - self.sideLength] = None
            else:
                return False
        elif isinstance(king, self.boardPieces[origin]):
            # castling exception
            # king moves 2 spaces towards rook and rook moves next to the king

            # the king mustn't pass a square that is attacked
            # the king (nor the rook that he is castling to) may have moved
            hasCastled = True  # we assume we can castle

            # check if the castle is legal (i.e in castling rights list)
            if (target == origin + 2) and (self.boardPieces[origin].colour in ("w", "b")):  # kingside
                if self.boardPieces[origin].colour == "w":
                    if not origin // self.sideLength == self.sideLength - 1:
                        return False
                    # king is on bottom row
                    pass
                else:
                    pass
            if (target == origin - 2) and (self.boardPieces[origin].colour in ("w", "b")):  # queenside castle
                pass
            else:
                return False  # castle is invalid
        else:
            return False  # move is illegal

        # at the end we need to switch moves (assuming move is legal)
        if self.playerTurn == "w":
            self.playerTurn = "b"
        else:
            self.playerTurn = "w"
        return True  # if we have reached the end of the function, we return True
