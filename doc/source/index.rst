.. exyapps documentation master file, created by
   sphinx-quickstart on Tue Dec 18 13:22:40 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



Welcome to exyapps's documentation!
===================================

Contents:

.. toctree::
   :maxdepth: 2


The Yapps Parser Generator System
http://theory.stanford.edu/~amitp/Yapps/
Version 2
 
Amit J. Patel
http://www-cs-students.stanford.edu/ amitp/ http://www-cs-students.stanford.edu/ amitp/


Introduction
======================================================================


Yapps (Yet Another Python Parser System) is an easy to use parser
generator that is written in Python and generates Python code. There
are several parser generator systems already available for Python,
including PyLR, kjParsing, PyBison, and mcf.pars, but I had different
goals for my parser. Yapps is simple, is easy to use, and produces
human-readable parsers. It is not the fastest or most powerful
parser. Yapps is designed to be used when regular expressions are
not enough and other parser systems are too much: situations where
you may write your own recursive descent parser.

Some unusual features of Yapps that may be of interest are:

 - Yapps produces recursive descent parsers that are readable by
   humans, as opposed to table-driven parsers that are difficult to
   read. A Yapps parser for a simple calculator looks similar to the
   one that Mark Lutz wrote by hand for Programming Python.

 - Yapps also allows for rules that accept parameters and pass
   arguments to be used while parsing subexpressions. Grammars that
   allow for arguments to be passed to subrules and for values to be
   passed back are often called attribute grammars. In many cases
   parameterized rules can be used to perform actions at parse time
   that are usually delayed until later. For example, information
   about variable declarations can be passed into the rules that parse
   a procedure body, so that undefined variables can be detected at
   parse time. The types of defined variables can be used in parsing
   as well -- for example, if the type of X is known, we can determine
   whether X(1) is an array reference or a function call.

 - Yapps grammars are fairly easy to write, although there are some
   inconveniences having to do with ELL(1) parsing that have to be
   worked around. For example, rules have to be left factored and
   rules may not be left recursive. However, neither limitation seems
   to be a problem in practice.

 - Yapps grammars look similar to the notation used in the Python
   reference manual, with operators like \*, +, \|, [], and () for
   patterns, names (tim) for rules, regular expressions ("[a-z]+")
   for tokens, and # for comments.

 - The Yapps parser generator is written as a single Python module
   with no C extensions. Yapps produces parsers that are written
   entirely in Python, and require only the Yapps run-time module
   (5k) for support.

 - Yapps's scanner is context-sensitive, picking tokens based on
   the types of the tokens accepted by the parser. This can be helpful
   when implementing certain kinds of parsers, such as for a preprocessor.

There are several disadvantages of using Yapps over another parser system:

 - Yapps parsers are ELL(1) (Extended LL(1)), which is less powerful
   than LALR (used by PyLR) or SLR (used by kjParsing), so Yapps would
   not be a good choice for parsing complex languages. For example,
   allowing both x := 5; and x; as statements is difficult because
   we must distinguish based on only one token of lookahead. Seeing
   only x, we cannot decide whether we have an assignment statement
   or an expression statement. (Note however that this kind of grammar
   can be matched with backtracking; see section F.)

 - The scanner that Yapps provides can only read from strings, not
   files, so an entire file has to be read in before scanning can
   begin. It is possible to build a custom scanner, though, so in
   cases where stream input is needed (from the console, a network,
   or a large file are examples), the Yapps parser can be given a
   custom scanner that reads from a stream instead of a string.

 - Yapps is not designed with efficiency in mind.

Yapps provides an easy to use parser generator that produces parsers
similar to what you might write by hand. It is not meant to be a
solution for all parsing problems, but instead an aid for those
times you would write a parser by hand rather than using one of the
more powerful parsing packages available.

Yapps 2.0 is easier to use than Yapps 1.0. New features include a
less restrictive input syntax, which allows mixing of sequences,
choices, terminals, and nonterminals; optional matching; the ability
to insert single-line statements into the generated parser; and
looping constructs \* and + similar to the repetitive matching
constructs in regular expressions. Unfortunately, the addition of
these constructs has made Yapps 2.0 incompatible with Yapps 1.0,
so grammars will have to be rewritten. See section ?? for tips on
changing Yapps 1.0 grammars for use with Yapps 2.0.


Examples
======================================================================

