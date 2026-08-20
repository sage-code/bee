
# Bee Objects


Bee has pre-defined root Object with standard methods and attributes. The Object can be extended and can have a custom design constructor. You can create instances of Object and, you can use dot notation to access object members.


Method Call


## Instantiation


An object can be instantiated using reserved keyword "new" and  JSON literal or constructor Object() with arguments. After the object is created you can enhance the object.


```
** empty object
new object := {}; 

** set attribute values
new object.a1 := 1;
new object.a2 := 2;

** check the object
expect object = {a1:1, a2:2};

** remove attributes
del object["a1"];
del object["a2"];

** check the object
expect object = {};
```


### Custom type


Type of objects can be defined using JSON. You can enumerate attributes with type declarations in a complex structure. Later you can create instances of this type using the default object constructor.


```
** object subtype with attributes
type TName: {a1, a2 ∈ Type, a3 ∈ Type, ...} < O;

** call default constructor
new myObject = TName(a1:value1, a2:value2, a3 value3 ...);
```


Note: Default object constructor is created automaticly by the compiler. You can use the type-name as if you have already implemented a constructor for this new type.


Next example demonstrate an object with two attributes that have default values. Attributes with default values can be created using type inference.


```
** define object type using JSON
type T:{a1:10, a2:5};

** create two new objects
new obj1 := T(a2:0); -- a1, a2 are optional
new obj2 := T(1,10); -- attribute names are optional

** check the object
expect obj1 = {a1:10, a2:0};
expect obj2 = {a1:1, a2:10};
```


### Object constructor


A custom object type can be created automaticly by the compiler using type inference. All you need is a rule that return an object with rule name reused as type. The compiler will detect that result  type is not defined so it will create a default type behind the scene.


```
** define object constuctor 
rule TName(a1 ∈ Type, ...) => (self ∈ TName):

  ** initialize object attributes 
  let self.a1 := a1;
  ....

  ** define object method
  rule .name(self  ∈ TName):
    ...
  return;
return;
```


### Encapsulation


An object constructor is a high order rule. It has a static context and can contain object states and methods. All methods are sharing the same context. Result is by convention called "self" and it represent the current context.


Access to public members is enable by using dot qualifier notation. The qualifier is the actual object represented as input-output parameter or result: "self"  that is explicitly defined as parameter for every public method.


Object scope is dynamic in contrast to the constructor scope that is static. The "self" scope is pass to public methods as a pointer. Object scope is created by the object constructor rule using keyword "new:.


We define an object constructor Foo that has two attributes and a public method. The constructor receive parameters (a,b) and create an object with attributes {a,b}. The .log() method is called using "apply" keyword.


```
** define object constructor:
rule Foo(a, b ∈ N) => (self ∈ Foo):
    ** create object attributes
    new self.a := a;
    new self.b := b;

    ** define method: log
    rule .log(self ∈ Foo):
        print "a =" + self.a;
        print "b =" + self.b;
    return;
return;

** test Foo
rule main:
    ** create an instance of Foo
    new test := Foo(1,2);

    ** call a method test.log
    apply test.log;

    ** verify attribute values
    fail if test.a ≠ 1; 
    fail if test.b ≠ 2; 

    ** what is the object type
    print type(test); -- Foo
return;
```


```
a = 1
b = 2
Foo
```

- Constructor name start with capital letter;
- Public members start with self. qualifier;
- Result self, is the new object instance;

## Object structure


Next example define an object using a constructor. This particular constructor can receive a variable number of arguments and produce an object that has two attributes.


```
** define the object type
rule MyObject(*v ∈ [N]) => 
             (self: {sum ∈ N, avg ∈ R}):
    ** private variable
    new count := 0;
    cycle:
        new x ∈ N;
    for ∀ x ∈ v do
        let self.sum  += x; 
        let count += 1;
    repeat;
    let self.avg := self.sum / count;
return;
```


Note: In previous example we demonstrate type inference for result object. Object attributes are defined in the result declaration: Compiler will create the attributes from JSON and assign default values.


## Key Looping


Bee objects are based on dictionaries. In fact an object do not have attributes it has keys. That is, each attribute is a (key:value) pair.


```
** define object type
rule MyObject(*values ∈ R) => (self ∈ O):
    ** set initial attributes
    let self:={a1, a2, ... ∈ N};

    ** set attribute values in a loop
    cycle:
        new i := 0;
        new k ∈ S;
    for ∀ k ∈ self.keys() do
        let self[k] := values[i];
        let i += 1;
    done;
return;
```


