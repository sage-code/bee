# Data Processing

In next topic we will explain several features that are important for data processing. These examples are not yet tested but once we create a compiler this is how things should work.

- Boxed Values
- Array Operations
- Array Slicing
- Matrix Operations
- Collection builders
- List operations
- Collection iteration
- String concatenation
- String generator
- String Interpolation

## Boxed values


A boxed value is a reference to a primitive type.


syntax Boxed value is an Array or Vector with a single element.


```
# define boxed values
new int ∈ [Z]; -- boxed integer
new flt ∈ [R]; -- boxed double float
```


Boxing is the process of converting a primitive type to a reference.


```
** define two integers
new n ∈  Z;  -- primitive integer
new k ∈ [Z]; -- boxed integer

rule main:
  ** check type of variable
  print type(k);          -- [Z]
  print type(k) is Array; -- 1 = True

  ** boxing notation
  let k :=  n;  -- auto-boxing
  let k := [n]; -- explicit boxing

  ** comparison
  print n = 0; -- 1 (true, initial value)
  print n = k; -- 1 (true, same values)
  print n ≡ k; -- 0 (false, different types)
  print n == k; -- 0 (false, not the same)

  ** consequence
  let n := 2; -- n = 2 (modify n)
  print k;      -- k = 0 (unmodified)
  print k := 10; -- auto-boxing
  print n;       -- n = 2 (unmodified)
return;
```


Unboxing is the process of converting a reference to a primitive type. This will unwrap the value from the heap and stores it on the stack. Unboxing is always explicit. If you try to do implicit unboxing the compiler will signal an error.


```
** create a native and boxed integer
new n: 0  ∈  Z;  -- native integer
new r: 10 ∈ [Z]; -- reference to integer
rule main:
  ** use data type like a function
  let n := Z(r);   -- explicit unboxing (default notation)
  let n := r :> Z  -- explicit unboxing (alternative notation)
  ** verify value identity
  print n = r; -- 1 (true:  same values)
  print n ≡ r; -- 0 (false: different types)
  ** consequence: variables are unbound
  let n += 2;  -- n = 12 (modified)
  print r; -- r = 10 (unmodified)
return;
```


## Share vs copy


A reference can be shared between two variables. As a consequence, when one is modified the other is also modified. In fact is a single variables with two or more references.


A reference is shared using operator ":="


```
** create a reference using ":="
new a := [1]; -- create a reference
new b :=  b;  -- share a reference

rule main:
  ** variable c is bound to a
  pass if b = a; -- 1 (same values)
  pass if b ≡ a; -- 1 (same location, same data type)
  ** consequence of sharing:
  let a := 2;    -- [2] (modify denoted value)
  print a;       -- [2] (new value is boxed)
  print b;       -- [2] (shared reference is modified)
  expect b = a; -- will pass
  expect b ≡ a; -- references are bound
return;
```


example for cloning

- A reference is copied using operator "::"

```
** create a clone using "::"
new a := [1]; -- create a reference
new b :: a;   -- value [1]

rule main:
  expect a  = b; -- pass (same values)
  expect a !≡ b; -- expect different locations

  ** consequence of cloning:
  let a := 3;
  print a; -- [3] (new value)
  print b; -- [1] (unmodified)
  expect a != b;       -- no longer equal
  expect a !≡ b; -- expect different locations
return;
```


## Array Operations

- Array elements have very fast direct access by index;
- Array index is a binary integer starting from zero;
- Maximum number of elements: 2³² = 4,294,967,296;
- Array capacity is establish on array creation;
- Array capacity initialization can be deferred;
- Capacity can be modified only with data movement;

```
new test ∈ [R](10); -- vector of 10 real numbers
new m := length(test)-1;

rule main:
  ** array index start from 0
  print test[0]; -- first element
  print test[m]; -- last element
  ** alternative notation
  print test[0];  -- first element
  print test[-1]; -- last element
  ** array traversal
  new x := 0;
  if (x < m) do
    test[i] := x;
    let x += 1;
  cycle;
  ** print all elements of array
  print test;
return;
```


