# Bee Types

Bee uses a gradual typing system with type inference. While dynamic typing can be fragile and error-prone, Bee enforces strong, explicit typing rules where every data value is constrained by a fixed data type.

- Bee provides predefined primitive data types.
- Sub-types and composite types can be declared to introduce additional constraints.
- Variable and expression data types can be introspected at runtime using `type()`.

## Primitive Types

Primitive data types are represented by single uppercase letters:

| Alias | Code | Description |
| :---| :---| :---|
| Boolean | B | Boolean or 8-bit number (0 = False, ≥ 1 = True) |
| Alpha | A | Alphanumeric ASCII character ('0'..'9', 'a'..'z', 'A'..'Z') |
| Unicode | U | Unsigned 32-bit Unicode code point (UTF-32) |
| Rational | Q | Fixed-point binary rational number (e.g. 1/2, Q(14,17)) |
| Natural | N | Unsigned 64-bit positive integer [0..+] |
| Integer | Z | Signed 64-bit integer [-..+] |
| Real | R | Double-precision 64-bit floating point (-..+) |

Notes:
- Primitive data types are allocated directly on the stack or in CPU registers.
- Integer bit width can be constrained using parentheses (e.g., `Z(32)` = 32-bit integer).

## Constant Literals

Symbolic representations for primitive data type values:

| Example | Type | Literal Character Set |
| :---| :---| :---|
| `'a'` | A | Single ASCII character |
| `'Ω'` | U | Single Unicode code point |
| `"str"` | S | UTF-8 encoded string literal |
| `0B0`, `0B1` | B | Binary boolean literals |
| `1234567890` | N | Positive unsigned integer |
| `+0`, `-10` | Z | Signed integer literal |
| `U+FFFF` | U | 16-bit hex Unicode code point |
| `U-FFFFFFFF` | U | 32-bit hex Unicode code point |
| `0.05` | R | Floating-point real literal |
| `1\2` | Q | Rational number fraction literal |
| `1E10`, `1e10` | R | Scientific notation floating-point |

Notes:
- Primitive types are ordered and comparable.
- Primitive literals are immutable values.

## Special Types

Special reference types manage complex data structures:

| Alias | Type | Description |
| :---| :---| :---|
| Complex | C | Pair of double-precision floats (`9r+9j`) |
| String | S | UTF-8 encoded double-quoted string |
| Date | D | Calendar date literal (`DD/MM/YYYY`) |
| Time | T | Time literal (`HH:MM:SS,MS`) |
| Lambda | L | Lambda function reference |

## Collection Types

Bee defines collection literals using specialized delimiters:

| Delimiter | Collection Type | Description |
| :---| :---| :---|
| `()` | List | Ordered sequence of elements |
| `[]` | Array / Matrix | Fixed-size ordered array or multi-dimensional matrix |
| `{}` | Set / Map / Object | Unordered set, key-value hash map, or object literal |

Notes:
- All collection instances are heap-allocated reference types.
- Key-value pairs in maps and objects use the colon delimiter (`key: value`).

## Type Declarations

Custom sub-types and type aliases are created using the type declaration statement. Aliases use `:`, while sub-types use `<:` (inheritance/subtyping):

```bee
-- declare new type alias / sub-type
type Type_Identifier: type_descriptor <: super_type;

-- declare variable using custom type
new var_name ∈ Type_Identifier;

-- declare multiple variables
new var1, var2 ∈ Type_Identifier;
```

Rules:
- Custom type identifiers must start with an uppercase letter.
- Sub-types enforce value ranges or domain restrictions on a super-type.

## Range Type

A range defines a sub-set of consecutive integers between lower and upper limits using parenthesis `()` and dot delimiters `..` or `!`:

```bee
range ::= (min..max);  -- both limits included
range ::= (min.!max); -- upper limit excluded
range ::= (min!.max); -- lower limit excluded
```

Examples:

```bee
rule main:
  print (0..5); -- 0, 1, 2, 3, 4, 5
  print (0.!5); -- 0, 1, 2, 3, 4
  print (0!.5); -- 1, 2, 3, 4, 5

  pass if 32667 ∈ (0..+); -- unbounded upper limit
  pass if -32668 ∈ (-..0); -- unbounded lower limit
return;
```

Ranges can also bound character domains:

