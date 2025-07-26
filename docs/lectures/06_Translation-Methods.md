# Lecture 6: Translation Methods
-----

## Outline

1.  **Syntax-directed translation and model-driven translation**
2.  **Syntax-Directed Definitions**
      * Inherited and synthesized attributes
3.  **Evaluation Orders for SDD's**
      * S-Attributed and L-Attributed SDDs
4.  **Applications of SDD**
5.  **Syntax-Directed Translation Schemes**
      * Postfix SDT's
      * Non-postfix SDT's
6.  **Model-Driven Translation**
      * Visitor mechanism
      * Listener mechanism
      * Exercises
7.  **Summary of Lecture 6**

-----
## Toward transforming everything

<img src="../pictures/lecture06_1.jpg" width="600"/>

-----
## 1\. Syntax-directed translation and model-drived translation


### Overview

We will explore two primary translation methods used in computer languages and compilers:

1.  **Syntax-directed translation**
2.  **Model-driven translation**

    * A **syntax-directed translator** reads input and immediately emits output as it goes.

    * A **model-driven translator** creates a **parse tree** or **syntax tree** input model and then walks it to generate output. Everything centers around an input model created by the parser.

<img src="../pictures/lecture06_2.jpg" width="600"/>


### Syntax-directed translation

  *  Syntax-directed translation is more efficient than model-driven translation.
  *  It augments the parser code of the grammar with application domain codes in a messy way.
  * **Limitations**:
      * It has no opportunity to analyze an input model, which is typically required for complex translations.
      * Syntax-directed translators also break down when the order of input and output constructs differs significantly.

### Model-driven translation

  * The only difference between this and a syntax-directed translator is that we generate text while walking a tree instead of while parsing a token stream.
  *  Model-driven translation is less efficient than syntax-directed translation.
  * **Advantages**:
      * Sequestering specific actions from parser code in a separate tree walker lets us reuse the parser for other tasks.
      * We can do more advanced analysis before generating output.

### Translation Methods Taxonomy
<img src="../pictures/lecture06_3.jpg" width="600"/>


-----
## 2\. Syntax-Directed Definitions (SDD)

A Syntax-Directed Definition (SDD) is a context-free grammar augmented with attributes and rules. Attributes are linked to grammar symbols, while rules are associated with productions. An SDD defines the values of attributes by linking semantic rules to grammar productions.

**Example: Infix-to-Postfix Translator**

| PRODUCTION | SEMANTIC RULE |
| :--- | :--- |
| E -> E1 + T | E.code = E1.code \|\| T.code \|\| '+' |

In this example:

  * Both E and T possess a string-valued attribute named code.
  * The semantic rule dictates that the string E.code is created by concatenating E1.code, T.code, and the character +.
  * Directly manipulating strings this way can be inefficient.

### Syntax-Directed Translation Schemes (SDT)

An SDT embeds program fragments, known as semantic actions, within the bodies of productions.

E -> E1 + T {print('+')}

Key points:

  * **Semantic actions** are conventionally enclosed in curly braces.
  * The placement of a **semantic action** within a production body dictates its execution order. In the example above, the action is executed at the end.
  * Semantic actions can be positioned anywhere within a production body.

### Comparing SDD and SDT

  * An SDT is similar to an SDD, but it explicitly defines the **evaluation order** of semantic rules.
  * SDDs are often more readable and better suited for specifications.
  * SDTs can be more efficient, making them preferable for implementations.
  * In practice, SDDs may have limited side effects, such as printing results or symbol table interactions. An SDD with no side effects is also known as an **attribute grammar**.

### Implementing SDD and SDT

  * Attributes of a symbol X can be implemented as data fields in the records representing the nodes for X.
  * A general approach to syntax-directed translation involves:
    1.  Building a parse tree or a syntax tree.
    2.  Computing attribute values by visiting the tree nodes in a left-to-right, depth-first order (pre-order traversal).
  * Translation can sometimes be performed during parsing without constructing an explicit tree, especially for L-attributed translations.

-----
### Inherited and Synthesized Attributes

