# Lecture 7: Semantic Analysis (Types and Symbol Tables)

-----

## Outline

1.  **Type Checking Basics**
      * Type systems
      * Type expressions
      * Type system implementation
      * Scope in type checking
2.  **Symbol Tables**
      * Implementing symbol tables
      * Use of symbol tables
3.  **Types and Declarations**
4.  **Type Checking, Conversion, and Inference SDT's**
      * Type checking
      * Type conversion
      * Type inference
5.  **Symbol Tables for Program Analysis and Transformation**
6.  **Summary of Lecture 7**

-----

### Type checking in compilers

<img src="../pictures/lecture07_1.jpg" width="600"/>

-----

## Non-context-free syntax

  * Programs that are correct with respect to the language's lexical and context-free syntactic rules may still contain other syntactic errors.
  * Lexical analysis and context-free syntax analysis are not powerful enough to ensure the correct usage of variables, objects, functions, statements, etc.
  * Non-context-free syntactic analysis is known as **semantic analysis**.

## Semantic analysis

  * The semantic analyzer uses the syntax tree and the information in the symbol table to check the source program for semantic consistency with the language definition.
  * **Symbol tables** are data structures that are used by compilers to hold information about source-program constructs.
  * The information is collected incrementally by the analysis phases of a compiler and used by the synthesis phases to generate the target code.
  * An important part of semantic analysis is **type checking**, where the compiler checks that each operator has matching operands.
  * We shall study various types of symbol tables and SDT's for type checking in this lecture.

## Incorrect programs

  * **Example 1**: lexical analysis does not distinguish between different variable or function identifiers (it returns the same token for all identifiers):

| Correct | Incorrect |
| :--- | :--- |
| `int a; a=1;` | `int a; b=1;` |

  * **Example 2**: syntax analysis does not correlate the declarations with the uses of variables in the program:

| Correct | Incorrect |
| :--- | :--- |
| `int a; a=1;` | `a=1;` |

  * **Example 3**: syntax analysis does not correlate the types from the declarations with the uses of variables:

| Correct | Incorrect |
| :--- | :--- |
| `int a; a=1;` | `int a; a=1.0;` |

## Goals of semantic analysis

  * Semantic analysis ensures that the program satisfies a set of additional rules regarding the usage of programming constructs (variables, objects, expressions, statements).
  * Examples of semantic rules:
      * Variables must be declared before being used.
      * A variable should not be declared multiple times in the same scope.
      * In an assignment statement, the variable and the assigned expression must have the same type.
      * The condition of an `if-statement` must have type Boolean.
  * Categories of rules:
      * Semantic rules regarding **types**.
      * Semantic rules regarding **scopes**.

-----

## 1\. Type Checking Basics

### Type systems

**What are types?**

  * Types describe the values possibly computed during execution of the program.
  * Types are predicates on values.
      * e.g., "int x" in Java means x ∈ [-2^31, 2^31-1].
  * Think "type = set of possible values".
  * **Type errors**: improper, type-inconsistent operations during program execution.
  * **Type-safety**: absence of type errors at run time.


**Type information**

Type information classifies a program's constructs (e.g., variables, statements, expressions, functions) into categories, and imposes rules on their use (in terms of those categories) with the goal of avoiding runtime errors.

| Construct | Example | Type |
| :--- | :--- | :--- |
| variables | `int a;` | integer location |
| expressions | `(a+1)==2` | Boolean |
| statements | `a=1.0;` | void |
| functions | `int pow(int n, int m)`| int × int → int |

**How to ensure type-safety?**

  * Bind (assign) types, then check types:
      * **Type binding**: defines types for constructs in the program (e.g., variables, functions).
        * Can be either **explicit** (`int x`) or **implicit** (`x=1`).
        * **Type consistency (safety)** = correctness with respect to the type bindings.
      * **Type checking**: static semantic checks to enforce the type safety of the program.
        * Enforce a set of type-checking rules.

**Static vs. dynamic typing**

  * Static and dynamic typing refer to type definitions (i.e., bindings of types to variables, expressions, etc.).
  * **Statically typed language**: types are defined and checked at compile-time, and do not change during the execution of the program.
      * E.g., Pascal, C, Java.
  * **Dynamically typed language**: types defined and checked at run-time, during program execution.
      * E.g., Lisp, Scheme, Smalltalk, Python.

**Strong vs. weak typing**

  * Strong and weak typing refer to how much type consistency is enforced.
    * **Strongly typed languages**: guarantees that accepted programs are type-safe: Java.
    * **Weakly typed languages**: allow programs that contain type errors: C.
  * Can achieve strong typing using either static or dynamic typing.

