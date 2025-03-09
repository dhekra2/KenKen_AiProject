Here’s an improved version of your project description with better clarity and structure:  

---

# **KenKen AI Project**  
This project is based on an AI course at university.  

## **Project Description: A Puzzle Problem**  
The KenKen puzzle is a logic-based mathematical puzzle played on an **N×N grid**. The grid is divided into irregularly shaped groups of adjacent cells, each assigned:  
- An **arithmetic operator** (+, -, ×, ÷)  
- A **target number**  

### **Objective:**  
Fill the grid with digits from **1 to N**, ensuring:  
1. Each row and column contains unique digits (like Sudoku).  
2. The numbers within each group, when combined using the specified arithmetic operator, result in the given target number.  

Below is an example for **N=6**:  

![image](https://github.com/user-attachments/assets/3f0762c7-a537-4e37-9916-f5b3eb32a12d)  

---

## **Project Approach: Constraint Satisfaction Problem (CSP)**  
This puzzle is formulated as a **Constraint Satisfaction Problem (CSP)** and solved using:  
- **Constraint propagation** (to reduce the search space).  
- **Backtracking with heuristics** (to efficiently find solutions).  

The solving process includes:  
1. **Arc-Consistency (AC-3) Algorithm:** Ensures initial consistency by removing inconsistent values.  
2. **Backtracking Search with Minimum Remaining Value (MRV) Heuristic:** Selects the most constrained variable first.  
3. **Forward Checking:** Eliminates invalid values dynamically to speed up the search.  

---

## **Input/Output Format**  
### **Input:**  
- Grid size (**N**), e.g., **N=6**.  
- Group constraints in the format:  
  ```
  <cells, arithmetic operation, target number>
  ```
  Example:  
  ```
  <{c(1,1), c(2,1)}, -, 4>
  <{c(3,1), c(3,2), c(4,1)}, +, 7>
  ```
### **Output:**  
- A **fully completed grid** that satisfies all constraints.  

---

## **Requirements:**  
1. **Model the problem as a CSP** by defining:  
   - **Variables:** Cells in the grid.  
   - **Domains:** Values {1, ..., N}.  
   - **Constraints:** Unique row/column values and arithmetic conditions.  
2. Implement the **AC-3 algorithm** to enforce arc consistency before backtracking.  
3. Develop a **backtracking search algorithm with MRV heuristic**.  
4. Implement **forward checking** to prune inconsistent values during the search.  
5. **Code the solver in Python or Java** to handle various puzzle instances.  
6. **Test on three different puzzle instances** and evaluate performance.  
7. **Analyze results**, providing:  
   - Solution grids.  
   - Best, worst, and average execution times.  
   - A visual summary of results.  

---

### **Example Test Instances:**  
![image](https://github.com/user-attachments/assets/aaab74b8-67bd-4622-b567-02ca420157d3)  

This project aims to efficiently solve KenKen puzzles using AI techniques, optimizing performance through CSP principles. 🚀