```bee
type .Digit:     ('0'..'9')       <: Z;
type .Capital:   ('A'..'Z')       <: A;
type .Lowercase: ('a'..'z')       <: A;
type .Latin:     (U+0041..U+FB02) <: U;

rule main:
  pass if '0' ∈ Digit;
  fail if 'x' ∈ Capital;
  pass if 'X' ∈ Capital;
  pass if 'e' ∈ Latin;
return;
```

## Domain Type

A domain is a range with an explicit step ratio, enabling rational or floating-point sequences:

```bee
type Domain: (min..max: ratio) <: Super_Type;
```

Examples:

```bee
-- rational number step sequence
print (0..1: 1\4); -- 0\4, 1\4, 2\4, 3\4, 1

-- floating-point step sequence
print (0..1: 0.25); -- 0.00, 0.25, 0.50, 0.75, 1.00
```

## Constant Declarations

Constants are bound to immutable literals using the `set` keyword:

```bee
-- constant declaration with explicit type
set constant_name: literal ∈ type_name;

-- constant declaration with type inference
set constant_name := literal;
```

Public module constants use the `.` prefix:

```bee
set .PI := 3.14159 ∈ R;
set forall1: U+2200 ∈ A; -- Symbol: ∀
```

## Variable Declarations

Variables are declared using the `new` keyword and initialized or mutated using assignment operators:

| Operator | Purpose |
| :---| :---|
| `∈` | Specify data type constraint |
| `:` | Parameter initial value / map key-value pair-up |
| `:=` | Type inference assignment / variable mutation |
| `::` | Deep copy / clone operator |
| `<:` | Supertype declaration |

Examples:

```bee
-- primitive variable declarations with explicit type
new var_name ∈ type_name;
new var_name: initial_value ∈ type_name;

-- variable declaration with type inference
new var_name := expression;

-- multiple variable declaration
new var1, var2 ∈ TypeName;
new var1, var2 := expression;
```

## Variable Mutation

Variable values are modified using `let` statements with assignment modifiers:

```bee
rule main:
  new a: 10, b: 0 ∈ Z;

  let b := a + 1; -- assign 11
  let b += 1;     -- increment to 12
  expect b = 12;

  -- swap values
  new x: 1, y: 2 ∈ Z;
  let x, y := y, x;
return;
```

Supported mutation modifiers: `{ :=, ::, +=, -=, *=, /=, ^=, %= }`.

## Type Conversion

Type conversion is performed explicitly using the `:>` cast operator:

```bee
rule main:
  new a: 0 ∈ Z;
  new v: 10.5 ∈ R;

  -- explicit truncation cast
  let a := v :> Z;
  print a; -- 10

  -- explicit conversion
  new x := a :> R;
  print x; -- 10.0
return;
```

## Alphanumeric Type

Type `A` represents a single ASCII/E-ASCII code point:

```bee
rule main:
  new a ∈ A;
  new x ∈ B;

  let a := '0';
  let x := a :> B; -- convert character '0' to numeric ASCII code 48
return;
```

## Type Inference

The assignment operator `:=` infers data types directly from literal expressions:

```bee
set i := 4;   -- inferred type: Z
set r := 2.5; -- inferred type: R
set q := 1\8; -- inferred type: Q

new x := 0;   -- inferred type: Z
new y := 0.0; -- inferred type: R
```

## Type Checking

Expression types are checked against variable constraints. The `∈` operator verifies type membership at runtime:

```bee
rule main:
  new a := 0 ∈ Z;
  expect a ∈ Z;
return;
```

## Boolean Type

Type `B` represents boolean / binary values (0 = False, 1 = True). Standard boolean constants `True` and `False` are built into the core library:

```bee
rule main:
  print False; -- prints 0B0
  print True;  -- prints 0B1
return;
```

### Logic Operations

Bee provides mathematical logic operators:

- `¬` (NOT)
- `∧` (AND)
- `∨` (OR)
- `⊕` (XOR)

Precedence order: `{ ¬, ∧, ∨ }`.

Bitwise operators:

- `~` (bitwise NOT)
- `&` (bitwise AND)
- `|` (bitwise OR)
- `⊕` (bitwise XOR)
- `«` (shift left)
- `»` (shift right)

```bee
-- bitwise evaluation examples
print 4 | 3;  -- 7 (100 | 011 = 111)
print ~4;     -- bitwise NOT
print 4 & 7;  -- 4 (100 & 111 = 100)
print 4 ⊕ 4;  -- 0 (100 ⊕ 100 = 000)
print 1 « 2;  -- 4 (001 shifted left 2)
print 6 » 2;  -- 1 (110 shifted right 2)
```

### Coercion