**Why static checking?**

  * **Efficient code**: Dynamic checks slow down the program execution.
  * **Guarantees that all executions will be safe**: With dynamic checking, you never know when the next execution of the program will fail due to a type error.
  * But is conservative for sound systems; needs to be expressive: Reject few type-safe programs.

**Type systems concept summary**

  * **Static vs. dynamic typing**: when to define/check types?
  * **Strong vs. weak typing**: how many type errors?
  * **Sound type systems**: statically catch all type errors (and possibly reject some programs that have no type errors).

| | **Strong Typing** | **Weak Typing** |
| :--- | :--- | :--- |
| **Static Typing** | ML, Pascal, Java, Modula-3 | C, C++ |
| **Dynamic Typing** | Scheme, Python, Smalltalk, PostScript | assembly code |

### Type expressions

**Recap: Type system**

  * Type is a predicate on value.
  * **Type expressions**: describe the possible types in the program: e.g., int, string, array[], class, etc.
  * **Type system**: defines types for language constructs (e.g., expressions, statements, ...).

**Type expression**

  * Languages have **basic types** (a.k.a. primitive types or ground types).
      * E.g., int, char, boolean.
  * Build type expressions using basic types with:
      * Type constructors
      * Type aliases

**Array type**

  * Various kinds of array types in different programming languages.
  * `array(T)`: array with elements of type T and no bounds.
      * C, Java: `int[]`, Modula-3: `array of integer`.
  * `array(T, S)`: array with size.
      * C: `int[10]`, Modula-3: `array[10] of integer`.
      * May be indexed 0..size-1.
  * `array(T, L, U)`: array with upper/lower bounds.
      * Pascal or Ada: `array[2..5] of integer`.
  * `array(T, S1, ..., Sn)`: multi-dimensional arrays.
      * FORTRAN: `real(3,5)`.

**Record type**

  * A record is `{id1: T1, ..., idn: Tn}` for some identifiers `idi` and types `Ti`.
  * Supports access operations on each field, with corresponding type.
  * C: `struct { int a; float b; }`
  * Pascal: `record a: integer; b: real; end`
  * Objects: generalize the notion of records.

**Pointers**

  * Pointer types characterize values that are addresses of variables of other types.
  * `Pointer(T)`: pointer to an object of type T.
  * C pointers: `T*` (e.g., `int *x;`).
  * Pascal pointers: `^T` (e.g., `x: ^integer;`).
  * Java: Object references.

**Function Types**

  * A function value can be invoked with some argument expressions with types `Ti`, returns return type `Tr`.
  * Type: `T1 × T2 × ... × Tn → Tr`.
  * C/C++ functions: `int pow(int x, int y)` has type `int × int → int`.
  * Java: methods have function types.
  * Some languages have first-class functions (usually in functional languages, e.g., ML, LISP).
  * C and C++ have function pointers.
  * Java does not.

**Type alias**

  * Some languages allow type aliases (type definitions, equates):
      * C: `typedef int int_array[];`
      * Modula-3: `type int_array = array of int;`
  * Java does not allow type aliases.
  * Aliases are not type constructors! `int_array` is the same type as `int[]`.
  * Different type expressions may denote the same type.

### Type system implementation

**Implementation approaches**

1.  Use a separate class hierarchy for type ASTs:
    ```java
    class BaseType extends Type
    ...
    class IntType extends BaseType
    ...
    class BoolType extends BaseType
    class ArrayType extends Type {
      Type elemType;
    }
    class FunctionType extends Type ...
    ```
2.  Translate type expressions to type objects during parsing:
    ```
    // non-terminal Type type
    type ::= BOOLEAN { RESULT=new BoolType(); }
           | ARRAY LBRACKET type:t RBRACKET { RESULT=new ArrayType(t); }
           ...
    ```
3.  Bind names to type objects in the symbol table during subsequent AST traversal.

### Scope in type checking

**Processing type declaration**

  * Type declarations add new identifiers and their types in the symbol tables.
  * Class definitions must be added to symbol table:
      * `class_defn ::= CLASS ID:id { decls:d }`
  * Forward references require multiple passes over AST to collect legal names.
      * Example: `class A { B b; } class B { ... }`
  * Need to handle scope information.

**Scope information**

  * Scope information characterizes the declaration of identifiers and the portions of the program where use of each identifier is allowed.
  * Example identifiers: variables, functions, objects, labels.
  * **Lexical scope** is a textual region in the program:
    1.  Statement block
    2.  Formal argument list
    3.  Object body
    4.  Function or method body
    5.  Module body
    6.  Whole program (multiple modules)
  * **Scope of an identifier**: the lexical scope in which it is valid.

