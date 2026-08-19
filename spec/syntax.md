
# Bee Syntax


Next we enumerate the fundamental concepts to grasp Bee syntax. After this overview we will go in details. We use long pages you can scroll. Here are the main topics for this page:

- Comments
- Keywords
- Variables
- Expressions
- Statements
- Conditions
- Operators

We use examples and sometimes a simplified version of BNF notation to explain the syntax rules. If you do not know anything about BNF don't wary, here is a short introduction to this weird notation:

- We use suggestive descriptors for language elements,
- We use "::=" to explain a descriptor,
- We use "..." for repetitive sequences of symbols,
- We use notes to explain the semantics,
- Optional keyword is enclosed in square brackets [];

## Comments


Comments are very important part of Bee code. We have multiple conventions for making good comments for any project. Bee comments are tailored by architectural principle: "if there are no comments in the code the code is wrong."


In next example we are using various comments into a demo program.


```
#!/bin/bee
+------------------------------------------------------------------
| At the beginning of program you can have  several comments,     |
| to explain how the program works. This notation is preferred.   |
+-----------------------------------------------------------------+
rule main:
  continue; -- this statement does nothing

  ** this is a single line comment
  print ("end of line comments",    -- first argument
         "can be used to explain",  -- second argument
         "diverse arguments"        -- third argument
        );
return;
*******************************************************************
** This is the old style boxed comment, used for matrix printers **
** In Bee you can add comments/notes at the end of your code     **
*******************************************************************
```


For single line title comments we use one "#" symbol. This can be used in combination with "!" to create "shebang" comment known in scripting languages on Linux to specify interpreter location. You can use two "##" for subtitles for large code sections.


For single line comments we use two stars like this: "**";

- This comment can be extended to multiple stars to create a separator,
- You can use single line comment at beginning of new line,
- You can use two spaces to indent the comment and align with the code.

Before new line of code: (EOL) you can use comments starting with: "-- "

- notice one line may be or not a full statement. the end of statement is not (EOL),
- you can use "-- " in the middle of an expression, if expression is on multiple lines,
- you can have multiple statements separated by ";" in a line but only one comment.

Bee has a specific notation for block comments not used in any other language so far. It is a multi-line comment starting with "+-" and end with "-+". The upper right corner is missing. I guess you will notice this defect later. However you can use old-style C comments.

- Bee comments are inspired from Ada language and Wiki markdown
- Bee comments are designed for better syntax coloring

## Bee Keywords


Bee is an expressive language but it's core has about 72 reserved keywords so far:


| Table |
| --- |
| begin | alias | and | apply | abort |
| other | case | continue | done | default |
| if | is | do | else | exit |
| fail | final | miss | panic | like |
| load | next | job | match | over |
| print | pass | void | rule | return |
| fail | retry | none | scrap | type |
| read | trial | stop | yield | xor |
| write | wait | when | or | with |
| hide | new | cycle | let | set |
| while | for | resum | put | pop |
| raise | not | as | in | start |
| try | expect |  |  |  |


- You can not use these keywords as identifiers;
- Some of these keywords are reserved but not implemented;
- New keywords are going to be created for new features;

### Semantic keywords


| Table |
| --- |
| Keyword | Purpose |
| if | conditional executor for one statement block |
| is | query element or variable data type |
| as | create alias for used modules |
| or | alternative for ladder decision |
| in | alternative for belong operation |
| and | alternative for cascade decision |
| xor | alternative for logic operation |
| not | alternative for logic operation |



## Statements


Statements can start with imperative keyword or a declarative keyword:


| Table |
| --- |
| set | create a constant  
new   create a variable  
let   modify a variable  
type  create a data type 
read  accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | new | create a variable  
let   modify a variable  
type  create a data type 
read  accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | let | modify a variable  
type  create a data type 
read  accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | type | create a data type 
read  accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | read | accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | write | register in console cash a string             
print output to console with end of new line | print | output to console with end of new line |
| new | create a variable  
let   modify a variable  
type  create a data type 
read  accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | let | modify a variable  
type  create a data type 
read  accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | type | create a data type 
read  accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | read | accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | write | register in console cash a string             
print output to console with end of new line | print | output to console with end of new line |
| let | modify a variable  
type  create a data type 
read  accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | type | create a data type 
read  accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | read | accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | write | register in console cash a string             
print output to console with end of new line | print | output to console with end of new line |
| type | create a data type 
read  accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | read | accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | write | register in console cash a string             
print output to console with end of new line | print | output to console with end of new line |
| read | accept input from console into a variable     
write register in console cash a string             
print output to console with end of new line | write | register in console cash a string             
print output to console with end of new line | print | output to console with end of new line |
| write | register in console cash a string             
print output to console with end of new line | print | output to console with end of new line |
| print | output to console with end of new line |


- One statement is usually indented 2 space,
- One statement is usually described in a single line,
- Multiple statements on a single line are separated with ";",
- One expression in a statement can extend on multiple lines.

### Code blocks


Statements can be contained in blocks of code.


| Table |
| --- |
| Keyword | Block description |
| start | start local scope for do block |
| with | qualifier suppression block |
| if | first block in decision statement |
| cycle | repetitive or iterative blocks |
| match | multi-path value selector block |
| trial | exception handler block |


- Block ending keyword can be one of: { done, cycle },
- Statements in nested blocks are using indentation.

### Definition statements


Next statements are used to declare new elements in a module.


