# Bee Syntax

This document details the fundamental concepts and grammar rules of Bee syntax.

Syntax rules are described using illustrative examples and Backus-Naur Form (BNF) notation:

- Descriptor names are used for syntax elements.
- `::=` defines a syntactic descriptor.
- `...` represents repetitive sequences of symbols.
- Optional elements are enclosed in square brackets `[]`.

## Comments

Bee supports two comment styles inspired by Ada.

Example:

```bee
-------------------------------------------------------------------
                  -- Bee Language Syntax Example --
+------------------------------------------------------------------
| Header block comment describing application behavior            |
+-----------------------------------------------------------------+
rule main:
  -- empty statement ';'
  ; 

  -- inline argument comments
  print ("end-of-line comments", -- first argument
         "can explain arguments", -- second argument
         "across multiple lines"  -- third argument
        );
return;
```

### Single-Line Comments

Single-line comments begin with two dashes `--`:

- Can extend across an entire line as a visual separator.
- Can be placed at the start of a line or indented alongside statements.
- When placed at the end of a line (EOL comment), the comment begins with `-- `.

### Block Comments

Bee uses a distinct box syntax for multi-line block comments:
- Starts with `+-` at the upper-left boundary.
- Ends with `-+` at the lower-right boundary.

## Keywords

Bee defines approximately 72 reserved keywords:

`{ alias, and, apply, abort, as, begin, case, continue, cycle, default, do, done, else, expect, exit, fail, final, for, hide, if, in, is, job, let, like, load, match, miss, next, none, not, or, other, over, panic, pass, print, read, raise, redo, repeat, rest, resum, retry, return, rule, scrap, set, start, stop, trial, try, type, use, void, wait, when, with, write, xor, yield }`

Key rules:
- Keywords cannot be used as identifier names.
- Keywords are reserved and case-sensitive.

### Semantic Keywords

| Keyword | Purpose |
| :---| :---|
| `if` | Conditional executor for a statement or block |
| `is` | Query data type of an element or variable |
| `as` | Create alias qualifier for imported modules |
| `or` | Short-circuit logical OR |
| `in` | Set membership check |
| `and` | Short-circuit logical AND |
| `xor` | Logical exclusive OR |
| `not` | Logical negation |

## Statements

Statements start with an imperative or declarative keyword and end with a mandatory semicolon `;`. A single statement may span multiple lines.

- Statements inside blocks are indented by 2 or more spaces.
- Multiple statements on a single line are separated by `;`.
- Missing semicolons produce a compiler syntax error.

### Declarative Statements

| Keyword | Description |
| :---| :---|
| `set` | Declare an immutable constant |
| `new` | Declare a new variable |
| `let` | Mutate an existing variable |
| `type` | Declare a custom sub-type or alias |
| `read` | Accept input from console into a variable |
| `write` | Write formatted text to output buffer |
| `print` | Output expression to console with newline |

### Code Blocks

Code blocks enclose groups of statements inside scope boundaries:

| Keyword | Block Description |
| :---| :---|
| `start` | Non-repetitive local scope block |
| `with` | Qualifier suppression block for module members |
| `if` | Conditional decision block |
| `cycle` | Repetitive / iterative execution loop block |
| `match` | Multi-path value selection block |
| `trial` | Exception handler block |

Block termination keywords: `{ done, cycle, repeat }`.

### Module Definition Statements

| Keyword | Purpose |
| :---| :---|
| `use` | Load an external or library module |
| `alias` | Create a local alias for a qualified module member |
| `hide` | Suppress public members from an imported module |
| `rule` | Declare a subroutine or business rule |
| `return` | End rule declaration and return control to caller |

### Imperative Execution Statements

| Keyword | Purpose |
| :---| :---|
| `apply` | Execute a rule and discard return results |
| `begin` | Spawn an asynchronous thread / coroutine |
| `wait` | Suspend thread execution for $t$ seconds or until child threads finish |
| `read` | Flush output buffer and read console user input |
| `write` | Append text to output buffer without newline |
| `print` | Evaluate and output expression to console with newline |
| `let` | Mutate a variable using an expression |
| `new` | Allocate memory and initialize a variable |
| `scrap` | Remove an element from a collection |

### Control Statements