**Scope examples in C:**

  * Scope of variables in statement blocks:

  <img src="../pictures/lecture07_2.jpg" width="600"/>


**Other scope examples:**

  * **Function arguments**: `int factorial(int n) { /* scope of n is the function body */ }`
  * **Labels**: `void f() { goto I; ... I: a=1; /* scope of I is the function body */ }`
  * **Object fields and methods**:
    ```java
    class A {
      private int x; // scope of x is class A
      public void g() { x=1; } // scope of g is class A and its subclasses
    }
    class B extends A {
      public int h() { g(); }
    }
    ```

**Semantic rules for scopes**

  * Main rules regarding scopes:
    * **Rule 1**: Use an identifier only if it is defined in an enclosing scope.
    * **Rule 2**: Do not declare identifiers of the same kind with identical names more than once in the same scope.
  
  * You can declare identifiers with the same name if they are of a different kind

  <img src="../pictures/lecture07_3.jpg" width="600"/>


-----

## 2\. Symbol Tables

  * Semantic checks refer to properties of identifiers in the program - their scope or type.
  * Need an environment to store the information about identifiers - **Symbol Table** (or Symtab).
  * Each entry in the symbol table contains:
      * The name of an identifier.
      * Additional information: its kind, its type, its size, if it is constant, ...

**Example Symbol Table:**

| NAME | KIND | TYPE | OTHER |
| :--- | :--- | :--- | :--- |
| foo | fun | int x int → bool | extern |
| m | par | int | auto |
| n | par | int | const |
| tmp | var | bool | const |

**Handling scope information in symbol table**

  * How to represent scope information in the symbol table?
    1.  There is a hierarchy of scopes in the program.
    2.  Use a similar hierarchy of symbol tables.
    3.  One symbol table for each scope.
    4.  Each symbol table contains the symbols declared in that lexical scope.

**Example**

  <img src="../pictures/lecture07_4.jpg" width="600"/>


**Handling identifiers with the same name**

  * The hierarchical structure of symbol tables automatically solves the problem of resolving name collisions.
  * To find the declaration of an identifier that is active at a program point:
    1.  Start from the current scope.
    2.  Go up in the hierarchy until you find an identifier with the same name, or fail.

  **Example:**

  <img src="../pictures/lecture07_5.jpg" width="600"/>



**Catching semantic errors**

  <img src="../pictures/lecture07_6.jpg" width="600"/>

**Symbol table operations**

  * Three main operations:
    1.  Create a new empty symbol table with a given parent table.
    2.  Insert a new identifier in a symbol table (or error on re-declaration).
    3.  Look-up an identifier in a symbol table (or error if not found).
  * Cannot build symbol tables during lexical analysis because the hierarchy of scopes is encoded in the syntax.
  * Build the symbol tables either:
      * While parsing, using semantic actions.
      * After the AST is constructed.

### Implementing symbol tables

**Implementation methods**

  * Array implementation
  * List implementation
  * **Hash-table implementation**

<!-- end list -->

1.  **Array implementation**:
      * Simple implementation = array
          * one entry per symbol.
          * Scan the array for loopup, compare name at each entry.

      * Disadvantage: 
          * Table has fixed size.
          * Need to know in advance the number of entries

2.  **List implementation**:
      * Dynamic structure = list
        * One cell per entry in the table.
        * Can grow dynamically during compilation.
      * Disadvantage:
        * Inefficient for large Symbol tables
        * Need to scan half the list on average


3.  **Hash-table implementation**:
      * Efficient implementation = hash table
        * It is an array of lists (buckets)
        * Uses a hashing function to map the symbol name to the corresponding bucket: `hashfunc : string → int`.
      * Good hash function = even distribution in the buckets.
      * We shall implement scopes by setting up a separate symbol table for each scope.

**Symbol table per scope (Chained symbol tables)**

  <img src="../pictures/lecture07_7.jpg" width="600"/>


  * A chain of symbol tables can represent nested scopes. A table for an inner scope holds a reference to the table for its parent (outer) scope.
  * Lookup proceeds from the current scope's table up through the chain of parent tables.

**Java implementation for Chained Symbol Tables:**

```java
// package symbols;
import java.util.*;
public class Env {
    private Hashtable table;
    protected Env prev;

    public Env (Env p) {
        table = new Hashtable();
        prev = p;
    }

    public void put (String s, Symbol sym) {
        table.put(s, sym);
    }

    public Symbol get(String s) {
        for(Env e = this; e != null; e = e.prev ) {
            Symbol found = (Symbol)(e.table.get(s));
            if(found != null) return found;
        }
        return null;
    }
}
```

