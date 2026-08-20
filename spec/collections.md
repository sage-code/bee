
# Bee Collections


Next links enable you to find definition of a particular collection type. Collections have different features and performance. Use browser back-button to jump back here and compare collections later.

- ordinal
- lists
- arrays
- data sets
- hash maps
- strings
- error

## Usability


Bee uses composite types to declare ...

- composite variables
- composite constants
- new data types

## Pattern


A new type is defined from a super-type using symbol "<:"


```
** type declaration
type new_type: descriptor <: super_type;
```

- new_type ::= identifier name usually start with capital letter
- descriptor ::= depending on super-type
- super_type ::= primitive type or composite type
- The type descriptor is usually enclosed in parenthesis: (), [] or {}
- The super_type is optional. It can be inferred from type descriptor

## Ordinal


Ordinal is an ordered small set of identifiers. Each identifier represents an integer value starting from a specified number with interval of one. It can be used for ranking, selection or codification.


The set of elements is enclosed in curly brackets, separated by coma. Usually the first element has value 1, but this can be specified using (n) in front of the curly bracket: (n){elements}.


```
type Type: (1){name1, name2, name3} <: Ordinal;
rule main:
  new a, b, c ∈ Type; -- a, b, c will have same type

  let a := Type.name1; -- 1
  let b := Type.name2; -- 2
  let c := Type.name3; -- 3
return;
```


Note: When element name start with "." no need to use qualifiers for the individual values. This is because values starting with "." are public by default and known in the scope where ordinal is defined (or loaded).


```
** using public elements in ordinal
type Type: (0){.name0, .name1} <: Ordinal;
rule main()
   new a, b ∈ Type;

   let a := name0; -- a = 0
   let b := name1; -- b = 1
return;
```


## Lists


A list is a dynamic collection of elements connected by two references:

- prior: element reference
- next: element reference

A list has two very important elements:

- head: first element
- tail: last element

Chained List


You can define a list type using empty list: ()


```
type Type_name: (element_type) <: List;
```


variable declaration You can use one of three forms of declarations:


```
** declare emty list without type
new name1: ();  -- element type will be established later
 
** declare empty list, using explicit type
new name1: (element_type);  

** declare populated lists using type inference
new name2 := (e1,e2...); -- implicit declaration

** 
new name3 := (e1,e2...) ∈ Type_name; -- full declaration
```


properties

- a list has unlimited capacity,
- a list can be initially empty (),
- all elements in a list have the same type,
- elements in a list are ordered,
- accessing elements in a list by index is slow.

```
## define a diverse lists
new two:(Z) <: List;  -- empty list of integers = ()
new one:(0);       -- initialize list using type inference
new two:(1,2);     -- initialize list with two elements
```


```
## list traversal demo
rule main:
  ** define a list variable of defined type Lou
  new myList := (0, 1, 2, 3, 4, 5);
  ** list traversal
  cycle: for ∀ x ∈ myList do
    write x;
    write "," if (x ≠ myList.head);
  repeat;
  print; -- 0,1,2,3,4,5
rule;
```


## Arrays


Bee define Arrays using notation: [type](c), where [type] is the data type of elements and (c) is the capacity (total number of elements). Arrays are automatically initialized. However, if the array contains composite types all elements are null until initialized.


```
** diverse array variables
new array_name1: [element_type]  ;    -- single element array
new array_name3: [element_type](c);   -- capacity c
new array_name4: [element_type](n,m); -- capacity c = n * m

** define new sub-type of array
type AType:[element_type] < Array;

** use previous defined sub-type
new array_name5 := AType(c);
```


In next example we declare an array and use index "i" to access each element of the array by position. Later we will learn smarter ways to initialize an arrays and access its elements by using a visitor pattern.


Array Index


Lets implement previous array: numbers[] and print its elements using a cycle. For initialization we use an explicit array literal that contains all the elements.


```
# define array
new numbers[Z](10) := [0,1,2,3,4,5,6,7,8,9];

** access .numbers elements one by one
rule main:
    write "numbers = [";
    cycle: for ∀ i ∈ (1..10) do
        write numbers[i];
        write ',' if i < 10;
    repeat;
    write "]";
    print; -- flush the buffer
return;
```


```
numbers = [0,1,2,3,4,5,6,7,8,9]
```

- Array index start from 1 so we use range (1..10);
- Array capacity (10) is immutable after array initialization;
- Array element is accessed by the index: numbers[i];

initialize elements


Initial value for elements can be set during declaration or later:


```
** you can use a single value to initialize all vector elements
rule main:
    new zum:[Z](10) ∈ Vector; 
    ** explicit initialization using single value
    let zum[*]  := 0;
    print zum; -- expect [0,0,0,0,0,0,0,0,0,0]

    ** modify two special elements:
    let zum.first  := 1;
    let zum.last   := 10;
    print zum; -- expect [1,0,0,0,0,0,0,0,0,10]
return;
```


Deferred initialization: We can define an empty array and initialize its elements later. Empty arrays have capacity zero until array is initialized.


```
** array without capacity
rule main:
    new vec:[A]();
    new nec:[N]();

    ** arrays are empty
    print vec = []; -- True
    print nec = []; -- True

    ** smart initializer with operator "++"
    let vec ++ 10; -- add 10 elements;
    print vec; -- expect ['','','','','','','','','','']
   
    ** smart initializer with 0 values
    let nec ++ 10;
    print nec; -- expect [0,0,0,0,0,0,0,0,0,0];
return;
```


## Matrix


A matrix is an array with 2 or more dimensions. In next diagram we have a matrix with 4 rows and 4 columns. Total 16 elements. Observe, matrix index start from [1,1] as in Mathematics.


Matrix Index


In next example we demonstrate a curious notation for matrix. You have maybe not seen this before in any other language because is ridiculous to parse. But from an esthetic point of view we think this is the way a matrix literal should look like:


```
# define a subtype of Matrix
type Mat:[R](4,4) ∈ Matrix

rule main()
    new mat ∈ Mat -- define matrix variable

    ** modify matrix using ":=" operator
    let mat := [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
    print mat[1,1]; -- 1  = first element
    print mat[4,4]; -- 16 = last element

    ** support for 2D matrix literals
    pass if mat =  ⎡ 1,  2 , 3,  4 ⎤
                   ⎢ 5,  6 , 7,  8 ⎥
                   ⎢ 9, 10 ,11, 12 ⎥
                   ⎣13, 14 ,15, 16 ⎦;

    ** nice output using array print method
    apply mat.print;
return;
```


```
⎡ 1,  2 , 3,  4 ⎤
⎢ 5,  6 , 7,  8 ⎥
⎢ 9, 10 ,11, 12 ⎥
⎣13, 14 ,15, 16 ⎦
```


Memory is linear, so we fake a matrix. In reality elements are organized in row-major order. That means first row, then second row...last row. We can access the entire matrix like it would be a longer array. So next program can initialize a matrix in a normal cycle, not nested!


```
** initialize matrix elements
rule main:
  new mat: [Z](3,3) <: Matrix;
  ** initialize matrix elements
  cycle: 
    new i   := 1;
    new x   := mat.length;
  while (i < x) do
    let mat[i] := i;
    let i += 1;
  repeat;
  apply mat.print; -- nice output
return;
```


```
⎡ 1  2  3 ⎤
⎢ 4  5  6 ⎥
⎣ 7  8  9 ⎦
```


## Data sets


A data set is a sorted collection of unique values. Elements of a data set can be accessed sequential. There is no index associated with elements like we have in Arrays so the access to an element is slow.


```
** user defined set
type NS:{N} <: Set -- define a set of natural numbers

rule main:
   new uds ∈ NS;     -- define a shared variable of type set
   ** define shared sets s1, s2 of 3 elements each
   new s1 := {1,2,3} ∈ {N};
   new s2 := {2,3,4} ∈ {N};
   ** specific operations
   new u  := s1 ∪ s2; -- {1,2,3,4,5}:union
   new i  := s1 ∩ s2; -- {2,3}  :intersection
   new d1 := s1 - s2; -- {1}        :difference 1
   new d2 := s2 - s1; -- {4}        :difference 2
   new d  := s2 Δ s1; -- {1,4}      :symmetric difference

   ** verify expectation
   expect d = d1 ∪ d2;

   ** belonging check
   print s1 ⊂ s;  -- True
   print s  ⊃ s2; -- True

   ** declare a new set
   new a := {1,2,3};

   ** using operator +/- to add/remove elements
   let a += 4;  -- {1,2,3,4}
   let a -= 3;  -- {1,2,4}
return;
```

- Elements in a set have the same data type;
- Set are internally sorted not indexed;
- Set elements must be sortable types;

## Hash Map


A hash map is a set of (key:value) pairs sorted by key.


```
** declare a new empty hash map
new new_map ∈ {key_type: value_type};
```


Hash-Map Anatomy


```
** initial value of map
rule main:
   new map := {key1:"value1", key2:"value2"};

   ** create new element
   let map['key3'] := "value3";

   ** finding elements by key
   print map['key1']; -- "value1"
   print map['key2']; -- "value2"
   print map['key3']; -- "value3"

   ** remove an element by key
   scrap map['key1']; -- remove "first" element
   apply map.print;   -- expected: {'key2':"value2", 'key3':"value3"};
return;
```