| Keyword | Purpose |
| :---| :---|
| `start` | Non-repetitive local scope |
| `if` | Start conditional branch |
| `else` | Start alternative branch |
| `do` | Start executable statement block |
| `cycle` | Repetitive loop block |
| `for` | Finite iterative loop |
| `while` | Conditional loop |
| `match` | Pattern matching value selector |
| `when` | Branch node in match statement |
| `other` | Default catch-all branch in match statement |
| `trial` | Declare protected exception region |
| `try` | Execute guarded block inside trial statement |
| `case` | Catch specific exception error code |
| `miss` | Default catch-all exception handler |
| `final` | Always-executed cleanup block |

### Transfer Statements

| Keyword | Purpose |
| :---| :---|
| `panic` | Raise unrecoverable error and abort execution |
| `over` | Cleanly terminate program execution |
| `exit` | Terminate current rule execution and return to caller |
| `yield` | Yield control from active coroutine |
| `rest` | Suspend routine until child threads complete |
| `stop` | Break out of active loop execution |
| `redo` | Restart current loop iteration from the beginning |
| `next` | Skip remainder of current iteration and proceed to next |
| `abort` | Abort execution of a trial block |
| `fail` | Raise recoverable error message and continue |
| `pass` | No-op pass statement |
| `expect` | Assert condition; raise `$unexpected` exception if false |
| `raise` | Raise runtime exception |
| `retry` | Restart guarded trial block from beginning |
| `resume` | Mark error as handled and resume execution |
| `done` | Close scope block statement |
| `repeat` | Close repetitive loop statement |

## Identifiers

Identifier names begin with a Latin letter, Greek letter, or Cyrillic letter. Identifiers may contain numeric digits in subsequent positions but cannot contain spaces or start with a number.

### Greek and Cyrillic Letters

Supported mathematical and Cyrillic identifier symbols:

```text
Σ Π Δ Ξ Γ Ψ Ω ζ
α β ɣ λ π μ φ ε δ η σ ω
Б Г Д Ж И Л Ф Ц Ч Ш Э Я
```

### Subscript Identifiers

Subscript numbers and letters are permitted as suffix characters in identifiers:

```text
x₀ x₁ x₂ x₃ x₄ x₅ x₆ x₇ x₈ x₉ x₁₀
aₐ eₑ hₕ iᵢ jⱼ kₖ lₗ mₘ nₙ o⒪ pₚ rᵣ sₛ tₜ uᵤ vᵥ zₓ
```

Rules:
- Subscript symbols must appear at the end of an identifier name.
- Once a subscript character appears, subsequent characters in that identifier must also be subscripts.

### Superscript Exponents

Superscript numbers and variable letters express exponentiation directly without requiring the caret `^` operator:

```bee
new x := 2;
new y := x³; -- equivalent to x^3 (value = 8)
```

Lowercase superscript characters:
```text
aᵃ bᵇ cᶜ dᵈ eᵉ fᶠ gᵍ hʰ iⁱ jʲ kᵏ lᶩ mᵐ nⁿ oᵒ pᵖ rʳ sˢ tᵗ uᵘ vᵛ wʷ xˣ yʸ zᶻ
```

Uppercase superscript characters:
```text
Aᴬ Bᴮ Dᴰ Eᴱ Gᴳ Hᵸ Iᴵ Jᴶ Kᴷ Lᴸ Mᴹ Nᴺ Oᴼ Pᴾ Rᴿ Tᵀ Uᵁ Wᵂ
```

Note:
For missing uppercase superscript characters (`C`, `F`, `Q`, `S`, `X`, `Y`, `Z`), or for complex exponent expressions, the caret operator `^` with parentheses must be used (e.g. `x^(n+1)`).

## Expressions

Expressions are constructed using identifiers, operators, subroutines, and literals.

- Multiplication uses `*`.
- Logical AND uses `∧`, logical OR uses `∨`.
- Exponentiation uses superscripts (e.g. `x²`) or caret syntax (`x^y`, `x^(1/2)`).

## Conditional Execution

Statements can include trailing conditional modifiers using `if` or `else`:

```bee
-- trailing statement execution condition
statement if condition;

-- trailing statement alternative execution
expect condition else statement;
```

Example:

```bee
rule main:
  new a := random(Z);
  new b := a;
  let b := -a if a < 0; -- trailing conditional execution
  print "|b| = ", b;
return;
```

Restrictions:
- Trailing `if` cannot be attached to `set`, `new`, or `done` statements.

## Pattern Matching

Conditional expressions support pattern-matching selections:

```bee
rule main:
  new x := '0';
  write "x:";
  read x;

  new kind := ("digit"   if x ∈ ['0'..'9'] else
               "letter"  if x ∈ ['a'..'z'] else
               "unknown");

  print ("x is " + kind);
return;
```

---

[Go back](features.md) | [Read next](operators.md)