**Forward references**

  * A forward reference is the use of an identifier within the scope of its declaration, but before the declaration itself appears in the text.
  * Any compiler phase that uses information from the symbol table must be performed *after* the table is fully constructed.
  * This means you cannot type-check and build the symbol table at the same time if forward references are allowed.
  * Example requiring 2 passes:
    ```java
    class A {
      int f1() { return f2(); } // f2 used before it's declared
      int f2() { return 1; }
    }
    ```

### Use of symbol tables

**SDT for translating with symbol tables**
An SDT can manage the creation and destruction of symbol tables for nested blocks.

  * When entering a block (`{`), create a new `Env` and link it to the previous one.
  * When exiting a block (`}`), restore the previous `Env`.
  * For declarations (`type id;`), add the symbol to the current `top` environment.
  * For uses (`id`), look up the symbol starting from the `top` environment.

Example Input:

```
{ int x; char y;
  { bool y; x; y; }
  x; y; }
```

Example Output (with types annotated):

```
{ { x:int; y:bool; } x:int; y:char; }
```

In a recursive-descent parser, the `saved` environment would be a local variable in the procedure for `block`.

-----

## 3\. Types and Declarations

An SDT can process type declarations and compute type information (like type expressions and memory width) to store in the symbol table.

**Grammar:**

  * $D → T id; D | ε$
  * $T → B C | record { D }$
  * $B → int | float$
  * $C → ε | [num] C$

**SDT with Semantic Rules:**
Attributes `type` and `width` are synthesized up the parse tree.

  * **For `B`**: Set base type and width (`int` is 4, `float` is 8).
  * **For `C`**: An inherited attribute passes the base type down, and synthesized attributes build up array types. `C.type = array(num.value, C1.type)` and `C.width = num.value * C1.width`.
  * **For `T`**: Combines the base type and array information.
  * **For `D`**: Adds the final type and computed offset to the symbol table for each identifier.
  * **For `P`**: A marker nonterminal `M` can be used to initialize a global `offset` variable, allowing the SDT to be written in postfix form. $P → M D$ where $M → ε {offset=0;}$.

-----

## 4\. Type Checking, Conversion, and Inference SDT's

### Type checking

**Type synthesis and type inference**

  * To do type checking, a compiler needs to assign a type expression to each component of the source program.
  * Type checking can take on two forms: synthesis and inference.
      * **Type synthesis** builds up the type of an expression from the types of its subexpressions.
      * **Type inference** determines the type of a language construct from the way it is used. It is needed for languages like ML, which check types but do not require names to be declared.

**Type checking rules**

  * Type checking is the validation of a set of type rules. Examples:
      * The type of a variable must match its declaration.
      * Operands of `+`, `*`, `-`, `/` must be integers; the result is an integer.
      * Operands of `==`, `!=` must be integer or string; the result is boolean.
      * In an assignment, the variable and expression types must match.
      * In a function call, actual argument types must match formal parameter types.
      * The return value type must match the function's declared return type.

**Semantic rules for type checking (Expressions):**

  * `E → literal` ⇒ `E.type := 'char'`
  * `E → num` ⇒ `E.type := 'int'`
  * `E → id` ⇒ `E.type := lookup(id.entry)`
  * `E → E1 mod E2` ⇒ `E.type := if E1.type == 'int' and E2.type == 'int' then 'int' else type_error`
  * `E → E1[E2]` ⇒ `E.type := if E2.type == 'int' and E1.type == 'array(s,t)' then t else type_error`

**Semantic rules for type checking (Statements):**

  * `S → id := E` ⇒ `S.type := if id.type == E.type then void else type_error`
  * `S → if E then S1` ⇒ `S.type := if E.type == 'boolean' and S1.type == void then void else type_error`
  * `S → while E do S1` ⇒ `S.type := if E.type == 'boolean' and S1.type == void then void else type_error`

**Type checking implementation**

  * Type checking can be implemented by an AST visitor.

<!-- end list -->

```java
class TypeCheck implements Visitor {
    Object visit(Add e, Object symbolTable) {
        Type t1 = (Type) e.e1.accept(this, symbolTable);
        Type t2 = (Type) e.e2.accept(this, symbolTable);
        if (t1 == Int && t2 == Int) return Int;
        else throw new TypeCheckError("+");
    }
    Object visit(Num e, Object symbolTable) {
        return Int;
    }
    Object visit(Id e, Object symbolTable) {
        return ((SymbolTable)symbolTable).lookupType(e);
    }
}
```