Numeric values and strings can be explicitly cast to boolean using `:>`:

```bee
set (a: 0.0, b: 1.5) ∈ R;

rule main:
  new (x, y) ∈ B;
  let x := a :> B; -- 0B0
  let y := b :> B; -- 0B1
return;
```

Coercion rules:
- Non-zero numbers cast to `True` (`0B1`), zero casts to `False` (`0B0`).
- Strings `"True"`, `"true"`, `"Yes"`, `"1"` cast to `True`.
- Strings `"False"`, `"false"`, `"No"`, `"0"` cast to `False`.

## Composite Types

Composite collections use brackets `()`, `[]`, and `{}`:

```bee
new d := [1, 2, 3, 4];              -- fixed-size array of 4 integers
new e := [0.00](10);                -- array initialized to 10 real elements
new b := (1, 2);                    -- ordered list of integers
new s := {1, 2, 3, 4};              -- set of integers
new c := {1: "one", 2: "two"};      -- map of (Integer: String)
new o := {name: "Goliath", age: 30}; -- object literal
```

## Parameter Types

Rule parameters require type annotations with `∈`. Default initializers make parameters optional:

```bee
-- optional parameters with default values
rule foo(a: 0 ∈ Z, b: 0 ∈ Z) => (r ∈ Z):
  let r := a + b;
return;

rule main:
  print foo();      -- 0
  print foo(1);     -- 1
  print foo(1, 2);  -- 3
return;
```

Arguments can be passed by name using pair-up syntax (`key: value`):

```bee
rule main:
  print foo(a: 1, b: 2); -- 3
return;
```

## Rational Numbers

Rational numbers (`Q`) represent exact fractions $p/q$ where $p \in \mathbb{Z}$ and $q \in \mathbb{N}_{>0}$.

Literal syntax: `p\q`.

```bee
new a: 1\2 ∈ Q; -- 0.5
new b: 1\4 ∈ Q; -- 0.25
new c: 1\8 ∈ Q; -- 0.125
```

### Q Notation

Fixed-point containers use `Qm.n` notation, where $m$ represents integer magnitude bits, $n$ represents fractional bits, and 1 bit is reserved for the sign ($m + n + 1$ total bits):

- Precision: $2^{-n}$
- Range: $[-2^m \dots (2^m - 2^{-n})]$

Example: `Q5.2` stores values in range `[-32.00 .. 31.75]` using 8 bits with precision $2^{-2} = 0.25$:

```bee
new v ∈ Q5.2;
let v := -32;   -- minimum value
let v := 31.75; -- maximum value
```

### Typical Q Configurations

| Resolution | 1\4 ≈ | 1\8 ≈ | 1\16 ≈ | 1\32 ≈ | 1\64 ≈ |
| :---| :---| :---| :---| :---| :---|
| ↓ Memory Space | ±0.25 | ±0.125 | ±0.062 | ±0.031 | ±0.015 |
| 8 bits | Q(5.2) | Q(4.3) | Q(3.4) | Q(2.5) | Q(1.6) |
| 16 bits | Q(13.2) | Q(12.3) | Q(11.4) | Q(10.5) | Q(9.6) |
| 32 bits | Q(29.2) | Q(28.3) | Q(27.4) | Q(26.5) | Q(25.6) |
| 64 bits | Q(61.2) | Q(60.3) | Q(59.4) | Q(58.5) | Q(56.6) |
| 128 bits | Q(125.2) | Q(124.3) | Q(123.4) | Q(122.5) | Q(121.6) |

### Default Q Number

The default type inference for `Q` numbers without explicit bit parameters uses `Q(14.17)` (32-bit container, 1 sign bit, 14 integer bits, 17 fractional bits):

- Range: `[-16384 .. +16383]`
- Precision: $2^{-17} \approx 0.0000076$

### Approximate Comparison

Numbers can be compared within tolerance limits using `≈` (approximate equality) and `±` (tolerance modifier):

```bee
set $precision := 0.01;

rule main:
  new a := 0.25; -- real
  new b := 1\3;  -- rational ~0.333

  print (a ≈ b);         -- 0B0 (False, difference > 0.01)
  print (a ≈ b ± 0.10);  -- 0B1 (True, difference within 0.10 tolerance)
return;
```

Explicit cast from `R` to `Q`:

```bee
rule main:
  new a := 0.25; -- real
  new b := 1\4;  -- rational

  new c := a :> Q;
  expect c = b;
return;
```

---

[Go back](structure.md) | [Read next](control.md)
