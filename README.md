# Hangmant

A terminal based hangman game

## Requirements

Python 3.6+

## Required modules

* getch
* random
* os
* time

## Notes

The game centres itself on a terminal based on the number of columns in it.
The game uses the output of `stty size` to find the number of columns in the
terminal. This shouldn't be a problem in a \*nix based system. In Windows, you
have to set the number of columns manually.