Nonterminals can have two kinds of attributes:

  * **Synthesized Attribute**: A synthesized attribute for a nonterminal A at a parse-tree node N is determined by a semantic rule linked to the production at N (which must have A as its head). It is defined solely based on the attribute values of its children and N itself.

  * **Inherited Attribute**: An inherited attribute for a nonterminal B at a node N is defined by a semantic rule associated with the production at the parent of N (where B is a symbol in the production's body). It is defined using attribute values from N's parent, N itself, and N's siblings.

### SDD with Synthesized Attributes: Example

This example illustrates an SDD for a simple desk calculator where each nonterminal has a single synthesized attribute, val.

| PRODUCTION | SEMANTIC RULES |
| :--- | :--- |
| 1) L -> E n | L.val = E.val |
| 2) E -> E1 + T | E.val = E1.val + T.val |
| 3) E -> T | E.val = T.val |
| 4) T -> T1 * F | T.val = T1.val × F.val |
| 5) T -> F | T.val = F.val |
| 6) F -> (E) | F.val = E.val |
| 7) F -> digit | F.val = digit.lexval |

In this example:

  * Each nonterminal has a single synthesized attribute, val.
  * The semantic rules define the values of the val attributes.

### Annotated parse tree with synthesized attribute
  * A parse tree, showing the value(s) of its attribe(s) is called an **annotated parse tree**.
  * Annotated parse tree for 3*5+4n
<img src="../pictures/lecture06_4.jpg" width="600"/>


### SDD with Inherited Attributes: Example

In this example, the nonterminal T' has both an inherited attribute (inh) and a synthesized attribute (syn). In the production T -> * F T'1, the head T' inherits the left operand of *.

| PRODUCTION | SEMANTIC RULES |
| :--- | :--- |
| 1) T -> F T' | T'.inh = F.val, T.val = T'.syn |
| 2) T' -> * F T'1 | T'1.inh = T'.inh × F.val, T'.syn = T'1.syn |
| 3) T' -> ϵ | T'.syn = T'.inh |
| 4) F -> digit | F.val = digit.lexval |

In this example:

  * The nonterminal T' has both an inherited attribute (inh) and a synthesized attribute (syn).
  * The semantic rules define the values of the inh and syn attributes.

### Annotated parse tree with inherited attribute
  * **annotated parse tree** for 3*5 in top-down parsing:

<img src="../pictures/lecture06_5.jpg" width="600"/>


-----
## 3\. Evaluation Orders for SDDs

### SDD Dependency Graphs

A **dependency graph** helps determine the computation order for attribute values. It illustrates the flow of information among attribute instances in a parse tree. An edge from one attribute instance to another signifies that the first attribute's value is required to compute the second.

**Algorithm for Constructing a Dependency Graph:**

1.  For each parse-tree node labeled with a grammar symbol X, the dependency graph includes a node for each attribute of X.
2.  If a semantic rule for production p defines a synthesized attribute A.b based on X.c, an edge is drawn from X.c to A.b.
3.  If a semantic rule for production p defines an inherited attribute B.c based on X.a, an edge is drawn from X.a to B.c. The node M for X can be the **parent** or a **sibling** of the node N for B.

### SDD dependency graphs: Example
<img src="../pictures/lecture06_6.jpg" width="600"/>
<img src="../pictures/lecture06_7.jpg" width="600"/>
<img src="../pictures/lecture06_8.jpg" width="600"/>


### Ordering the Evaluation of Attributes

If a dependency graph contains an edge from node M to node N, the attribute for M must be evaluated before the attribute for N. The permissible evaluation orders are sequences of nodes `<N1, N2, ..., Nk>` where if an edge exists from Ni to Nj, then i < j. Such an ordering is known as a **topological sort** of the graph.

### Ordering the evaluation of attributes: Example
<img src="../pictures/lecture06_9.jpg" width="600"/>


### S-Attributed and L-Attributed SDDs

### S-Attributed Definitions

  * An SDD that exclusively uses synthesized attributes is called **S-attributed**.
  * The attributes in an S-attributed SDD can be evaluated in any **bottom-up order** of the parse tree nodes. A postorder traversal is a common method for this.
  * S-attributed definitions can be implemented during bottom-up parsing, as this process corresponds to a postorder traversal.

