# Lecture 8: Intermediate-Code Generation

-----

## Outline

1.  **Intermediate representations in compilers**
2.  **Abstract Syntax Trees**
      * Variants of abstract syntax trees
3.  **Three-Address Codes**
      * Three address code implementation
      * SDT's for three address code generation
4.  **Static Single-Assignment Form**
5.  **Basic blocks and control flow graphs**
6.  **Summary of Lecture 8**

-----

### Intermediate-code generation in compilers

  <img src="../pictures/lecture08_1.jpg" width="600"/>


**Diagram Description: Compiler Pipeline**

The diagram illustrates the flow from source code to assembly code within a compiler, divided into a front-end and a back-end.

1.  **Source Code** (e.g., `if (b==0)a=b;`) is processed by **Lexical Analysis** into a **Token Stream**.
2.  The **Token Stream** is processed by **Syntax Analysis** to build a **Parse tree and syntax tree**. This stage interacts with the **Symbol table** by inserting information.
3.  **Semantic Analysis** takes the syntax tree and produces a **Decorated AST**. This stage uses the symbol table. An example symbol table is shown:

    | Name | Type | Size |
    | :--- | :--- | :--- |
    | b | int | 4 byte |
    | a | float | 8 byte |

4.  **Intermediate code generation** transforms the decorated AST into an intermediate representation.
    *The components from Lexical Analysis to Intermediate Code Generation constitute the **Front-end** (machine independent).*
5.  **Code optimization** refines the intermediate code.
6.  **Code generation** produces the final target code (e.g., **Assembly code** like `cmp rcx, 0` and `cmovz [rbp-8],rcx`).
    *The components from Code Optimization to the final target code constitute the **Back-end** (machine dependent).*

-----

## 1\. Intermediate representations in compilers

### Overview

  * This lecture covers different types of intermediate representations (IRs):
    1.  Abstract syntax trees
    2.  Three-address codes
    3.  Static single-assignment (SSA) form 
  * We will use the syntax-directed formalisms from Lecture 6 to specify the translation from high-level to low-level code.

### Front-end vs. back-end in compilers

  * In the analysis-synthesis model of a compiler, the front-end analyzes a source program and creates an intermediate representation, from which the back-end generates target code.
  * Details of the source language are confined to the front-end, and details of the target machine to the back-end.
  * With a suitably defined IR, a compiler for language `i` and machine `j` can be built by combining the front-end for language `i` with the back-end for machine `j`.
  * This approach can save considerable effort: `m x n` compilers can be built by writing just `m` front-ends and `n` back-ends (i.e., `m+n`).

### High-level vs. low-level IR

  *  In the process of translating a program in a given source
 language into code for a given target machine, a compiler may
 construct **a sequence of intermediate representations.**
  * **High-level representations** are close to the source language.    
    * Syntax-trees are high level.
  * **Low-level representations** are close to the target machine.
    * **Three-address code** can range from high- to low-level, depending on the choice of operators.
  * For looping statements, a syntax tree represents the components of a statement, whereas three-address code contains labels and jump instructions, similar to machine language.

  <img src="../pictures/lecture08_2.jpg" width="600"/>


**Diagram Description: IR Flow**

The diagram shows a flow from multiple source languages (C, Fortran, Pascal) to a High-Level IR (HIR), which is then translated to a Low-Level IR (LIR). The LIR is then used to generate code for multiple target machines (Pentium, Java bytecode, PowerPC).

### C programming language as an intermediate code

  * The choice of an IR varies from compiler to compiler.
  * An IR may be an actual language or internal data structures shared by the compiler phases.
  * C is often used as an intermediate form because:
    1.  it is flexible,
    2.  it compiles into efficient machine code,
    3.  and its compilers are widely available.
  * The original C++ compiler used a front-end that generated C code, treating a C compiler as its back-end.

-----

## 2\. Abstract Syntax Trees

### Recap: ASTs for expressions

An Abstract Syntax Tree (AST) for the expression `a1 := (2 + 12 * 3) / (6 - 19)` visually represents the operations and their operands in a hierarchical structure. The root is the assignment `:=`, with `a1` as the left child and the division `/` as the right child. The structure continues downwards, representing each sub-expression.

### Code generation based on AST

A post-order traversal of the AST can generate stack-based machine code. For the expression `a1 := (2 + 12 * 3) / (6 - 19)`, the steps would be:

1.  `push 2`
2.  `push 12`
3.  `push 3`
4.  `mul`
5.  `add`
6.  `push 6`
7.  `push 19`
8.  `sub`
9.  `div`
10. `pop a1`

  <img src="../pictures/lecture08_3.jpg" width="600"/>


### AST for if statement

  * An AST can be an n-ary tree instead of a binary tree. For example, an `if` statement can have three children: the condition, the `then` block, and the `else` block.
    <img src="../pictures/lecture08_4.jpg" width="600"/>

  * We are interested in binary ASTs.

### Left-child, right-sibling representation (LCRS) of ASTs

  * LCRS is a method for encoding a multi-way tree (where nodes can have any number of children) as a binary tree.
  * Instead of each node pointing to all its children, it holds only two pointers: one to its first child and one to its immediate next sibling.
  * **Advantages of this binary tree representation:**
    1.  It removes the need to know the number of children a node has in advance.
    2.  It restricts the number of pointers per node to a maximum of two, simplifying the code.

### SDT for AST construction

A syntax-directed definition can be used to produce syntax trees for arithmetic expressions. Each production has a semantic rule that creates a new node (either `Node` for operators or `Leaf` for operands).

  <img src="../pictures/lecture08_5.jpg" width="600"/>


### AST in Eclipse JDT

The Eclipse Java Development Tools (JDT) generate detailed ASTs for Java code.

  * **If Statement**: An `IfStmt` node has children for the condition (e.g., `BinaryExpr:greater`), the `then` block, and the `else` block. Each block contains further statements.
  * **While Statement**: A `WhileStmt` node has children for the loop condition (e.g., `UnaryExpr:not`) and the loop body, which is a `BlockStmt`.

-----

### Variants of abstract syntax trees

#### Directed acyclic graphs for expressions

  * In an AST, the tree for the common subexpression subtree
 would be replicated as many times as the subexpression
 appears in the original expression.
  * Adirected acyclic graph (hereafter called a DAG ) for an
 expression identifies the common subexpressions
 (subexpressions that occur more than once) of the expression.
  * Like the syntax tree for an expression, a DAG has leaves
 corresponding to atomic operands and interior nodes
 corresponding to operators.
  * The difference is that a node N in a DAG has more than one
 parent if N represents a common subexpression.
  * DAG’s can be constructed by using the same techniques that
 construct syntax trees.

  * DAG representation for the expression
 a +a*(b−c)+(b−c)*d.
  * Node ’−’ has two parents, representing its two uses in the
 subexpressions, `a * (b − c) and a + a *(b −c)`.

  <img src="../pictures/lecture08_6.jpg" width="600"/>


#### The Value-Number method for constructing DAGs

  * This method stores nodes of a DAG in an array of records.
  * Each record contains an operation code, and pointers to its children (or a lexical value for leaves). The index of the record in the array is its "value-number".
  * **Algorithm**: When creating a new node, the algorithm first searches the array to see if an identical node (same operator and children) already exists. If so, it returns the value-number of the existing node; otherwise, it creates a new node and returns its new value-number.

-----

## 3. Three-Address Codes

### Three-address codes: General style

* In three-address code (TAC), there is at most one operator on the right side of an instruction; that is, no built-up arithmetic expressions are permitted.
* A source-language expression like `x+y*z` might be translated into the sequence of three-address instructions:
    ```
    (1) T1 = x * y 
    (2) T2 = x + T1
    ```
* where T1 and T2 are compiler-generated temporary names. 
* unraveling of multi-operator arithmetic expressions and of nested ow-of-control statements makes three-address code desirable for target-code generation and optimization.

### Three-address codes vs. ASTs

* Three-address code is a linearized representation of a syntax tree or a DAG in which explicit names correspond to the interior nodes of the graph. 

  <img src="../pictures/lecture08_7.jpg" width="600"/>


### Addresses and Instructions

An address in three-address code can be one of the following: 

1.  **A name**: Source-program names can be used as addresses in three-address code.
2.  **A constant**: A compiler must handle many different types of constants and variables.
3.  **A compiler-generated temporary**: It is useful, especially in optimizing compilers, to create a distinct name each time a temporary is needed.

A **symbolic label** represents the index of a three-address instruction in the sequence of instructions.

### Common forms of the three-address instructions

1.  **Assignment instructions**:
    * `x = y op z`, where op is a binary arithmetic or logical operation.
    
