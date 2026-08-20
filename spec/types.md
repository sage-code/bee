
# Bee Types


Bee use several kind of data types described below. Use these links to jump to a particular data type. Use browser back-button to revisit a particular data type:

- Primitive types;
- Constant literals;
- Special types;
- Type declaration;
- Range type;
- Domain type;
- Constant declarations;
- Variable declarations;
- Modify values;
- Alphanumeric type;
- Type inference;
- Type checking;
- Boolean type;
- Rational numbers;
- Bee is using a gradual typing system. We think dynamic typing is more fragile and prone to errors. Therefore Bee is a strongly typed language with type inference. That means any data is constrained by fixed  "data type" rules.

Bee is using a gradual typing system. We think dynamic typing is more fragile and prone to errors. Therefore Bee is a strongly typed language with type inference. That means any data is constrained by fixed  "data type" rules.

- Bee has predefined data types. You can create new data types based on predefined types using a type declaration. You can create sub-types or composite types having new constraints and rules that can improve data validation further.

Bee has predefined data types. You can create new data types based on predefined types using a type declaration. You can create sub-types or composite types having new constraints and rules that can improve data validation further.

- A data type can be manipulated using rules and operators. You can have a variable of type:  Type. To detect a data type of any variable you can use the introspection function type().

A data type can be manipulated using rules and operators. You can have a variable of type:  Type. To detect a data type of any variable you can use the introspection function type().


## Primitive Types


Primitive data types are defined using one capital letter. This may be unusual in Computer Science but standard in Mathematics. Therefore Bee uses this convention.


| Table |
| --- |
| Alias | Code | Description + Default representation |
| Boolean | B | Boolean or 8 bit number, 0 = False, >= 1 True |
| Alpha | A | Alpha-numeric E-ASCII ('0'..'9') ('a'..'Z') |
| Unicode | U | Unsigned 32 bit, max: U-FFFFFFFF (UTF32) | Rational | Q | Fix point representation number: like 1/2. Notation: Q(14,17) | Natural | N | Unsigned large positive integer 64 bit [0..+] | Integer | Z | Signed large integer 64 bit [-..+] Z(64) | Real | R | Double precision float 64 bit (-..+) R(64) |
| Unicode | U | Unsigned 32 bit, max: U-FFFFFFFF (UTF32) |
| Rational | Q | Fix point representation number: like 1/2. Notation: Q(14,17) |
| Natural | N | Unsigned large positive integer 64 bit [0..+] |
| Integer | Z | Signed large integer 64 bit [-..+] Z(64) |
| Real | R | Double precision float 64 bit (-..+) R(64) |


- Each data type has a default representation for literal, print & output,
- Output representation can be establish using a format template,
- Using print with primitive type will create a specific representation,
- Precision can be specified in parenthesis after the type: Z(32) = 32 bit integer,
- Primitive data types are values allocated on the stack or in the registry.

## Constant Literals


These are symbolic representations for primitive data types:


| Table |
| --- |
| Example | Type | Literal characters |
| 'a' | A | (+-) & (0..9) & (a..z) & (A..Z) |
| 'Ω' | U | (Δ Λ Φ Γ Ψ Ω Σ Π π ⊥ ǁ α β ɣ ε δ μ ω ...) |
| "str" | S | (∀ UTF8) |
| 0B0,0B1 | B | (0,1) & B |
| 1234567890 | N | (0,1,2,3,4,5,6,7,8,9) |
| +0 | Z | (-+) & (0,1,2,3,4,5,6,7,8,9) |
| 'a','b' | A | ASCII (0x00..OxFF) |
| U+FFFF | U | (U+) & (0,1,2,3,4,5,6,7,8,9) & ABCDEF |
| U-FFFFFFFF | U | (U-) & (0,1,2,3,4,5,6,7,8,9) & ABCDEF |
| 0.05 | R | (-.) & (0,1,2,3,4,5,6,7,8,9) |
| -1/2 | Q | (-/) & (0,1,2,3,4,5,6,7,8,9) |
| 1E10 | R | (-1E)& (0,1,2,3,4,5,6,7,8,9) |
| 1e10 | R | (-1e)& (0,1,2,3,4,5,6,7,8,9) |



note

- primitive types are ordered and can be compared,
- primitive literals are identical to themselves,
- primitive variables are identical to themselves.

## Special types


Special types have an alias starting with capital letter. These types are embeded in the language and contribute to language coherence. All these types are actually references to memory structures:


| Table |
| --- |
| Alias | Type | Description |
| Complex | C | Double precision pair of double float numbers (9r+9j) |
| String | S | UTF8 encoded double quoted string "α β ɣ ε δ μ ω" |
| Date | D | "DD/MM/YYYY" |
| Time | T | "hh:mm,ms" |
| Lambda | L | Lambda expression or function. |



## Collection types


Bee define a collection literal using a special notation based on brackets. These types are going to be explained later in another page. We mention these types here because they represent types.


| Table |
| --- |
| delimiter | collection types |
| () | List |
| [] | Array / Matrix |
| {} | Set / Map / Object / Ordinal |


- All collections are actually references,
- Collection elements can be references or native types,
- Elements of collection are separated by comma,
- Pair of values are separated by columns ":"

## Type declaration


User can define type alias using operators ":" and sub-types using operator "<:" (inheritance). Usr can specify type of variables explicit usin operator ∈


```
** declare new type alias
type Type_Identifier: type_descriptor <: super_type;

** declare variables using type alias
new var_name ∈ Type_Identifier;

** declare many variables using type alias
new var_name, var_name ... ∈ Type_Identifier;
```

- User defined types are starting with capital letter;
- User defined super-types are usually composite types;
- User defined sub-types are usually domains of values;

## Range Type


A range is a notation that designate a sub-set of consecutive  integer numbers between two limits: lower limit and upper limit included in round parenthesis and separated by two dots (..) or (!).


```
range ::= (min..max);
range ::= (min.!max); -- exclude upper limit
range ::= (min!.max); -- exclude lower limit
```

- Both limits are included in range by default
- Upper or lower limits can be excluded using "!"
- Range notation can be open at one end or both ends
- Open lower limit is symbolic (-) with no number
- Open upper limit is symbolic (+) with no number

```
#integer domain
rule main:
  print (0..5); -- 0,1,2,3,4,5
  print (0.!5); -- 0,1,2,3,4
  print (0!.5); -- 1,2,3,4,5

  pass if  32667 ∈ (0..+); -- expect to pass
  pass if -32668 ∈ (-..0); -- expect to pass
return;
```


Ranges can use symbols that are ASCII or Unicode. In this case the symbols must be included in single quotes: 'X' or use U+ notation:


```
** sub-type declarations
type  .Digit:    ('0'..'9')       <: Z;
type  .Capital:  ('A'..'Z')       <: A;
type  .Lowercase:('a'..'z')       <: A;
type  .Latin:    (U+0041..U+FB02) <: U;

rule main:
  ** following statements should pass
  pass if '0' ∈ Digit;
  fail if 'x' ∈ Capital;
  pass if 'X' ∈ Capital;
  pass if 'e' ∈ Latin;
return;
```


## Domain Type


Domain is very similar to range except a domain has a ratio. This is the difference, the numbers are not integers, can be fractional or Q umber.


```
type Domain: (min..max:ratio)  <: Super_Type;
```


```
** generate rational numbers
print (0..1:1&\4); -- 0&\4, 1&\4, 2&\4, 3&\4, 1

** generate float numbers
print (0..1:0.25); -- 0.00, 0.25, 0.50, 0.75, 1.00
```


## Constant declarations


Constants literals bound to identifiers using keyword "set".


```
** using explicit type
set constant_name: constant_literal ∈ type_name;

** using implicit type
set constant_name := constant_literal;
```

- Unfortunate English is using "set" to define a sequence,
- In Bee we use "set" keyword to setup a constant not a sequence,
- Constant initial value can be assigned using operator ":=" or "=",
- Constants can be public, private or local,
- Public constants are defined using prefix ".",
- Local constants are defined in a local scope.

```
#define symbol constants
set forall1: U+2200     ∈ A; -- Symbol: ∀
set forall2: U-00002200 ∈ U; -- Symbol: ∀
```

- After U+ compiler is expecting 4 hexadecimal symbols;
- After U- compiler is expecting 8 hexadecimal symbols;

## Variable declarations


Variables are defined using type inference and these operators:


| Table |
| --- |
| operator | purpose |
| ∈ | declare variable/element type |
| : | define | block start | pair up operator |
| : | set initial value (require type in declarations) |
| := | type inference | share a reference | assign operator |
| :: | deep copy | duplicate object | cloning operator |