```
[0,1,2,3,4,5,6,7,8,9]
```


operations


```
# Initialized arrays
new a1 := [1, 2, 3]; 
new a2 := [2, 3, 4];
rule main:
  ** addition between two Arrays "+"
  new a3 := a1 + a2; -- [1,2,3,2,3,4]

  ** difference between two Arrays "-"
  new a4 := l1 - l2; -- [1]
  new := l2 - l1; -- [4]
  
  ** intersection between two Arrays "&"
  new := a1 ∩ a2; -- [2,3]

  ** union between two Arrays "|"
  new := a1 ∪ a2; -- [1,2,3,4]
return;
```


```
rule test_array:
  ** array  with capacity of 10 elements
  new my_array ∈ [Z](10);
  new m := my_array.capacity();

  ** traverse array and modify elements
  cycle:
    new i := 0 ∈ N;
  while i < m do
    let my_array[i] := i;
    let i += 1;
  repeat;
  ** array  elements using escape template by index #[]
  print ("First element: #[1]"  ? my_array);
  print ("Last element:  #[-1]" ? my_array);

  ** range of array elements are comma separated [1,2,3]
  print ("First two: #[1..2]"  ? my_array);
  print ("Lat two:   #[-2..-1]"  ? my_array);
  print ("All except lat two: #[1..-3]"  ? my_array);
return;
```


console:


```
This is the first element: 1
This is the last element: 10
```


resize Array capacity can be modified using union operator "+" or "+=". This will reset the array reference. That means it will not update any slice or other references you may have to this array.


```
** define new array and reference
new array := [0](10);
new acopy := array; -- copy reference
rule main:
  print array = acopy; -- 1 = True (same array)

  ** extend array with 10 more elements
  let acopy    ++ [0](10); -- 10 new elements
  let acopy[*] := 1; -- modify all

  ** print new array and reference
  print acopy;  -- [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
  print array;  -- [0,0,0,0,0,0,0,0,0,0]

  print array = acopy; -- 0 = False (different arrays)
return;
```


## Array spreading


Array data can be used as arguments for feeding a function that receive variable arguments.


```
rule sum(*args ∈ Z) => (result: 0 ∈ Z):
  cycle:
    new e ∈ Z;
  for ∀ e ∈ args do
    let result += e;
  repeat;
return;

rule main:
  new array := [1,2,3,4,5,6,7,8,9,10];
  new s := sum(*array); -- array spreading
  print s;
return;
```


## Array decomposition


Array data can be assigned to multiple variables. Last elements can be captured using rest notation:


```
* define array of 5 elements
new array := [1,2,3,4,5];

rule main():
  ** read all array elements using decomposition
  new x, y, *other := [1,2,3,4,5]; 
  print "x = #(n)" ? x;  -- x = 1
  print "y = #(n)" ? y;  -- y = 2
  print "other = #[*]" ? other; -- other = [3,4,5]
return;
```


## Array slicing


A slice is a small view from a larger array, created with notation [n..m].


```
** declare array with capacity c
new array_name ∈ [element_type](c);

rule main:
  ** unnamed slice can be used in expressions
  print array_name[n..m];
  ** create named slice from array
  new slice_name := array_name[n..m];
return;
```


Where: n,m are 2 optional numbers, n ≥ 0, m <= capacity-1.


Anonymous slicing notation can be used to extract or modify specific elements from an array;


```
** initialized array
start:
  new a:= [0,1,2,3,4,5,6,7,8,9];
do
  print a[1..$];   -- will print [0,1,2,3,4,5,6,7,8,9]
  print a[$-2..$]; -- will print [7,8,9]
  print a[1..1];   -- will print [0]
  print a[1..4];   -- will print [1,2,3,4]

  ** modify first 4 elements
  let a[1..4] += 2;

  ** first 4 elements of (a) are modified
  print a; -- [2,3,4,5,4,5,6,7,8,9]
done;
```


Slicing notation can be used to create a view to original array.