### L-Attributed Definitions

  * In **L-attributed definitions**, dependency-graph edges can only flow from left to right.
  * This structure allows attributes to be evaluated in a single left-to-right pass, making them ideal for single-pass compilers.
  * Each attribute must be either:
      * Synthesized.
      * Inherited, but with a restriction: for a production A -> X1X2...Xn, an inherited attribute Xi.a can only depend on:
          * Inherited attributes of the head A.
          * Attributes of the symbols to its left (X1, ..., Xi-1).
          * Attributes of Xi itself, without creating cycles in the dependency graph.

### L-attributed definitions: Example
<img src="../pictures/lecture06_10.jpg" width="600"/>


-----
## 4\. Applications of SDD

### Construction of Syntax Trees for Bottom-Up Parsing

An S-attributed definition can be used to construct syntax trees for a simple expression grammar.

| PRODUCTION | SEMANTIC RULES |
| :--- | :--- |
| 1) E -> E1 + T | E.node = new Node('+', E1.node, T.node) |
| 2) E -> E1 - T | E.node = new Node('-', E1.node, T.node) |
| 3) E -> T | E.node = T.node |
| 4) T -> (E) | T.node = E.node |
| 5) T -> id | T.node = new Leaf(id, id.entry) |
| 6) T -> num | T.node = new Leaf(num, num.val) |

For the input a - 4 + c, the syntax tree construction steps during a bottom-up parse would be:

1.  p1 = new Leaf(id, 'a');
2.  p2 = new Leaf(num, 4);
3.  p3 = new Node('-', p1, p2);
4.  p4 = new Leaf(id, 'c');
5.  p5 = new Node('+', p3, p4);

<img src="../pictures/lecture06_11.jpg" width="600"/>

### Construction of Syntax Trees for Top-Down Parsing

An L-attributed definition can achieve the same syntax tree translation as the S-attributed one.

| PRODUCTION | SEMANTIC RULES |
| :--- | :--- |
| 1) E -> T E' | E.node = E'.syn, E'.inh = T.node |
| 2) E' -> + T E'1 | E'1.inh = new Node('+', E'.inh, T.node), E'.syn = E'1.syn |
| 3) E' -> - T E'1 | E'1.inh = new Node('-', E'.inh, T.node), E'.syn = E'1.syn |
| 4) E' -> ϵ | E'.syn = E'.inh |
| 5) T -> (E) | T.node = E.node |
| 6) T -> id | T.node = new Leaf(id, id.entry) |
| 7) T -> num | T.node = new Leaf(num, num.val) |

-----
## 5\. Syntax-Directed Translation Schemes (SDT)
  * Syntax-directed translation schemes (SDTs) are a
 complementary notation to syntax-directed definitions (SDDs).
  *  Weuse SDT’s to implement two important classes of SDD’s
 efficiently (during parsing):

    1. The underlying grammar is LR-parsable, and the SDD is
    S-attributed.
    2. The underlying grammar is LL-parsable, and the SDD is
    L-attributed.

  * In SDT, an action may be placed at any position within the
 body of a production.

**Definition:**
 Postfix translation schemes: SDT’s with all actions at the right
 ends of the production bodies are called postfix SDT’s. 

### Implementing SDTs
Any SDT can be implemented as follows:

1.  Ignoring the actions, parse the input and produce a parse
 tree as a result.
2.  Examine each interior node N, say one for production A → α.
 Add additional children to N for the actions in α, so the
 children of N from left to right have exactly the symbols and
 actions of α.
3.  Perform a preorder traversal of the tree, and as soon as a
 node labeled by an action is visited, perform or execute that
 action.

### Postfix SDT's

  * Postfix SDT’s can be implemented during LR parsing by
 executing the actions when reductions occur.
  * To do this, the attribute(s) of each grammar symbol must
 be put on the stack in a place where they can be found during
 the reduction.
  * The best plan is to place the attributes along with the
 grammar symbols (or the LR states that represent these
 symbols) in records on the stack itself.

**Example:**

<img src="../pictures/lecture06_12.jpg" width="600"/>

<img src="../pictures/lecture06_13.jpg" width="600"/>

### Non-postfix SDT's