| Table |
| --- |
| Keyword | Purpose |
| use | Load module or module |
| alias | Eliminate scope qualifier |
| hide | Hiding public members from a loaded module |
| rule | Create a new business rule or prototype |
| return | End rule declaration and transfer control to caller |



### Execution statements


Next keywords are simple statements. These represents actions called imperative statements.


| Table |
| --- |
| Keyword | Purpose |
| apply | Execute a rule and ignore the result if there is one |
| begin | Commence execution of a coroutine |
| wait | Suspend current thread execution for a number of seconds |
| read | Flush the console buffer and accept user input from console |
| write | Add something to console buffer but no new line |
| print | Output expression result, variable or constant to console |
| let | Mutate variable value using an expression |
| scrap | Remove one element from its collection |



## Control statements


Control statements are used to create local blocks of code that resolve a small task synchronously. After task is finished the control is returned to the main thread.


| Table |
| --- |
| Keyword | Purpose |
| start | Create non repetitive local scope |
| if | Start a conditional branch |
| else | Start an alternative branch |
| do | Start a block of code |
| cycle | Create repetitive local scope |
| for | Create finite iterative block |
| while | Create conditional repetitive block |
| match | Value multi-path search selector |
| when | Create node for match statement |
| other | Default branch for match statement |
| trial | Start declaration region for a protected block of code |
| try | Begin the executable region in a trial statement |
| case | Associated with trial to resolve specific errors |
| miss | Default trial block, executed when there is no case |
| final | Associated with trial to finalize the trial block |



## Transfer statements


These statements execute a jump or make an interruption of current thread.


| Table |
| --- |
| Keyword | Purpose |
| panic | Create unrecoverable error code and stop current program |
| over | Silent termination of program. No error is raised in this case. |
| exit | Silently stop execution of current rule and return to the caller |
| yield | Suspend one coroutine and give control to another routine |
| rest | Suspend a routine and wait for all threads created by the routine to finish |
| stop | Interrupt execution for current cycle and continue after the cycle, | redo | Continue current cycle from the beginning making a shortcut, | next | Continue current iteration from the beginning making a shortcut, | abort | stop early a trial block | fail | Create error message and continue with next step | pass | Skip the rest and continue with next step | expect | Does nothing if condition is true, otherwise create an $unexpected exception | raise | Intrerupt a try job or trial and issue an error | retry | Repeat a trial block from the begioning | resume | Mark error as handled and continue trial | done | end a block statement | repeat | end a repetitive block |
| stop | Interrupt execution for current cycle and continue after the cycle, |
| redo | Continue current cycle from the beginning making a shortcut, |
| next | Continue current iteration from the beginning making a shortcut, |
| abort | stop early a trial block |
| fail | Create error message and continue with next step |
| pass | Skip the rest and continue with next step |
| expect | Does nothing if condition is true, otherwise create an $unexpected exception |
| raise | Intrerupt a try job or trial and issue an error |
| retry | Repeat a trial block from the begioning |
| resume | Mark error as handled and continue trial |
| done | end a block statement |
| repeat | end a repetitive block |



Bee identifiers can start with dolar ($), dot (.), underscore (_), Latin, Greek, Chyrillic. An identifier can contain numbers but can not start with a number.


In mathematics is very popular notation for angles to use Greek letters. We support in Bee a limited number of Greek an Cyrillic letters for identifiers:


```
Σ Π Δ Ξ Γ Ψ Ω ζ
α β ɣ λ π μ φ ε δ η σ ω
Б Г Д Ж И Л Ф Ц Ч Ш Э Я
```


### Subscript:


You can use a limited number of letters and numbers available in Unicode as subscript to make identifier names. You can not start an identifier with one of these symbols and you can't add other symbols that are not subscript after a subscript:


```
x₀ x₁ x₂ x₃ x₄ x₅ x₆ x₇ x₈ x₉ x₁₀
yₐ yₑ yₕ yᵢ yⱼ yₖ yₗ yₘ yₙ yₒ yₚ yᵣ yₛ yₜ yᵤ yᵥ yₓ
```


### Superscript:


Bee has support for exponent using superscript. You can make any integer exponent including negative numbers but you can not use dot or fraction in the exponent.

x⁺ x⁻ x¹ x² x³ x⁴ x⁵ x⁶ x⁷ x⁸ x⁹ x¹⁰

Note: 
Symbol (^) is exponent operator and is not required when you use superscript exponent. You can use it with expressions, constants or rational numbers to resolve the exceptional cases.
Lowercase exponent:
Identifiers that start with a lowercase Latin letter can be used as exponent. The superscript variable can start with a letter and can also use numbers.

yᵃ yᵇ yᶜ yᵈ yᵉ yᶠ yᵍ yʰ yⁱ yʲ yᵏ yᶩ 
yᵐ yⁿ yᵒ yᵖ yʳ yˢ yᵗ yᵘ yᵛ yʷ yˣ yʸ yᶻ

Uppercase exponent:
If you define a constant or variable that start with capital letter there may be some issues. You can't use all Latin letters or any Greek or Cyrilic capital letters in exponent. So your options are limited to create uppercase exponents.

zᴬ zᴮ zᴰ zᴱ zᴲ zᴳ zᵸ zᴵ zᴶ zᴷ zᴸ 
zᴹ zᴺ zᴻ zᴼ zᴾ zᴿ zᵀ zᵁ zᵂ


Caution: Observe letters: {C, F ,S ,Q} are missing. So if you define a constant that use any of these letters, you will need symbol (^) to create exponent.
Variable declarations
In Bee, all variables must be declared using an imperative statement. Variables can be dynamic or static and can have a data type. Data type can be custom or pre-defined.


