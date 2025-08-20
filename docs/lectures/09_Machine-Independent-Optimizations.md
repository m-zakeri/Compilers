# Lecture 9: Machine-Independent Optimizations

------------------------------------------------------------------------

## Outline

1.  **Optimization Goals and Scopes**
2.  **Common Optimizations**
3.  **Optimization Implementation on Control Flow Graphs (CFGs)**
4.  ## Space Optimization
   - **Three-Address Code Optimization in ANTLR**
5.  **Summary of Lecture 9**

------------------------------------------------------------------------

## 1. Optimization Goals and Scopes
<img width="1618" height="1017" alt="image" src="https://github.com/user-attachments/assets/f2dc1fde-de56-4aaa-848c-9223c5ed4d82" />


### What is Code Optimization?

-   Code optimization (sometimes called *program improvement*) refers to
    transforming intermediate code into a more efficient version while
    preserving the program's semantics.
-   **Objectives:**
    -   **Execution Time:** Reduce the number of cycles, memory access,
        or pipeline stalls.
    -   **Memory Usage:** Reduce memory allocation, variable lifetime,
        and redundant temporaries.
    -   **Power Usage:** Particularly important in embedded systems and
        mobile devices.

### When to Optimize?

-   **On AST (Abstract Syntax Tree):** Machine-independent but too
    high-level.
-   **On Assembly Code:** Exposes machine details but requires
    reimplementation for each architecture.
-   **On Intermediate Representation (IR):** Ideal
    balance---machine-independent yet low-level enough for powerful
    optimizations.
### Types of compiler optimizations

 ## Different kinds (Aho et al., 2006):
-   **∙ Space optimizations**: reduce memory use,
-   **∙ Time optimizations**: reduce execution time,
-   **. Power optimization**: reduce power usage,
### Levels of Optimization

-   **Local Optimizations:** Applied within a single basic block.
    Example: constant folding inside one block.
-   **Global Optimizations:** Apply across multiple basic blocks (entire
    control flow graph).
-   **Interprocedural Optimizations:** Apply across procedure/method
    boundaries (function inlining, interprocedural constant
    propagation).
### Why optimize?
-∙ Programmers may write suboptimal code to make it clearer,
-∙ Many programmers cannot recognize ways to improve the efficiency,
- ∙ High-level language may make some optimizations inconvenient or impossible to express.
### Examples from Universities

