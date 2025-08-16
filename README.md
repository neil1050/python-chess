# Python Chess

A basic chess game, supporting FEN and SAN.  

## Board Indexes

A board is stored as a list of pieces internally.  
The indexing starts at 0, which is defined as the top-left corner in the code (aka a8 on the chess board).  
The index then goes from left to right, then top to bottom (e.g from a8 -> h8, then repeating on the seventh rank, and continuing).  

### Boards with different side lengths

Boards with different side lengths use the same indexing system, however with a different amount of pieces in the list.  
> Note that it is not a requirement to support side lengths other than 8, and not all custom pieces may be supported  