type
declare custom data type


new
declare a dynamic variable


set
declare a static variable


Expressions
Expressions are created using identifiers, operators, rules and constant literals. Expressions can be anonymous or can be assigned to identifiers to create lambda expressions.
expressions ...

can use () to establish order of operations,
can be enumerated using comma separator "," in a list,
can be combined to create more complex expressions,

Examples
** expressions
print 10
print 10 + 10 + 15
print "this is a test"

** complex expressions
print (10 > 5) ∨ (2 < 3)
print -b + sqr(b² - 4·a·b)/(2·a)

** enumeration of expressions
print (1,2,3)
print (1,',',2,',',3)

Conditional Execution
A condition is a logic expression used to control statement execution. For this we use {"if", "else"} keywords at end of statements.

** conditional statement execution
statement if condition;

Note: Previous statement is executed only if the condition is True.

** alternative statement 
  expect condition else statement;

** alternative expression
  expect condition else expression;

Note: Previous statement is executed only if the condition is False.
restrictions:

Can not use "if" with set statement;
Can not use "if" with new statement;
Can not use "if" after done;

Example:

rule main:
  ** generate a random number
  new a := random(Z);

  ** conditional execution
  new b := a;
  let b := -a if a < 0;

  ** print result
  print "|b| = ", a;
return;

Operations:
Bee has support for fractions. Bee is using regular slash "/" for all fractions. You can use superscript for left and subscript for right: These two are equivalent (1/2 = ¹/₂). Unfortunately we can not support fractional power due to lower readability.

¹/₂ ¹/₃ ¹/₄ ¹/₅ ¹/₆ ¹/₇ ¹/₈ ¹/₉  ¹/₁₀ ¹/₁₀₀
x⁻¹ = 1/x, x⁻² = 1/x², x⁻³ = 1/x³ ...

Power operations have priority but we have support only for (+, -) no other operations are possible in exponent. In next expressions, (n-1) is done first before making the power operation.

-- equivalent notation
xⁿ⁻¹ = x^(n-1)
xˣ⁺¹ = x^(n+1)

-- equivalent  notation
x^(¹/₂) = √2(x)  
x^(¹/₃) = √3(x) 


Note:In expressions above () symbols are mandatory. The compiler will detect missing paranthesis and will ask for it. This will improve code readability and eliminate confusions.
Pattern Matching
Instead of ternary operator we use conditional expressions. Conditional expressions enable many choices unlike ternary operator that enable only 2 choices. Conditional expressions are also known as pattern matching expressions.
Syntax:

rule main:
  ** define a local variable
  new var ∈ type;

  ** single condition matching
  let var := (xp1 if cnd1 else xp);

  ** multiple matching with default value
  let var := (xp1 if cnd1, xp2 if cnd2,..., xp);

  ** alternative code alignment
  let var := ( xp1 if cnd1 else
               xp2 if con2 else
               xp3 if cnd3 else
               xp
              );
return;

Example:
rule main:
   new x := '0'; -- symbol
   write "x:"
   read   x;

   new kind := ("digit"  if x ∈ ['0'..'9'] else
                "letter" if x ∈ ['a'..'z'] else
                "unknown");

   print ("x is " + kind); -- expect: "x is digit"
return;

Operators
Bee operators are ASCII or Unicode symbols. One operator can be created using one or two characters. This is why Bee language is considered experimental, esoteric & disruptive.
Delimiters



Symbol
Description




+-...-+
Multi-line boxed comments


#(....)
String interpolation (placeholder) for operator "?"


(_,_,_)
Expression | List literal


[_,_,_]
Index | Array literals | Parameterize types


{_,_,_}
Enumeration type | Set of values | Hash map



Strings



symbol
description




`x`
Back quoted string: regular expression.


'x'
Single quoted string literal or ASCII code point


"y"
Double quoted string literal or UTF32 code point



Single Symbols



symbol
description




!
Negation symbol for relations | Excluded from domain


?
Template modifier. Associated with string templates


*
String replication | Varargs prefix | Spread operator | Many something


@
Domain name | Example @sagecode.net


$
System constant | Environment variables


&
String concatenation | number concatenation


#
Title | String interpolation 


∈
Define variable/constant/result/parameter type


_
Anonymous variable | Constant value = one space (_ = ' ')


+
Maximum upper limit for a domain | Unicode notation U+


-
Minimum lower limit in a domain | Unicode notation U-


:
Start a block or define something


:
Pair-up key-value in: objects, rule parameters, rule arguments, hash-map pairs


;
End of statement | Statement separator


.
Decimals for real numbers | Path string concatenation


.
Membership dot notation | Prefix for public member/attribute

,
Enumeration of elements | expressions


|
Declarative collection builder: set := { x*2 | x ∈ (0..3)}