In this section are several examples that show the use of Yapps.
First, an introduction shows how to construct grammars and write
them in Yapps form. This example can be skipped by someone familiar
with grammars and parsing. Next is a Lisp expression grammar that
produces a parse tree as output. This example demonstrates the use
of tokens and rules, as well as returning values from rules. The
third example is a expression evaluation grammar that evaluates
during parsing (instead of producing a parse tree).

Introduction to Grammars
-------------------------------------------------------------------------------

A grammar for a natural language specifies how words can be put
together to form large structures, such as phrases and sentences.
A grammar for a computer language is similar in that it specifies
how small components (called tokens) can be put together to form
larger structures. In this section we will write a grammar for a
tiny subset of English.

Simple English sentences can be described as being a noun phrase
followed by a verb followed by a noun phrase. For example, in the
sentence, "Jack sank the blue ship," the word "Jack" is the first
noun phrase, "sank" is the verb, and "the blue ship" is the second
noun phrase. In addition we should say what a noun phrase is; for
this example we shall say that a noun phrase is an optional article
(a, an, the) followed by any number of adjectives followed by a
noun. The tokens in our language are the articles, nouns, verbs,
and adjectives. The rules in our language will tell us how to combine
the tokens together to form lists of adjectives, noun phrases, and
sentences: ::

    sentence: noun_phrase verb noun_phrase
    noun_phrase: [article] adjective* noun 

Notice that some things that we said easily in English, such as
"optional article" are expressed using special syntax, such as
brackets. When we said, "any number of adjectives," we wrote
adjective\*, where the \* means "zero or more of the preceding
pattern".

The grammar given above is close to a Yapps grammar. We also have
to specify what the tokens are, and what to do when a pattern is
matched. For this example, we will do nothing when patterns are
matched; the next example will explain how to perform match actions. ::

  parser TinyEnglish:
    ignore:          "\\W+"
    token noun:      "(Jack|spam|ship)"
    token verb:      "(sank|threw)"
    token article:   "(a|an|the)"
    token adjective: "(blue|red|green)"
  
    rule sentence:       noun_phrase verb noun_phrase
    rule noun_phrase:    [article] adjective* noun

The tokens are specified as Python regular expressions. Since Yapps
produces Python code, you can write any regular expression that
would be accepted by Python. (Note: These are Python 1.5 regular
expressions from the re module, not Python 1.4 regular expressions
from the regex module.) In addition to tokens that you want to see
(which are given names), you can also specify tokens to ignore,
marked by the ignore keyword. In this parser we want to ignore
whitespace.

The TinyEnglish grammar shows how you define tokens and rules, but
it does not specify what should happen once we've matched the rules.
In the next example, we will take a grammar and produce a parse
tree from it.


Lisp Expressions
---------------------------------------------------------------------

Lisp syntax, although hated by many, has a redeeming quality: it
is simple to parse. In this section we will construct a Yapps grammar
to parse Lisp expressions and produce a parse tree as output.

Defining the Grammar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The syntax of Lisp is simple. It has expressions, which are
identifiers, strings, numbers, and lists. A list is a left parenthesis
followed by some number of expressions (separated by spaces) followed
by a right parenthesis. For example, 5, "ni", and (print "1+2 = "
(+ 1 2)) are Lisp expressions. Written as a grammar, ::

    expr:   ID | STR | NUM | list
    list:   ( expr* )  

In addition to having a grammar, we need to specify what to do every
time something is matched. For the tokens, which are strings, we
just want to get the "value" of the token, attach its type (identifier,
string, or number) in some way, and return it. For the lists, we
want to construct and return a Python list.

Once some pattern is matched, we enclose a return statement enclosed
in {{...}}. The braces allow us to insert any one-line statement
into the parser. Within this statement, we can refer to the values
returned by matching each part of the rule. After matching a token
such as ID, "ID" will be bound to the text of the matched token.
Let's take a look at the rule: ::

    rule expr: ID   {{ return ('id', ID) }}
      ...

In a rule, tokens return the text that was matched. For identifiers,
we just return the identifier, along with a "tag" telling us that
this is an identifier and not a string or some other value. Sometimes
we may need to convert this text to a different form. For example,
if a string is matched, we want to remove quotes and handle special
forms like \n. If a number is matched, we want to convert it into
a number. Let's look at the return values for the other tokens: ::

      ...
             | STR  {{ return ('str', eval(STR)) }}
             | NUM  {{ return ('num', atoi(NUM)) }}
      ...

If we get a string, we want to remove the quotes and process any
special backslash codes, so we run eval on the quoted string. If
we get a number, we convert it to an integer with atoi and then
return the number along with its type tag.