### Inheritance


By default, Bee custom types are dynamic and can be extended using inheritance. We use symbol "<:" to define the super-type. A derived type can call super type constructor using qualifier: "super."


```
** define custom type
type Foo: {a, b ∈ N} <: Object;

** define Foo constructor
rule Foo(p1, p2 ∈ N) => (self ∈ Foo);
   let self := {a:p1, b:p2};

   ** overvrite the original method
   rule .log():
      print "a = ", self.a; 
      print "b = ", self.b; 
   return;
return;

** define Bar derived type:
type Bar: {a, b ∈ N, c ∈ R} <: Foo;

** define Bar constructor
rule Bar(p1, p2 ∈ N) => (self ∈ Bar);
   let self   := super(p1, p2);
   new self.c := p1+p2;

   ** overvrite the original method
   rule .log():
      super.log();
      print "c = ", slef.c;
   return;
return;

** test Bar constructor
rule main:
   new bar := Bar(3,4);
   apply bar.log();
return;
```


```
a = 3
b = 4
c = 7
```


### Abstraction


Bee can define an abstract constructor. This can contain forward declarations. These are method signatures that have no statements and can't be run.


Next example demonstrate how to create a constructor for abstract type. An abstract rule can't be instantiated directly. It is design for inheritance. You must implement all the abstract methods when you extend it.


```
** define abstract type
rule Root() => (self ∈ Root):
   ** define an abstract method
   rule .log(self ∈ Root);
return;

** implement an abstract type
rule Foo(a,b ∈ N) =>(self ∈ Foo <: Root);
   ** imlement the log method
   rule .log(self ∈ Foo):
      for x ∈ self.keys() do
         print x + " = " + self[x]; 
      done;
   return;
return;

rule main:
   new foo := Foo(1,2);
   apply foo.log;
return;
```


### Traits


A trait is a special rule that encapsulate behaviour. Traits can be used to extend a specific type. When you apply a rule to an object this is enhanced with new behaviour.


An object, can be augmented using traits. The trits are specified using symbol + follow by a comma separated list of traits. The traits can be local or imported from other module.


```
type TName {attribute Type, ...} <: Object+(trait_list):
```


In next example we define a trait. The trait is used to define type Foo that is augmented. To signal an augmented object type you must use symbol "+" after the type name.


```
** define new trait
rule augment(self ∈ O):
   ** overvrite the log method
   rule .log(self ∈ O):
      for x ∈ self.keys() do
          print x + " = " + self[x]; 
      done;
   return;
return;

** use trait augment to define Foo
rule Foo(a, b ∈ N) => (self:Foo <: Foo+):
   ** apply the augmentation
   apply augment(self);
return;

rule main:
   new bar = Foo(a:1, b:2);
   apply bar.log;
return;
```


```
a = 10
b = 20
```


## Data Structures


In data science you need to organize structured data in memory. Memory is flat so you can use Objects to make a complex structure. For example you can store Object references into a Collection.

Array of Objects


### Array of Objects


```
type  Person: {name ∈ S, age ∈ N} <: Object;
rule main:
  ** array of 10 persons
  new catalog ∈ [Person](10);

  ** initialize value using literals
  new catalog[1] := {name:"Cleopatra", age:15};
  new catalog[2] := {name:"Martin", age:17};

  ** using one element with dot operators
  print catalog[1].name;  -- will print Cleopatra
  print catalog[2].name;  -- will print Martin

  ** member type can be check using _type()_ built in
  print type(Person.name); -- will print U
  print type(Person.age);  -- will print W

  ** print size of structure
  print size(Person);
return;
```


### Recursive Structures


Recursive structure type is an Object that contains one or more references to other Objects of the same type as himself. The Object can grow in size and create a tree.


```
** example of single recursive node
type Node: {
  data ∈ Z,       -- integer data
  previous ∈ Node -- reference to previous node
} <: Object;
```


A linked List could be created using this kind of Object. In principle a Linked List has 2 references. One is for prior element and another is the next element:


```
** example of double recursive node
type Node: {
  data  ∈ Z,    -- integer data
  prior ∈ Node, -- reference to previous node
  next  ∈ Node  -- reference to next node
} <: Object;
```


Note: First element will have prior = Null. Last element will have next = Null. There is more to say about these kind of objects. We will explain complex data structures in the next chapter.
Read next:
Collections

---

[Go back](functions.md) | [Read next](collections.md)
