
# Bee Functions

Bee is a hybrid language, it has functional behaviour. In this chapter we ellaborate the functional aspects of Bee language.

## Lambda expressions


A lambda expressions can have parameters and results. Lamda expressions can be used to create functions. Lamda expressions do not have a local scope.


```
--  declaration of Lambda expressns
new name := λ(p1 ∈ Type,...) => (expression) ∈ ResultType;
```


```-- define lambda expression
new exp := λ(x,y ∈ Z) => x^y ∈ Z;
-- use introspection
print type(exp); -- L
-- use the lambda expression
new z := 2 * exp(2,3);
-- verify the result
expect z = 16; -- will pass
print z;
```


Lambda Expressions...

- are similar to mathematical functions;
- can be used in other expressions;
- can be used as arguments for call-back;
- can be created from a rule as a result;
- can be assigned to variables of type: L

restrictions:

- have no internal states;
- have deterministic result;
- do not have side-effects;
- do not modify external states;

result:

- lambda expressions can produce one single result;
- result type must be specified but not the result name;
- result is temporary and can be used in other expressions;

## Lambda type


Lambda expressions have a special type: "L", that is a reference. This type can be used to define variables, collection elements  or parameters that require a lambda expression;


In next example we create a dictionary of expressions then we call every expression in the dictionary by string ID. This is a trick useful to parse a specific formula that comes as a string. You can use this trick for example to implement custom domain specific expressions.


```-- instantiate 3 Lambda expressions
new gt := λ(x, y ∈ Z) => (x > y) ∈ L;
new lt := λ(x, y ∈ Z) => (x < y) ∈ L;
new eq := λ(x, y ∈ Z) => (x = y) ∈ L;
-- define a sub-type, dictionary of rules
type Dic: {[A]:L} <: Map;
-- define a hash map of expressions
new dic := {'gt':gt,'lt':lt,'eq':eq} ∈ Dic;
-- call 3 rules in very unusual way
print dic['gt'](3,1); -- 1
print dic['lt'](1,2); -- 1
print dic['eq'](2,2); -- 1
```


## Call-back functions


Lambda expressions become call-back functions when used as arguments for specific rules that require lambda expressions. The function is executed later in the rule. Lambda function signature is required to define the parameter.


```
rule foo(a1, a2 ∈ N, xp: λ(x,y ∈ N) => R) => (r ∈ Type):
-- prepare the result
   let r := xp(a1,a2);
return;

rule main:
-- call foo using anonymous expression
   print foo(2,3,(x,y)=> x^y); -- 8.0
   print foo(2,3,(x,y)=> x*y); -- 6.0
   print foo(2,3,(x,y)=> x/y); -- 1.5 
return
```
---

[Go back](rules.md) | [Read next](objects.md)