```
** original array
start:
    new a:= [0](5); -- [0,0,0,0,0]
    
    ** making two slices
    new c := a[1..3]; -- [0,0,0]
    new e := a[4..5]; -- [0,0]
do
  ** modify all slice elements
  let c[*] := 1;
  let e[*] := 2;

  ** original array is modified
  print a; -- [1,1,1,2,2]

  ** modify last 2 elements using anonymous slicing
  let a[$-1..$] := [2,3];
  print a; -- [1,1,1,2,3]
done;
```


## Matrix Operations


Modify all elements of the matrix is possible using [*] and assign operator “ := ”


```
** a matrix having 2 rows and 2 columns
new M: [Z](2,2);

rule main():
  let M[*] := 100; -- initialize all elements with 100
  print M;   -- [[100,100],[100,100]]
return;
```

- A matrix can be initialized using literals or constructor.
- A matrix can support scalar operations like Array

```
#define a shared matrix
new M: [Z](2,2);
rule main():
  ** assign same value to all elements
  let M[*] := 100;

  ** modify all elements
  let M[*] += 10;
  print(M); -- [[110,110],[110,110]]

  ** modify an entire row
  let M[1,*] := 0;
  let M[2,*] := 1;
  print(M); -- [[0,0],[1,1]]

  ** modify an entire column
  let M[*,1] += 1;
  let M[*,2] += 2;
  print(M); -- [[1,2],[2,3]]
return;
```


matrix addition Two matrices can be added to each other if they have the same dimensions.


```
start:
  ** creation of local matrix with 10 × 10 elements
  new M  := [1](10,10) + [2](10,10); 
do
  ** verify the result is a matrix of same dimensions
  expect M = [3](10,10); 
done;
```


Memory impedance


Matrices are multidimensional while computer memory is linear. This is an impedance mismatch that require mapping. Some computer languages organize matrices row by row and some others organize memory column by column. The difference between the orders lies in which elements of an array are contiguous in memory.


Transposition Passing a memory matrix from one computer language into another can require a transposition that can be a performance bottleneck. EVE uses row-major order therefore passing matrix arguments is the most efficient with Rust and C++ languages.


Matrix Traversal When you traverse elements use rows first, than you change the column. A processor will use the internal cache more efficient in this way. If the matrix is large this can be a significant performance issue.


Example: In this example we traverse all the rows then all the column, this is the most efficient way to traverse a matrix.


```
# define a matrix using unicode literal
new M :=  ⎡'a0','b0','c0'⎤
          ⎢'a1','b1','c1'⎥
          ⎣'a2','b2','c2'⎦;

rule main():
  ** local control variables
  new row, col := 0;  -- type inference: ∈ Z

  ** traverse matrix with index pattern
  if col < 3 do     -- traverse columns
    if row < 3 do   -- traverse row first
      print M[row,col];
      let row += 1;
    repeat;
    let col += 1;
  repeat;

  ** traversal with visitor pattern
  for e ∈ M do
    print e;
  repeat;
return;
```


## Collection Builders

- set builders
- hash builders
- array builders
- logic qualifiers

## Set Builders


A set builder is a declarative structure used to produce a sub-set from a set. It can take elements from one set and filter them or translate them into new values using a map() that can be a deterministic rule.


Most common is to create a set from a range of values after we filter out some values:


```
new my_set  := { var | var ∈ range ∧ filter(var)};
```


More general we can use a map() rule to convert the source elements that can be a range or a list. The elements of the new set are calculated by the map() rule.


```
new my_set := { map(x) | x ∈ source ∧ filter(x)};
```


legend

- map ::= rule or expression
- source ::= can be any collection: set, list, domain
- filter ::= condition, logic rule or logic expression

```
# define new sets of integer numbers
new (test1, test2): {Z};
rule main;
  ** populate the sets with new values
  new test1 := { x  | x ∈ (1..3)};
  new test2 := { x² | x ∈ (1..3)};
  ** expected result
  exlect test1 = {1,2,3};
  exlect test2 = {1,4,9};
return;
```


## Hash-Map Builder