- Symbol ":" can be used to define a type or set initial value or type for a variable or parameter.
- Symbol ":" can be used as pair-up operator for arguments and map pairs.
- Symbol ":=" can can be used to define or mutate the value of variables or parameters.
- Symbol "<:" used in declarations is used to indicate a supertype,

```
** primitive variable declarations with type
new var_name ∈  type_name; -- declaration only type without initial value
new var_name: value ∈  type_name; -- declaration with initial value and type

** Variable declaration using type inference
new var_name := expression; -- expression ":=" do not require type hint ("∈").

** Multiple variables can be define in one single line using comma separator:
new var1, var2 ... ∈  TypeName;   -- default initial values
new var1, var2 ... := Expression; -- use type inference for all initial values

** Initialize multiple variables, of the same type (type is required)
new var1:con1, var2:con2 ... ∈ TypeName;
```


## Modify values


One can modify variables using alter statement.


```
#fragment of code

new a:10, b:0 ∈ Z; -- initialize two variables
let b := a + 1;   -- modify b using binding operator :=
let b += 1;       -- modify b using modifier +=
expect b = 12;    -- check if b has proper value
```

- Multiple variables can be modified all at once when separated by comma;
- Following operators are called modifiers and can change value of a variable:
- {":=","::"}
- {"+=","-=","&\=","*=","^=","%=", "*=", "/=", "√="}

```
** declare a public constant
set .PI: 3.14 ∈ R;

rule main:
  ** declare a single variable
  new a   ∈ Z; -- Integer

  ** declare multiple variables
  new (x,y):0 ∈ R; -- Double
  new (q,p):0 ∈ L; -- Logic

  ** using modifiers
  let a := 10; -- modify value of: a == 10
  let a += 1;  -- increment value of: a == 11
  let a -= 1;  -- decrement value of: a == 10

  ** modify two variables using one single constant
  let x, y := 10.5;

  ** modify two variables using two constants
  let q, p := True, False;

  ** swapping two variables
  let p, q := q, p;
return;
```


## Type conversion


When data type mismatch you must perform explicit conversion.

- Explicit conversion is using a symbolic operator: ":>"
- This is unsafe operation. A range check is recommended before conversion;
- Data precision may suffer. Some decimals may be lost;
- If data do not fit in the new type, the overflow exception is raised.

```
** data conversion
rule main:
   new a:0, b:20 ∈ Z;
   new v:10.5, x:0.0 ∈ R;
** explicit conversion
   let a:=v :> N;
   print a; -- truncated to 10
** explicit conversion
   let x := b :> R;
   print x; -- expect 20.00
return;
```

- making conversion will copy value not reference
- conversion to same data type is equivalent to copy "::"

## Alphanumeric type


Bee define A as single UTF-8 code point with representation: U+HH


```
rule main:
  new a, b ∈ A; -- ASCII
  new x, y ∈ B; -- Binary integer
  let a :='0';     -- ASCII symbol '0'
  let x := a :> B; -- convert to binary 30
  let y := 30;     -- decimal code for '0'
  let b := y :> A; -- convert to ASCII symbol '0'
return;
```


## Type inference


You can use symbol ":=" to initialize variables using type inference.


```
** declare constants
set i := 4;   -- integer constant
set r := 2.5; -- real constant
set q := 1&\8; -- rational constant
** declare variables
new x := 0;   -- integer number
new y := 0.0; -- real number
new z := 0\1; -- rational number
```


## Type checking


We can use variable type to validate expression type.


```
** using type inference
rule main:
  new a := 0;   -- integer variable
  new b := 0.0; -- real variable

  let a:= 10.5; -- error: explicit conversion is required
return;
```


You can use operator "∈" to verify data type:


```
rule main:
  new a := 0 ∈ Z;

  ** expected: Integer
  expect a ∈ Z;
return;
```


## Boolean type


Boolean type is Bee is native numeric of type B. However we also implement native two constants True, False that are publicly available in core library


```
** overwrite the default values
set False = 0; 
set True  = 1;
```


Printing native Boolean values is going to print numbers. Type B can support a number between 0b0 and 0b00000001. Therefore printing this type is done using notation 0B0 and 0B1.


```
** printing Boolean values
rule main:
  print False; -- 0B0
  print True;  -- 0B1
return;
```


You can convert B to a number, safely. You can convert a number to B explicit using cast operator: number :> B. The number will loose all it's significance and become 0B1 or 0B0.


### Logic operations


Bee uses several familiar logic operators from mathematics:

- ¬ - equivalent "not"
- ∧ - equivalent "and"
- ∨  - equivalent "or"

Precedence: { ¬, ∧, ∨ }. Symbol ¬ will apply first, symbol ∨ will apply last.


bitwise


In Bee we define special operators to perform bitwise operations. One opperator is overwrite: ⊕. This operator (xor) can operate on both, logical values or expressions and also on integer numbers.

- ~ (not)
- & (and)
- | (or)
- ⊕ (xor)

```
# bitwise operations
print 4 | 3; -- out:7 is because 100 | 011 = 111 = 7;
print ~4;    -- out:3 is because: 100 ~  100 = 011 = 3;
print 4 & 7; -- out:4 is because: 100 & 111 = 100 = 4;
print 4 ⊕ 4;  -- out:0 is because: 100 ⊕ 100 = 000 = 0;
print 1 << 2;  -- out:2 is because: 001 << 2   = 100 = 4;
print 6 >> 2;  -- out:1 is because: 110 >> 2   = 001 = 1;
```


Comparison operators will create a Boolean response: 1 = True or 0 = False. Also, the equivalent and belonging operators will create a Boolean response. You can combine them to create Boolean expressions.

- comparison ( ≈, =, ≠, ≡, !≡,  >, <, ≤, ≥)
- equivalents (==, !=, <=, >=)
- belonging ( ∈, !∈ )

```
rule main:
  new (x, y):4 ∈  Z; -- primitive integer
  ** value comparison
  print x = 4;  -- 1 (equal)
  print x ≡ 4;  -- 1 (identical)
  print x = y;  -- 1 (equal)
  print x ≡ y;  -- 1
  print x ≠ 5;  -- 1 (different)
  print x!≡ 5;  -- 1 (not identical)

  ** reference ordering
  print x ≥ y;  -- 1: x and a are actually equal
  print x ≥ 4;  -- 1: greater or equivalent to 4
  print x ≤ 4;  -- 1: less than or equivalent to 4
  print x > 4;  -- 0: not greater than 4
  print x < 4;  -- 0: not less than 4


  ** arithmetic expressions have primitive results
  print x - 4 = 0; -- 1
  print x - 4 ≡ 0; -- 1
return;
```


singleton


Primitive types are unique. That means they are equivalent. A literal or constant is equivalent to another literal having the same value.


```
** primitive values are singleton
print  1  ≡  1;  -- 1
print "s" ≡ "s"; -- 1

** alternative operator have the same significance
print  1  == 1;  -- 1
print "s" == "s"; -- 1
```


Precedence:


Logic operators have greater precedence than comparison operators.


### Logical expression


Logical expression have value { 0 = False, 1 = True }


```
** define constants based on Boolean values
set f: False;
set t: True;

rule main:
  ** expressions with single operant
  print f; -- 0
  print ¬ t; -- 0

  ** expressions with two operands
  print (f = t); -- 0
  print (f ≡ t); -- 0
  print (f ≠ t); -- 1
  print (f < t); -- 1
  print (f > t); -- 0
  print (f ∧ t); -- 0
  print (f ∨  t); -- 1
  print (f ⊕ t); -- 1
return;
```

- Operators { ¬ } is unary operator;
- Operators { ∧, ∨ } are also bitwise operators;
- Operators { ¬, ⊕ } are also bitwise operators;
- Operators { «, » } are bitwise operators;

coercion Any numeric expression  can be converted to a logic value using coercion operator ":>" (easy to memorize if you think is like an arrow).


```
set (a: 0.0, b: 1.5) ∈ R;
rule main:
  new (x, y) ∈ B;

  let x := a :> B; -- 0
  let y := b :> B; -- 1
return;
```

- Real number is truncated before conversion to Boolean;
- A string: "Yes", "yes", "True", "true", "On","on", "T", "t" or "1" convert to: True = 1
- A string: "No", "no", "False", "false", "Off","off", "F", "f" or "0" convert to: False = 0

design


```
** logical values are numeric
print True  ≡ 1;  -- 1
print False ≡ 0;  -- 1

** logical values do not compute
print False - True; -- Error
print True  + True; -- Error

** Null value is not True
print Null  ≡ True   -- 0
** Null value is not False
print Null  ≡ False  -- 0
```


## Type inference


Type inference is a logical deduction of data type from constant literals.

- Default types
- Composite types
- Parameter types

### Default types


Each literal has associated a default type, induced by operators {":=", "::"}.