2. * `x = op y`, where op is a unary operation like unary minus, logical negation, or type conversion operators.
3.  **Copy instructions**: `x = y`, where x is assigned the value of y.
4.  **Unconditional jump**: `goto L`. The instruction with label L is executed next.
5.  **Conditional jumps**: `if x goto L` and `ifFalse x goto L`. These instructions execute the instruction with label L next if x is true or false, respectively.
6.  **Relational jumps**: `if x relop y goto L`, which applies a relational operator to x and y and jumps to L if the relation is true.
7.  **Procedure and function calls**:
    * `param x` for parameters.
    * `call p, n` for a procedure call.
    * `y = call p, n` for function calls.
    * `return y` where y is an optional returned value.
8.  **Indexed copy instructions**:
    * `x = y[i]` sets x to the value in the location i memory units beyond location y.
    * `x[i] = y` sets the contents of the location i units beyond x to the value of y.
9.  **Address and pointer assignments**: `x = &y`, `x = *y`, and `*x = y`.

### Three-address instructions: Example

For the statement `do i = i + 1; while (a[i] < v);`, the TAC can use symbolic labels or position numbers.

  <img src="../pictures/lecture08_8.jpg" width="600"/>


### Addressing array elements

* To access an element in a one-dimensional array `A[low..high]` with element type `t` of size `T`, the address is calculated as `base + (i - low) * T`.
* This expression can be rewritten as `i * T + (base - low * T)`.
* The subexpression `C = base - low * T` can be pre-calculated at compile time.
* Accessing an element then requires two TAC instructions:
    ```
    T1 = i * T
    T2 = T1 + C 
    ```
* For a two-dimensional array `A[low1..high1][low2..high2]` stored in **row-major** order (used in C-family languages), the address of `A[i1, i2]` is: `base + ((i1 - low1) * n2 + i2 - low2) * T` where `n2` is the number of columns.
* This can be optimized to `((i1 * n2) + i2) * T + C`, where the constant `C` is pre-calculated at compile time. This requires four TAC instructions.

### Three-address code implementation

  * The description of three-address instructions specifies the
 components of each type of instruction, but it does not specify
 the representation of these instructions in a data structure.
  * In a compiler, these instructions can be implemented as objects
 or as records with fields for the operator and the operands.
  * Three such representations are called "quadruples,"
 "triples,"and "indirect triples."

* **Quadruples**: A quadruple has four fields: `op`, `arg1`, `arg2`, and `result`. For the code `a = (b * (-c)) + (b * (-c))`:

| | op | arg1 | arg2 | result |
| :--- | :--- | :--- | :--- | :--- |
| **0** | minus | c | | t1 |
| **1** | * | b | t1 | t2 |
| **2** | minus | c | | t3 |
| **3** | * | b | t3 | t4 |
| **4** | + | t2 | t4 | t5 |
| **5** | = | t5 | | a |

* **Triples**: A triple has only three fields: `op`, `arg1`, and `arg2`. The result of an operation is referred to by its position, rather than by an explicit temporary name.

| | op | arg1 | arg2 |
| :--- | :--- | :--- | :--- |
| **0** | minus | c | |
| **1** | * | b | (0) |
| **2** | minus | c | |
| **3** | * | b | (2) |
| **4** | + | (1) | (3) |
| **5** | = | a | (4) |

* **Indirect Triples**: This representation consists of a list of pointers to triples. This allows an optimizing compiler to move an instruction by reordering the pointer list, without affecting the triples themselves.

### SDT's for three address code generation

Syntax-Directed Translation (SDT) can be used to generate three-address code during parsing by attaching semantic rules to grammar productions.

* **Expressions**: For an expression like `E1 + E2`, the semantic rule generates code for `E1` and `E2`, creates a new temporary variable `temp`, and then generates the instruction `temp := E1.place + E2.place`.
* **Array References**: For an array reference like `id[E]`, the rules compute the offset. For a multi-dimensional array like `L1[E]`, the rules recursively calculate the address.
* **Control Flow**:
    * For an `if-then` statement, the SDT generates a new label `end` and creates a conditional jump: `if E.place = 0 then goto end`.
    * For `if-then-else`, it uses two new labels (`else` and `end`) to manage the control flow.
    * For a `while` loop, it uses two new labels (`begin` and `after`) to create the loop structure with a conditional jump to exit.

-----

## 4. Static Single-Assignment Form

* Static single-assignment form (SSA) is an intermediate representation that facilitates certain code optimizations.
* **Key Property**: In SSA, all assignments are to variables with distinct names. To achieve this, original variables are split into multiple versions, typically with a subscript (e.g., `p` becomes `p1`, `p2`, `p3`, etc.), so that each new variable name corresponds to only one definition.