A map builder can create also a hash map by using a "map" rule. A map is just a rule that create a value for each key. For example x² can be a map rule.


```
map_name := { (key:map(key)) | (key ∈ source) ∧ filter(key)}
```


legend

- source ::= a collection or domain of values
- key ::= a value member from source
- map() ::= rule or expression that produce value for key
- filter() ::= a logical expression or logical rule

New map defined from a domain


```
# define hash-map using a map-builder
new mymap := { (x:x²) | x ∈ (0.!10) ∧ (x % 2 = 0) };
rule main():
  print mymap; -- {(0:0),(2:4),(4:16),(6:36),(8:64)}
return;
```


## Array Builder


Similar to a set builder you can initialize an array or matrix:


```
new array  := [ x | x ∈ (1..10:2) ]; -- [1,3,5,7,9]
```


## Logic Qualifiers


Logic quantification verify a domain to satisfy a condition. The two most common quantifiers are: "all" and "exists".


symbols:

- Universal quantifier "all" is ∀, a rotated letter A
- Existential quantifier "exists" is ∃, a rotated letter E

Qualifiers can be used as logical expressions in conditional expressions.


```
∃ (x ∈ DS) ∧ condition(x);
∀ (x ∈ DS) ∧ condition(x);
```


```
** create a set of bit-masks
start:
  new here := {0b10011,0b10001,0b11101};
  new verify ∈ L; -- logical flag
do
  ** verify if any mask element has second bit from the end
  let verify := ∃(x ∈ here) ∧ (x ⊕ 0b10 = x);
  ** verify if all elements in Here ha ve first bit from the end
  let verify := ∀(x ∈ here) ∧ (x ⊕ 0b01 = x);
done;
```


## Collection Casting


It is common for one collection to be created based on elements from another collection. Collection members can be copy into the new collection using collection builder:


```
new source := [0,1,2,2,2,2];
rule main():
  new set := { x | x ∈ source }; -- eliminate duplicates
  print set; -- {0,1,2}
return;
```


## Collection Filtering


Build notation can use expressions to filter out elements during build.


```
new source := [0,1,2,3,4,5];
rule main()
  new set := { x | x ∈ source ∧ (x % 2 = 0) };
  print set; -- {0,2,4}
return;
```


## Collection Mapping


The elements in one set or list can be transformed by a function or expression to create a new collection.


```
new source := {0,1,2,3,4,5};
rule main():
  ** create Table pairs (key, value) for Table map
  new target := {(x:x^2) | x ∈ source };
  print target; -- { 0:0, 1:1, 2:4, 3:9, 4:16, 5:25}
return;
```


## List Operations


We can add elements to a list or remove elements from the list very fast:

- operator <+ append one element to end of list
- operator +> append one element to beginning of list
- operator += append one element in a set
- operator -= delete one element from a set
- operator << shift left a list (remove first element or more)
- operator >> shift right a list (remove last element or more)

### List Concatenation


List concatenation is ready using operator “+”. This operator represent union. Therefore union act very similar to append, except we add multiple elements at the end of first list and we create a new list as result.


```
new a := ('a','b','c');
new b := ('1','2','3');
rule main():
  new c := a + b;
  print c; -- ('a','b','c','1','2','3');
return;
```


### Join built-in


The join function receive a list and convert elements into a string separated be specified character.


```
rule main():
  new str := join([1,2,3],',');
  print (str); -- '1,2,3';
return;
```


### Split built-in


The join function receive a list and convert elements into a string separated be specified character.


```
rule main():
  new lst := split("1,2,3",",");
  print lst; -- (1,2,3)
return;
```


### List as stack


A stack is a LIFO list of elements: LIFO = (last in first out)


```
** declare a list
new a := (1, 2, 3); 
rule main():

  ** add using equeue operator: "<+"
  put a <+ 4; -- (1,2,3,4)

  ** delete operator "-="
  pop a -= a.tail; -- a = (1,2,3)
return;
```


### List as queue


A queue is a FIFO collection of elements: (first in first out)