-   **MIT 6.035 -- Loop Optimizations:** Example of loop unrolling for
    time vs. space tradeoff.\
    🔗 [MIT Lecture 7 Slides
    (PDF)](https://ocw.mit.edu/courses/6-035-computer-language-engineering-spring-2010/resources/mit6_035s10_lec07/)

-   **Stanford CS143 -- Local vs. Global Optimization:** Example showing
    difference between optimization inside a basic block vs. across
    CFG.\
    🔗 [Stanford CS143 Lecture Notes on Optimizations
    (PDF)](https://web.stanford.edu/class/cs143/lectures/optimizations.pdf)

------------------------------------------------------------------------
### Compromising between space and time in optimization
- ∙ **Usual goal**: improve time performance
- ∙ **Problem**: many optimizations tradeoff space versus time.
##   Loop unrolling increases code space, speeds up one loop.
- 1 Frequently-executed code with long loops: Preferably unroll the loop.
   -  Optimize code execution time at expense of space.
- 2 Infrequently-executed code: Preferably do not unroll the loop.
-  Optimize code space at expense of execution time.
-  Save instruction cache space.
## 2. Common Optimizations
-1 Common Subexpression Elimination
-2 Constant Propagation
-3 Constant Folding
-4 Algebraic Simplification
-5 Copy Propagation
-6 Unreachable Code Elimination
-7 Dead Code Elimination
-8 Function Inlining
-9 Loop-invariant Code Motion
-10 Strength Reduction

### Classical Optimizations

1.  **Common Subexpression Elimination (CSE)**
   - ∙ Uses DAG to compute common subexpressions.
   - ∙ Example: a := (b * (-c)) + (b * (-c))

   <img width="1461" height="454" alt="image" src="https://github.com/user-attachments/assets/44e9462a-3d9b-446a-8770-856a6f608297" />

2.  **Constant Propagation**
    - If value of variable is known to be a constant, replace use of variable with constant.
    - Value of variable must be propagated forward from point of assignment.
      <img width="758" height="759" alt="image" src="https://github.com/user-attachments/assets/1a5adfc1-eed0-4209-9895-02ebc7748e8d" />

3.  **Constant Folding**
   - If operands are known at compile time, evaluate at compile time when possible.
     -∙ float x = 2.1 * 2; --> float x = 4.2;
   - Useful at every stage of compilation.
   - Constant expressions are created by translation and by optimization.
     <img width="1448" height="431" alt="image" src="https://github.com/user-attachments/assets/f489b960-7b81-42d3-8646-6ce8073192c4" />

4.  **Algebraic Simplification**
    -   ∙ More general form of constant folding: take advantage of
        <img width="1425" height="816" alt="image" src="https://github.com/user-attachments/assets/dcf75522-5801-4f0d-acfe-baa62b02aeb6" />

simplification rules
5.  **Copy Propagation**
- ∙ Like constant propagation, instead of constant a variable is used.
- ∙ After assignment x = y, replace subsequent uses of x with y.
- ∙ Replace until x is assigned again.
- ∙ May make x a dead variable, result in dead code
  <img width="1418" height="292" alt="image" src="https://github.com/user-attachments/assets/178ee743-0fc0-47e5-a283-bd640857fc84" />

6.  **Dead Code Elimination (DCE)**
    -   If effect of a statement is never observed, eliminate the statement:

    -   Example:

            x = y-1 ;
            y=5;
            x=z+1;
           finally:
            y=5;
            x=z+1;
- ∙ Variable is dead if value is never used after definition.
- ∙ Eliminate assignments to dead variables.
- ∙ Other optimizations may create dead code.
- ∙ Deadness is a data-flow property: “May this data ever arrive anywhere?”
- 
7.  **Unreachable Code Elimination**
    - Remove code that will never be executed regardless of the values of variables at run time.
    -  Reductions in code size improve cache, translation lookaside buffer (TLB) performance
      <img width="741" height="190" alt="image" src="https://github.com/user-attachments/assets/8d2e023e-c717-43dc-9112-cb392fa301a5" />
   -  Unreachability is a control-flow property: “May control ever arrive at this point?

8.  **Loop-Invariant Code Motion**
    -    If a statement or an expression does not change during loop, and has no externally-visible side effect, can move before loop.
      <img width="1035" height="851" alt="image" src="https://github.com/user-attachments/assets/77d5ed59-c52e-4d76-8379-4bd1f9be4eb6" />

        → compute `a * b` once before loop.
9.  **Strength Reduction**
   -  ∙ Replace expensive operations (*, /) by cheap ones (+, −) via dependent induction variable.∙ Induction variable: loop variable -      -  . whose value is depends linearly on the iteration number.
      <img width="984" height="690" alt="image" src="https://github.com/user-attachments/assets/a55fff00-da8a-4f72-a272-9f68ba1deb7c" />

10. **Function Inlining**
    -   Replace a function call with the body of the function:
      <img width="1234" height="240" alt="image" src="https://github.com/user-attachments/assets/062cfa3d-a02c-49c6-a0e2-418fce9f3fa3" />

    - May need to rename variables to avoid name capture:
       -  Same name happen to be in use at both the caller and inside the callee for different purposes.
    - How about recursive functions?
### Examples from Universities

-   **Berkeley CS164 -- CSE:** Example where `x = a + b; y = a + b;`
    becomes `t = a + b; x = t; y = t;`.\
    🔗 [Berkeley CS164 Lecture 20 -- Code Optimization
    (PDF)](https://inst.eecs.berkeley.edu/~cs164/sp12/lectures/lec20-code-optimization.pdf)

-   **MIT 6.035 -- Constant Folding:** Example where `4 * 1024` becomes
    `4096` at compile time.\
    🔗 [MIT Lecture 8 Slides
    (PDF)](https://ocw.mit.edu/courses/6-035-computer-language-engineering-spring-2010/resources/mit6_035s10_lec08/)

      **Stanford CS143 -- Dead Code Elimination:** Example: after
    `x = 5; x = 6;`, first assignment is dead.\
    🔗 [Stanford CS143 Assignments
    PDF](https://web.stanford.edu/class/cs143/assignments/assignment2.pdf)

------------------------------------------------------------------------

## 3. Optimization Implementation on CFGs(Control Flow Graphs)

-   Optimizations typically rely on **control flow analysis**.
-   **Control Flow Graph (CFG):**
    -   **Nodes:** Basic blocks (straight-line sequences).
    -   **Edges:** Show flow of control (branches/jumps).
- ∙ We will optimize the intermediate representation (IR) by performing multiple passes over the control flow graph (CFG).
- ∙ Each pass performs a specific, simple optimization.
- ∙ We will repeatedly apply the simple optimizations in multiple passes, until the we cannot find any further optimizations to perform.
- ∙ Collectively, the simple optimizations can combine to achieve very complex optimizations.
- ∙ Read more: Zhu, Hao and Chen, 2024

### IR optimization: Example
<img width="1207" height="779" alt="image" src="https://github.com/user-attachments/assets/45b1557d-ef4c-46b1-9cca-65241baa1d73" />
<img width="1432" height="769" alt="image" src="https://github.com/user-attachments/assets/2e4a530e-eb3c-46cb-b7ee-7eaf936f64a0" />
<img width="1451" height="758" alt="image" src="https://github.com/user-attachments/assets/2fd454aa-90da-473c-8079-6a195fb47166" />
<img width="1437" height="853" alt="image" src="https://github.com/user-attachments/assets/cc29c317-70a5-4470-b4da-9a6187f5d9c4" />
<img width="1390" height="498" alt="image" src="https://github.com/user-attachments/assets/2b5d8299-69c0-4564-a312-de7f72e7294e" />
<img width="1496" height="881" alt="image" src="https://github.com/user-attachments/assets/7c9e332a-5d7c-4f18-97fe-5e42b892f27e" />



### Examples from Universities

-   **MIT 6.035 -- Control Flow Analysis:** Example of *live variable
    analysis* performed on a CFG.\
    🔗 [MIT Lecture 9 Notes
    (PDF)](https://ocw.mit.edu/courses/6-035-computer-language-engineering-spring-2010/resources/mit6_035s10_lec09/)

-   **Berkeley CS164 -- Loop Invariant Code Motion:** Example moving
    invariant code outside the loop in a CFG.\
    🔗 [Berkeley CS164 Lecture 20 -- Code Optimization
    (PDF)](https://inst.eecs.berkeley.edu/~cs164/sp12/lectures/lec20-code-optimization.pdf)

-   **Stanford CS143 -- Reaching Definitions:** Example of definitions
    propagating across basic blocks used for CSE and DCE.\
    🔗 [Stanford CS143 Lecture Notes on Dataflow
    (PDF)](https://web.stanford.edu/class/cs143/lectures/dataflow.pdf)

------------------------------------------------------------------------

## 4. Space Optimization

-   **Trade-off between time and space**:
    -   Faster code may use more memory.
    -   Smaller code may execute more slowly.

### Loop Unrolling Example

-   Original:

``` c
for (i=0; i<4; i++) {
   A[i] = A[i] + 1;
}
```

-   Unrolled:

``` c
A[0] = A[0] + 1;
A[1] = A[1] + 1;
A[2] = A[2] + 1;
A[3] = A[3] + 1;
```

-   Faster (less loop overhead), but larger code.

**Reference:** [MIT 6.035: Space-Time
Tradeoffs](https://web.mit.edu/6.035/www/)

------------------------------------------------------------------------

## 5. Three-Address Code Optimization in ANTLR

- ∙ Using ANTLR (Parr, 2013; Parr, 2009) for syntax-directe translation:
- ∙ Semantic rules to perform type checking.
- ∙ Semantic routines (actions) to generate intermediat representation with minimum number of ’temp’ variables.
- ∙ The implementation is available on https://github.com/mzakeri/Compilers/blob/master/grammars/AssignmentStatement4.g4

### Three address code optimized for expression ii

- /*
- * - Reference: https://github.com/m-zakeri/Compilers/blob/master
-/grammars/AssignmentStatement4.g4
- */
- 5
-grammar AssignmentStatement4;
- 7
-@parser::members{
- temp_counter = 0
-
- def create_temp(self):
- self.temp_counter += 1
- return ’T’ + str(self.temp_counter)
-
- def remove_temp(self):
   self.temp_counter -= 1

- def get_temp(self):
- return ’T’ + str(self.temp_counter)
-
- def is_temp(self, var:str):
- if var[0] == ’T’:
- return True
- return False
- }
-
-
- start returns [value_attr = str(), type_attr = str()]: p=prog
- {$value_attr=$p.value_attr
- $type_attr = $p.type_attr
- print(’Parsing was done!’)
- };
-
- prog returns [value_attr = str(), type_attr = str()]: prog a=
- assign | a=assign {$value_attr=$a.value_attr
- $type_attr = $a.type_attr
- print(’----------’)
- };
-
- assign returns [value_attr = str(), type_attr = str()]: ID ’:=’
- e=expr (NEWLINE | EOF) {$value_attr=$e.value_attr
- $type_attr = $e.type_attr
- print(’Assignment value:’, $ID.text, ’=’, $e.value_attr)
- print(’Assignment type:’, $e.type_attr)
- };
-
- expr returns [value_attr = str(), type_attr = str()]:
- e=expr ’+’ t=term {
- if $e.type_attr != $t.type_attr:
- print(’Semantic error4 in "+" operator: Inconsistent types!’)
- else:
- $type_attr = $t.type_attr
- if $t.type_attr==’float’:
- $value_attr = str(float($e.value_attr) + float($t.value_attr))
- print($value_attr, ’ = ’, $e.value_attr, ’ + ’, $t.value_attr)
-elif $t.type_attr==’int’:
- $value_attr = str(int($e.value_attr) + int($t.value_attr))
- print($value_attr, ’ = ’, $e.value_attr, ’ + ’, $t.value_attr)
 - elif $t.type_attr==’str’:
- if self.is_temp($e.value_attr):
- $value_attr = $e.value_attr
- if self.is_temp($t.value_attr):
- self.remove_temp()
- elif self.is_temp($t.value_attr):

- $value_attr = $t.value_attr
- else:
- $value_attr = self.create_temp()
- print($value_attr, ’ = ’, $e.value_attr, ’ + ’, $t.value_attr)
- }
-
- | e=expr ’-’ t=term {
- if $e.type_attr != $t.type_attr:
- print(’Semantic error3 in "-" operator: Inconsistent types!’)
- else:
- $type_attr = $t.type_attr
- if $t.type_attr==’float’:
- $value_attr = str(float($e.value_attr) - float($t.value_attr))
- print($value_attr, ’ = ’, $e.value_attr, ’ - ’, $t.value_attr)

- elif $t.type_attr == ’int’:
- $value_attr = str(int($e.value_attr) - int($t.value_attr))
- print($value_attr, ’ = ’, $e.value_attr, ’ - ’, $t.value_attr)
- elif $t.type_attr==’str’:
- if self.is_temp($e.value_attr):
- $value_attr = $e.value_attr
- if self.is_temp($t.value_attr):
- self.remove_temp()
- elif self.is_temp($t.value_attr):
- $value_attr = $t.value_attr
- else:
- $value_attr = self.create_temp()
- print($value_attr, ’ = ’, $e.value_attr, ’ - ’, $t.value_attr)
-
-
-
-| expr RELOP term
-
- | t=term {$type_attr = $t.type_attr
- $value_attr = $t.value_attr };
-
-
-
- term returns [value_attr = str(), type_attr = str()]:
- t=term ’*’ f=factor {
- if $t.type_attr != $f.type_attr:
- print(’Semantic error2 in "*" operator: Inconsistent types!’)
- else:
- $type_attr = $f.type_attr
- if $f.type_attr==’float’:
- $value_attr = str(float($t.value_attr) * float($f.value_attr))
- print($value_attr, ’ = ’, $t.value_attr, ’ * ’, $f.value_attr)
- elif $f.type_attr==’int’:
- $value_attr = str(int($t.value_attr) * int($f.value_attr))
-print($value_attr, ’ = ’, $t.value_attr, ’ * ’, $f.value_attr)
- elif $f.type_attr==’str’:
- if self.is_temp($t.value_attr):
- $value_attr = $t.value_attr
- if self.is_temp($f.value_attr):
- self.remove_temp()
- elif self.is_temp($f.value_attr):
- $value_attr = $f.value_att
- else:
- $value_attr = self.create_temp()
- print($value_attr, ’ = ’, $t.value_attr, ’ * ’, $f. value_attr) }
-
- | t=term ’/’ f=factor {
- if $t.type_attr != $f.type_attr:
- print(’Semantic error1 in "/" operator: Inconsistent types!’)
- else:
- $type_attr = $f.type_attr
-if $f.type_attr==’float’:
 $value_attr = str(float($t.value_attr) / float($f.value_attr))
 print($value_attr, ’ = ’, $t.value_attr, ’ / ’, $f.value_attr)
- elif $f.type_attr==’int’:
- $value_attr = str(int(int($t.value_attr) / int($f.value_attr)))
- print($value_attr, ’ = ’, $t.value_attr, ’ / ’, $f.value_attr)
 elif $f.type_attr==’str’:
- if self.is_temp($t.value_attr):
- $value_attr = $t.value_attr
- if self.is_temp($f.value_attr):
- self.remove_temp()
- elif self.is_temp($f.value_attr):
- $value_attr = $f.value_attr
- else:
- $value_attr = self.create_temp()
- print($value_attr, ’ = ’, $t.value_attr, ’ / ’, $f.value_attr)
- }
-
- | f=factor {$type_attr = $f.type_attr
- $value_attr = $f.value_attr
- }
- ;
-
-
- factor returns [value_attr = str(), type_attr = str()]:
- ’(’ e=expr ’)’ {$type_attr = $e.type_attr
- $value_attr = $e.value_attr
- }
-
- | ID {$type_attr = ’str’
- $value_attr = $ID.text
- }
-
- | n=number {$type_attr = $n.type_attr
- $value_attr = $n.value_attr
- }
- ;
-
-
- number returns [value_attr = str(), type_attr = str()]:
- INT {$value_attr = $INT.text
- $type_attr = ’int’
- }
- |FLOAT {$value_attr = $FLOAT.text
- $type_attr = ’float’
- }
- ;
-
- /* Lexical Rules */
- INT: DIGIT+ ;
-
- FLOAT:
- DIGIT+ ’.’ DIGIT*
- | ’.’ DIGIT+ ;
-
- String:
- ’"’ (ESC|.)*? ’"’
- ;
-
- ID:
- LETTER(LETTER|DIGIT)* ;
-
- RELOP: ’<=’ | ’<’ ;
-
- fragment
- DIGIT: [0-9] ;
- fragment
-LETTER: [a-zA-Z] ;
- fragment
- ESC: ’\\"’ | ’\\\\’ ;
- 
- WS: [ \t\r]+ -> skip ;
- NEWLINE: ’\n’;


**Reference:** [The Definitive ANTLR 4 Reference -- Terence
Parr](https://pragprog.com/titles/tpantlr2/the-definitive-antlr-4-reference/)

------------------------------------------------------------------------

## 6. Summary of Lecture 9

-   Optimizations improve **time, space, and power usage**.
-   Optimizations must **preserve program semantics**.
-   Many optimizations are **machine-independent**, applied at IR level.
-   Classical optimizations: constant folding, propagation, dead code
    elimination, loop optimizations.
-   Optimizers often apply multiple passes until no further improvement
    is possible.
-   Optimization phase is the **largest and most complex part** of
    modern compilers.

------------------------------------------------------------------------

## References

-   [Compilers: Principles, Techniques, and Tools (Dragon Book, 2nd
    Ed.)](http://infolab.stanford.edu/~ullman/dragon/errata.html) --
    Aho, Lam, Sethi, Ullman (Stanford/Princeton)
-   [Engineering a Compiler, 2nd
    Ed.](https://www.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-088478-0)
    -- Keith Cooper, Linda Torczon (Rice University)
-   [MIT 6.035: Computer Language Engineering
    (Compilers)](https://web.mit.edu/6.035/www/)
-   [Stanford CS143: Compilers
    Course](https://web.stanford.edu/class/cs143/)
-   [UC Berkeley CS164: Programming Languages and
    Compilers](https://inst.eecs.berkeley.edu/~cs164/)
-   [The Definitive ANTLR 4 Reference (Terence
    Parr)](https://pragprog.com/titles/tpantlr2/the-definitive-antlr-4-reference/)
-   [Compiler Autotuning through Multiple-phase Learning -- ACM
    2024](https://doi.org/10.1145/3640330)