For matching a list, we need to do something slightly more complicated.
If we match a Lisp list of expressions, we want to create a Python
list with those values. ::

    rule list: "\\("                 # Match the opening parenthesis
               {{ result = [] }}     # Create a Python list
               ( 
                  expr               # When we match an expression,
                  {{ result.append(expr) }}   # add it to the list
               )*                    # * means repeat this if needed
               "\\)"                 # Match the closing parenthesis
               {{ return result }}   # Return the Python list

In this rule we first match the opening parenthesis, then go into
a loop. In this loop we match expressions and add them to the list.
When there are no more expressions to match, we match the closing
parenthesis and return the resulting. Note that # is used for
comments, just as in Python.

The complete grammar is specified as follows: ::

  parser Lisp:
      ignore:      '\\s+'
      token NUM:   '[0-9]+'
      token ID:    '[-+*/!@%^&=.a-zA-Z0-9_]+' 
      token STR:   '"([^\\"]+|\\\\.)*"'
  
      rule expr:   ID     {{ return ('id', ID) }}
                 | STR    {{ return ('str', eval(STR)) }}
                 | NUM    {{ return ('num', atoi(NUM)) }}
                 | list   {{ return list }}
      rule list: "\\("    {{ result = [] }} 
                 ( expr   {{ result.append(expr) }}
                 )*  
                 "\\)"    {{ return result }} 

One thing you may have noticed is that "\\(" and "\\)" appear in
the list rule. These are inline tokens: they appear in the rules
without being given a name with the token keyword. Inline tokens
are more convenient to use, but since they do not have a name, the
text that is matched cannot be used in the return value. They are
best used for short simple patterns (usually punctuation or keywords).

Another thing to notice is that the number and identifier tokens
overlap. For example, "487" matches both NUM and ID. In Yapps, the
scanner only tries to match tokens that are acceptable to the parser.
This rule doesn't help here, since both NUM and ID can appear in
the same place in the grammar. There are two rules used to pick
tokens if more than one matches. One is that the longest match is
preferred. For example, "487x" will match as an ID (487x) rather
than as a NUM (487) followed by an ID (x). The second rule is that
if the two matches are the same length, the first one listed in the
grammar is preferred. For example, "487" will match as an NUM rather
than an ID because NUM is listed first in the grammar. Inline tokens
have preference over any tokens you have listed.

Now that our grammar is defined, we can run Yapps to produce a
parser, and then run the parser to produce a parse tree.


