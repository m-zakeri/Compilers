# Mini-Java compiler front-end development

The project includes parse tree and intermediate code generation (in form of C three addresses (TAC) code) for the [MiniJava](https://www.cambridge.org/resources/052182060X) or [eMiniJava](https://cs.rit.edu/~hh/teaching/cc17/eminijava) programming languages with [ANTLR](https://www.antlr.org/).


## Project Title
**Three-Address Code Generation for [MiniJava](https://www.cambridge.org/resources/052182060X/) Language Using [ANTLR](https://www.antlr.org/)**

## Introduction
The goal of this project is to design and implement a compiler that translates a subset of the Java programming language, referred to as [MiniJava](https://www.cambridge.org/resources/052182060X/) or [eMiniJava](https://cs.rit.edu/~hh/teaching/cc17/eminijava), into Three-Address Code (TAC) in C programming language. The project will involve constructing a parse tree, performing semantic analysis, and generating intermediate code that can be used for further compilation or execution.

## Objectives
1. **Define the [MiniJava](https://www.cambridge.org/resources/052182060X/) or [eMiniJava](https://cs.rit.edu/~hh/teaching/cc17/eminijava) Language**: Establish the syntax and semantics of the [MiniJava](https://www.cambridge.org/resources/052182060X/) language, including data types, control structures, and function definitions.
2. **Build a Parser Using [ANTLR](https://www.antlr.org/)**: Utilize [ANTLR](https://www.antlr.org/) to create a parser that can read Mini-Java source code and produce a parse tree.
3. **Create a Semantic Analyzer**: Implement a semantic analysis phase to check for type correctness and scope resolution.
4. **Generate Three-Address Code**: Develop an intermediate code generation module that translates the parse tree into TAC in C language.
5. **Testing and Validation**: Test the compiler with various [MiniJava](https://www.cambridge.org/resources/052182060X/) programs to validate the correctness and efficiency of the generated TAC.

## Project Steps

### Step 1: Define the Mini-Java Language
- **Syntax Specification**: Create a formal grammar for [MiniJava](https://www.cambridge.org/resources/052182060X/) or [eMiniJava](https://cs.rit.edu/~hh/teaching/cc17/eminijava), including:
  - Basic data types (int, boolean, etc.)
  - Control structures (if-else, while loops)
  - Method definitions and calls
  - Class declarations
- **Semantics**: Outline the semantic rules, including type checking and scoping.

**Note:** The grammar can be found on [MiniJava grammar](https://www.cambridge.org/resources/052182060X/MCIIJ2e/grammar.htm) or [eMiniJava](https://cs.rit.edu/~hh/teaching/cc17/eminijava) or [Java8](https://github.com/antlr/grammars-v4/tree/master/java/java8) or [Java20](https://github.com/antlr/grammars-v4/tree/master/java/java20).

### Step 2: Build a Parser Using ANTLR
- **[ANTLR](https://www.antlr.org/) Setup**: Install [ANTLR](https://www.antlr.org/) and set up the development environment.
- **Grammar File Creation**: Write the [ANTLR](https://www.antlr.org/) grammar file (`.g4`) based on the defined syntax.
- **Parser Generation**: Use [ANTLR](https://www.antlr.org/) to generate the parser and lexer from the grammar file.
- **Parse Tree Construction**: Implement code to construct the parse tree from [MiniJava](https://www.cambridge.org/resources/052182060X/) source code.

### Step 3: Create a Semantic Analyzer
- **Symbol Table Management**: Implement a symbol table to store variable and method information.
- **Type Checking**: Develop functions to perform type checking during the traversal of the parse tree.
- **Scope Resolution**: Ensure correct scoping rules for variables and methods.

### Step 4: Generate Three-Address Code
- **Intermediate Representation Design**: Define the structure of TAC, which _typically_ consists of instructions in the form `OP dst, src1, src2` ( or `dst = scr1 OP scr2 ;` in the C language).
- **Code Generation Algorithm**:
  - Traverse the parse tree.
  - Generate TAC instructions based on the constructs encountered (_e.g._, assignments, arithmetic operations, method calls). Implement a visitor or listener to traverse the parse tree and generate TAC.
  - Maintain temporary variables for intermediate results.
- **Output Format**: Implement functionality to output the generated TAC in C language format (_e.g._, `dst = scr1 OP scr2 ;`).

### Step 5: Testing and Validation
- **Test Cases Creation**: Develop a suite of [MiniJava](https://www.cambridge.org/resources/052182060X/) programs that cover various features of the language (see also: [MiniJava example programs](https://www.cambridge.org/resources/052182060X/#programs).
- **Validation Process**: Execute the generated TAC using a C compiler to verify correctness.
- **(Optional)** **Performance Evaluation**: Assess the efficiency of the generated code and optimize if necessary.

## Deliverables
1. **[ANTLR](https://www.antlr.org/) Grammar File**: The `.g4` file defining the [MiniJava](https://www.cambridge.org/resources/052182060X/) syntax.
2. **Parser Implementation**: Code for the parser and lexer generated by [ANTLR](https://www.antlr.org/).
3. **Semantic Analyzer Code**: Implementation of type checking and scope resolution.
4. **TAC Generation Module**: Code that translates the parse tree into Three-Address Code in C.
5. **Documentation**: A comprehensive report detailing the design decisions, implementation steps, and testing results.

## Timeline
| Week | Task |
|------|------|
| 1    | Define [MiniJava](https://www.cambridge.org/resources/052182060X/) language syntax and semantics |
| 2    | Set up [ANTLR](https://www.antlr.org/) and create grammar file |
| 3    | Generate parser and lexer; construct parse tree |
| 4    | Implement semantic analysis |
| 5    | Develop TAC generation module |
| 6    | Testing and validation of generated code |
| 7    | Finalize documentation and prepare presentation |

## Teamwork
Read more at [Teamwork Policy](team_work_policy.md) page.

## Conclusion
This project aims to provide a comprehensive understanding of compiler design principles by implementing a complete pipeline from parsing to intermediate code generation. By focusing on [MiniJava](https://www.cambridge.org/resources/052182060X/) and utilizing ANTLR, students will gain hands-on experience with modern tools and techniques in compiler construction. 

The project will provide hands-on experience in compiler design, specifically in parsing and intermediate code generation. By the end of the project, students will have a functional compiler that translates [MiniJava](https://www.cambridge.org/resources/052182060X/) code into three-address code in C, demonstrating their understanding of compiler construction principles.

The successful completion of this project will not only enhance theoretical knowledge but also practical skills in programming languages and compilers.