- Hash operators are working like for a set of keys,
- Hash key type can be numeric or: {A, U, S, Date, Time},
- Hash keys are not ordered but sorted by hash function,
- Hash keys have limited length of 32 code points,

## Check for inclusion


We can check if an element is included in a collection using "∈".


```
type  Tmap: {A:U} <: Map;

rule main:
   new map  := {a:"first"), b:"second"} ∈ Tmap;
   when ('a' ∈ map) do
     print("a is found");
   else
     print("not found");
   done;
return;
```


## Strings


Bee has 4 basic types for characters and strings:

- A: ASCII code point,
- U: Unicode code point,
- S: Double quoted string,
- X: Markup large text.
- "A" and "U" represent primitive data types, they are single symbols and immutable
- [A] and [U] can be used as boxed primitive types (mutable)

| Table |
| --- |
| quote | used for |
| '_' | Byte / ASCII single symbol |
| "_" | Double quoted UTF32 Unicode string or string template |



### Text


For large text literals (X) we can use a markup tag:

- <text>...</text> : Text block
- <sql>...</sql>   : SQL text block
- <html>...</html> : HTML template
- <xml>...</xml>   : XML template

```
<text>
  Bee language has suport for large text literal.
  A text can be SQL, XML, HTML or report template.
</text>;
```


```
<sql>
select name, age 
  from persons
 where age < 24;
</sql>;
```


```
<html>
   <p>Hello World</p>
   <p>Bee is a great language.</p>
</html>;
```


### Array of symbols


Single quoted or back quoted literals can contain a single symbol.


```
** fixed capacity vector of ASCII symbols
type A128: [A](128) <: Vector;
rule main()
  ** declare a string of type A128
  new str ∈ A128;

  ** populate vector using spreading operator (*)
  let *str := 'test'; -- spreading the ASCII literal
  print str;   -- ['t','e','s','t']

  ** fixed capacity vector of symbols UTF32
  new  uco: [U](128);
  let *uco := "∈≡≤≥÷≠"; -- spreading a Unicode literal
  print  uco; -- ["∈","≡","≤","≥","÷","≠"];
return;
```


### String literals


Double quoted string literals are Unicode strings.


```
rule main:
   ** variable capacity string UTF32
   new uco ∈ S; -- Unicode string unknown capacity
   let uco := "∈ ≡ ≤ ≥ ÷ ≠ × ¬ ↑ ↓ ∧ ∨";
return;
```


Escape You can use this literal with escape sequence: \n to break a line


```
print("this represents \n new line in string");
```


```
this represents
new line in string
```

- Double quoted string can be "rope" or "radix tree";
- Single quoted strings are ASCII literals: 'like this';
- Back quoted strings are regular expressions `...`;

Next example demonstrate working with strings. We use "+" operator to make several concatenations and "*" operator to replicate a character and create a longer string.


```
rule main:
   new (c, s) ∈ S; -- default length is 128 octets = 1024 bit

   ** string concatenation
   let c := "This is 
             a large unicode string";
   ** automatic conversion to string
   let s := 'This is an ASCII string';
return;
```


## Errors


An error is when program enter a difficult state that is confusing. An error can be declared by the user or by the system. Bee has predefined type: Error that can be used to declare your own kind of errors. In other languages we use therm Exception, that is synonim to Error.


Parts of Bee compiler will be created using Bee language. Here is the definition of global variable $error, that is available for introspection after you call a rule.


```
** global error type
define Error: {code ∈ Z, message ∈ S, line ∈ Z} <: Object;
** global system error
new $error ∈ Error;
```


You can define errors with code > 200 and raise error with 3 statements:

- fail  :raise error if condition is True
- pass  :raise error if condition is False

```
new my_error := {200,"message"} ∈ Error;
fail my_error if condition;
pass if condition;
```


String interpolation "?" can be used to customize the error messages:


```
rule main:
   new  flag ∈ L;
   read (flag, "enter flag (0/1):");

   new my_error: {201,"error:#(s)"} ∈ Error;
   fail (my_error ? "test") if flag;
return;
```


```
error:"test"
```

- Keyword fail will modify create an error message;
- Keyword pass is opposite of fail
- Keyword over will liberate the resources and terminate the program;
- Error code < 200 are system reserved error codes;
- Error code ≤ -1 are unrecoverable errors created with panic;
- Recoverable errors must be analyzed by the program using a trial block;

Next we create unrecoverable error. In this case the program crash and exit. The operating system receive a number that signal the error code:


```
panic -1; -- end program immediately
panic 2; -- end program and error code = 2
```


See also:

- Set Builder Notation
- Qualifier Notation


---

[Go back](objects.md) | [Read next](processing.md)