```
new q := (1,2,3);
rule main():
   new first ∈ N;

   ** enqueue new element into list
   put q <+ 4; -- (1,2,3,4)

   ** read first element using ":="
   let first := a.head; -- first = 1

   ** shift list to left with 1
   pop a << 1; -- a = (2,3,4)
return;
```


### Other built-ins


Following other rules should be available

- List.append(value) -- can append an element at the end of the list
- List.insert(value) -- can insert an element at the beginning of the list
- List.delete(value) -- can delete one element at specified index
- List.count() -- retrieve the number of elements

### Special attributes


A list has properties that can be used in logical expressions:

- List.empty() -- True or False
- List.full() -- True or False

## Collection Iteration


Collections have common rules that enable traversal using for statement.


built-in:


Available for: {List, Table, Set} but not Array or Slice

- count - retrieve the number of elements
- fetch - position next element
- first - position to first element
- last - position to last element

```
#visitor pattern
rule main():
   new my_map := {("a":1),("b":2),("c":3)};
   for ∀ key, value ∈  my_map do
     print('("' + key + '",' + value +')');
   repeat;
return;
```


Will print:


```
("a",1)
("b",2)
("c",3)
```


## Hash collections


Hash tables are sorted in memory by key for faster search. It is more difficult to search by value because is not unique and not sorted. To search by value one must create a cycle and verify every element. This rule is very slow so you should never use it.


```
** check if a key is present in a hash collection
new my_map := {(1:'a'),(2:'b'),(3:'c')};
rule main()
   let my_key := 3;
   when my_key ∈ my_map do
     print("True"); -- expected
   else
     print("False");
   done;
return;
```


```
new animals ∈ {S,S};
rule main():
  new animals["Bear"] := "dog";
  new animals["Kiwi"] := "bird";
  print(animals);
return;
```


Output:


```
{("Bear":"dog"),("Kiwi":"bird")}
```


## Type inference

- The default type inference for empty "set" is {}
- An empty hash map will be created using notation {}

### Example


```
** partial declaration
new animals := {}; 
rule main():
  ** establish element types (S:X)
  new animals["Rover"] := "dog";

  ** use direct assignment to create 2 more element
  new animals["Bear"] := "dog";
  new animals["Kiwi"] := "bird";
  print(animals);
return;
```


output:


```
{('Rover':"dog"),("Bear":"dog"),("Kiwi":"bird")}
```


### String Conversion


Conversion of a string into number is done using parse rule:


```
rule main:
  new x,y ∈ R;
  ** rule parse return; a Real number
  let x := parse("123.512",2);     -- convert to real 123.5
  let y := parse("10,000.3333",2); -- convert to real 10000.33
return;
```


### String: concatenation


Strings can be concatenated using:

- default concatenation operator: "+"
- path concatenation operator: "/"

```
** this is example of string concatenation
new str := "";
rule main():
  ** stupid fast concatenate two string as they are
  let str := "this " + " string"; -- "this  string"

  ** smart slower concatenation for path or url
  let str := "this/  " / "  string";   -- "this/string"
  let str := "c:\this" . "is\path";         -- "c:\this\is\path"
  let str := "https:" . "domain.com";    -- "https://domain.com"
return;
```


path concatenation Two strings can be concatenated using concatenation operator "/" or "\". This operator is used to concatenate "path" strings or URL locations. Notice "\" is also escape character used for string templates.


```
new s := "";
rule main()
  let s := "te/" / "/st"; -- "te/st"
  let s := "te/" \ "/st"; -- "te\\st"
  let s := "te"."st"; -- "te\\st" or "te/st" depending on OS
return;
```


### String Generator


Replication operator: "*" will concatenate a string with itself multiple times:


```
** create string of 10 spaces
new s := ' ' * 10;
```


```
rule main():
  ** a string from pattern 01
  new a := "01" * 4;
  print a; -- 01010101;

  ** used in expression will generate string
  new b := (a & ' ') * 4;
  print b; -- 01010101 01010101 01010101 01010101
return;
```


### String Pattern


It is common to create strings from a string pattern using operator "*".