**Types comparison**

  * **Option 1**: Implement `T1.Equals(T2)`. For OO languages, also need `T1.SubtypeOf(T2)`.
  * **Option 2**: Use unique objects for each distinct type. This allows for faster comparison using `==`.

### Type conversion

  * **Widening conversions**: intended to preserve information (e.g., `int` to `float`).
  * **Narrowing conversions**: can lose information (e.g., `double` to `int`).
  * **Explicit conversion (cast)**: programmer must write something to cause the conversion.
  * **Implicit conversion (coercion)**: done automatically by the compiler. Usually limited to widening conversions.

**Type conversion implementation**

  * For an expression like `E → E1 + E2`:
    1.  Find the maximum type: `E.type = max(E1.type, E2.type)`.
    2.  Widen both operands to the max type: `a1 = widen(E1.addr, E1.type, E.type)`.
    3.  Generate code for the operation: `gen(E.addr '=' a1 '+' a2)`.
  * The `widen` function generates conversion instructions if necessary.
    ```
    Addr widen(Addr a, Type t, Type w) {
        if (t == w) return a;
        else if (t == integer && w == float) {
            temp = new Temp();
            gen(temp '=' '(float)' a);
            return temp;
        }
        else error;
    }
    ```

### Type inference

  * **Unification** is the problem of determining whether two expressions `s` and `t` can be made identical by substituting expressions for the variables in `s` and `t`.
  * This process is used to infer types in languages that don't require explicit type declarations.
  * Example: For `fun length(x) = if null(x) then 0 else length(tl(x)) + 1;`, the compiler unifies type variables to deduce that `x` must be a `list(α)` and the function's type is `list(α) → integer`.

-----

## 5\. Symbol Tables for Program Analysis and Transformation

  * Symbol tables are not just for compilation; they are crucial for advanced program analysis and transformation tools, like those used for automated refactoring.
  * **Generic Symbol Table**: A generic, reusable symbol table implementation for statically scoped languages is available at `github.com/antlr/symtab`.
  * **Object-oriented models**: Some tools (like JDeodorant) use detailed object-oriented models to represent types, properties, and relationships for sophisticated analysis.
  * **SciTools Understand**:
      * Provides a code-search database based on **Entities** (anything in code like a file, class, variable) and **References** (a specific place where an entity appears, defining a relationship).
      * A **Kind Filter** is a string used to filter lists (e.g., `db->ents("public method")`).
      * The Python API allows querying this database to analyze code structure.
      * Example Query: List the file and line where each function is defined.
        ```python
        import understand
        db = understand.open("test.udb")
        ents = db.ents("function ~unknown ~unresolved")
        for ent in sorted(ents, key=lambda ent: ent.longname()):
            ref = ent.ref("definein");
            if ref is not None:
                print (ent.longname(), "(", ent.parameters(), ")");
                print (" ", ref.file().relname(), "(", ref.line(), ")");
        ```
  * **Open Understand**: An open-source implementation of the SciTools Understand Python API.

-----

## Summary

  * Semantic checks ensure the correct usage of variables, objects, expressions, statements, functions, and labels in the program.
  * **Scope semantic checks** ensure that identifiers are correctly used within the scope of their declaration.
  * **Type semantic checks** ensure the type consistency of various constructs in the program.
  * **Symbol tables**: a data structure for storing information about symbols in the program.
      * Used in semantic analysis and subsequent compiler stages.
      * Used in program analysis for code query.

-----

## References

  * Aho, Alfred V., Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman (2006). Compilers: Principles, Techniques, and Tools (2nd Edition).
  * Hagberg, Aric A., Daniel A. Schult and Pieter J. Swart (2008). “Exploring Network Structure, Dynamics, and Function using NetworkX”.
  * Leicht, E. A. and M. E. J. Newman (mar. de 2008). “Community Structure in Directed Networks”.
  * Mitchell, Brian S. and Spiros Mancoridis (mar. de 2006). “On the Automatic Modularization of Software Systems Using the Bunch Tool”.
  * Parr, T. (2009). Language Implementation Patterns: Create Your Own Domain-Specific and General Programming Languages.
  * SciTools (2020). Understand.
  * Tsantalis, Nikolaos and Alexander Chatzigeorgiou (2009). “Identification of Move Method Refactoring Opportunities”.
  * Zafeiris, Vassilis E., Sotiris H. Poulias, N.A. Diamantidis and E.A. Giakoumakis (2017). “Automated refactoring of super-class method invocations to the Template Method design pattern”.