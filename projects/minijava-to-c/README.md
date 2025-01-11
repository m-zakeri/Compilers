# **CheckOut Main Repository:** [MiniJava-C-Compiler](https://github.com/Aghajari/MiniJava-C-Compiler)

# MiniJava-C-Compiler

The MiniJava-C Compiler is a project designed to compile MiniJava code into C. MiniJava is a simplified version of Java that includes essential object-oriented features, making it ideal for educational purposes and lightweight application development. This compiler parses MiniJava code, performs semantic checks, and generates equivalent C code for execution.

**Note:** This project was developed for **educational purposes** as part of the **Compiler Design** course at **Amirkabir University of Technology (AUT)**.

## Compiler Phases
1. Lexer:
   - Converts the input MiniJava code into a stream of tokens.
   - Identifies keywords, identifiers, literals, and symbols.
   - Reports lexical errors if invalid characters are encountered.
   - Uses [SimpleJavaLexer](https://github.com/Aghajari/SimpleJavaLexer)
2. Parser:
   - Analyzes the token stream to construct an Abstract Syntax Tree (AST).
   - Ensures the syntax conforms to the MiniJava grammar.
   - Reports syntax errors with precise locations.
3. Semantic Analyzer:
   - Performs type checking and ensures the semantic correctness of the program.
   - Validates variable declarations, method calls, and expression types.
   - Reports semantic errors, such as type mismatches or undeclared variables.
4. Code Generator:
   - Translates the validated AST into equivalent C code.
   - Handles variable initialization, method calls, control flow, and expressions.
   - Produces optimized and readable C output.

## Features
- Object-Oriented Programming Support :
  + Classes and inheritance
  + Method overriding
  + Field access across inheritance chains
  + this reference
- Control Structures :
  + `if`, `else` statements
  + `for`, `while` loops
  + break and continue statements
- Arrays :
  + Integer array support (int[])
  + Array length property
  + Array indexing
- Basics :
  + Basic data types: int, boolean
  + Classes and objects
  + Method calls
  + Conditional statements (if-else)
  + Loops (while)
  + Arithmetic operations (+, -, *, /, %)
  + Logical operations (&&, ||, !)
  + Relational operators (<, <=, >, >=, ==, !=)
  + Variable assignments

## Example

```java
class Main {
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        int result = 2 + calc.add(4, calc.multiply(2, 4) / 2) * 4;
        System.out.println(result);
    }
}
class Base {
    public int add(int a, int b) {
        return a + b;
    }
}
class Calculator extends Base {
    public int multiply(int a, int b) {
        return a * b;
    }
}
```

Compiles to:

```c
// Main.c
int main() {
	Calculator *calc = $_new_Calculator();
	int result;
	int $_t_1 = calc->$_function_multiply(calc, 2, 4);
	int $_t_2 = $_t_1 / 2;
	int $_t_3 = calc->super.$_function_add(calc, 4, $_t_2);
	int $_t_4 = $_t_3 * 4;
	int $_t_5 = 2 + $_t_4;
	result = $_t_5;
	printf("%d\n", result);
}

// Base.h
struct Base {
	int (*$_function_add)(void *, int, int);
};
typedef struct Base Base;
int Base_add(void *$this, int a, int b);
Base *$_new_Base();

// Base.c
Base *$_new_Base() {
	Base *self = (Base *) malloc(sizeof(Base));
	self->$_function_add = Base_add;
	return self;
}
int Base_add(void *$this, int a, int b) {
	Base *super = (Base *) $this;
	int $_t_0 = a + b;
	return $_t_0;
}

// Calculator.h
struct Calculator {
	Base super;
	int (*$_function_multiply)(void *, int , int );
};
typedef struct Calculator Calculator;
int Calculator_multiply(void *$this, int a, int b);
Calculator *$_new_Calculator();

// Calculator.c
Calculator *$_new_Calculator() {
	Calculator *self = (Calculator *) malloc(sizeof(Calculator));
	self->$_function_multiply = Calculator_multiply;
	self->super.$_function_add = Base_add;
	return self;
}
int Calculator_multiply(void *$this, int a, int b) {
	Calculator *super = (Calculator *) $this;
	int $_t_0 = a * b;
	return $_t_0;
}
```

Parse Tree:
```c
...
Class{
  Name: Calculator
  Extends: Base
  Fields: (0)
  Methods: (1)
    Method{Name: multiply, Type: int, Params: (Field{Name: a, Type: int}, Field{Name: b, Type: int})} {
      CodeBlock
        Return: 
          BinaryExpression (*) (Type:int)
            Reference (Type:int): a
            Reference (Type:int): b
    }
}
```

## Implementation Details
- Class Translation
  + Classes become C structs
  + Methods become function pointers
  + Inheritance uses nested structs
  + Inheritance validation
  + Static type checking
- Method Dispatch
  + Virtual method tables via function pointers
  + $this pointer passed as first argument
  + Method override verification



  