```
str := constant * n ∈ S(n);
```


```
new sep := '-' * 19;
rule main():
  print ('+' + sep + "-");
  print ('|   this is a test   |');
  print ('+' + sep + '+');
return;
```


```
+--------------------
|  this is a test   |
+-------------------+
```


### Control codes


You can insert constants using notation $X or #(nn):


**ASCI Special Codes:**

| DEC | HEX | CODE| NAME            |
| :---| :---| :---| :---            |
| 00 | 0x00 | $NL | Null            |
| 08 | 0x08 | $BS | Backspace       |
| 09 | 0x09 | $HT | Horizontal Tab  |
| 10 | 0x0A | $LF | Line Feed       |
| 11 | 0x0B | $VT | Vertical Tab    |
| 12 | 0x0C | $FF | Form Feed       |
| 13 | 0x0D | $CR | Carriage Return |
| 27 | 0x1B | $ES | Escape          |
| 39 | 0x27 | $AP | Apostroph ''    |
| 34 | 0x22 | $QM | Quotation ""    |



## String Interpolation


In computer programming, string interpolation is the process of evaluating a string literal named template that contains one or more placeholders. An interpolation expression is yielding a result in which the placeholders are replaced with their corresponding values.


We use notation "#()" or "#()[]" to create a placeholder template inside of a String or Text. You can use operator "?" to replace the placeholder with values from a data source. If placeholder is not found the result will contain the placeholder unmodified.

- We can inject values into a string template using modifier symbol: "?";
- System constants "$" are automatically interpolated, do not require symbol "?";
- Template must be included in double quotes "..." not single quotes '...';
- Inside template we use a symbol or format "#()" follow by index "[]";
- The index start from "[0]" and it can be negative;
- If a placeholder index is not resolved then it is preserved unmodified;
- Unlike JavaScript or other languages, variables are not recognized in string templates;

```
** next template uses #(n) placeholder
new template := "Duration:#(n) minutes and #(n) seconds";
new var1 := 4;
new var2 := 55;

rule main():
  print template ? (var1,var2,...); -- Duration:4 minutes and 55 seconds
return;
```


```
** define two A codes
new x := 30; -- Code ASCII 0
new y := 41; -- Code ASCII A
rule main():
   ** template writing alternative
   print "#(n) > #(n)" ? (x,y); -- "30 > 41"
   print "#(a) > #(a)" ? (x,y); -- "0 > A"

   ** using two dots : to separate hour from minutes
   print "#(n):#(n)" ? (10, 45); -- 10:45

   ** using numeric format
   print "#(1,000.00)" ? (1000.45); -- 1,234.56
return;
```


**Placeholders:**
Format template stings can use escape sequences:

```
"#(n)"   = natural number
"#(z)"   = integer number
"#(r)"   = real number using default precision
"#(s)"   = single quoted string for string, symbol or number
"#(q)"   = double quoted string for string, symbol or number
"#(a)"   = ASCII symbol representation of code
"#(u)"   = Unicode symbol representation of code
"#(+)"   = UTF16 code point representation (U+HHHH) for symbol
"#(-)"   = UTF32 code point representation (U-HHHHHHHH) for symbol
"#(b)"   = binary number
"#(h)"   = hexadecimal number
"#(t)"   = time format defined by @time
"#(d)"   = date format defined by @date
"#[*]"   = display array elements (separated by comma)
"#[i]"   = search element by index [i]
"#[k]"   = search element by key value [k]
```


```
rule main:
  print "Numbers:   #(n) and #(n)" ? (10, 11);
  print "Alpha:     #(a) and #(a)" ? (30, 41);
  print "Strings:   #(s) and #(s)" ? ('odd','even');
  print "Quoted:    #(q) and #(q)" ? ('odd','even');
  print "Unicode:   #(u) and #(u)" ? (U+2260,U+2261);
  print "Unicode:   #(q) and #(q)" ? (U+2260,U+2261);
  print "Collection:#[*] and #[*]" ? ([1,2,3],{'a','b','c'});
  print "Collection:#(s)[*] and #(q)[*]" ? ([1,2,3],{'a','b','c'});
return;
```


