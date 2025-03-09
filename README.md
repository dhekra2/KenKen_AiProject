# KenKen_AiProject
This project isfrom an AI course at university.
# Project Description: A puzzle problem
Consider the following puzzle: Given a grid of size NxN and adjacent cells are grouped in an
irregular form and assigned an arithmetic operator and target number. The task is to fill the grid with
digits from 1..N such that each digit appears once in each row and each column, and when we apply
the arithmetic operator to the digits in each group, the result will be the assigned target number.
Below is an example with N=6.   

![image](https://github.com/user-attachments/assets/5dea6268-8b2b-4e49-8d97-e95c02bff3c8)

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
