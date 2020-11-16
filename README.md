## Small collection of tests for UCI chess engines

Run each test like so `python perft.py`.

The tests will run for each engine placed in the engines/ folder.


### Perft

Tests the engine on perftsuite.epd, a set of 127 positions.

Requires the engine to respond to\
`position <fen>`\
`perft <depth> <fen>`\
with a perft count. This can be part of a longer info print, as long as the perft count is given either as line with only one number, or as the first number following the word "nodes" ("Nodes", "nodes:", "nodes searched:" etc all work) in the first string "nodes" occurs.


### Eval Symmetry

Tests whether the engine gives the same eval if the board is mirrored.

Requires the engine to respond to\
`position <fen>`\
`eval`\
with an evaluation from white's point of view, given as a single integer.


### Mate

Tests an engine's aptitude at finding mating lines in positions from mate_in_x.epd with x going from 1 to 8.

Requires the engine to suport these uci commands\
`position <fen>`\
`go mate x movetime y`