Expected output:


```
Numbers:   10 and 11
Alpha:     0 and A
Strings:   'odd' and 'even'
Quoted:    "odd" and "even"
Unicode:   ≠ and ≡
Collection:1,2,3 and a,b,c
Collection:'1','2','3' and "a","b","c"
```

- Template modifier: "?" is polymorph and overloaded,
- For template source you can use: { tuple, list, set, hash, array, matrix },
- The parentheses () or [] are exclusive optional. You can use one or the other or both,
- Multiple [*] can be used with any enumerable collection types

## Large template


A large template can be stored into a file, loaded from file and format().

- Create a map collection of elements;
- Create the template text and store it in external file;
- Use a cycle to visit the template file row by row;
- Use template modifier: "?" to replace placeholders row by row;
- Alternative use format() build-in rule to replace all placeholders;

Using Hash:


```
new template1 := "Hey look at this #[key1] it #[key2]!";
new template2 := "Hey look at this #(s)[key1] it #(q)[key2]!";
new map       := {("key1":"test"),("key2":"works")};
rule main():
  print template.format(map);
  print template ? map;
return;
```


Expect output:


```
Hey look at this test it works!
Hey look at this 'test' it "works"!
```


Using Set:


```
new template := "Hey look at this #[0] it #[1]!";
new my_set   := {"test","works"};
rule main():
  print template ? my_set;
return;
```


Expect Output:


```
Hey look at this test it works!
```


## Numeric format


Number type is implementing format() rule. This rule has one string parameter that is optional.


```
# format signature
rule format(number ∈ R, pattern ∈ S) => (result ∈ S):
  ...
return;
```


Where pattern cab gave two forms:

- p := "#(ap:l.d)" -- 1,000.00
- p := "#(ap:l,d)" -- 1.000,00
- p := "#(ap:l;d)" -- 1,000.00 | 1.000,00 (depending on country)

Note: Last pattern is depending on regional settings: $decimal:'.'/','

- a is alignment one of { < > ^ },
- p is the padding character: { _ 0 }
- l is the length of result
- d is number of decimals after "."

Alignment symbol "a" can be one of:


```
> is used to align to the right
< is used to align to the left
= is used to align to center
```


```
"#(r)"       -- real number, with default precision left align
 "#(n)"       -- natural number, unsigned left align
 "#(z)"       -- integer number, with sign left align
 "#(10)"      -- right align numeric with 10 digits padded with spaces
 "#(10.2)"    -- 10 integer digits and 2 decimals, right padded with spaces
 "#(>_:10)"   -- right align 10 digits padded with spaces
 "#(>0:10.2)" -- right align padded to 10 integer digits and 2 decimals
 "#(>0:10,2)" -- right align European numeric style with 2 decimals
```

- format (str ∈ Text, map ∈ {S}) ∈ X;
- format (str ∈ Text, map ∈ {Z}) ∈ X;
- format (str ∈ Text, map ∈ [Z]) ∈ X;
- replace(str ∈ Text, target ∈ String, arrow ∈ String) ∈ X;
- find (str ∈ Text, pattern ∈ String) ∈ N;
- count (str ∈ Text, pattern ∈ String) ∈ N;
- length (str ∈ Text) ∈ N;

Reading a Text:


Text is iterable by "row". The row separator CR or CRLF. So we can read a text line by line. You can use for iteration to check every line of text. Each row is a string. You can also parse a row word by word using a nested for.


Note: The text also support escape sequences like a normal string. However in a text literal we do not have to escape the single quote symbols: "'". We have to escape the double quotes like: "This is "quoted" text". This is very rare since quoted text should use symbols: "« »" like "«quoted»".


This was the Bee draft design for basic concepts. Thank you for reading it all. Our effort has merely begun. There is a lot of testing and developing ahead of us. Next chapter are advanced research topics, just some ideas. Don't read yet.

---

[Go back](collections.md) | [Read next](concurrency.md)