| Three-Address Code | Static Single-Assignment Form |
| :--- | :--- |
| `p = a + b` | `p1 = a + b` |
| `q = p - c` | `q1 = p1 - c` |
| `p = q * d` | `p2 = q1 * d` |
| `p = e - p` | `p3 = e - p2` |
| `q = p + q` | `q2 = p3 + q1` |

### The φ-function

* The same variable may be defined in two different control-flow paths in a program.
* SSA uses a special **φ (phi) function** to merge the different versions of a variable that come from different control-flow paths. `y3 = φ(y1, y2)` means that the value of `y3` will be `y1` if control came from the path where `y1` was defined, and `y2` if it came from the path where `y2` was defined.
* φ-functions are not implemented as machine operations. A compiler implements a φ-function by inserting "move" operations at the end of every predecessor block.
* SSA makes data-flow analyses like determining use-define (UD) chains easier to perform. When looking at a use of a variable, there is only one place where that variable may have received its value.

-----

## 5. Basic blocks and control flow graphs

### Control Flow Graph (CFG)

* A Control Flow Graph (CFG) is a graph representation of computation and control flow in a program.
* **Nodes**: The nodes of the graph are **Basic Blocks**.
* **Edges**: An edge represents a branch between basic blocks.
* **Basic Block**: A sequence of assignment and expression evaluations that ends with a branch. It is a sequence of operations that are executed as a unit. Once the first operation in a basic block is performed, the remaining operations will also be performed without any other intervening operations.

### Control flow graph for three addresses codes

  * Control-Flow graph (CFG), similar to AST, is kind of a
 intermediate representation generated by the compilers.
  * It is typically created from the three addresses codes.
  * Example: Programs that turns a 10 × 10 matrix a into an
 identity matrix.
    * Real-valued array elements take 8 bytes each, and that the
 matrix a is stored in row-major form.

```
for i from 1 to 10 do
    for j from 1 to 10 do
        a[i, j] = 0.0;
for i from 1 to 10 do
    a[i, i] = 1.0;
```

  <img src="../pictures/lecture08_9.jpg" width="600"/>


### Generating Control-Flow Graphs

The process involves two steps:

1.  **Partitioning into Basic Blocks**: This is done by identifying the **leaders** in the three-address code. A leader is the first instruction of a basic block. The rules for finding leaders are:
    1.  The first three-address instruction is a leader.
    2.  Any instruction that is the target of a conditional or unconditional jump is a leader.
    3.  Any instruction that immediately follows a conditional or unconditional jump is a leader.
    A basic block consists of a leader and all instructions up to but not including the next leader.

2.  **Constructing the Flow Graph**:
    * The basic blocks are the nodes of the flow graph.
    * There is an edge from block `B` to block `C` if and only if it is possible for the first instruction in block C to immediately follow the last instruction in block B. This can happen in two ways:
        * There is a jump from the end of `B` to the beginning of `C`.
        * `C` immediately follows `B` in the original order, and `B` does not end in an unconditional jump.
    * Special `entry` and `exit` nodes that do not correspond to executable instructions are often added.

CFGs are essential for many code optimizations because they make the transfer of control explicit and are helpful for tasks like register allocation.

-----

## 6. Summary of Lecture 8

* **Intermediate Representation (IR)**: A compiler's front-end analyzes a source program and creates an IR, from which the back-end generates target code. An IR is typically a combination of a graphical notation and three-address code. 
* **Abstract Syntax Tree (AST)**: A node in an AST represents a construct, and the children of the node represent its subconstructs.
* **Three-Address Code (TAC)**: Takes its name from instructions of the form "x = y op z", with at most one operator per instruction. It also includes additional instructions for control flow. 
* **Control Flow Graph (CFG)**: A graph representation of all paths that might be traversed through a program during its execution. The CFG is an essential tool for many compiler optimizations and static analysis.

-----

## References

  * Aho,Alfred V., Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman
 (2006). Compilers: Principles, Techniques, and Tools (2nd
 Edition). USA: Addison-Wesley Longman Publishing Co., Inc. ISBN:
 0321486811. URL: http://infolab.stanford.edu/
 %5C~ullman/dragon/errata.html.
 
 * Ammann,P. and J. Offutt (2016). Introduction to software
 testing. Cambridge University Press. ISBN: 9781316773123. URL:
 https://cs.gmu.edu/%5C~offutt/softwaretest.
