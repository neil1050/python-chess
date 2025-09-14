# Copyright 2025 Neil Li
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import importlib
import json

from pieces import king, queen, rook, bishop, knight, pawn

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

        def _checkForCheck(colour) -> bool:
            kingIndex = -1
            for index, piece in self.boardPieces:
                if piece != None:
                    if isinstance(piece, king) and piece.colour == colour:
                        kingIndex = index
                        break  # there should only be one king
            if kingIndex == -1:
                return False
            # execute get moves on all black pieces, if any piece
            # attacks the king, then the king is in check
            for index, piece in enumerate(self.boardPieces):
                if self.checkMove(index, kingIndex) and piece.colour != colour:
                    return True
            return False

        if self.boardPieces[origin] == None:
            return False  # moving nothing

        if self.boardPieces[origin].colour == self.boardPieces[target].colour:
            return False  # capturing own colour
        
        originalBoard = self.boardPieces  # in case we need to revert due to check

        # check if the move is in the getMoves list
        if self.checkMove(origin, target):
            _move(origin, target)
        elif isinstance(self.boardPieces[origin], pawn):
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
        elif isinstance(self.boardPieces[origin], king):
            # castling exception
            # king moves 2 spaces towards rook and rook moves next to the king

            # the king mustn't pass a square that is attacked
            # the king (nor the rook that he is castling to) may have moved

            _checkCastlingRights(self.boardPieces[origin].colour)

            if self.boardPieces[origin].colour == "w":
                castleRightToCheck = str.upper  # the uppercase rights (whites)
            else:
                castleRightToCheck = str.lower  # the lowercase rights (blacks)

            # check if the castle is legal (i.e in castling rights list)
            if (target == origin + 2) and (self.boardPieces[origin].colour in ("w", "b")):  # kingside
                if not castleRightToCheck("k") in self.castling:
                    return False
                # if castle is still in the castling rights
                # check for blocking pieces between
                
                currentIndex = origin
                rookIndex = -1
                while currentIndex % self.sideLength < self.sideLength - 1:
                    currentIndex += 1
                    if ((self.boardPieces[currentIndex] is not None) and
                        ((not isinstance(self.boardPieces[currentIndex], rook)) or currentIndex - origin < 3)):
                        # there is a piece in the way
                        return False
                    elif isinstance(self.boardPieces[currentIndex], rook):
                        rookIndex = currentIndex
                        break  # the rook has been found
                if rookIndex < 0:
                    return False  # no rook found

                _move(origin, origin + 1)
                if _checkForCheck(self.boardPieces[origin + 1].colour):
                    # revert the state
                    self.boardPieces = originalBoard
                    return False
                _move(origin + 1, target)
                if _checkForCheck(self.boardPieces[target].colour):
                    self.boardPieces = originalBoard
                    return False
                # the castle has been proven valid
                _move(rookIndex, target - 1)

            if (target == origin - 2) and (self.boardPieces[origin].colour in ("w", "b")):  # queenside castle
                if not castleRightToCheck("q") in self.castling:
                    return False
                # if castle is still in the castling rights
                # check for blocking pieces between
                
                currentIndex = origin
                rookIndex = -1
                while currentIndex % self.sideLength > 0:
                    currentIndex -= 1
                    if ((self.boardPieces[currentIndex] is not None) and
                        ((not isinstance(self.boardPieces[currentIndex], rook)) or origin - currentIndex < 3)):
                        # there is a piece in the way
                        return False
                    elif isinstance(self.boardPieces[currentIndex], rook):
                        rookIndex = currentIndex
                        break  # the rook has been found
                if rookIndex < 0:
                    return False  # no rook found

                _move(origin, origin - 1)
                if _checkForCheck(self.boardPieces[origin - 1].colour):
                    # revert the state
                    self.boardPieces = originalBoard
                    return False
                _move(origin - 1, target)
                if _checkForCheck(self.boardPieces[target].colour):
                    self.boardPieces = originalBoard
                    return False
                # the castle has been proven valid
                _move(rookIndex, target + 1)
                
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

importedMods = {}
modIdentifier = {}

def importMods(modsList: list[str] | None = None):
    global importedMods

    if modsList is None:
        # due to mutable default arguments
        modsList = []
    
    for mod in modsList:
        if mod in importedMods.keys():
            # mod has already been imported
            continue
        try:
            importedMod = importlib.import_module(mod)
        except ModuleNotFoundError:
            print(f"Failed to import {mod}")
            continue
        
        try:
            importedMods[mod] = {"class": importedMod, "manifest": importedMod.manifest}
        except AttributeError:
            print(f"Manifest is unavailable for {mod}, skipping...")
            continue
        finally:
            del importedMod

        modManifest = importedMods[mod]["manifest"]
        try:
            importedMods[mod]["identifier"] = modManifest.identifier
            if modManifest.identifier is None or not isinstance(modManifest.identifier, str):
                raise Exception("Identifier is an invalid value")

            importedMods[mod]["name"] = modManifest.name
            importedMods[mod]["author"] = modManifest.author
            importedMods[mod]["shortDesc"] = modManifest.description

            importedMods[mod]["classMappings"] = modManifest.mappings

            modIdentifier[importedMods[mod]["identifier"]] = mod
        except NameError:
            print("Manifest incomplete, skipping...")
            del importedMods[mod]
            continue
        except Exception:
            print("Identifier is an invalid value, skipping...")
            del importedMods[mod]
            continue