\
Escape character ( \n := New Line), ( \" = Double Quotes)



Numeric operators
Listed in the order of precedence top down.



symbol
description




-
Change sign, replace "y = -x" with "y = -1*x"


/
Rational number division


^
Power symbol used with fractions or expressions


√
Radical: x√n is equivalent to x^(1/n)


*
Multiplication alternative


\
Rational number division


/
Real number division


×
Array multiplication | Matrix multiplication


%
Modulo operator 5 % 2 = 2


+
Numeric addition | List append | Matrix addition


-
Numeric subtraction | Collection difference


±
Numeric tolerance (use with ≈)



Double Symbols
Double symbols is a group of two ASCII symbols considered as one. Some of these symbols have an Unicode equivalent, some do not. When available, Unicode equivalent is preferred choice.



symbol
description




-- 
End of line comments (not in expression)


##
Single line subtitle comments (no indentation)


**
Single line comments (allow indentation)


..
Define range/domain/slice (n..m) | [n..m]


.!
Define range/domain with excluded limit (n.!m) | [n.!m]


!.
Define range/domain with excluded limit (n!.m) | [n.!m] 


!!
Define range/domain with excluded limits: (n!!m) | [n.!m] 


-.
Minus infinite domain: instead of [-∞..0] write: [-..0]


.+
Plus infinite domain: instead of [0..+∞] write: [0..+]


=>
Define: rule expression | rule result


<-
Define and generate values in a loop from range or set


<:
Define subset from set | Specify super-type for a new type


:>
Data cast pipeline operator / Type conversion


<<
Shift values of collection to right by removing first elements


>>
Shift values of collection to left by removing first elements


::
Deep copy | Clone operator


++
Extend an array with one or more elements


-=
Find and delete one element, from a collection

+=
Append an element in a set or a map but not in a list


+>
Append element to beginning of a list


<+
Append element to end of a list

==
Relation operator for identical (the same)

!=
Relation operator not identical (not the same)


~=
Relation operator: regular expression match


>=
Relation operator: greater then or equal to


<=
Relation operator: less then or equal to



Modifiers
Each modifier is created with pattern "x=" where x is a single symbol:



symbol
meaning




:=
Modify | (value | reference)


+=
Increment value


-=
Decrement value


*=
Multiplication modifier


/=
Real division modifier


^=
Power modifier


√=
Radical modifier


%=
Modulo modifier



Relation Operators
Relation operators are used to compare expressions.



symbol
meaning




∈
check if element belong to collection


=
equal { compare values or attributes}


≠
different { compare values or attributes}


≡
equivalent | { compare values / convert type }


≈
approximating equal numbers, used with ± like: (x ≈ 4 ± 0.25)


>
value is greater than: (2 > 1)


<
value is less than: (1 < 2)


≥
greater than or equal to


≤
less than or equal to

÷
Exact divisor: 3 &division 15 ≡ True



negation:
Operator: "!" can be used in combination with other operators:

 x != y; -- equivalent to: ¬(x = y)
 x !≡ y; -- equivalent to: ¬(x ≡ y)
 x !∈ y; -- equivalent to: ¬(x ∈ y)
 x !≈ y; -- equivalent to: ¬(x ≈ y)
 x !~ y; -- equivalent to: ¬(x ~ y)

Collection operators



symbol
result
meaning




∩
Set
Intersection between two collections


∪
Set
Union between two collections


⊂
Logic
Set is included in superset: "⊂"


⊃
Logic
Set contain subset: "⊃"


Δ
Set
Set symmetric difference


+
String
Concatenation between two strings


+
List
Concatenation between two lists


+
Array
Concatenation between two arrays


∀
Element
All: used in collection qualification


∃
Logic
One: used in collection qualification



Logic Operators
Bee is using enumeration symbols: True = 1 and False = 0



symbol
meaning
notes




¬
NOT
unary operator


∧
AND
shortcut operator


∨
OR
shortcut operator


⊕
XOR
exclusive OR


↓
NOR
p ↓ q = ¬ (p ∨ q)


↑
NAND
p ↑ q = ¬ (p ∧ q)



The table of truth



p
q
¬ p
p ⊕ q
p ∧ q
p ∨ q




1
1
0
0
1
1


1
0
0
1
0
1


0
1
1
1
0
1


0
0
1
0
0
0



Bitwise operators
Bitwise operators are processing numbers not Boolean values.



symbol
meaning
notes




«
bit SHIFTL
shift bits to left


»
bit SHIFTR
shift bits to right


~
bit NOT
negate all bits


&
bit AND
execute AND between each bits


|
bit OR
execute OR between each bits


⊕
bit XOR
execute XOR between each bits




Arity = 1



a
~ a
a « 1
a » 2



0000111100000000
1111000011100011
0111100011100001
0110100111000001

Arity = 2



aba & ba | ba ⊕ b


0000000000
0100000101
1101011110
1011101101


String operators



SymbolDescription



*string pattern repetition (right operator must be numeric)
/concatenate url or path using / not depending on OS
+concatenate two strings as they are preserving trial spaces.
-concatenate two strings and trim spaces to a single space.
.concatenate strings with "/" on Linux or "\" on Windows.
?string format operator, replace "#" with number.




Read next:
Structure


x⁺ x⁻ x¹ x² x³ x⁴ x⁵ x⁶ x⁷ x⁸ x⁹ x¹⁰

Note: 
Symbol (^) is exponent operator and is not required when you use superscript exponent. You can use it with expressions, constants or rational numbers to resolve the exceptional cases.
Lowercase exponent:
Identifiers that start with a lowercase Latin letter can be used as exponent. The superscript variable can start with a letter and can also use numbers.

yᵃ yᵇ yᶜ yᵈ yᵉ yᶠ yᵍ yʰ yⁱ yʲ yᵏ yᶩ 
yᵐ yⁿ yᵒ yᵖ yʳ yˢ yᵗ yᵘ yᵛ yʷ yˣ yʸ yᶻ

Uppercase exponent:
If you define a constant or variable that start with capital letter there may be some issues. You can't use all Latin letters or any Greek or Cyrilic capital letters in exponent. So your options are limited to create uppercase exponents.

zᴬ zᴮ zᴰ zᴱ zᴲ zᴳ zᵸ zᴵ zᴶ zᴷ zᴸ 
zᴹ zᴺ zᴻ zᴼ zᴾ zᴿ zᵀ zᵁ zᵂ


Caution: Observe letters: {C, F ,S ,Q} are missing. So if you define a constant that use any of these letters, you will need symbol (^) to create exponent.
Variable declarations
In Bee, all variables must be declared using an imperative statement. Variables can be dynamic or static and can have a data type. Data type can be custom or pre-defined.


type
declare custom data type


new
declare a dynamic variable


set
declare a static variable


Expressions
Expressions are created using identifiers, operators, rules and constant literals. Expressions can be anonymous or can be assigned to identifiers to create lambda expressions.
expressions ...

can use () to establish order of operations,
can be enumerated using comma separator "," in a list,
can be combined to create more complex expressions,

Examples
** expressions
print 10
print 10 + 10 + 15
print "this is a test"

** complex expressions
print (10 > 5) ∨ (2 < 3)
print -b + sqr(b² - 4·a·b)/(2·a)

** enumeration of expressions
print (1,2,3)
print (1,',',2,',',3)

Conditional Execution
A condition is a logic expression used to control statement execution. For this we use {"if", "else"} keywords at end of statements.

** conditional statement execution
statement if condition;

Note: Previous statement is executed only if the condition is True.

** alternative statement 
  expect condition else statement;

** alternative expression
  expect condition else expression;

Note: Previous statement is executed only if the condition is False.
restrictions:

Can not use "if" with set statement;
Can not use "if" with new statement;
Can not use "if" after done;

Example:

rule main:
  ** generate a random number
  new a := random(Z);

  ** conditional execution
  new b := a;
  let b := -a if a < 0;

  ** print result
  print "|b| = ", a;
return;

Operations:
Bee has support for fractions. Bee is using regular slash "/" for all fractions. You can use superscript for left and subscript for right: These two are equivalent (1/2 = ¹/₂). Unfortunately we can not support fractional power due to lower readability.

¹/₂ ¹/₃ ¹/₄ ¹/₅ ¹/₆ ¹/₇ ¹/₈ ¹/₉  ¹/₁₀ ¹/₁₀₀
x⁻¹ = 1/x, x⁻² = 1/x², x⁻³ = 1/x³ ...

Power operations have priority but we have support only for (+, -) no other operations are possible in exponent. In next expressions, (n-1) is done first before making the power operation.

-- equivalent notation
xⁿ⁻¹ = x^(n-1)
xˣ⁺¹ = x^(n+1)

-- equivalent  notation
x^(¹/₂) = √2(x)  
x^(¹/₃) = √3(x) 


Note:In expressions above () symbols are mandatory. The compiler will detect missing paranthesis and will ask for it. This will improve code readability and eliminate confusions.
Pattern Matching
Instead of ternary operator we use conditional expressions. Conditional expressions enable many choices unlike ternary operator that enable only 2 choices. Conditional expressions are also known as pattern matching expressions.
Syntax:

rule main:
  ** define a local variable
  new var ∈ type;

  ** single condition matching
  let var := (xp1 if cnd1 else xp);

  ** multiple matching with default value
  let var := (xp1 if cnd1, xp2 if cnd2,..., xp);

  ** alternative code alignment
  let var := ( xp1 if cnd1 else
               xp2 if con2 else
               xp3 if cnd3 else
               xp
              );
return;

Example:
rule main:
   new x := '0'; -- symbol
   write "x:"
   read   x;

   new kind := ("digit"  if x ∈ ['0'..'9'] else
                "letter" if x ∈ ['a'..'z'] else
                "unknown");

   print ("x is " + kind); -- expect: "x is digit"
return;

Operators
Bee operators are ASCII or Unicode symbols. One operator can be created using one or two characters. This is why Bee language is considered experimental, esoteric & disruptive.
Delimiters



Symbol
Description




+-...-+
Multi-line boxed comments


#(....)
String interpolation (placeholder) for operator "?"


(_,_,_)
Expression | List literal


[_,_,_]
Index | Array literals | Parameterize types


{_,_,_}
Enumeration type | Set of values | Hash map



Strings



symbol
description




`x`
Back quoted string: regular expression.


'x'
Single quoted string literal or ASCII code point


"y"
Double quoted string literal or UTF32 code point



Single Symbols



symbol
description




!
Negation symbol for relations | Excluded from domain


?
Template modifier. Associated with string templates


*
String replication | Varargs prefix | Spread operator | Many something


@
Domain name | Example @sagecode.net


$
System constant | Environment variables


&
String concatenation | number concatenation


#
Title | String interpolation 


∈
Define variable/constant/result/parameter type


_
Anonymous variable | Constant value = one space (_ = ' ')


+
Maximum upper limit for a domain | Unicode notation U+


-
Minimum lower limit in a domain | Unicode notation U-


:
Start a block or define something


:
Pair-up key-value in: objects, rule parameters, rule arguments, hash-map pairs


;
End of statement | Statement separator


.
Decimals for real numbers | Path string concatenation


.
Membership dot notation | Prefix for public member/attribute

,
Enumeration of elements | expressions


|
Declarative collection builder: set := { x*2 | x ∈ (0..3)}


\
Escape character ( \n := New Line), ( \" = Double Quotes)



Numeric operators
Listed in the order of precedence top down.



symbol
description




-
Change sign, replace "y = -x" with "y = -1*x"


/
Rational number division


^
Power symbol used with fractions or expressions


√
Radical: x√n is equivalent to x^(1/n)


*
Multiplication alternative


\
Rational number division


/
Real number division


×
Array multiplication | Matrix multiplication


%
Modulo operator 5 % 2 = 2


+
Numeric addition | List append | Matrix addition


-
Numeric subtraction | Collection difference


±
Numeric tolerance (use with ≈)



Double Symbols
Double symbols is a group of two ASCII symbols considered as one. Some of these symbols have an Unicode equivalent, some do not. When available, Unicode equivalent is preferred choice.



symbol
description




-- 
End of line comments (not in expression)


##
Single line subtitle comments (no indentation)


**
Single line comments (allow indentation)


..
Define range/domain/slice (n..m) | [n..m]


.!
Define range/domain with excluded limit (n.!m) | [n.!m]


!.
Define range/domain with excluded limit (n!.m) | [n.!m] 


!!
Define range/domain with excluded limits: (n!!m) | [n.!m] 


-.
Minus infinite domain: instead of [-∞..0] write: [-..0]


.+
Plus infinite domain: instead of [0..+∞] write: [0..+]


=>
Define: rule expression | rule result


<-
Define and generate values in a loop from range or set


<:
Define subset from set | Specify super-type for a new type


:>
Data cast pipeline operator / Type conversion


<<
Shift values of collection to right by removing first elements


>>
Shift values of collection to left by removing first elements


::
Deep copy | Clone operator


++
Extend an array with one or more elements


-=
Find and delete one element, from a collection

+=
Append an element in a set or a map but not in a list


+>
Append element to beginning of a list


<+
Append element to end of a list

==
Relation operator for identical (the same)

!=
Relation operator not identical (not the same)


~=
Relation operator: regular expression match


>=
Relation operator: greater then or equal to


<=
Relation operator: less then or equal to



Modifiers
Each modifier is created with pattern "x=" where x is a single symbol:



symbol
meaning




:=
Modify | (value | reference)


+=
Increment value


-=
Decrement value


*=
Multiplication modifier


/=
Real division modifier


^=
Power modifier


√=
Radical modifier


%=
Modulo modifier



Relation Operators
Relation operators are used to compare expressions.



symbol
meaning




∈
check if element belong to collection


=
equal { compare values or attributes}


≠
different { compare values or attributes}


≡
equivalent | { compare values / convert type }


≈
approximating equal numbers, used with ± like: (x ≈ 4 ± 0.25)


>
value is greater than: (2 > 1)


<
value is less than: (1 < 2)


≥
greater than or equal to


≤
less than or equal to

÷
Exact divisor: 3 &division 15 ≡ True



negation:
Operator: "!" can be used in combination with other operators:

 x != y; -- equivalent to: ¬(x = y)
 x !≡ y; -- equivalent to: ¬(x ≡ y)
 x !∈ y; -- equivalent to: ¬(x ∈ y)
 x !≈ y; -- equivalent to: ¬(x ≈ y)
 x !~ y; -- equivalent to: ¬(x ~ y)

Collection operators



symbol
result
meaning




∩
Set
Intersection between two collections


∪
Set
Union between two collections


⊂
Logic
Set is included in superset: "⊂"


⊃
Logic
Set contain subset: "⊃"


Δ
Set
Set symmetric difference


+
String
Concatenation between two strings


+
List
Concatenation between two lists


+
Array
Concatenation between two arrays


∀
Element
All: used in collection qualification


∃
Logic
One: used in collection qualification



Logic Operators
Bee is using enumeration symbols: True = 1 and False = 0



symbol
meaning
notes




¬
NOT
unary operator


∧
AND
shortcut operator


∨
OR
shortcut operator


⊕
XOR
exclusive OR


↓
NOR
p ↓ q = ¬ (p ∨ q)


↑
NAND
p ↑ q = ¬ (p ∧ q)



The table of truth


```
x⁺ x⁻ x¹ x² x³ x⁴ x⁵ x⁶ x⁷ x⁸ x⁹ x¹⁰
```


Note: 
Symbol (^) is exponent operator and is not required when you use superscript exponent. You can use it with expressions, constants or rational numbers to resolve the exceptional cases.


Identifiers that start with a lowercase Latin letter can be used as exponent. The superscript variable can start with a letter and can also use numbers.


```
yᵃ yᵇ yᶜ yᵈ yᵉ yᶠ yᵍ yʰ yⁱ yʲ yᵏ yᶩ 
yᵐ yⁿ yᵒ yᵖ yʳ yˢ yᵗ yᵘ yᵛ yʷ yˣ yʸ yᶻ
```


If you define a constant or variable that start with capital letter there may be some issues. You can't use all Latin letters or any Greek or Cyrilic capital letters in exponent. So your options are limited to create uppercase exponents.


```
zᴬ zᴮ zᴰ zᴱ zᴲ zᴳ zᵸ zᴵ zᴶ zᴷ zᴸ 
zᴹ zᴺ zᴻ zᴼ zᴾ zᴿ zᵀ zᵁ zᵂ
```


## Variable declarations


In Bee, all variables must be declared using an imperative statement. Variables can be dynamic or static and can have a data type. Data type can be custom or pre-defined.


| Table |
| --- |
| type | declare custom data type |
| new | declare a dynamic variable |
| set | declare a static variable |



## Expressions


Expressions are created using identifiers, operators, rules and constant literals. Expressions can be anonymous or can be assigned to identifiers to create lambda expressions.


expressions ...

- can use () to establish order of operations,
- can be enumerated using comma separator "," in a list,
- can be combined to create more complex expressions,

```
** expressions
print 10
print 10 + 10 + 15
print "this is a test"

** complex expressions
print (10 > 5) ∨ (2 < 3)
print -b + sqr(b² - 4·a·b)/(2·a)

** enumeration of expressions
print (1,2,3)
print (1,',',2,',',3)
```


## Conditional Execution


A condition is a logic expression used to control statement execution. For this we use {"if", "else"} keywords at end of statements.


```
** conditional statement execution
statement if condition;
```


Note: Previous statement is executed only if the condition is True.


```
** alternative statement 
  expect condition else statement;

** alternative expression
  expect condition else expression;
```


Note: Previous statement is executed only if the condition is False.


restrictions:

- Can not use "if" with set statement;
- Can not use "if" with new statement;
- Can not use "if" after done;

```
rule main:
  ** generate a random number
  new a := random(Z);

  ** conditional execution
  new b := a;
  let b := -a if a < 0;

  ** print result
  print "|b| = ", a;
return;
```


Bee has support for fractions. Bee is using regular slash "/" for all fractions. You can use superscript for left and subscript for right: These two are equivalent (1/2 = ¹/₂). Unfortunately we can not support fractional power due to lower readability.


```
¹/₂ ¹/₃ ¹/₄ ¹/₅ ¹/₆ ¹/₇ ¹/₈ ¹/₉  ¹/₁₀ ¹/₁₀₀
x⁻¹ = 1/x, x⁻² = 1/x², x⁻³ = 1/x³ ...
```


Power operations have priority but we have support only for (+, -) no other operations are possible in exponent. In next expressions, (n-1) is done first before making the power operation.


```
-- equivalent notation
xⁿ⁻¹ = x^(n-1)
xˣ⁺¹ = x^(n+1)

-- equivalent  notation
x^(¹/₂) = √2(x)  
x^(¹/₃) = √3(x)
```


### Pattern Matching


Instead of ternary operator we use conditional expressions. Conditional expressions enable many choices unlike ternary operator that enable only 2 choices. Conditional expressions are also known as pattern matching expressions.


```
rule main:
  ** define a local variable
  new var ∈ type;

  ** single condition matching
  let var := (xp1 if cnd1 else xp);

  ** multiple matching with default value
  let var := (xp1 if cnd1, xp2 if cnd2,..., xp);

  ** alternative code alignment
  let var := ( xp1 if cnd1 else
               xp2 if con2 else
               xp3 if cnd3 else
               xp
              );
return;
```


```
rule main:
   new x := '0'; -- symbol
   write "x:"
   read   x;

   new kind := ("digit"  if x ∈ ['0'..'9'] else
                "letter" if x ∈ ['a'..'z'] else
                "unknown");

   print ("x is " + kind); -- expect: "x is digit"
return;
```


## Operators


Bee operators are ASCII or Unicode symbols. One operator can be created using one or two characters. This is why Bee language is considered experimental, esoteric & disruptive.


## Delimiters


| Table |
| --- |
| Symbol | Description |
| +-...-+ | Multi-line boxed comments |
| #(....) | String interpolation (placeholder) for operator "?" |
| (_,_,_) | Expression | List literal |
| [_,_,_] | Index | Array literals | Parameterize types |
| {_,_,_} | Enumeration type | Set of values | Hash map |



## Strings


| Table |
| --- |
| symbol | description |
| `x` | Back quoted string: regular expression. |
| 'x' | Single quoted string literal or ASCII code point |
| "y" | Double quoted string literal or UTF32 code point |



## Single Symbols


| Table |
| --- |
| symbol | description |
| ! | Negation symbol for relations | Excluded from domain |
| ? | Template modifier. Associated with string templates |
| * | String replication | Varargs prefix | Spread operator | Many something |
| @ | Domain name | Example @sagecode.net |
| $ | System constant | Environment variables |
| & | String concatenation | number concatenation |
| # | Title | String interpolation |
| ∈ | Define variable/constant/result/parameter type |
| _ | Anonymous variable | Constant value = one space (_ = ' ') |
| + | Maximum upper limit for a domain | Unicode notation U+ |
| - | Minimum lower limit in a domain | Unicode notation U- |
| : | Start a block or define something |
| : | Pair-up key-value in: objects, rule parameters, rule arguments, hash-map pairs |
| ; | End of statement | Statement separator |
| . | Decimals for real numbers | Path string concatenation |
| . | Membership dot notation | Prefix for public member/attribute | , | Enumeration of elements | expressions | | | Declarative collection builder: set := { x*2 | x ∈ (0..3)} | \ | Escape character ( \n := New Line), ( \" = Double Quotes) |
| , | Enumeration of elements | expressions |
| | | Declarative collection builder: set := { x*2 | x ∈ (0..3)} |
| \ | Escape character ( \n := New Line), ( \" = Double Quotes) |



## Numeric operators


Listed in the order of precedence top down.


| Table |
| --- |
| symbol | description |
| - | Change sign, replace "y = -x" with "y = -1*x" |
| / | Rational number division |
| ^ | Power symbol used with fractions or expressions |
| √ | Radical: x√n is equivalent to x^(1/n) |
| * | Multiplication alternative |
| \ | Rational number division |
| / | Real number division |
| × | Array multiplication | Matrix multiplication |
| % | Modulo operator 5 % 2 = 2 |
| + | Numeric addition | List append | Matrix addition |
| - | Numeric subtraction | Collection difference |
| ± | Numeric tolerance (use with ≈) |



## Double Symbols


Double symbols is a group of two ASCII symbols considered as one. Some of these symbols have an Unicode equivalent, some do not. When available, Unicode equivalent is preferred choice.


| Table |
| --- |
| symbol | description |
| -- | End of line comments (not in expression) |
| ## | Single line subtitle comments (no indentation) |
| ** | Single line comments (allow indentation) |
| .. | Define range/domain/slice (n..m) | [n..m] |
| .! | Define range/domain with excluded limit (n.!m) | [n.!m] |
| !. | Define range/domain with excluded limit (n!.m) | [n.!m] |
| !! | Define range/domain with excluded limits: (n!!m) | [n.!m] |
| -. | Minus infinite domain: instead of [-∞..0] write: [-..0] |
| .+ | Plus infinite domain: instead of [0..+∞] write: [0..+] |
| => | Define: rule expression | rule result |
| <- | Define and generate values in a loop from range or set |
| <: | Define subset from set | Specify super-type for a new type |
| :> | Data cast pipeline operator / Type conversion |
| << | Shift values of collection to right by removing first elements |
| >> | Shift values of collection to left by removing first elements |
| :: | Deep copy | Clone operator |
| ++ | Extend an array with one or more elements |
| -= | Find and delete one element, from a collection |
| +> | Append element to beginning of a list |
| <+ | Append element to end of a list |
| ~= | Relation operator: regular expression match |
| >= | Relation operator: greater then or equal to |
| <= | Relation operator: less then or equal to |



## Modifiers


Each modifier is created with pattern "x=" where x is a single symbol:


| Table |
| --- |
| symbol | meaning |
| := | Modify | (value | reference) |
| += | Increment value |
| -= | Decrement value |
| *= | Multiplication modifier |
| /= | Real division modifier |
| ^= | Power modifier |
| √= | Radical modifier |
| %= | Modulo modifier |



## Relation Operators


Relation operators are used to compare expressions.


| Table |
| --- |
| symbol | meaning |
| ∈ | check if element belong to collection |
| = | equal { compare values or attributes} |
| ≠ | different { compare values or attributes} |
| ≡ | equivalent | { compare values / convert type } |
| ≈ | approximating equal numbers, used with ± like: (x ≈ 4 ± 0.25) |
| > | value is greater than: (2 > 1) |
| < | value is less than: (1 < 2) |
| ≥ | greater than or equal to |
| ≤ | less than or equal to |



negation:


Operator: "!" can be used in combination with other operators:


```
x != y; -- equivalent to: ¬(x = y)
 x !≡ y; -- equivalent to: ¬(x ≡ y)
 x !∈ y; -- equivalent to: ¬(x ∈ y)
 x !≈ y; -- equivalent to: ¬(x ≈ y)
 x !~ y; -- equivalent to: ¬(x ~ y)
```


## Collection operators


| Table |
| --- |
| symbol | result | meaning |
| ∩ | Set | Intersection between two collections |
| ∪ | Set | Union between two collections |
| ⊂ | Logic | Set is included in superset: "⊂" |
| ⊃ | Logic | Set contain subset: "⊃" |
| Δ | Set | Set symmetric difference |
| + | String | Concatenation between two strings |
| + | List | Concatenation between two lists |
| + | Array | Concatenation between two arrays |
| ∀ | Element | All: used in collection qualification |
| ∃ | Logic | One: used in collection qualification |



## Logic Operators


Bee is using enumeration symbols: True = 1 and False = 0


| Table |
| --- |
| symbol | meaning | notes |
| ¬ | NOT | unary operator |
| ∧ | AND | shortcut operator |
| ∨ | OR | shortcut operator |
| ⊕ | XOR | exclusive OR |
| ↓ | NOR | p ↓ q = ¬ (p ∨ q) |
| ↑ | NAND | p ↑ q = ¬ (p ∧ q) |



| Table |
| --- |
| p | q | ¬ p | p ⊕ q | p ∧ q | p ∨ q |
| 1 | 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 |



## Bitwise operators


Bitwise operators are processing numbers not Boolean values.


| Table |
| --- |
| symbol | meaning | notes |
| « | bit SHIFTL | shift bits to left |
| » | bit SHIFTR | shift bits to right |
| ~ | bit NOT | negate all bits |
| & | bit AND | execute AND between each bits |
| | | bit OR | execute OR between each bits |
| ⊕ | bit XOR | execute XOR between each bits |



| Table |
| --- |
| a | ~ a | a « 1 | a » 2 |
| 0000 | 1111 | 0000 | 0000 |
| 1111 | 0000 | 1110 | 0011 |
| 0111 | 1000 | 1110 | 0001 |
| 0110 | 1001 | 1100 | 0001 |



| Table |
| --- |
| a | b | a & b | a | b | a ⊕ b |
| 00 | 00 | 00 | 00 | 00 |
| 01 | 00 | 00 | 01 | 01 |
| 11 | 01 | 01 | 11 | 10 |
| 10 | 11 | 10 | 11 | 01 |



## String operators


| Table |
| --- |
| Symbol | Description |
| * | string pattern repetition (right operator must be numeric) |
| / | concatenate url or path using / not depending on OS |
| + | concatenate two strings as they are preserving trial spaces. |
| - | concatenate two strings and trim spaces to a single space. |
| . | concatenate strings with "/" on Linux or "\" on Windows. |
| ? | string format operator, replace "#" with number. |



Read next:
Structure
