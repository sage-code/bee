## Data Processing

By using collections and control structures one can load, modify and store data.

* [Array Operations](#Array-Operations)
* [Array Slicing](#Array-Slicing)
* [Matrix Operations](#Matrix-Operations)
* [Set builders](#Set-builders)
* [List operations](#List-operations)
* [Collection Iteration](#Collection-Iteration)
* [Scanning items](#Scanning-items)
* [String Generator](#String-Generator)
* [Text template](#Text-template)

## Array Operations

* Negative index is counting from the end toward the beginning;
* Array elements have very fast direct access by index;
* Array index is a binary integer starting from zero;
* Maximum number of elements: 2³² = 4,294,967,296;
* Array capacity is establish on array creation;
* Array capacity initialization can be deferred;
* Array capacity can be modified with data movement;

**example**

```
make test ∈ [R](10); -- vector of 10 real numbers
make m := length(test)-1;

-- array index start from 0
print test[0]; --first element
print test[m]; --last element

-- alternative notation
print test[!]; --first element
print test[?]; --last element

-- array traversal 
make x := 0;
while (x < m) do
  alter test[i] := x;
  alter x += 1;
repeat;

-- print all elements of array
print test;
over.
```

**Output:**
```
[0,1,2,3,4,5,6,7,8,9]
```

**operations**

```
make a1 := [1, 2, 3];  -- Initialized array
make a2 := [2, 3, 4];  -- Initialized array

-- addition between two Arrays "+" 
make a3 := a1 + a2; --[1,2,3,2,3,4]

-- difference between two Arrays "-"
make a4 := l1 - l2; -- [1]
make a5 := l2 - l1; -- [4]

-- intersection between two Arrays "&" 
make a6 := a1 & a2; -- [2,3]

-- union between two Arrays "|" 
make a7 := a1 | a2; -- [1,2,3,4]
```

**example**
```
rule test_array():
  -- array  with capacity of 10 elements
  make my_array ∈ [Z](10);
  make m := my_array.capacity();
  make i := 0 ∈ u4;
  -- traverse array and modify elements
  while i < m do
    alter my_array[i] := i;     
    alter i += 1;
  repeat;
  ** array  elements using escape template \[]
  print ("This is the first element: \[1]" <+ my_array); 
  print ("This is the last element: \[-1]" <+ my_array);
  
  ** range of array elements are comma separated [1,2,3]
  print ("These are the first two: \[1..2]"        <+ my_array);
  print ("These are the lat two: \[-2..-1]"        <+ my_array);
  print ("These are all except lat two: \[1..-3]"  <+ my_array);
return;
```

**console:**
```
This is the first element: 1   
This is the last element: 10   
```

**resize**
Array capacity can be modified using union operator "∪". This will reset the array reference. That means it will not update any slice or other references you may have to this array. 

```
  -- creation of 10 elements
  make array := [0 * 10]; 
  make refer := array;
  
  print array ≡ refer; --> 0 = True (same array)
  
  -- extend array with 10 more elements
  alter array    := array ∪ [0 * 10]; -- 10 new elements
  alter array[*] := 1; -- modify all 
  
  -- print new array and reference
  print array; --> [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
  print refer; --> [0,0,0,0,0,0,0,0,0,0]  
  
  print array ≡ refer; --> 0 = False (different arrays)
```

## Array slicing

A slice is a small view from a larger array.

**Syntax:**

```
-- declare array with capacity c
make array_name ∈ [element_type](c);

-- unnamed slice can be used in expressions
print array_name[n..m]; 

-- create named slice from array
make slice_name := array_name[n..m]; 
```

Where: n,m are 2 optional numbers, n ≥ 0, m <= capacity-1. 


**example:**

Anonymous slicing notation can be used to extract or modify specific elements from an array; 

```
make a:= [0,1,2,3,4,5,6,7,8,9];
do
  print a[1..-1];  -- will print [0,1,2,3,4,5,6,7,8,9]
  print a[-3..-1]; -- will print [7,8,9]
  print a[1..1];   -- will print [0]
  print a[1..4];   -- will print [1,2,3,4]
 
  -- modify first 4 elements
  alter a[0..3] += 2; 
  
  -- first 4 elements of (a) are modified
  print a;  --> [2,3,4,5,4,5,6,7,8,9]
done;
```

**example**

Slicing notation can be used to create a view to original array.

```
-- original array
make   a := [0 * 5]; 
print  a; --[0,0,0,0,0]

-- making two slices
make c := a[0..2]; --[0,0,0]
make e := a[3..4]; --[0,0]

--modify slice elements
alter c[*] := 1;
alter e[*] := 2;

--original array is modified
print a; -- expect [1,1,1,2,2]

--modify last 2 elements using anonymous slicing
alter a[3..?] := [2,3];

--                     ↓ ↓
print a; --expect [1,1,1,2,3]
```
## Matrix Operations

Modify all elements of the matrix is possible using [*] and assign operator “ := ”

```
** a matrix having 2 rows and 2 columns
** initialize all elements with 100
make M: [Z](2,2);
do
  M[*] := 100;
  print (M);
done;
```
[[100,100],[100,100]]

A matrix can be initialized using literals or constructor.
A matrix can support scalar operations like Array

```
make M ∈ [Z](2,2);
do
  M[*] := 100;
  ** modify all elements
  M[*] += 10;
  print(M); -- [[110,110],[110,110]]

  ** modify an entire row 
  M[1,*] := 0;
  M[1,*] := 1;
  print(M); -- [[0,0],[1,1]]
  
  ** modify an entire column
  M[*,1] += 1;
  M[*,2] += 2;
  print(M); -- [[1,2],[2,3]]
done;
```

**resize matrix**

```
  -- creation of matrix with 10 × 10 elements
  make matrix := [0 * 10, 0 * 10];  

  -- increase matrix number of rows
  alter matrix := matrix & [0 * 5]; -- 5 new rows

  -- increase matrix number of columns
  alter matrix := matrix & [,0 * 5]; -- 5 new columns  
```

**Memory impedance**

Matrices are multidimensional while computer memory is linear. This is an impedance mismatch that require mapping. Some computer languages organize matrices row by row and some others organize memory column by column. The difference between the orders lies in which elements of an array are contiguous in memory.

Row-major and column-major order

Transposition Passing a memory matrix from one computer language into another can require a transposition that can be a performance bottleneck. EVE uses row-major order therefore passing matrix arguments is the most efficient with Rust and C++ languages.

Matrix Traversal When you traverse elements use rows first, than you change the column. A processor will use the internal cache more efficient in this way. If the matrix is large this can be a significant performance issue.

Example: In this example we traverse all the rows then all the column, this is the most efficient way to traverse a matrix.

```
make M := [ 
       ['a0','b0','c0'],
       ['a1','b1','c1'],
       ['a2','b2','c2']
      ];     
** traverse matrix      
make row, col := 0;
while col < 3 do     -- traverse columns
  while row < 3 do   -- traverse row first
    print M[row,col];
    alter row += 1;
  repeat;
  alter col += 1;
repeat;

** traversal with scan
scan M :> e do
  print e; -- element
next;
```

## Set Builders

You can define elements of a subset from a set using the following construction:

```
make sub_set := { var | var ∈ set_name ∧ condition(var)}
```

You can use _var_ to create the _condition_.

**example:**

New set defined from a range or domain:

```
make  new_set := { x | x ∈ [0..5:1] };  -- [0,1,2,3,4,5]
make  new_set := { x | x ∈ [0.!10:2] }; -- [0,2,4,6,8]
```

### Collection Casting

It is common for one collection to be created based on elements from another collection. 
Collection members can be copy into the new collection using a comprehension notation: 

**Example:**
```
make source  := [0,1,2,2,2,2];
do
  -- eliminate duplicates
  make set := { x | x ∈ source };
  print set; -- {0,1,2} 
done;
```

### Collection Filtering
Build notation can use expressions to filter out elements during comprehension operation.

**Example:**
```
make source := [0,1,2,3,4,5];
do
  make set := { x | x ∈ source ∧ (x % 2 = 0) };
  print set; -- {0,2,4} 
done;
```

### Collection Mapping
The elements in one set or list can be transformed by a function or expression to create a new collection.

**Example:**
```
make source := {0,1,2,3,4,5};
do
  -- create Table pairs (key, value) for Table map   
  make target := {(x:x^2) | x ∈ source };
  print target;  -- { 0:0, 1:1, 2:4, 3:9, 4:16, 5:25} 
done;
```

## List Operations
We can add elements to a list or remove elements from the list very fast: 

* operator += append one element to end of list
* operator -= delete one element by reference


### List Concatenation
List concatenation is ready using operator “+”. This operator represent union. 
Therefore List union act very similar to append, except we add multiple elements. 

```
  make a := ('a','b','c');
  make b := ('1','2','3');
  make c := ();

  alter c := a + b;
  print c; --> ('a','b','c','1','2','3');
```

### Join built-in
The join function receive a list and convert elements into a string separated be specified character.

```
  make str := join([1,2,3],',');
  print (str) -- '1,2,3';
```

### Split built-in
The join function receive a list and convert elements into a string separated be specified character.

```
make lst := split("1,2,3",",");
print lst; -- (1,2,3)
```

### List as stack

A stack is a LIFO list of elements: LIFO = (last in first out)

```
make a := (1, 2, 3); --list
make last ∈ N;

-- append to stack with operator "+="
alter a += 4; -- (1,2,3,4)

-- read last element using "-="
alter last := a[?]; --last = 4

-- remove last element using -=
alter a -= a[?]; -- a = (1,2,3)
```

### List as queue

A queue is a FIFO collection of elements: (first in first out)

```
make q := (1,2,3); list
make first : N;

-- enqueue new element into list "+=" 
alter q += 4; -- (1,2,3,4)

-- read first element using ":="
alter first := a[!]; --first = 1

-- dequeue first element using "-="
alter a -= a[!]; --a = (2,3,4)
```


### Other built-ins

Following other functions should be available
* List.append(value) -- can append an element at the end of the list
* List.insert(value) -- can insert an element at the beginning of the list
* List.delete(value) -- can delete one element at specified index
* List.count() -- retrieve the number of elements 

### Special attributes
A list has properties that can be used in logical expressions:

* List.empty()  -- True or False
* List.full()   -- True or False

## Collection Iteration

A special _while loop_ that is executed for each element belonging to a collection.

**pattern**
```
make element := collection.first();
while ¬(element is Null) do
  ** statements
  ...
  element := collection.next(element);
repeat;
```

The "element" is local to iteration and is used as control variable.

**example**

```
make my_list := ['a','b','c','d','e']; 
scan my_list :> element do
  write element;
  when element = 'd' do
    stop; -- early termination;
  else
    write(',');
  done;
next;
```
> a,b,c,d

## Scanning items

Collections have common methods that enable traversal using _scan_. 

{List, Table, Set} 

**built-in:**

* count      - retrieve the number of elements 
* capacity   - retrieve the maximum capacity
* next       - position next element 
* first      - position to first element
* last       - position to last element
* this       - reference to current element

### Set Iteration
Hash and Set are similar. We can visit all elements using _scan_:

**Example:**
```
my_map := {("a":1),("b":2),("c":3)};
scan my_map :> (key:value) do
  print('("' + key + '",' + value +')');
repeat;
```

Will print:
```
("a",1)
("b",2)
("c",3)
```

## Hash collections

Hash tables are sorted in memory by _key_ for faster search. It is more difficult to search by value because is not unique and not sorted. To search by value one must create a loop and verify every element. This is called full scan and is very slow so you should never use this method.


**example:**
```
** check if a key is present in a hash collection
make my_map := {(1:'a'),(2:'b'),(3:'c')};
make my_key := 3;
when (my_key ∈ my_map) do
  print('True'); -- expected
else
  print('False');
done;
```

**example**
```
make animals ∈ {S,S};
do
  animals['Bear'] := 'dog';
  animals['Kiwi'] := 'bird';
  print(animals);
done;
```

Output:
```
{('Bear':'dog'),('Kiwi':'bird')}
```

## Type inference

* The default type inference for empty "set" is {}
* An empty hash map will be created using notation {} 

### Example
```  
make animals := {}; -- partial declaration
do
  -- establish element types (S:X)
  animals['Rover'] := "dog";

  -- use direct assignment to create 2 more element
  animals['Bear'] := "dog";
  animals['Kiwi'] := "bird";
  print(animals);
done;
```
output:
```
{('Rover':"dog"),('Bear':"dog"),('Kiwi':"bird")}  
```

## String: concatenation

Strings can be concatenated using:

* fast concatenation operator: "&"
* trim concatenation operator: "+"
* path concatenation operator: "/"

**Example:**
```
** this is example of string concatenation
make str := ""; 
do
  ** set string value using different operators
  str := "this " & " string";  -- "this  string"
  str := "this " + " string";  -- "this string"
done;
```

**path concatenation**
Two strings can be concatenated using concatenation operator "/" or "\\". This operator is used to concatenate "path" strings or URL locations. Notice "\\" is also escape character used for string templates.

```
make s := "";
do  
  alter s := 'te/' / '/st'; -- "te/st"
  alter s := 'te/' \ '/st'; -- "te\\st"
done;
```

## String Generator

It is common to create strings automatically.

**Operator:**  "*"

```
make str := constant * n ∈ S(n);
```

**Example:**
```
make sep := '-' * 19;

print ('+' & sep);
print ('|   this is a test   |');
print (sep & '+');
```

**Output:**

```
+--------------------
|  this is a test   |
--------------------+
```

### Text Template

We use hash "\{}" to create a placeholder into a Text. We use "<+" operator to replace the placeholder with values. If placeholder is not found the compiler raise an error. If the string is a variable this verification is not possible at compile time so maybe you get a run-time error.

**Notes:**

* We can include numbers into a string using template operator "<+"
* Inside template we use "\{n}" notation to find a value using the member index
* Template must be included in double quotes " " 
* If a placeholder index is not found then it is preserved as is

```
make var_name := template <+ (variable);
make var_name := template <+ (var1,var2,...);
```

**Examples:**
```
make x := 30; --Code ASCII 0
make y := 41; --Code ASCII A

--template writing
print ("\{0} > \{1} > \{2}" <+ (x,y)); --print "30 > 41 > {2}"
  
```

**Escaping**

Format/template stings can use escape sequences:

```
\s  : single quoted string
\q  : double quoted string
\n  : number  
\a  : ASCII symbol 
\u  : Unicode symbol
\h  : hexadecimal
\b  : binary
\t  : time format
\d  : date DMY format
\() : [numeric format](#numeric-format)
\{} : Attribute by name/ Value by key
\[] : Array/Matrix element by index \| List elements: [!] or [?] 
```

**examples**
```
print "Numbers: \n and \n" <+ (10, 11);
print "Alpha: \n and \n" <+ ('a', 'b');
print "Strings: \s and \s" <+ ('odd','even');
print "Quoted:  \q and \q" <+ ('odd','even');
print "Unicode: \u and \u" <+ (U+2260,U+2261);
```
**Expected output:**
```
Numbers: 10 and 11
Alpha: a and b <+ ('a', 'b');
Strings:'odd' and 'even'
Quoted: "odd" and "even"
Unicode: ≠ and ≡
```

**Notes**: 
* Injector "<+" is polymorph and overloaded operator. 
* For template you can use: { tuple, list, table, array }

## Large template

A large template can be stored into a file, loaded from file and format().

1. Create a map collection of elements;
2. Create the template text;
3. Use _scan_ to visit all elements;
4. Use injector operator: "<+" to replace template row by row;
5. Alternative use _format()_ build-in to replace placeholders in all text;

**Using Hash**
```
make template := "Hey look at this \{key1} it \{key2}";
make map      := {("key1":"test"),("key2":"works!")};

print template.format(map);
```

Expect output:
```
Hey look at this test it works!
```

**Using Set**
```
make template := "Hey look at this #[0] it #[1]";
make my_set  := {"test","works!"};
print (template <+ my_set);
```

Expect Output:
```
Hey look at this test it works!
```

## Numeric format
Number type is implementing format() method. This method has one string parameter that is optional.

```
rule format(Number: n, String: f) => (result @ S);
```

Where "f" is a pattern: '(ap:m.d)'

* a is alignment one of {<,>,^}, 
* p is the padding character: {'_','.',' ',0...}
* m is the length 
* d is number of decimals 

### Alignment symbol "a" can be one of:
```
> is used to align to the right
< is used to align to the left
^ is used to align to center
```
### Format examples:
```
 '(>_:10)'   -- right align string fill with spaces to 10 characters
 '(>0:10.2)' -- right align fill with 0 up to 10 digits and use 2 decimals
```

### Text functions

* Text:    format (Text: str, Table: map);
* Text:    replace(Text: str, String: target, String: arrow );
* Integer: find   (Text: str, String: patern);
* Integer: count  (Text: str, String: patern);
* Integer: length (Text: str);

**Reading a Text**

Text is iterable by "word". The word separator is one space. So we can read a text string word by word not line by line. We can use "for" iteration to check every word in the text. One word can not start/end with space. 

**Note:**
The text also support escape sequences like a normal string. However in a text literal we do not have to escape the single quote symbols: "'". However we have to escape the double quotes like: "This is \"quoted\" text". This is very rare since quoted text should use symbols: "« »" like "«quoted»"

**Read next:** [Standard Library](standard.md)