# Solidity Contract Generator

A simple python script to generate a series of functions that assign variables to function calls and arithmetic. For the purpose of making random compiled circuits.

Functions will only call upon functions already generated before them, and will never call themselves to prevent infinite recursion.

Included is a function to generate structs with random data types as well, but currently not in use as generating functions wont return anything other than Solidity's data types.
