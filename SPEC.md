-- Bee-3 — Language Specification

**Version:** 3.0 · **Status:** implemented and conformance-tested · **Date:** 2026-08-17

Bee-3 is Bee-2 with twenty-four deliberate changes made for safety, recorded as D66–D89 and summarised
in §29. Eleven of them are breaking. Every one removes a way for a correct-looking program to mean
something other than it looks like.

Bee-3 is a safety-oriented dialect of the Bee language designed by Sage-Code Laboratory
([github.com/sage-code/bee](https://github.com/sage-code/bee), Apache-2.0). It covers most of the
upstream design; §26 lists what it deliberately omits and why, and §29 lists what it changes.

This document is **normative for the implementation in this repository**. Where it departs from the
upstream design, the departure is deliberate and recorded in `DECISIONS.md` as a numbered ruling;
the ruling is cited inline as (D*n*). There are 89 such rulings, and they exist because the upstream
sources — the documentation, the demo programs, and the repository README — **contradict each other
on nearly every hard question**. Where they conflict, the conflict is itself the finding, and a
ruling is made on the merits.

Conformance is defined in §27 and enforced by `run_tests.py`.

---

## 1. Overview

Bee is statically typed, compiled in intent, and rule-oriented. A program is one or more modules;
one of them holds `rule main`, which is the entry point.

```bee
-- hello world
rule main:
  print "Hello World";
return;
```

Distinguishing characteristics:

- **Explicit over implicit.** Declarations require a keyword, narrowing requires a cast, and a call
  that can mutate a caller's variable says so at the call site.
- **Unicode operators.** `∈ ∧ ∨ ¬ ∀ ∃ ∪ ∩ Δ ⊂ ⊃ ≠ ≤ ≥ λ √ ± ≈` and superscript exponents.
- **Named results.** A rule declares its results as variables; there is no `return value`.
- **Fixed-point rationals.** The `Q` type is exact binary fixed point with a programmer-chosen
  container size — the part of the design that is not in other languages.
- **No hoisting.** Every name must be declared textually before use.

---

## 2. Lexical structure

### 2.1 Source

UTF-8, extension `.bee`. One file is one module. Newlines are not significant; an expression may
span lines.

### 2.2 Comments

| Form | Rule |
|---|---|
| `# text` | to end of line. `#!` on line 1 is a shebang and is ignored. |
| `## text` | to end of line. |
| `** text` | to end of line, **in any position**. |
| `-- text` | to end of line, **only when followed by whitespace or end of line** (D27). |
| `+- ... -+` | block comment, **only when `+-` starts a line** (D26). Does not nest. |

The two positional rules exist because both markers share a prefix with arithmetic. Without them
`a +-b` becomes a comment swallowing the rest of the file, and `5--3` becomes `5` followed by a
comment. With them, `a +-b` is addition of a negated value and `5--3` is subtraction.

`**` follows the same positional rule (D67): mid-line it is an error naming both readings, so
`a ** b` can never silently comment out the rest of a line.

Nested comments (`|: :|`) are not in Bee-2 (D23).

### 2.3 Identifiers

```
identifier     ::= ident_start ident_continue*
ident_start    ::= letter | "_"
ident_continue ::= letter | digit | "_" | subscript
letter         ::= Latin | greek | cyrillic
greek          ::= Σ Π Ξ Γ Ψ Ω ζ α β ɣ λ π μ φ ε δ η σ ω
cyrillic       ::= Б Г Д Ж И Л Ф Ц Ч Ш Э Я
subscript      ::= ₀..₉ ₐ ₑ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ ᵣ ₛ ₜ ᵤ ᵥ ₓ
```

Case-sensitive. A subscript may not begin an identifier, and nothing but subscripts may follow one:
`x₁` is a name, `x₁y` is an error.

`Δ` is **not** a letter — it is the symmetric-difference operator (D46). `λ` is not a letter either;
it opens a lambda.

Names beginning with `$` are system names (§13). A leading `.` marks a public member and is
recognised only immediately after a declaration keyword (§20, D53).

### 2.4 Superscripts

A superscript immediately following a primary expression is exponentiation:

```
superscript ::= ("⁺" | "⁻")? (⁰..⁹)+ | latin_superscript+
```

`x²` is `x ^ 2`; `xⁿ` references the variable `n`; `x⁻¹` is `x ^ -1`. A sign may only appear at the
front. `x²` and `x ^ 2` produce the same tree — the two spellings are interchangeable everywhere.

### 2.5 Literals

| Literal | Type | Notes |
|---|---|---|
| `0` `42` | `Z` | A leading `-` or `+` is a unary operator, not part of the literal (D25). |
| `0.5` `1E10` `1e-3` | `R` | Must contain `.` or an exponent. |
| `p\q` | `Q` | Rational literal. Binds tighter than any operator (D62). |
| `0B0` `0B1` | `B` | |
| `True` `False` | `B` | |
| `'a'` | `A` | Exactly one ASCII code point. |
| `"text"` | `S` | UTF-8. |
| `U+HHHH` | `A` | Exactly four hex digits. |
| `[1,2,3]` | array | §10.1 |
| `(1,2,3)` | list | §10.3 |
| `{1,2,3}` | set | §10.4 |
| `{1:"a"}` | map | §10.5 |
| `{a: 1}` | object | §16 |

### 2.6 Escapes

`\n` `\t` `\r` `\\` `\"` `\'` `\0`. Any other escape is an error.

### 2.7 Operator normalisation

One canonical token per operator. ASCII spellings are aliases:

| ASCII | Canonical | | ASCII | Canonical |
|---|---|---|---|---|
| `>=` | `≥` | | `<=` | `≤` |
| `!∈` | `∉` | | `!≡` / `≢` | `≠≡` |
| `and` | `∧` | | `or` | `∨` |
| `not` | `¬` | | `xor` | `⊕` |
| `in` | `∈` | | `root` | `√` |
| `forall` | `∀` | | `exists` | `∃` |
| `union` | `∪` | | `inter` | `∩` |
| `sdiff` | `Δ` | | `divides` | `÷` |
| `subset` | `⊂` | | `superset` | `⊃` |
| `approx` | `≈` | | `plusminus` | `±` |
| `===` | `≡` | | `!==` | `≠≡` |

**Every operator has an ASCII spelling** (D68). The Unicode forms remain preferred and are what the
examples use, but nothing in Bee-3 *requires* a keyboard nobody has.
| `<<` | `«` | | `>>` | `»` |

`==` is **not** an alias for `=`, and `!=` is **not** an alias for `≠` (D24): `=`/`≠` compare
values, `==`/`!=` compare references.

`≢` appears in the upstream corpus but in no upstream operator table; it is adopted as a third
spelling of `≠≡`.

### 2.8 Statement termination

Every statement ends with `;` (D7). Lines ending in `do`, `:` or `else` open a block and take none.

---

## 3. Keywords

52 reserved words:

```
abort   alias   apply   as      begin   case    cycle   do      done    else
exit    expect  fail    final   for     hide    if      let     match   miss
new     next    other   over    panic   pass    print   raise   read    redo
repeat  resume  retry   return  rule    scrap   self    set     start   stop
super   then    trial   try     type    use     wait    when    while   with
write   yield
```

Reserved for a later version, and rejected by name: `continue` `default` `del` `in` `is` `job`
`like` `load` `module` `none` `pop` `put` `resum` `void`.

`claim` and `store` appear in the upstream demos but are not Bee keywords; they are recognised only
to suggest `expect` and `set` (D6, D16).

`all` and `one` are **contextual**: they name a `match` variant only when a selector follows, so a
variable may still be called `all` (D51).

---

## 4. Types

### 4.1 Primitives

| Code | Name | Representation | Zero value |
|---|---|---|---|
| `B` | Boolean | 8-bit; `0` false, `1` true | `0B0` |
| `A` | Alpha | one ASCII code point | `'\0'` |
| `Z` | Integer | signed 64-bit | `0` |
| `N` | Natural | unsigned 64-bit | `0` |
| `R` | Real | IEEE-754 binary64 | `0.0` |
| `S` | String | UTF-8, growable, mutable, shared | `""` |
| `Q` | Rational | fixed point, §12 | `0` |
| `Λ` | Longitude | `Q(8,17)` constrained −180..180 (D83) | `0` |
| `Φ` | Latitude | `Q(7,17)` constrained −90..90 (D83) | `0` |
| `L` | Lambda | a pure expression value, §17 | — |

`B` is Boolean and `L` is Lambda (D12). The upstream demos use `L` for logic values; that is drift,
and `∈ L` on a Boolean is diagnosed.

### 4.2 Composite types

```
array_type  ::= "[" type "]" [ "(" size ("," size)* ")" ]
list_type   ::= "(" type ")"
set_type    ::= "{" type "}"
map_type    ::= "{" type ":" type "}"
record_type ::= "{" field ("," field)* "}"        field ::= name "∈" type
lambda_type ::= "λ" "(" param ("," param)* ")" [ "=>" type ]
sized_type  ::= "Q" "(" m "," n ")"
```

Bracket meaning is positional (D30): an **array type** after `∈`, `<:` or in a `type` descriptor;
an **index or slice** immediately after a primary expression; an **array literal** anywhere else an
expression may begin.

Brace meaning is decided by content (D42, D44, D48): `{}` is the empty set; bare identifier keys
make an **object**; expression keys make a **map**; a single type makes a **set**; `name ∈ type`
fields make a **record type**.

### 4.3 Type declarations

```
type_decl ::= "type" ["."] Identifier ":" descriptor [ "<:" super_type ] ";"
```

```bee
type Digit:  ('0'..'9')      <: A;      -- a constrained A
type Vec10:  [Z](10);                   -- an alias
type Point:  {x ∈ Z, y ∈ Z}  <: Object; -- a record
```

User type names begin with a capital letter.

A **range descriptor names a domain of values of its base type** (D40), not a range value: `Digit`
is an `A` constrained to `'0'..'9'`. **The constraint is enforced at every store** — assigning
outside the domain raises `$out_of_range`.

### 4.4 Type inference

`:=` infers from the initialiser:

| Literal | Inferred |
|---|---|
| integer | `Z` (untyped, see D37) |
| real | `R` |
| `p\q` | `Q` |
| `'x'` | `A` |
| `"x"` | `S` |
| `True`/`False` | `B` |
| `[...]` `(...)` `{...}` | collection of the element type |
| `λ(...) => ...` | `L` |

An empty collection literal without an annotation is an error: the element type is underivable.

### 4.5 Conversion

**Integer literals are untyped** (D37). They take the type of whatever context they meet, if the
value fits, and in arithmetic they take the other operand's type — so `n - 1` stays in `N` when
`n ∈ N`. Without this rule no recursive function over `N` compiles.

**Real literals are typed `R`** and never adapt downward: `new n ∈ Z; let n := 10.5;` is an error.

Beyond untyped literals there is no implicit numeric conversion, with three exceptions:

1. **Widening.** `N` → `Z` → `R`, wherever a value meets an expected type. Non-lossy.
2. **Q to R.** Implicit. `R` to `Q` requires a cast.
3. **String concatenation.** In `a + b` where either operand is `S`, the other is converted to its
   display form (D22).

Explicit conversion is `:>` (D17). It truncates toward zero, and traps rather than wrapping.

---

## 5. Declarations

```
const_decl ::= "set" ["."] name ":"  expression [ "∈" type ] ";"
             | "set" ["."] name ":=" expression ";"
var_decl   ::= "new" ["."] binding ("," binding)* [ "∈" type ]
               [ (":=" | "::") expression_list ] ";"
binding    ::= (Identifier | "_") [ ":" initial ]
```

Declaration keywords are **mandatory** (D11). Bare `x := 1;` is an error suggesting `new` or `let`.

The documentation argues for `set`/`new`/`let`; the demos merely omit them. Argument beats exhibit:
implicit declaration is the footgun where a mistyped assignment silently creates a variable instead
of updating one, which the language's own stated principle rejects.

```bee
new a ∈ Z;                  -- zero-initialised
new b: 10 ∈ Z;              -- with an initial value
new c := 10;                -- type inferred
new d :: c;                 -- a deep copy (D39)
new x, y ∈ R;               -- several
new p:1, q:2 ∈ Z;           -- several with initial values
set PI: 3.14159 ∈ R;        -- a constant
```

When parsing a declaration's value, a top-level `∈` **ends the value and begins the annotation**
(D33). To use `∈` as a membership test in an initialiser, parenthesise it.

Every variable is zero-initialised unless given a value (D10). A **scalar** that is read and never
written anywhere in its scope is an error (D79): that is a forgotten assignment, not a use of the
zero. Collections are exempt, because their zero value — empty — is one programs legitimately
declare and then fill.

```bee
new total ∈ Z;          -- fine: the loop below writes it
for i ∈ (1..4) do
  let total += i;
repeat;

new forgotten ∈ Z;      -- E254: read, never written
print forgotten;
``` Assigning to a constant is an error.
Redeclaring a name in one scope is an error; shadowing an outer scope is permitted and warns.

---

## 6. Assignment

```
assign_stmt ::= "let" target_list modifier expression_list ";"
target_list ::= target ("," target)* | "(" target ("," target)* ")"
target      ::= Identifier | index | slice | member
modifier    ::= ":=" | "::" | "+=" | "-=" | "*=" | "/=" | "%=" | "^=" | "√="
              | "++" | "<+" | "+>" | "<<" | ">>"
```

- `:=` assigns. Primitives copy; **strings, arrays, lists, sets, maps and objects share**.
- `::` deep-copies.
- `x!` **moves** ownership out of `x` (D81). Only owned types move — strings and collections. The
  source holds nothing afterwards and reading it is an error until it is given a new value:

  ```bee
  new numbers := [1,2,3];
  print consume(numbers!);   -- ownership moves
  print numbers;             -- error: was moved
  let numbers := [10];       -- a new value revives the name
  ```

  This is how a value can be handed somewhere that will mutate it without any lock: nothing else
  can reach it, so there is nothing to race over.
- Compound modifiers require a target that supports the operation. `++ <+ +> << >>` reshape
  collections (§10).

### 6.1 Right-hand sides

A parenthesised comma list on the right of `:=` is read by the number of targets (D29): with one
target it is a **list literal**, with two or more an **expression list**. Parentheses around the
target list are optional and inert.

```bee
new v := (1,2,3);        -- one target: v is a list
let x, y := (1,2);       -- two targets: x = 1, y = 2
let (a, b) := (b, a);    -- identical to: let a, b := b, a
```

### 6.2 Parallel assignment

All right-hand expressions are evaluated **before any assignment**, so `let p, q := q, p;` swaps. A
length mismatch is an error, except a single expression, which broadcasts to every target.

---

## 7. Expressions

### 7.1 Precedence

Tightest first. Level 4 **chains** rather than associating: see §7.5.

| Level | Operators | Assoc |
|---|---|---|
| 12 | `x²` superscript · `a[i]` index · `a[n..m]` slice · `f(...)` call · `x.y` member | left |
| 11 | unary `-` `+` `¬` `~` `@` | right |
| 10 | `^` `√` | right |
| 9 | `*` `/` `%` `\` `×` | left |
| 8 | `+` `-` `±` | left |
| 7 | `«` `»` | left |
| 6 | `&` `\|` `⊕` `∪` `∩` `Δ` | left |
| 5 | `:>` cast · `?` template | left |
| 4 | `=` `≠` `==` `!=` `≡` `≠≡` `is` `≈` `!≈` `~=` `<` `>` `≤` `≥` `∈` `∉` `÷` `⊂` `⊃` | none |
| 3 | `∧` | left |
| 2 | `∨` | left |
| 1 | `..` `.!` `!.` `!!` range construction | none |

**Comparison binds tighter than logic** (D66), so `p = 1 ∧ q = 2` means what it looks like.
Bee-2 ordered these the other way, which made every unparenthesised compound condition an error.
Bitwise operators still bind tighter than comparison, which is the correct half of C's arrangement:
`flags & MASK = 0` groups as `(flags & MASK) = 0`.

`±` sits at additive level so that `a ≈ b ± t` groups the tolerance with `b`.

### 7.2 Arithmetic

`+ - * /` on numerics. `/` on two integers is **integer division truncating toward zero**; use `:>`
for real division. `%` takes the sign of the dividend. Division or modulo by zero raises
`$zero_division`.

Arithmetic **traps on overflow** (D8) — it does not wrap. Semantic analysis records the resolved
type on every expression, so an intermediate that leaves its type's range is caught where it
happens, not where it lands.

`\` is rational division and produces `Q` (§12).

### 7.3 Power and radical

`^` is right-associative. `x√n` is the *n*-th root of `x`. An integer base with a non-negative
integer exponent yields `Z`; anything else yields `R`, except that a `Q` base stays `Q`.

### 7.4 Logic

`¬ ∧ ∨ ⊕`, short-circuiting for `∧` and `∨`. Operands must be `B`. **There is no truthiness**:
`if x do` where `x ∈ Z` is an error (E010) suggesting `x ≠ 0`.

### 7.5 Comparison

| Operator | Meaning |
|---|---|
| `=` / `≠` | equal / not equal **by value** |
| `≡` | equal value **and** type |
| `==` / `!=` | **the same object** (reference identity) |
| `≈` / `!≈` | approximately equal, §12.4 |
| `<` `>` `≤` `≥` | ordering; numerics, `A`, and `S` lexicographically |
| `∈` / `∉` | membership or type test, §7.6 |
| `⊂` / `⊃` | subset / superset |
| `÷` | left operand divides right exactly |

Collections, records and maps compare structurally. Sets are kept sorted, so set equality is
order-independent.

### 7.6 Membership and type tests

`x ∈ T` is a **type test** when `T` resolves to a type name in scope, and a **membership test**
otherwise (D9). Resolution happens at compile time; a name bound to both a type and a variable in
one scope is an error.

For a range subtype the two readings coincide: `'0' ∈ Digit` tests the value domain.

### 7.7 The `@` reference marker

`@x` at an argument position passes `x` by reference to a boxed parameter (D13). Valid only there.
See §9.3.

### 7.8 Suffix conditionals

```
statement if condition ;
```

The statement runs only when the condition holds. Not permitted on `set`, `new` or `type`.

### 7.9 Quantifiers

```
"∀" "(" name "∈" source ")" [ "∧" condition ]
"∃" "(" name "∈" source ")" [ "∧" condition ]
```

Both yield `B`. `∀` over an empty collection is true; `∃` is false.

---

## 8. Ranges

```
(min..max)        both included
(min.!max)        upper excluded
(min!.max)        lower excluded
(min!!max)        both excluded
(min..max:step)   with a step
```

A range built entirely from untyped integer literals is itself untyped, so a control variable
declared `N` may iterate `(0..3)`.

---

## 9. Rules

```
rule_decl ::= "rule" ["."] name [param_list] [ "=>" result_list ] ":"
                statement*
              "return" ";"
param     ::= ["*"] name [ ":" default | ":" lambda_type ] [ "∈" type ]
result    ::= name [ ":" default ] [ "∈" type ] [ "<:" parent ]
```

Every rule ends with `return;` (D18).

### 9.1 Parameters

The parameter list is **flat**, and a post-pass propagates each declared type **leftward** over the
untyped parameters preceding it (D31). So `(a, b, c: 0 ∈ Z)` gives all three type `Z` with `c`
optional. A nested-group reading would need unbounded lookahead.

Optional parameters follow mandatory ones. Once a named argument is used, all following arguments
must be named. A trailing `*` parameter is variadic and collects the rest.

### 9.2 Results

Results are declared variables, zero-initialised at entry; their values at `return` are the rule's
results.

```bee
rule com(x ∈ Z, y: 0 ∈ Z) => (s, d ∈ Z):
  let s := x + y;
  let d := x - y;
return;

new r := com(3,2);        -- one target: a list, (5,1)
new s, d := com(3,2);     -- destructured
new a, _ := com(3);       -- second result discarded
```

A rule with two or more results may not appear inside a larger expression; it may only be the
entire right-hand side of a declaration or assignment. With one target its results collapse into a
list, which requires them to share a type.

### 9.3 Parameter passing

| Parameter | Passing | Written | Callee may modify |
|---|---|---|---|
| primitive `T` | by value | `f(x)` | no |
| `[T]` | an array, by reference | `f(a)` | yes |
| `@T` | a boxed `T`, by reference | `f(@x)` | yes |

`@T` and `[T]` are different types (D88). Inside the body a boxed parameter **is** its element, so
`let n += 1` increments it; `let a += 1` on an array appends. Bee-2 spelled both `[T]` and let the
argument decide at run time, which made a rule's meaning depend on its caller. Only the second needs `@`,
because only the second can modify a caller's own local. Omitting it is E009; adding it to an array
is E231.

### 9.4 Invocation

- **As an expression:** `new r := fib(5);` — only for rules with exactly one result.
- **As a statement:** `apply sort(test);` — `apply` is **mandatory** (D15). If the rule declares
  results, they must be bound or the discard written down (D80): `apply _ := value();`
- Recursion is permitted, bounded by `$max_recursion`. **Mutual recursion is permitted** through
  forward declarations (D71): a rule may be written with a signature and no body, and defined
  later. A forward declaration with no matching definition is an error.

```bee
rule odd(n ∈ Z) => (r ∈ B);          -- forward declaration

rule even(n ∈ Z) => (r ∈ B):
  if n = 0 do
    let r := True;
  else
    let r := odd(n - 1);
  done;
return;
```

### 9.5 Type parameters

A rule may be written once for many types (D86):

```
rule_decl ::= "rule" ["."] name [type_params] [params] ["=>" results] ":" ...
type_params ::= "[" var ["<:" trait] ("," var ["<:" trait])* "]"
```

```bee
rule first_of[T](items ∈ [T]) => (r ∈ T):
  let r := items[0];
return;

print first_of([1,2]);        -- T is Z
print first_of(["a","b"]);    -- T is S
```

- Parameters are **inferred from the arguments**; they are never written at the call site.
- A variable appearing more than once must agree, widening if both occurrences are numeric.
- A **bound** is a trait (§16.3), and is what makes members visible. Without one, a member access
  on `T` is rejected: nothing is known about it.
- Generic rules are **monomorphised** — the backend emits one function per set of type arguments.

Type parameters exist on rules only. Types and traits cannot take them, and there is no variance,
no explicit instantiation, and no specialisation.

### 9.6 Contracts

A rule may state what it requires of its caller and what it promises in return (D75). Contracts sit
between the signature and the body, so a reader looking only at the interface still sees them.

```
rule_decl ::= "rule" ["."] name [params] ["=>" results] ":"
                contract*
                statement*
              "return" ";"
contract  ::= ("require" | "ensure") expression ";"
```

```bee
rule half(n ∈ Z) => (r ∈ Z):
require n ≥ 0;
require n % 2 = 0;
ensure r * 2 = n;
  let r := n / 2;
return;
```

- **`require`** is checked once the parameters are bound, before the body runs.
- **`ensure`** is checked after the body, with the results holding the values the caller will see.
  It may name parameters and results together.
- Both are checked on **every** call, including recursive ones.
- **`old n`** in an `ensure` is what parameter `n` held at entry (D89), so a postcondition can
  describe a change and not only a result:

  ```bee
  rule bump(n ∈ @Z):
  ensure n = old n + 1;
    let n += 1;
  return;
  ```

  `old` appears only in `ensure`, and takes a bare parameter name. On a collection it deep-copies
  at entry, so a rule pays for what it asks about and nothing else.
- A failure raises `$broken_contract` (§22), naming the rule and the condition.
- Every condition must be `B`, and must be **free of side effects**: it may only call rules that
  are isolated in the sense of §17.3. A condition that changes what it is checking is rejected.

### 9.7 Constructors

A rule whose single result is named **`self`** is a constructor (D61). Its **name is also its
type**, held in a separate registry so the two do not shadow each other: `Point(3,4)` is the call,
`∈ Point` is the type.

```bee
rule Point(x, y ∈ Z) => (self ∈ Point):
  new self.x := x;
  new self.y := y;
return;
```

A parent is named on the result, and `super(...)` chains to it:

```bee
rule Square(size ∈ Q) => (self ∈ Square <: Shape):
  let self := super("square");
  let self.sides := 4;
return;
```

### 9.8 Lambdas

```bee
new square := λ(x ∈ Z) => x² ∈ Z;
print square(7);
```

Lambdas are values of type `L`. They close over the enclosing scope, may be stored in collections
and called from there, and may be passed as callbacks with a declared shape:

```bee
rule twice(x ∈ Z, f: λ(v ∈ Z) => Z) => (r ∈ Z):
  let r := f(f(x));
return;
```

---

## 10. Collections

### 10.1 Arrays

Fixed capacity, contiguous, homogeneous. **Indices are 0-based** (D1) — negative indexing composes
cleanly with 0 and incoherently with 1, and two of the three upstream sources already use 0.

```bee
new a ∈ [Z](10);        -- ten elements, zero-initialised
new b := [1,2,3];
print b[0];             -- first
print b[-1];            -- last
let b[*] := 0;          -- every element
let b ++ 5;             -- grow by five
```

An out-of-range index raises `$out_of_range`. `++` allocates a **new** buffer and invalidates every slice taken from the array (D73).

Compatibility ignores capacity — two collections fit when their **element types** do (D41).

### 10.2 Slices

`a[n..m]` is a **view** sharing the array's storage; writing through the slice writes through to
the array. Range forms `.! !. !!` apply. A slice keeps its buffer alive.

```bee
new v := [0,0,0,0,0];
new w := v[0..2];
let w[*] := 7;
print v;                -- [7,7,7,0,0]
```

### 10.3 Lists

Doubly linked, unbounded, ordered, homogeneous. `()` is an empty list; `(x,)` is a one-element
list; `(x)` is **grouping**, not a list (D32).

Operations: `<+` append · `+>` prepend · `<<` drop first *n* · `>>` drop last *n* · `+`
concatenate.

**Attributes.** Lists, arrays and strings carry `head`/`first`, `tail`/`last`, and
`length`/`count`/`capacity` without a call. Both spellings work on all three, since they mean the
same thing; §10.3 names a list's ends `head` and `tail`, §10.1 an array's `first` and `last`. Taking
`head` of an empty collection raises `$out_of_range`. A set has no ends, being unordered.

### 10.4 Sets

Sorted, unique, homogeneous, unindexed. `{}` is the empty set (D42).

```bee
print {3,1,2,1};        -- {1,2,3}
print {1,2} ∪ {2,3};    -- {1,2,3}
print {1,2,3} ∩ {2,3};  -- {2,3}
print {1,2,3} Δ {2,3,4};-- {1,4}
print {1,2} ⊂ {1,2,3};  -- 0B1
let s += 9;             -- add
let s -= 1;             -- remove
```

Indexing a set is an error; test membership with `∈`.

### 10.5 Maps

Key to value, kept in key order. Keys are numeric, `A` or `S`. A brace literal is a map when its
keys are **expressions** (D44, D48).

```bee
new m := {1:"a", 2:"b"};
let m[3] := "c";        -- assignment creates
print m[2];
scrap m[1];             -- remove a key
print 1 ∈ m;            -- key membership
for key, value ∈ m do   -- pair iteration
  print (key, value);
repeat;
```

Maps display as `{(k:v),(k:v)}` (D45), resolving a conflict between two upstream chapters.
Iterating a map with one variable walks its keys.

### 10.6 Builders

```
{ expression | name ∈ source [ ∧ filter ] }      set
[ expression | name ∈ source [ ∧ filter ] ]      array
{ (key:value) | name ∈ source [ ∧ filter ] }     map
```

```bee
print { x | x ∈ (1..5) ∧ (x % 2 = 1) };   -- {1,3,5}
print { x² | x ∈ (1..3) };                -- {1,4,9}
print [ x | x ∈ (1..9:2) ];               -- [1,3,5,7,9]
print { (x:x²) | x ∈ (0.!10) ∧ (x % 2 = 0) };
```

Inside `{}` or `[]`, a **top-level `|` is the builder separator**, not bitwise-or (D43). Bitwise-or
in a collection literal must be parenthesised: `{(1 | 2)}`. This matters because `|` binds tighter
than `∈`, so without the rule a builder parses as `{(x|x) ∈ (1..3)}` — silently wrong rather than
an error.

---

## 11. Strings

`S` is mutable, growable and **shared by `:=`**, so `let s += "x"` is visible to every holder.

| Operator | Meaning |
|---|---|
| `+` | concatenate; the other operand is coerced to its display form (D22) |
| `*` | replicate: `'-' * 19`, on `A` or `S`, yielding `S` |
| `?` | template interpolation, §11.1 |

`length(s)` counts code points. `s[i]` yields `A`; a slice of `S` is `S`.

### 11.1 Templates

`template ? (arguments)` fills placeholders left to right. After `?`, a **written** parenthesised
list is the argument list and need not be homogeneous; anything else is a single argument, so
`"#[*]" ? (array)` sees the whole array (D47).

| Placeholder | Renders |
|---|---|
| `#(z)` `#(n)` | integer |
| `#(r)` | real |
| `#(s)` | single-quoted |
| `#(q)` | double-quoted |
| `#(a)` | one character, or a code point as a character |
| `#(b)` `#(h)` | binary, hexadecimal |
| `#[*]` | every element, comma-separated |
| `#[i]` | element by index |
| `#[key]` | map value by key |

The numeric picture is `#(ap:l.d)`: alignment `a` is `>` right, `<` left, `=` centre; padding `p` is
`_` for **spaces** or `0` for zeros (D49); `l` is width and `d` decimals.

```bee
print "n=#(z) s=#(s)" ? (5, "hi");   -- n=5 s='hi'
print "pi=#(r:0.3)" ? (3.14159);     -- pi=3.142
print "#(>0:5)" ? (42);              -- 00042
```

---

## 12. Rational numbers

`Q` is **exact binary fixed point**: a scaled integer `raw / 2ⁿ` in an `m+n+1` bit signed container.
No floating point appears in the arithmetic chain, so results are reproducible and saturation is
detectable rather than silent.

### 12.1 Containers

`Q(m,n)` has `m` integer bits and `n` fractional bits, precision `2⁻ⁿ`, and range
`[-2ᵐ .. 2ᵐ-2⁻ⁿ]`. Bare `Q` is `Q(14,17)` — 32 bits, precision ≈ 10⁻⁵.

`Q(5,2)` is 8 bits, −32.00 to 31.75, step 0.25.

The spelling is `Q(m,n)`, not `Qm.n` (D58): `Q5` is a valid identifier, so `Q5.2` arrives as an
identifier, a dot and an integer — the shape of member access. `Q5.2` is recognised in type position
only to point at the right form.

### 12.2 Literals

`p\q` is a rational literal and **binds tighter than any operator** (D62), because the
documentation calls it a literal. Without this `1\4 / 1\8` parses as `((1\4) / 1) \ 8`.

```bee
print 1\2;      -- 0.5
print 1\32;     -- 0.03125
print 1\3;      -- 0.33334, rounded to $precision
```

Between non-literals, `\` is the rational-division operator at multiplicative precedence.

### 12.3 Arithmetic

Addition and subtraction align scales; multiplication shifts right by `n` with round-half-away-
from-zero; division shifts left before dividing. Mixing `Q` with any other numeric keeps fixed
point. Exceeding the container raises `$value_overflow`.

```bee
print 1\4 + 1\8;    -- 0.375, exactly
print 1\4 / 1\8;    -- 2
```

`Q` widens to `R` implicitly; `R` to `Q` needs a cast. `Q :> Z` truncates toward zero.

### 12.4 Approximate comparison

`a ≈ b` uses `$precision`; `a ≈ b ± t` uses `t`.

```bee
set $precision: 0.001;
print (0.333 ≈ 1\3);        -- 0B1
print (0.25 ≈ 1\3 ± 0.1);   -- 0B1
```

### 12.5 Display

`Q` prints rounded to `$precision`, trailing zeros stripped. `exact(q)` returns the full value, and
a template picture may ask for more digits than `$precision` (D77):

```bee
print 1\10;            -- 0.1
print exact(1\10);     -- 0.09999847412109375
```

One tenth has no finite binary form, so `Q` cannot hold it exactly. `exact` is how a programmer
tells which values are exact and which are approximations. The upstream examples showing `1\16` as
`0.062` are inconsistent with their own stated precision of 10⁻⁵; the exact value is `0.0625`.

---

## 13. System names

| Name | Meaning | Settable |
|---|---|---|
| `$error` | the current error object: `code`, `message` | no |
| `$precision` | tolerance for `≈` (10⁻⁵) | yes |
| `$deci` `$centi` `$mili` `$micro` | 10⁻¹ 10⁻² 10⁻³ 10⁻⁶ | yes |
| `$max_iteration` | per-cycle iteration ceiling | yes |
| `$max_recursion` | recursion depth ceiling (10000) | yes |
| `$pro` `$lib` | module path roots, §20 | no |

Settable constants are set at **module level only**: `set $precision: 0.01;`. Any other `$` name is
rejected.

---

## 14. Control flow

Blocks open with a keyword and `:` or `do`, and close with `done`, `repeat` or `return` (D4).

### 14.1 `if`

```bee
if condition do
  ...
else if condition do
  ...
else
  ...
done [label];
```

`else if` is **always a ladder rung**, never `else` containing a nested if (D34) — the two differ
only in how many `done`s follow, which is not decidable with one token of lookahead. Nothing is
lost: a rung means what a nested if means, with one fewer terminator. A plain `else` branch may not
begin with a bare `if`; wrap it in `start` to nest.

`when` is not a synonym for `if` (D5).

### 14.2 `start`

```bee
start [label]:
  -- declarations
do
  -- statements
done [label];
```

### 14.3 `cycle`

```bee
cycle [label]:
  -- declarations, evaluated once
( do | while condition do )
  -- body
[ then
  -- runs once, when the while condition first fails ]
repeat [label] [ if condition ];
```

`repeat if` tests after each iteration. With no condition anywhere, only an interruption ends the
loop, bounded by `$max_iteration`.

### 14.4 `for`

```bee
[ cycle [label]: declarations ]
for [∀] name [, value] ∈ iterable do
  ...
[ then ... ]
repeat [label];
```

The `cycle` prefix is optional and exists only to provide a declaration region and a label.

**`∀` claims the iterations are independent** (D82), and the compiler checks it. An iteration may
write only its own locals and an element its control variable selects; it may not do I/O, write
anything else, or call a rule that is not isolated (§17.3). A plain `for` has no such restriction.

```bee
for ∀ i ∈ (0.!6) do
  let squares[i] := i * i;      -- a different element each time
repeat;
```

Nothing runs in parallel yet; the claim is checked. Two variables require a map (§10.5). Iterables are ranges, domains,
arrays, lists, sets, maps and strings.

### 14.5 `match`

```bee
match [all|one] selector [label]:
when value, value do
  ...
other
  ...
done [label];
```

**This construct is designed here, not read from a specification (D51).** The upstream chapter is
four sentences of prose, a broken diagram link and one type declaration; it states that a match has
an "all" variant and a "one" variant and never shows the syntax of either. The design stays as close
to the rest of the language as possible: it opens with a keyword and `:`, branches use `do`, it
closes with `done;`, and `when`/`other` keep the meanings the trial chapter gives them.

- `one` (the default) runs the first matching branch; `all` runs every matching branch.
- **A `one` match must be total** (D72): a selector matching no branch would otherwise do nothing
  at all, silently. `all` is a filter and needs no default.
- **Totality is inferred where it can be** (D76). `other` is required only when the branches cannot
  be shown to cover the selector's domain — a domain counts as finite when it is `B`, or a range
  subtype over at most 1024 integers. A partial match names the values it misses.
- A branch matches by **membership** when its value is a set, list, array, map or range, and by
  **equality** otherwise — including strings, so `when "a"` is not "contains an a" (D50).
- `all` and `one` are contextual words, not reserved.

This ruling is marked provisional and should yield if upstream ever specifies `match`.

### 14.6 Transfer

| Statement | Effect |
|---|---|
| `stop [label] [if c];` | leave the cycle |
| `next [label] [if c];` | next iteration |
| `redo [label] [if c];` | restart the cycle; the declaration region is **not** re-run |
| `exit [if c];` | leave the rule; results keep their current values |
| `over;` | end the program with status 0 |
| `panic n;` | end the program with status *n* |

An unlabelled transfer binds to the innermost enclosing cycle. A label naming no enclosing cycle is
a compile-time error.

---

## 15. Error handling

```bee
trial [label]:
  -- declarations, run once
try [code]:
  -- a job
case condition do
  -- a handler
miss
  -- no case matched
final
  -- always runs
done [label];
```

| Statement | Effect |
|---|---|
| `pass;` | skip the rest of this job, continue with the next |
| `fail [code,] [message];` | record the error, continue with the next job |
| `raise [code,] [message];` | set the error and jump to the cases |
| `abort;` | jump straight to `final` |
| `resume;` | the error is handled; continue at the **next** job |
| `retry;` | restart the jobs; the declaration region is **not** re-run |

`raise "text"` with no code uses 200, the user-error code.

**A trial is a state machine, not host try/catch.** `resume` continues at the job *after* the one
that raised, so a handler hands control back into the middle of the job sequence — which no
try/except construct can express.

`retry` not re-running declarations is the same rule as `redo`, and is load-bearing: the documented
retry-counter pattern depends on the counter surviving.

Falling off the end of a `case` resolves the error. `$error` holds `code` and `message`, and is
empty outside a trial.

---

## 16. Objects

Records with named fields, resolved at compile time.

```bee
type Point: {x ∈ Z, y ∈ Z} <: Object;

new p ∈ Point;          -- {x: 0, y: 0}
let p.x := 3;
new q := {x: 10, y: 20};
print q.y;
```

A brace literal with **bare identifier keys** is an object; a map needs expression keys (D48). The
documentation writes maps as `{key1:"value1"}` and objects as `{a1:1}` — identical syntax. Something
had to break, and the map form has a natural repair (quote the key) while an object's field names
are not values.

Objects are shared by `:=` and copied by `::`, and compare structurally. `Object` is the root type.
Constructors and inheritance are in §9.5.

---

### 16.3 Traits

A trait names the methods a type must provide, and may carry the contracts every implementation
inherits (D84).

```
trait_decl ::= "trait" ["."] Name ":" method* "done" ";"
method     ::= "rule" name [params] ["=>" results] contract* ";"
```

```bee
trait Shape:
  rule area() => (a ∈ R)
  ensure a > 0;
  rule name() => (n ∈ S);
done;
```

A type declares which trait it satisfies on its constructor's result, and writes the methods inside
the constructor, where `self` is in scope:

```bee
rule Circle(radius ∈ R) => (self ∈ Circle <: Shape):
  new self.radius := radius;
  rule .area() => (a ∈ R):
    let a := 3.14159 * self.radius * self.radius;
  return;
  rule .name() => (n ∈ S):
    let n := "circle";
  return;
return;
```

- Conformance is **nominal**: the compiler checks every required method is provided, with matching
  arity and matching parameter and result **names** — the trait's contracts are evaluated in the
  implementation's scope and refer to them.
- A trait-typed parameter accepts any implementer: `rule describe(s ∈ Shape)` takes a `Circle` or a
  `Square`, dispatching on the object.
- A trait's `require` and `ensure` conditions become every implementation's, checked on every call.
  A violation is reported at the **trait's** line, because that is where the promise was made.
- An object may have methods without satisfying any trait.

## 17. Concurrency

### 17.1 Coroutines

A rule containing a bare `yield;` is a **coroutine** (D60). `begin` starts it; `yield v << name`
resumes it and takes its next value.

```bee
rule ticker(n ∈ N) => (v ∈ N):
  for i ∈ (1..n) do
    let v := i;
    yield;
  repeat;
  let v := 0;
return;

begin ticker(3);
yield r << ticker;      -- 1, then 2, then 3, then 0
```

A coroutine publishes its **final** result when its body ends, not the last value it yielded, which
is what makes the terminating-sentinel pattern work. Several coroutines may be live at once, each
keeping its own state; `tests/demos/producer_consumer.bee` runs two against a shared channel.

Coroutines are implemented as suspended generators rather than threads (D63), so they work on hosts
with no threading — including a browser.

### 17.2 Jobs

Any other rule started with `begin` is a **job**. `begin` queues the call; `wait` runs the queue.

```bee
new results ∈ (Z);
begin results <+ scaled(1);
begin results <+ scaled(2);
wait;
print results;          -- (10,20)
```

**Jobs run in start order, not in parallel (D59).** The upstream example states that results arrive
"ordered by completion" — by how long each happens to take. That is a race, and a race is not a
testable specification.

The reason is not implementation convenience: **Bee has no memory model.** No locks, no atomics, no
ordering guarantees, and no statement anywhere about what two threads touching one array means.
There is nothing a truly parallel `begin` could correctly mean yet. Deterministic ordering keeps
every program using it testable.

The cost is stated rather than implied: **`begin` gives concurrency's shape without its speedup.**

### 17.3 Isolation

Real parallelism needs a memory model, and Bee has none. D64 supplies the smallest one that works:
a job may run in parallel **only if it is isolated** — reading no module variable that any rule
writes (D78), writing
through no reference parameter, performing no I/O, starting no other work, and calling only
isolated rules. Under that restriction no interleaving can change a result, so no locks are needed.

Isolation is decided statically and reported by:

```
python3 -m bee --isolation program.bee
```

Nothing runs in parallel yet. The analysis establishes which jobs *could*, which is the part that
has to be true before the rest is worth building.

**Bee has no locks and will not get them** (D65). The design removed pointers on safety grounds and
made every mutation of a caller's variable visible at the call site; reintroducing data races
through a lock the programmer must remember to hold would undo that. Any future widening of
parallelism restricts aliasing — ownership, channels, immutability — rather than guarding access.

`wait n;` evaluates its argument; elapsed time is simulated.

---

## 18. Input and output

| Statement | Effect |
|---|---|
| `write expr;` | append to the console buffer |
| `print expr;` | append, flush, newline |
| `print;` | flush and newline |
| `print (a, b, c);` | append each, comma-separated |
| `print (a, b, sep:" ");` | with an explicit separator |
| `read var;` | flush, read a line, parse it as the variable's type |
| `read (prompt, var);` | prompt, then read |

After `print`, `write` or `read`, a parenthesised comma list is the **argument list**, never a list
literal (D28). To print a literal list, bind it first or double the parentheses.

Display forms: `Z`/`N` decimal · `R` shortest round-tripping · `Q` rounded to `$precision` · `B` as
`0B0`/`0B1` · `A` bare · `S` unquoted · arrays `[a,b,c]` · lists `(a,b,c)` · sets `{a,b,c}` · maps
`{(k:v)}` · objects `{n: v}`.

---

## 19. Built-ins

| Built-in | Signature | Notes |
|---|---|---|
| `length(x)` | collection or string → `N` | elements or code points |
| `capacity(x)` | array → `N` | allocated size |
| `count(x)` | collection → `N` | alias of `length` |
| `kind(x)` | any → `S` | the name of a value's type, **for display** (D87) |
| `exact(q)` | `Q` → `S` | every fractional digit, which display rounds (D77) |

### 19.1 The standard library

Always in scope, and polymorphic where it makes sense (D85):

| Group | Rules |
|---|---|
| Numbers | `abs` `min` `max` `clamp` `sign` `floor` `ceil` `round` `gcd` |
| Characters | `ord` `chr` |
| Text | `upper` `lower` `trim` `reverse` `find` `contains` `replace` `split` `join` |
| Reading | `parse_z` `parse_r` |
| Collections | `sum` `sorted` `first` `last` `empty` `reverse` |

`abs`, `min`, `max` and `clamp` keep their argument's type, so they serve `Z`, `N`, `R` and `Q`
alike. `round` goes to the nearer integer, halves away from zero. `find` gives −1 when the text is
absent. `parse_z` and `parse_r` raise `$type_mismatch` on text that is not a number.

These are built-ins rather than a library written in Bee because Bee has no generics; see D85.

`type` is both a keyword and a built-in; one token of lookahead separates them — `kind(` is the
call, `type Name` is the declaration (D36).

---

## 20. Modules

```
use [ $root "." ] path [ "." "(" names | "*" ")" ] [ "as" qualifier ] ";"
alias name = qualifier.member ;
hide qualifier.member ;
with qualifier ("," qualifier)* do ... done ;
```

### 20.1 Paths

Components are separated by `.`, and there are two roots (D52):

| Root | Resolves to |
|---|---|
| `$pro` | the project root — the directory holding the main module |
| `$lib` | `lib/` under the project root |
| *(none)* | relative to the directory of the loading module |

The upstream corpus spells paths four different ways — `$bee_lib.folder.module`,
`$pro.src.demo_module`, `$pro_src.test_module`, `lib_folder/test_module`. Two roots and one
separator cover every documented layout.

`use path.(*)` loads every module in a folder; `use path.(a, b)` loads the named ones.

Path components may be **keywords**, because module names come from file names and a filesystem
does not know Bee's keyword list (D57). If the *implied* qualifier would be a keyword, an explicit
`as` is required.

### 20.2 Visibility

A leading `.` on `set`, `new`, `type` or `rule` marks a **public** member; everything else is
private. The marker is a parser concern, not a lexical one (D53): it appears only immediately after
a declaration keyword, so it never collides with member access.

Visibility restricts what a **qualifier** can reach, not what a module can do internally (D56). A
private rule is callable anywhere in its own file, and a `hide` blocks only the importing module's
view.

### 20.3 Loading

A module is loaded **once per program**, cached by resolved path, so two modules using a third share
one instance and its state (D54). Circular loading is a compile-time error naming the chain. A
module defining `rule main` cannot be loaded.

### 20.4 `with`

`with q do ... done;` suppresses the qualifier inside the block. If two suppressed modules export
the same name, that is an error naming both (D55) — silent shadowing across a module boundary is
what the language's explicitness principle rejects.

---

## 21. Program structure

```
module ::= use* module_statement* rule_declaration+
```

Module-level statements are `set`, `new`, `type`, `alias` and `hide`. They run once, in source
order, before `main`.

**No hoisting.** Every identifier must be declared textually before use, so `main` is
conventionally last and mutual recursion cannot be written.

A project is laid out as:

```
project/
  main.bee          the main module: has rule main, cannot be loaded
  src/              secondary modules, reached as $pro.src.x
  lib/              library modules, reached as $lib.x
```

---

## 22. Errors

Every runtime error is fatal; there is no recovery outside a `trial`.

| Code | Name | Raised by |
|---|---|---|
| 2 | `$unexpected_error` | a failed `expect`, recursion or iteration limits |
| 100 | `$zero_division` | division or modulo by zero |
| 102 | `$value_overflow` | arithmetic overflow, failed narrowing, `Q` saturation |
| 103 | `$out_of_range` | a bad index or slice, a value outside a range subtype |
| 104 | `$type_mismatch` | a failed `read` parse |
| 105 | `$broken_contract` | a failed `require` or `ensure` (§9.5) |

Arithmetic **traps** rather than wrapping (D8).

---

## 23. Diagnostics

Compile-time diagnostics are numbered by phase, and each names the construct and, where useful,
the rewrite:

| Range | Phase |
|---|---|
| E001–E031 | lexical |
| E100–E119 | syntactic |
| E201–E246 | semantic |
| W001–W002 | warnings: shadowing, type naming |

The suite in `tests/errors/` pins sixteen of these to specific programs.

A runtime error also reports the **call stack** — how the program arrived, innermost frame first —
rather than only where it stopped.

### 23.1 Tools

| Command | Does |
|---|---|
| `--run` | interpret |
| `--check` | analyse only |
| `--format` | reformat on stdout, preserving comments |
| `--isolation` | report which jobs could run in parallel (§17.3) |
| `--emit-c FILE` / `--show-c` / `--build` / `--wasm` | compile |
| `--tokens` / `--ast` / `--print` | inspect a pipeline stage |
| `--lsp` | run a language server over stdio |

The formatter emits parentheses only where precedence requires them, keeps every comment, and is
idempotent. It refuses to touch a file that does not parse.

The language server provides diagnostics, hover types, go-to-definition, document symbols and
formatting.

---

## 24. Memory

`:=` shares references; `::` deep-copies. Reference counting is specified (D2), and the reference
implementation relies on the host's tracing collector, which subsumes it and reclaims cycles as
well — cycles are constructable now that objects exist (`let a.next := a;`).

The observable semantics are exactly as specified and strictly stronger. **A native backend must
implement this properly**; this is the one place where the reference implementation is easier than
the real thing.

---

## 25. Grammar summary

```
module       ::= use* module_stmt* rule_decl+
use          ::= "use" path [ "as" name ] ";"
module_stmt  ::= const_decl | var_decl | type_decl | alias | hide

rule_decl    ::= "rule" ["."] name [params] ["=>" results] ":" stmt* "return" ";"

stmt         ::= const_decl | var_decl | type_decl | assign
               | apply | begin | wait | yield | io | expect | scrap
               | transfer | raise
               | if_stmt | start_stmt | cycle_stmt | for_stmt
               | match_stmt | trial_stmt | with_stmt
               | stmt "if" expr ";"

expr         ::= (see §7.1)
primary      ::= literal | name | "$" name | call | index | slice | member
               | lambda | quantifier | array_lit | list_lit | set_lit
               | map_lit | object_lit | builder | "(" expr ")"
```

---

## 26. Deliberately not in Bee-3

| Feature | Why |
|---|---|
| Mixins, default implementations, trait inheritance | Traits are nominal and signature-only (D84). |
| True parallelism | Needs a memory model first (D59). |
| Graphics and drawing | §22 upstream defines symbols and four keywords and says nothing about what any of them do — no coordinate system, no rendering target, no colour model, no example that draws anything. Implementing it means designing a 2D runtime, not reading a specification. The chapter is labelled research. |

| `C` `D` `T` `X` `U` `O` types | Complex, Date, Time, Text, Unicode, Object-as-dictionary. |
| Forward declarations | Deferred; mutual recursion is unavailable as a result. |
| Matrix bracket-art literals | `⎡⎢⎣` layout-sensitive notation. |

Each is rejected with a diagnostic naming the feature, so nothing silently half-works.

---

## 27. Conformance

An implementation conforms when:

1. Every program in `tests/demos/` produces exactly its `.expected` output.
2. Every program in `tests/errors/` produces its specified diagnostic.
3. Every construct in §26 is rejected with a diagnostic naming it.
4. Printing any parsed program and reparsing it yields an identical tree.

`tests/legacy/` holds the 34 upstream demo files verbatim. They are **not** conformance tests: they
are written in a different dialect (D11–D18) and several contain bugs, catalogued in `DECISIONS.md`.

---

## 28. On the rulings

The 62 rulings in `DECISIONS.md` are not stylistic preferences. Each records a place where the
upstream sources contradict each other, or leave a gap that no implementation can straddle, and
each states the evidence on both sides before deciding.

They fall into three kinds, and the distinction matters when arguing about them:

- **Readings** (D1–D58, D60–D62) resolve a contradiction or fill a gap. A reading can be shown
  wrong by pointing at the documentation.
- **Designs** (D51 for `match`, D59 and D64–D65 for concurrency, D84 for traits) supply something
  the sources do not contain at all. A design can only be argued about.
- **Changes** (D66–D89) deliberately depart from a design that was clear but unsafe. Each names
  what was wrong and what it costs, so the trade can be disputed on its merits.

The last group is what makes this Bee-3 rather than another implementation of Bee-2.

---

## 29. What Bee-3 changes, and what it guarantees

### 29.1 The twenty-four changes

| | Change | Breaking | Ruling |
|---|---|---|---|
| 1 | Comparison binds tighter than logic | yes | D66 |
| 2 | `**` opens a comment only at the start of a line | yes | D67 |
| 3 | Every operator has an ASCII spelling | no | D68 |
| 4 | `==` and `!=` compare values; `is` compares identity | yes | D69 |
| 5 | Shadowing is an error | yes | D70 |
| 6 | Forward declarations, so mutual recursion is writable | no | D71 |
| 7 | A `one` match must have `other` | yes | D72 |
| 8 | Reshaping an array invalidates its slices | yes | D73 |
| 9 | Comparisons chain, as in mathematics | no | D74 |
| 10 | Rules may carry `require` and `ensure` contracts | no | D75 |
| 11 | Match totality is inferred where the domain is finite | no | D76 |
| 12 | `exact(q)` shows a rational in full | no | D77 |
| 13 | Only a *written* module variable counts as shared state | no | D78 |
| 14 | A scalar read but never written is an error | yes | D79 |
| 15 | Discarding a rule's results must be written down | yes | D80 |
| 16 | `x!` moves ownership | no | D81 |
| 17 | `for ∀` claims independence, and it is checked | yes | D82 |
| 18 | `Λ` and `Φ` are predeclared geospatial domains | no | D83 |
| 19 | Traits: nominal conformance, carrying contracts | no | D84 |
| 20 | A standard library of 27 rules | no | D85 |
| 21 | Type parameters on rules, monomorphised | no | D86 |
| 22 | The built-in is `kind`, not `type` | yes | D87 |
| 23 | `@T` is a boxed parameter, distinct from `[T]` | yes | D88 |
| 24 | `old n` in a postcondition | no | D89 |

Each removes a way for a **correct-looking program to mean something other than it looks like**.
That is the common thread, and it is the only criterion applied: no change here was made for
elegance, familiarity or taste alone.

### 29.2 What the language guarantees

Bee-3 guarantees, statically:

- **No undeclared use.** Every name is declared before use; no hoisting, no implicit creation.
- **No implicit narrowing.** Converting `R` to `Z`, or any value to a smaller type, requires `:>`.
- **No truthiness.** A condition is `B` or it is an error; `if x` on a number does not compile.
- **No shadowing.** One name means one thing in any scope a reader can see.
- **No silent fall-through.** A `one` match covers every selector.
- **No unowned references.** There are no pointers and no pointer arithmetic; a caller's variable
  can only be modified through a parameter marked `@` at the call site.
- **No data races**, because there is no shared mutable state across jobs (D64) and no locks
  to forget (D65).

and at run time:

- **No unchecked promises.** A rule's `require` and `ensure` conditions are verified on every call.
- **No forgotten assignment.** A scalar read but never written is rejected (D79).
- **No silently dropped answer.** A rule's results are bound, or the discard is written (D80).
- **No use after move.** A moved name holds nothing until reassigned (D81).
- **No silent overflow.** Integer arithmetic traps; it does not wrap.
- **No out-of-domain values.** A range subtype constrains every store.
- **No stale views.** A slice whose array has been reshaped fails loudly.
- **No inexact fixed point.** `Q` arithmetic is exact binary fixed point, with saturation detected.

What it does **not** guarantee: memory exhaustion, non-termination, and the correctness of the
program's logic. It is a language for writing programs that mean what they say, not for proving
they say the right thing.

### 29.3 Migrating from Bee-2

Six changes are breaking. In practice a Bee-2 program needs:

1. **Nothing for D66.** Compound conditions were already parenthesised, because the old precedence
   made bare ones an error. Parenthesised code parses identically.
2. **Nothing for D67** unless a `**` comment appears mid-line, which nothing in the corpus does.
3. **`is` for identity comparisons**, if any exist. `==` now means value equality.
4. **A rename** wherever an inner declaration shadowed an outer one.
5. **An `other` branch** on every `one`-variant match.
6. **Care with slices**, which now fail rather than reporting stale data after a resize — this
   turns a silent wrong answer into a diagnosable one.

The whole 18-program conformance corpus needed exactly two edits: one rename and eight `other`
branches in the test suite.

---

---

## 30. What the checks cost

Bee-3 puts safety above performance, so the price should be stated rather than assumed (D90).
Measured at 60 million iterations, `cc -O2`, against a noise floor from timing one program against
a copy of itself:

| Check | Cost | May be omitted |
|---|---|---|
| Contracts (`require`, `ensure`) | within noise | yes |
| Range domains | **−17%**: faster with the check | yes |
| Index bounds | within noise | no |
| Overflow traps | not measurable separately | no |

The domain figure is not a mistake. Emitting the check tells the optimiser the value's range, and
it narrows the following arithmetic accordingly — the check pays for itself.

```
python3 -m bee --unchecked=contracts,domains --build fast program.bee
python3 tools/bench/measure.py
```

**Overflow trapping and index bounds cannot be omitted.** The measurement gives no reason to, and
switching them off turns a caught mistake into silent corruption. `--unchecked` is a compiler flag
and cannot be written in source: a library able to disable checks for its caller would be a worse
hazard than any it removes.

---
