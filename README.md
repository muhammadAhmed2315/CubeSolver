# CubeSolver
A Python program is able to solve a Rubik's Cube. Users are able to scramble the cube, apply individual moves (e.g., U, U', F, F', etc.) as well as being able to see a 2D visualisation of the (net of) the cube. The program uses the IDA* algorithm, and for the heuristic function, generates a pattern database (by default the database contains ~ 10.5 million key value pairs, which take ~ 650MB to store in memory). The cube.py file contains the Cube class (which contains the functions for manipulating the cube), as well as a function for generating the pattern database. The solver.py file contains IDA_star class, which solves the cube. Finally, the project.py class 
# Getting Started

## Prerequisites
Make sure you have Python3 installed and you use it to run this program.
```
pip install -r requirements.txt
```

# Basic Functionality and Future Improvements
<ins>Basic Functionality:</ins>
* Representation of a 3x3x3 Rubik's Cube
* 18 different moves that the user to manipulate the cube
* Prints a 2D visualisation of the (net of) the cube
* Build a pattern database that uses the breadth-first search algorithm to store cube states and the number of moves required to reach that state 
* Automatically scramble the cube and specify the length of the scramble
* Return an algorithm that the user can use to solve a scrambled cube
<div dr="rtl"><ins>Future Improvements</u></div>

* Implement the cube using a different data structure. This will allow for a pattern database that uses the same amount of memory but is able to represent more cube states, and a higher number of states in the database is likely to result in significant performance increases.
* Use tree pruning in order to reduce the branching factor of the tree to below 18

<br><br>
# Project Demo
Video example: [https://www.youtube.com/watch?v=r2CcIj203fQ](https://www.youtube.com/watch?v=r2CcIj203fQ))
