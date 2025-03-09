# KenKen_AiProject
This project isfrom an AI course at university.
# Project Description: A puzzle problem
Consider the following puzzle: Given a grid of size NxN and adjacent cells are grouped in an
irregular form and assigned an arithmetic operator and target number. The task is to fill the grid with
digits from 1..N such that each digit appears once in each row and each column, and when we apply
the arithmetic operator to the digits in each group, the result will be the assigned target number.
Below is an example with N=6.

 ![image](https://github.com/user-attachments/assets/3f0762c7-a537-4e37-9916-f5b3eb32a12d)

In this project, you will model this puzzle as a Constraint Satisfaction Problem (CSP) and develop a
solution using constraint propagation and backtracking with the Minimum Remaining Value (MRV)
heuristic and forward checking to improve search efficiency.
The goal of this project is to solve any given instance of the above puzzle using the CSP approach,
optimizing the solving process using arc-consistency checking, MRV heuristic, and forward
checking to ensure that the solution is found efficiently.
For the above example the input/output for the agent is as follows:
Input:
Grid size (N), e.g. N=6.
Groups details which is given in the following format: <cells, arithmetic operation, target
number> e.g <{𝑐{1,1}
, 𝑐{2,1}},-,4>, <{𝑐{3,1}
, 𝑐{3,2}
, 𝑐{4,1}},+,7>, .. etc.
Output:
The program should output the completed grid with numbers filled in all the empty cells while
satisfying the puzzle rules.
# Requirements:
1. Formulate the puzzle as a Constraint Satisfaction Problem (CSP) by identifying the variables,
domains, and constraints.  
2. Design an AC-3 algorithm to enforce arc-consistency before the backtracking search. 
3. Design a backtracking search algorithm with the MRV heuristic to solve the puzzle. 
4. Design forward checking to eliminate values from the domains of neighboring cells as the
backtracking algorithm proceeds.
5. Write a Java or Python code for the AC-3 algorithm, backtracking search algorithm with the MRV
heuristic and forward checking. Ensure the code can handle different instances of the puzzle.
6. Test the solver on the 3 various instances of the puzzles as given below in test instances. 
7. Analyze and comment your results. Provide for each problem instance the solution, and the average/
worst/best time. Draw a figure summarizing all results. Interpret your results.


![image](https://github.com/user-attachments/assets/aaab74b8-67bd-4622-b567-02ca420157d3)