```
** string expressions
new c := 'a'     ;  -- type = A
new s := '∈'    ;  -- type = U
new s := "str"   ;  -- type = S
** numeric expressions
new i := 0;    -- type = Z
new j := 0.50; -- type = R
** define synonyms for logic constants
set f := False; -- type B
set t := True;  -- type B
** multiple variables get same value
new (x, y, z) := 5; -- type = Z for all
** multiple variables get multiple values
new int, rea := -4, 4.44;
print type(int); -- Z
print type(rea); -- R
```


### Composite Types


Composite structures are using () [] and {} to create different data types. Next you can study some examples. We wil explain later all these types: List, Map, Array, Object. All of these are also called Bee collections.


```
** boxed integer (type = Z)
new i := [10]; -- array of one value = 10!
** array with capacity of 4 integers: Z
new d := [1,2,3,4];
** array with capacity of 10 real numbers: R = 0.00
new e := [0.00](10);
** list of one value (Z)
new a := (1);
** list of integers (Z)
new b := (1,2);
** list of symbols (type = A)
new l := ('a','b');
** list of Unicode symbol (type = U)
new u := ("Δ", "Λ", "Γ");
** 2d matrix with capacity of 10x10 real numbers: R
new m := [0.00](10,10);
** 3d matrix with capacity of 10x10x10 reals: R = 0.00
new m := [0.00](10,10,10);
** data set of 4 integers: Z
new s := {1,2,3,4};
** hash map of (Integer: String)
new c := {1:"storage",2:"string"};
** object with two attributes: name ∈ S, age ∈ Z
new b := {name:"Goliath", age:30};
```


### Parameter types


When we define parameters we can use type inference only for optional parameters. Mandatory parameters must have type declaration using ∈ symbol. If default value is not specified the parameter will have defailt zero initial value.


Optional Parameters:


```
** in rule foo, parameters a, b are optional.
rule foo(a: 0 ∈ Z, b: 0 ∈ Z) => (r ∈ Z):
  let r := a + b;
rule;

rule main:
  print foo();    -- 0
  print foo(1);   -- 1
  print foo(1,2); -- 3
return;
```


Multiple parameters:


```
** parameters: a, b are mandatory, c is optional.
rule foo(a, b, c:0 ∈ Z) => (r ∈ Z):
  let r := a + b + c;
return;

rule main:
  print foo(1,2);   -- 3
  print foo(1,2,3); -- 6
  print foo(1);     -- Error: expected 2 arguments
return;
```


Pass arguments by name:


We can use parameter name and pair-up symbol ":" for argument value.


```
** rule with optional parameter (c)
rule bar(a, b, c:0 ∈ Z) => (result ∈ Z):
  let result := a+b+c;
return;
** observe we use pair-up ":" to give value for each argument
rule main:
  print bar( 1, 1 );    -- print 2 because c = 0
  print bar( a:1, b:1, c:1 ); -- print 3 because c = 1
return;
```


## Rational numbers


In mathematics rational number is any number that can be expressed as the fraction p/q of two integer numbers: numerator "p" of type integer and a non-zero denominator "q" of type natural> 0. Since "q" may be equal to 1, every binary integer is also a rational number.


Note: Q numbers are approximated numbers.

- Default precision for Q numbers is $precision: 10⁻⁵ = 0.00001
- Default precision can be set using: $precision:x; global constant
- Operator "≈" is using the precision if the operator "±" is not used;

Other precision constants:

- $deci  := 1d = 10⁻¹
- $centi := 1c = 10⁻²
- $mili  := 1m = 10⁻³
- $micro := 1μ = 10⁻⁶

Literal Notation: p\q


It can be used with type inference to create Q numbers:


```
new x: 0     ∈ Q; -- 0
new a: 1\2   ∈ Q; -- 0.5
new b: 1\4   ∈ Q; -- 0.25
new c: 1\8   ∈ Q; -- 0.125
new d: 1\16  ∈ Q; -- 0.062
new e: 1\32  ∈ Q; -- 0.031
```

- The inch is a unit of length in the British imperial and United States
- It is equal to 1\36 yard or 1\12 of a foot
- One inch is divided in 1\2, 1\4, 1\8, 1\16 and 1\32

See also: wikipedia


### Q Notation

- Qm.n is m+n+1 bit signed integer container with n fractional bits.

Qm.n is m+n+1 bit signed integer container with n fractional bits.