**SDT's with actions inside productions**

  * We converted S-attributed SDD’s into postfix SDT’s, with
 actions at the right ends of productions.
  * As long as the underlying grammar is LR, postfix SDT’s can be
 parsed and translated bottom-up.
  * We now consider SDT’s for the more general case of an
 L-attributed SDD assuming that the underlying grammar can
 be parsed top-down.
  * With any grammar, the technique below can be implemented
 by attaching actions to a parse tree and executing them during
 preorder traversal of the tree.


**SDT's for L-attributed definitions**

  * The rules for turning an L-attributed SDD into an SDT are as
 follows:
 
    1. Embed the action that computes the inherited attributes for
 a nonterminal A immediately before that occurrence of A in
 the body of the production. If several inherited attributes for A
 depend on one another in an acyclic fashion, order the
 evaluation of attributes so that those needed first are
 computed first.
    2. Place the actions that compute a synthesized attribute for
 the head of a production at the end of the body of that
 production.
    3. Treat actions as dummy nonterminals, and then variables can
 be treated as the synthesized attributes of dummy
 nonterminals.

**Implementationof SDT’s for L-attributed SDD’s**

  * During top-down parsing, semantic actions for inherited
 attributes can be executed while descending into the parse
 tree.
  * Synthesized attributes are calculated while returning up the
 tree, ensuring that the semantic analysis does not require
 revisiting nodes.
  * We discuss the following methods for translation L-attributed
 SDD’s during (recursive-descent) parsing:
 
    1. Use a recursive-descent parser with one function for each
 nonterminal. The function for nonterminal A receives the
 inherited attributes of A as arguments and returns the
 synthesized attributes of A.
    2. Generate code-on-the-fly, using a recursive-descent parser.


**L-Attributed SDD's and LL Parsing**

  * Suppose that an L-attributed SDD is based on an LL-grammar
 and that we have converted it to an SDT with actions
 embedded in the productions.
  * Wecan perform the translation during LL parsing by extending
 the parser stack to hold actions and certain data items needed
 for attribute evaluation.
  * To implement an SDT in conjunction with an LL-parser
 the attributes are kept on the parsing stack, and the rules
 fetch the needed attributes from known locations on the stack.

  * We use the following two principles to manage attributes on
 the stack:

    1. The inherited attributes of a nonterminal A are placed in the
 stack record that represents that nonterminal.
      * The code to evaluate these attributes will usually be represented
 by an action-record immediately above the stack record for A.
      * in fact, the conversion of L-attributed SDD’s to SDT’s ensures
 that the action-record will be immediately above A.
    2. The synthesized attributes for a nonterminal A are placed in a
 separate synthesize-record that is immediately below the
 record for A on the stack.

  * Action-records contain pointers to code to be executed.
 Actions may also appear in synthesize-records.
  * (Refer to Aho et al., 2006, Section 5.5.3)



**L-Attributed SDD's and LR Parsing**

  * So far, we saw that every S-attributed SDD on an LR
 grammar can be converted to a postfix SDT and then
 implemented during a bottom-up parse.
  * Also, L-attributed SDD on an LL grammar can be parsed
 top-down.
  * We also know that LL grammars are a proper subset of the
 LR grammars, and the S-attributed SDD’s are a proper subset
 of the L-attributed SDD’s.
 
So, the question is:
Can we handle L-attributed SDD’s on LR grammars?

  * The answer is: **No! We cannot** (See Aho et al., 2006, P. 348).
    * Remember: We still can build the parse tree first and then
    perform the translation, i.e., do model-driven translation.

  * We can do bottom-up every translation that we can do
 top-down.
  * More precisely, given an L-attributed SDD on an LL grammar,
 we can adapt the grammar to compute the same SDD on
 the new grammar during an LR parse.
  * Introduce into the grammar a **marker nonterminal** in place of
 each embedded action (Refer to Aho et al., 2006, Section
 5.5.4).

**Remarks**

  * Markers are **nonterminals** that derive only ϸ and that appear
 only once among all the bodies of all productions.
  * L-attributed grammars are well-suited for top-down parsing as
 they allow semantic information to be propagated and
 evaluated in a manner consistent with the left-to-right order of
 parsing.
