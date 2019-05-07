# DeSW
Just a simple De-switcher.

# Uhhhmmm
First of all, this project was not concieved to be used alone.

# How it works
The idea is this:
*Apply Lief on the original PE

*dissasemble the code

*detect switch

*patch de instructions, and the tables

*hook where the switch was to a new area, where we assemble several cmp/jxx which emulates the switch

# Input output
As input the module takes the code and the relocs, and as output you should get the code and relocs, but modified


This module uses Lief, Capstone and Keystone.