- Qm is a m+1 bit signed integer containing 0 fractional bits.

Qm is a m+1 bit signed integer containing 0 fractional bits.

- number of bits = m+n+1

number of bits = m+n+1

- precision is 2⁻ⁿ

precision is 2⁻ⁿ

- range is [-(2ᵐ)..(2ᵐ-2⁻ⁿ)]

range is [-(2ᵐ)..(2ᵐ-2⁻ⁿ)]


For example: Number format "Q5.2" can store in range (-32.00..31.75) on 8 bits.

- with precision of 2⁻² = 1\4 = 0.25
- from value: -2⁵ = -32.00
- to value: 2⁵ - 2⁻² = 32 - 0.25 = 31.75

```
new v ∈ Q5.2;
let v := -32;   -- minim value
let v := 31.75; -- maxim value
```


See also: wikipedia


### Typical Q numbers


Next I have predefined some numbers for orientation.


| Table |
| --- |
| rezolution | 1\4 ≈ | 1\8 ≈ | 1\16 ≈ | 1\32 ≈ | 1\64 ≈ |
| ↓ memory space | ±0.25 | ±0.125 | ±0.062 | ±0.031 | ±0.015 |
| 8 bytes | Q(5.2 ) | Q(4.3 ) | Q(3.4 ) | Q(2.5 ) | Q(1.6 ) |
| 16 bytes | Q(13.2 ) | Q(12.3 ) | Q(11.4 ) | Q(10.5 ) | Q(9.6  ) |
| 32 bytes | Q(29.2 ) | Q(28.3 ) | Q(27.4 ) | Q(26.5 ) | Q(25.6 ) |
| 64 bytes | Q(61.2 ) | Q(60.3 ) | Q(59.4 ) | Q(58.5 ) | Q(56.6 ) |
| 128 bytes | Q(125.2) | Q(124.3) | Q(123.4) | Q(122.5) | Q(121.6) |



Note: r ≈ is the approximate resolution.


A very large number with high resolution on 64 bit:


Q(50.12)

- Min: -1125899906842624
- Max: +1125899906842623
- Res: 0.000244140625

A number on 32 bit with resolution = 0.0005:


Q(20.11)

- Min: -1048576
- Max: 1048575
- Res: 0.00048828125

### Default Q number


Q(14.17)


Bee is using default Q type for type inference, when precision is not specified. Default Q number has precision 10⁻⁵ = 2⁻¹⁷ ≈ 0.00001 and occupy 32 bit. It's a relative small number. For larger numbers you must specify the resolution and capacity.

- Min: -16384
- Max: +16383
- Res: 0.0000076
- Smallest fraction: 1\10000
- Largest fraction: 32766\2

### Approximate comparison


Rational numbers and other numbers can be compared using "≈" instead of "=". Bee can be used to make aproximative computations and logic expressions based on precision.

- Operator "≈" can be used to compare two numbers using default precision;
- Operator "≈" can be used with "±" to overwrite default precision;

In next example b = 0.33(3), delta = (b - a) = 0.083


```
** override default precision
set $precision := 0.01;

rule main:
    new a := 0.25; -- real
    new b := 1\3;  -- rational O.33(3)
    ** using specified precision 0.01
    print (a ≈ b); -- 0B0: (False, 0.033 - 0.25 = 0.08 )

    ** using specified precision:
    print (a ≈ b ± 0.01); -- 0B0 (False)     
    print (a ≈ b ±  0.05); -- 0B0 (False)    
    print (a ≈ b ±  0.10); -- 0B1 (True)
return
```

- Operator "\" has high priority in expressions;
- Rational numbers improve computation efficiency;

Rational numbers are similar to complex numbers. The calculation of rational number is postponed until is necesary in expressions and it can produce different results depending on the precision.

- Conversion from rational number to real is implicit;
- Conversion from real to rational is explicit;

```
** execute conversion
rule main:
    new a := 0.25; -- real
    new b := 1\4;  -- rational

    ** explicit conversion R :> Q
    expect a ≠ b; -- not equal, type mismatch
    expect a ≈ b; -- values match, aproximation
    expect a ≡ b; -- implicit conversion, match

    ** explicit conversion R :> Q
    new c := a :> Q; 
    expect c = b; -- type & value match
    expect c ≡ b; -- type & value match

    ** implicit conversion Q :> R
    new r := c ∈ R;
    expect c = 0.25;
return
```


Read next:
Control