* This makes them a natural fit for implementing
 syntax-directed translation in top-down parsers, particularly in
 the context of single-pass compilers.

-----
## 6\. Model-Driven Translation

Model-driven translation utilizes parse-tree visitors and other tree walkers for language applications like type checking and code generation. We will look at the **visitor** and **listener** mechanisms provided by ANTLR.

The primary difference between these mechanisms is that listener methods are called automatically by an ANTLR-provided walker, while visitor methods require explicit calls to traverse their children. If you forget to invoke visitor methods on a node's children, those subtrees will not be visited.

### Parse-Tree Listeners

  * ANTLR's runtime provides the ParseTreeWalker class to walk a tree and trigger calls to a listener. It performs a depth-first walk.
  * ANTLR generates a ParseTreeListener subclass for each grammar, with enter and exit methods for each rule.

### Parse-Tree Visitors

  * Visitors are useful when you need to control the tree walk yourself by explicitly calling methods to visit children.
  * To start a walk, you create a visitor implementation and call its visit() method.

### Building a Translator with a Listener

As an example, we can build a tool to generate a Java interface file from a Java class definition. This involves listening for "events" from a Java parse-tree walker. The core interface is JavaListener, which ANTLR generates automatically.

-----
## Summary

  * **Syntax-Directed Translation**: Computes values or performs actions on-the-fly during parsing without creating an explicit parse tree.
  * **Model-Driven Translation**: Computes values or performs actions after building a parse tree by walking it.
  * **Inherited and Synthesized Attributes**: SDDs use two attribute types. Synthesized attributes are computed from children's attributes, while inherited attributes are computed from the parent's and/or siblings' attributes.
  * **S-Attributed Definitions**: Contain only synthesized attributes.
  * **L-Attributed Definitions**: Can have both inherited and synthesized attributes, with restrictions on inherited attributes to ensure a left-to-right evaluation order.
  * **Dependency Graphs**: Show the flow of information between attribute instances and determine the evaluation order. Cyclic dependency graphs indicate problematic SDDs where attribute evaluation is not possible.
  * **Implementing S-Attributed SDD's**: Can be done with a postfix SDT on an LR parser stack.
  * **Implementing L-Attributed SDD's**: Can be handled by a recursive-descent parser for top-down parsable grammars.
  * **Listener and Visitor Mechanisms**: ANTLR offers two model-driven translation approaches. Listeners are event-driven, while visitors give you explicit control over the tree traversal.

-----
## Reading Assignments

1.  Read and practice Chapter 5 of the Dragon book (Aho et al., 2006).
2.  Read and practice Chapter 5 of the Engineering a Compiler book (Cooper and Torczon, 2022).
3.  Read and practice Chapter 4 of The Definitive ANTLR 4 Reference book (Parr, 2013).
4.  Read and practice Appendix 1 of Lecture 6.


-----

## References

  * Aho,Alfred V., Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman
 (2006). Compilers: Principles, Techniques, and Tools (2nd
 Edition). USA: Addison-Wesley Longman Publishing Co., Inc. ISBN:
 0321486811. URL: http://infolab.stanford.edu/
 %5C~ullman/dragon/errata.html.
 
 * Cooper, K.D. and L. Torczon (2022). Engineering a Compiler.
 Elsevier Science, Morgan Kaufmann Publishers Inc. ISBN:
 9780128154120. URL:
 https://books.google.com/books?id=WxTozgEACAAJ.

  * Cormen, T. H., C. E. Leiserson, R. L. Rivest and C. Stein (2022).
 Introduction to algorithms. 4th edition. MIT Press. ISBN:
 9780262046305. URL:
 https://mitpress.mit.edu/books/introduction
algorithms-fourth-edition.

  * Parr, T. (2009). Language Implementation Patterns: Create
 Your Own Domain-Specific and General Programming
 Languages. Pragmatic Bookshelf. ISBN: 9781680503746. URL:
 https://books.google.com/books?id=Ag9QDwAAQBAJ.
 
  * —(2013). The Definitive ANTLR 4 Reference. Pragmatic
 Bookshelf. ISBN: 9781680505009. URL:
 https://books.google.com/books?id=gA9QDwAAQBAJ.
