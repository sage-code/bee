# Bee Syntax


Next we enumerate the fundamental concepts to grasp Bee syntax. After this overview we will go in details. We use long pages you can scroll down and reaad. A better experience is on our homepage where we have bookmarks for headers.

We use examples and sometimes a simplified version of BNF notation to explain the syntax rules. If you do not know anything about BNF don't wary, here is a short introduction to this weird notation:

- We use suggestive descriptors for language elements,
- We use "::=" to explain a descriptor,
- We use "..." for repetitive sequences of symbols,
- We use notes to explain the semantics,
- Optional keyword is enclosed in square brackets [];

## Comments

Comments are very important part of Bee code. We have multiple conventions for making good comments for any project. Bee comments are tailored by architectural principle: "if there are no comments in the code the code is wrong."

**Example:**


```
# Bee Language Syntax Example
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


For single line title comments we use one "#" symbol. You can use two "##" for subtitles for large code sections. This can be used in combination with "!" to create "shebang" comment known in scripting languages on Linux to specify interpreter location. This is in case someone create an interpreter for Bee. We plan to create a compiler where such a comment is useless. 


For single line comments we use two stars like this: "**", there is a catch single line comments can't be also end of line comments. For end of line we use -- comments.

- This comment can be extended to multiple stars to create a separator,
- You can use single line comment at beginning of new line,
- You can use two spaces to indent the comment and align with the code.

**end of line comments**

Before new line of code: (EOL) you can use comments starting with: "-- "

- notice one line may be or not a full statement. the end of statement is not (EOL),
- you can use "-- " in the middle of an expression, only if the expression span over multiple lines,
- you can have multiple statements separated by ";" in a line but only one comment at the end of all statements on a single line.

**block comments**

Bee has a specific notation for block comments not used in any other language so far. It is a multi-line comment starting with "+-" and end with "-+". The upper right corner is missing. I guess you will notice this defect later. However you can use old-style C comments.

- Bee comments are inspired from Wiki Markdown, Python and Ada languages
- Bee comments are designed for better syntax coloring, that is not available in other languages. So Bee comments are expressive and easy to use to create documentation based on comments with a tool.

## Bee Keywords

Bee is an expressive language but it's core has about 72 reserved keywords so far:

{begin , alias , and , apply , abort , other , case , continue , done , default , if , is , do , else , exit , fail , final , miss , panic , like , load , next , job , match , over , print , pass , void , rule , return , fail , retry , none , scrap , type , read , trial , stop , yield , xor , write , wait , when , or , with , hide , new , cycle , let , set , while , for , resum , put , pop , raise , not , as , in , start , try , expect} 


- You can not use these keywords as identifiers;
- Some of these keywords are reserved but not implemented;
- New keywords are going to be created for new features;

### Semantic keywords

| Keyword | Purpose |
| :--- | :--- |
| if | conditional executor for one statement block |
| is | query element or variable data type |
| as | create alias for used modules |
| or | alternative for ladder decision |
| in | alternative for belong operation |
| and | alternative for cascade decision |
| xor | alternative for logic operation |
| not | alternative for logic operation |


## Statements

Statements can start with an imperative or declarative keyword and must end with a mandatory semicolon `;`. While one statement can span multiple lines, all statements must be explicitly terminated.

- Statements are indented by 2 or more spaces.
- Multiple statements on a single line are separated by `;`.
- Expressions within a statement may span multiple lines.
- **Note:** All code examples in this specification strictly follow this rule, and the compiler will issue an error for any missing semicolons.

| Key | Description |
| :--- | :--- |
| `set` | Create a constant |
| `new` | Create a variable |
| `let` | Modify a variable |
| `type` | Create a data type |
| `read` | Accept input from console into a variable |
| `write` | Register in console cache a string |
| `print` | Output to console with end of new line |


### Code blocks

Statements can be contained in blocks of code.


| Kword | Block description |
| :---  | :--- |
| start | start local scope for do block |
| with  | qualifier suppression block |
| if    | first block in decision statement |
| cycle | repetitive or iterative blocks |
| match | multi-path value selector block |
| trial | exception handler block |


- Block ending keyword can be one of: { done, cycle },
- Statements in nested blocks are using indentation.

### Definition statements


Next statements are used to declare new elements in a module.


| Keyword | Purpose |
| :--- | :--- |
| use | Load module or module |
| alias | Eliminate scope qualifier |
| hide | Hiding public members from a loaded module |
| rule | Create a new business rule or prototype |
| return | End rule declaration and transfer control to caller |


### Execution statements

Next keywords are simple statements. These represents actions called imperative statements.


| Keyword | Purpose |
| :--- | :--- |
| apply | Execute a rule and ignore the result if there is one |
| begin | Commence execution of a coroutine |
| wait | Suspend current thread execution for a number of seconds |
| read | Flush the console buffer and accept user input from console |
| write | Add something to console buffer but no new line |
| print | Output expression result, variable or constant to console |
| let | Mutate variable value using an expression |
| new  | Create a new variable and allocate space in memory |
| scrap | Remove one element from its collection |


## Control statements

Control statements are used to create local blocks of code that resolve a small task synchronously. After task is finished the control is returned to the main thread.


| Keyword | Purpose |
| :--- | :--- |
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


| Keyword | Purpose |
| :--- | :--- |
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

## Identifiers

Bee identifiers (names), can start with Latin letters. An identifier can contain numbers but can not start with a number and can't use spaces inside. Bee is Unicode language but does not permit Unicode identifiers for a good reason: Unicode characters are hard to find and select. 


In mathematics is very popular notation for angles to use Greek letters. Bee will support a limited set of Greek an Cyrillic letters for identifiers. We include these letters on the Bee keyboard design for easy access. 

```
Σ Π Δ Ξ Γ Ψ Ω ζ
α β ɣ λ π μ φ ε δ η σ ω
Б Г Д Ж И Л Ф Ц Ч Ш Э Я
```


### Subscript


You can use a limited number of letters and numbers available in Unicode as subscript. If used these are permited to make identifier names in second and next positions but not first postion. You can not start an identifier with one of these symbols:

**examples**

```
x₀ x₁ x₂ x₃ x₄ x₅ x₆ x₇ x₈ x₉ x₁₀
aₐ eₑ hₕ iᵢ jⱼ kₖ lₗ mₘ nₙ oₒ pₚ rᵣ sₛ tₜ uᵤ vᵥ zₓ
```

**restrictions**

* subscript symbol must be last letter in identifier
* after first subscript, next symbols can be only subscript
* not all letters in latin alphabet have a subscript unfortunately


### Superscript

Bee has support for exponent using superscript. You can make any integer exponent including negative numbers but you can not use dot in the exponent. Here are some examples permitted:
```
x⁺ x⁻ x¹ x² x³ x⁴ x⁵ x⁶ x⁷ x⁸ x⁹ x¹⁰
```
**Note:**

Symbol (^) is exponent operator and is not required when you use superscript exponent. You can use it with expressions, constants or rational numbers to resolve the exceptional cases.

**Lowercase exponent:**

Identifiers can be used as exponent. The superscript variable can start with a letter and can also use numbers. An exponent therefore can be a number or a variable or a constant recognized by Bee and replaced by it's value.
```
aᵃ bᵇ cᶜ dᵈ eᵉ fᶠ gᵍ hʰ iⁱ jʲ kᵏ lᶩ 
mᵐ nⁿ oᵒ pᵖ rʳ sˢ tᵗ uᵘ vᵛ wʷ xˣ yʸ zᶻ
```

**restrictions**
* there is limited support for expressions
* only 3 expressions are permited in superscript (+, -, /)

**Uppercase exponent:**

If you define a constant or variable that start with capital letter there may be some issues. You can't use all Latin letters or any Greek or Cyrilic capital letters in exponent. So your options are limited to create uppercase exponents.

```
Aᴬ Bᴮ Dᴰ Eᴱ Eᴲ Gᴳ Hᵸ Iᴵ Jᴶ Kᴷ Lᴸ 
Mᴹ Nᴺ Nᴻ Oᴼ Pᴾ Rᴿ Tᵀ Uᵁ Wᵂ
```

**Caution:** Observe letters: {C, F ,S ,Q, X, Y, Z} are missing unfortunately. We just don't find them in Uncode set. I think this is a Unicode bug. So if you define a constant that use any of these letters, you will need symbol (^) to create exponent instead of superscript.

All exponents will be replaced with variable value. For example if a variable A has value 3, the expression Aᴬ becomes 9, because 3^3 = 9. 

**Variable declarations**

In Bee, all variables must be declared using an imperative statement Variables can be dynamic or static and can have a data type. Data type can be custom or pre-defined.


* type - declare custom data type
* new  - declare a dynamic variable
* set  - declare a static variable

## Expressions

Expressions are created using identifiers, operators, rules, and constant literals. 

- Mathematical multiplication is performed using the `*` operator. The middle dot `·` may be used in documentation for illustrative purposes but is not a valid operator in Bee code.
- Boolean operations utilize the symbols `∧` (AND) and `∨` (OR). The keywords `and` and `or` act as semantic aliases in formal language descriptions but must not be used as operators in expressions.

**Precedence and Power Operators:**
- Simple integer or negative powers may be represented via superscript notation (e.g., `x²`, `x⁻¹`).
- For fractional powers, complex expressions, or any case where superscript characters are unavailable, the caret `^` operator is mandatory (e.g., `x^(n+1)`, `x^(¹/₂)`, `x^y`).
- The compiler strictly enforces the use of `^` and parentheses for complex exponents to eliminate ambiguity.

## Conditional Execution

A condition is a logic expression used to control statement execution. For this we use {"if", "else"} keywords at end of statements.

** conditional statement execution
statement if condition;

**Note:** Previous statement is executed only if the condition is True.

```
** alternative statement 
  expect condition else statement;

