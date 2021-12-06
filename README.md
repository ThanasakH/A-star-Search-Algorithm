# Problem solving with A* Search Algorithm

## Background
Consider a grid of size N x N that represents a topographic map. Each tile describes the characteristics of its terrain, which could be of two types: normal or mountainous. ROBBIE the robot must navigate from a starting position (xs,ys) to a goal position (xg,yg) using a learned algorithms (there can only be one start and one goal).
**Note:** In the explanations below, we assume that tile (1,1) is the top-left tile in the map.

### Transition rules:
ROBBIE is allowed to go to one of the (at most) eight surrounding tiles, as shown in Figure 1(a). However, it cannot move to a mountainous tile, and it cannot move diagonally if one of the directions composing the diagonal contains a mountainous tile. For instance, the black tile in Figure 1(b) represents a mountain, hence ROBBIE can move only to the five white tiles indicated by the arrows. In contrast, ROBBIE can move to seven tiles in Figure 1(c).

<p align="center"><img src="https://user-images.githubusercontent.com/34445145/144842089-df1326fb-259a-4b85-9c8c-c9d4b7dc7cd0.png"></p>

### Path cost:
ROBBIE’s wheels are built so that a diagonal move is the easiest. Hence, the cost of
such a move is 1. Any other move has a cost of 2.

## Instructions
Your task is to write a Python 3 program called planpath that plans a path from a given starting tile to a goal tile.
- You should implement either Graph or Treesearch procedure to perform A*.
- Propose and implement a heuristic function for solving this problem.
- Determine whether this function is admissible or monotonic, and explain why.
- You will need to implement tie-breaking rules when all options have equal merit. Specify clearly in your documentation what are your tie-breaking rules.

### Excution:
Your program will have two command line arguments as follows: python code.py INPUT/inputi.txt OUTPUT/outputi.txt iteration_number

### Input:
- The first line will contain one number that specifies the number of rows and columns in the map.
- Subsequent lines will contain the map, one line per row. The following values will be accepted for each tile:

<p align="center"><img src="https://user-images.githubusercontent.com/34445145/144842948-90af1fc2-cf8f-4dd0-8d20-9c7ec02c4677.png"></p>

The following illustrates a procedure call and sample input for applying A/A* to a 3x3 map and printing diagnostic output for 5 iterations:
python code.py INPUT/input1.txt OUTPUT/output1.txt 5

The input1.txt:
```
3
SXR 
RRR 
XXG
```

### Output:
- For example, a path that goes Start, Right, Right-Down, Down, Down, Left- Down and Goal, with a total cost of 8, is represented as follows: S-R-RD-D-D- LD-G 8

### Programming Requirements:
- Your program should be written in Python 3.
- Your program should create a unique identifier for every generated node. The identifier of the start node should be N0, and other nodes should be identified as N1, N2, . . . according to the order in which they are generated. If you wish, you can include the actions used to reach a node in its identifier, e.g., N0-R-D.

### Output example:
Say node N0:S at position (1, 1) is the first node to be expanded by some search
algorithm not A*. The output for this step should be something like the following:

- N0:S1000#IDexpansion-orderg,h,f
- Children: {N1:S-R, N2:S-RD, N3:S-D }
- OPEN: {(N1:S-R 2 0 2), (N2:S-RD 1 0 1), (N3:S-D 2 0 2) }
- CLOSED: {(N0:S 1 0 0 0)}