Running Yapps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the Yapps module is a function generate that takes an input
filename and writes a parser to another file. We can use this
function to generate the Lisp parser, which is assumed to be in
lisp.g. ::

  % python
  Python 1.5.1 (#1, Sep  3 1998, 22:51:17)  [GCC 2.7.2.3] on linux-i386
  Copyright 1991-1995 Stichting Mathematisch Centrum, Amsterdam
  >>> import yapps
  >>> yapps.generate('lisp.g')

At this point, Yapps has written a file lisp.py that contains the
parser. In that file are two classes (one scanner and one parser)
and a function (called parse) that puts things together for you.

Alternatively, we can run Yapps from the command line to generate
the parser file: ::

  % python yapps.py lisp.g

After running Yapps either from within Python or from the command
line, we can use the Lisp parser by calling the parse function. The
first parameter should be the rule we want to match, and the second
parameter should be the string to parse. ::

  >>> import lisp
  >>> lisp.parse('expr', '(+ 3 4)')
  [('id', '+'), ('num', 3), ('num', 4)]
  >>> lisp.parse('expr', '(print "3 = " (+ 1 2))')
  [('id', 'print'), ('str', '3 = '), [('id', '+'), ('num', 1), ('num', 2)]]

The parse function is not the only way to use the parser; section
5.1 describes how to access parser objects directly.

We've now gone through the steps in creating a grammar, writing a
grammar file for Yapps, producing a parser, and using the parser.
In the next example we'll see how rules can take parameters and
also how to do computations instead of just returning a parse tree.


Calculator
-------------------------------------------------------------------------------

A common example parser given in many textbooks is that for simple
expressions, with numbers, addition, subtraction, multiplication,
division, and parenthesization of subexpressions. We'll write this
example in Yapps, evaluating the expression as we parse.

Unlike yacc, Yapps does not have any way to specify precedence
rules, so we have to do it ourselves. We say that an expression is
the sum of terms, and that a term is the product of factors, and
that a factor is a number or a parenthesized expression: ::

    expr:           factor ( ("+"|"-") factor )*
    factor:         term   ( ("*"|"/") term )*
    term:           NUM | "(" expr ")"

In order to evaluate the expression as we go, we should keep along
an accumulator while evaluating the lists of terms or factors. Just
as we kept a "result" variable to build a parse tree for Lisp
expressions, we will use a variable to evaluate numerical expressions.
The full grammar is given below: ::

  parser Calculator:
      token END: "$"         # $ means end of string
      token NUM: "[0-9]+"
  
      rule goal:           expr END         {{ return expr }}
  
      # An expression is the sum and difference of factors
      rule expr:           factor           {{ v = factor }}
                         ( "[+]" factor       {{ v = v+factor }}
                         |  "-"  factor       {{ v = v-factor }}
                         )*                 {{ return v }}
  
      # A factor is the product and division of terms
      rule factor:         term             {{ v = term }}
                         ( "[*]" term         {{ v = v*term }}
                         |  "/"  term         {{ v = v/term }}
                         )*                 {{ return v }}
  
      # A term is either a number or an expression surrounded by parentheses
      rule term:           NUM              {{ return atoi(NUM) }}
                         | "\\(" expr "\\)" {{ return expr }}

The top-level rule is goal, which says that we are looking for an
expression followed by the end of the string. The END token is
needed because without it, it isn't clear when to stop parsing. For
example, the string "1+3" could be parsed either as the expression
"1" followed by the string "+3" or it could be parsed as the
expression "1+3". By requiring expressions to end with END, the
parser is forced to take "1+3".

In the two rules with repetition, the accumulator is named v. After
reading in one expression, we initialize the accumulator. Each time
through the loop, we modify the accumulator by adding, subtracting,
multiplying by, or dividing the previous accumulator by the expression
that has been parsed. At the end of the rule, we return the
accumulator.

The calculator example shows how to process lists of elements using
loops, as well as how to handle precedence of operators.

Note: It's often important to put the END token in, so put it in
unless you are sure that your grammar has some other non-ambiguous
token marking the end of the program.


Calculator with Memory
-------------------------------------------------------------------------------

In the previous example we learned how to write a calculator that
evaluates simple numerical expressions. In this section we will
extend the example to support both local and global variables.

To support global variables, we will add assignment statements to
the "goal" rule. ::

      rule goal:           expr END         {{ return expr }}
                | 'set' ID expr END         {{ global_vars[ID] = expr }}
                                            {{ return expr }}   

To use these variables, we need a new kind of terminal: ::

      rule term: ... | ID {{ return global_vars[ID] }} 

So far, these changes are straightforward. We simply have a global
dictionary global_vars that stores the variables and values, we
modify it when there is an assignment statement, and we look up
variables in it when we see a variable name.

To support local variables, we will add variable declarations to
the set of allowed expressions. ::

      rule term: ... | 'let' VAR '=' expr 'in' expr ...

This is where it becomes tricky. Local variables should be stored
in a local dictionary, not in the global one. One trick would be
to save a copy of the global dictionary, modify it, and then restore
it later. In this example we will instead use attributes to create
local information and pass it to subrules.

A rule can optionally take parameters. When we invoke the rule, we
must pass in arguments. For local variables, let's use a single
parameter, local_vars: ::

      rule expr<<local_vars>>:   ...
      rule factor<<local_vars>>: ...
      rule term<<local_vars>>:   ...

Each time we want to match expr, factor, or term, we will pass the
local variables in the current rule to the subrule. One interesting
case is when we pass as an argument something other than local_vars: ::

     rule term<<local_vars>>: ...
                  | 'let' VAR '=' expr<<local_vars>>
                    {{ local_vars = [(VAR, expr)] + local_vars }}
                    'in' expr<<local_vars>>
                    {{ return expr }}

Note that the assignment to the local variables list does not modify
the original list. This is important to keep local variables from
being seen outside the "let".

The other interesting case is when we find a variable: ::

  global_vars = {}
  
  def lookup(map, name):
      for x,v in map:  if x==name: return v
      return global_vars[name]
  %%
     ...
     rule term<<local_vars>: ...
                  | VAR {{ return lookup(local_vars, VAR) }}
  
The lookup function will search through the local variable list,
and if it cannot find the name there, it will look it up in the
global variable dictionary.

A complete grammar for this example, including a read-eval-print
loop for interacting with the calculator, can be found in the
examples subdirectory included with Yapps.

In this section we saw how to insert code before the parser. We
also saw how to use attributes to transmit local information from
one rule to its subrules.


BEGIN WITH SECTION 3 HERE


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