** alternative expression
  expect condition else expression;
```

**Note:** Previous statement is executed only if the condition is False.

**restrictions:**

* Can not use "if" with set statement;
* Can not use "if" with new statement;
* Can not use "if" after done;

**Example:**
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

**Operations:**

Bee has support for fractional power. Bee is using regular slash "/" for all fractions. You can use superscript for left and subscript for right: These two are equivalent 1/2 = (¹/₂). Using ^() when we create fractional power expressions is mandatory. For example:

```
x^(¹/₂)  
x^(¹/₆) 
x^(¹/₁₀)
```

**negative power**

```
x⁻¹ = 1/x¹ 
x⁻² = 1/x² 
x⁻³ = 1/x³
```
**expressions power**

```
new n := 3;   -- define new variable to be used as exponent 
new y := 2ⁿ⁻¹; -- expression n-1 is evaluated first to 3 then power 
expect y = 4; 
```   


**priority:**

Power operations have priority but we have support only for (+, -) no other operations are possible in exponent expressions. In next expressions, (n-1) is evaluated first before making the power operation.
```
** equivalent notation
xⁿ⁻¹ = x^(n-1)
xˣ⁺¹ = x^(n+1)

** equivalent  notation
x^(¹/₂) = √2(x)  
x^(¹/₃) = √3(x) 
```

**Note:** The compiler will detect missing paranthesis and missing carot symbol "^" and will signal error. This will improve code readability and eliminate confusions. Using "^" enable complex expressions inclusiv fraction exponent.

### Pattern Matching
Instead of ternary operator we use conditional expressions. Conditional expressions enable many choices unlike ternary operator that enable only 2 choices. Conditional expressions are also known as pattern matching expressions.

**Syntax:**
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

Example:

```
rule main:
   new x := '0'; -- symbol
   write "x:";
   read   x;

   new kind := ("digit"  if x ∈ ['0'..'9'] else
                "letter" if x ∈ ['a'..'z'] else
                "unknown");

   print ("x is " + kind); -- expect: "x is digit"
return;
```

---

[Go back](features.md) | [Read next](operators.md)
