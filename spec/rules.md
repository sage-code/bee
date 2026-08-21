# Bee Rules

Bee is a rule-oriented language. We use rules to create small sub-programs that serve diverse roles. You can define a rule and later you can apply a rule once or several times.

## Rule Anatomy

A rule declaration starts with the keyword "rule" and ends with "return". 

- A rule starts with keyword: `rule`
- A rule ends with keyword: `return`
- Rules are subprograms that can have side-effects, similar to procedures, methods, or subroutines.
- Rules can have public/private states.

## Rule Parameters

Parameters are special variables defined in the rule signature using parentheses.

```bee
** a rule with two parameters
rule foo(name ∈ S, message ∈ [S]):
    let message := "hello: " + name + ". I am Foo. Nice to meet you!";
return;

rule main:
    new str ∈ S;
    apply foo("Bee", str);
    print str;
return;
```

**Notes:**
- Parameters are enumerated in a list separated by comma.
- Optional parameters are initialized using `=`.
- Primitive type parameters receive values by copy.
- Composite type parameters receive values by share.

## Rule Results

A rule can have multiple results, declared in a result list similar to the parameter list. A rule that have results can be used like a function in right side of the assign expression.

```bee
** rule with two results "s" and "d"
rule com(x ∈ Z, y: 0 ∈ Z) => (s, d ∈ Z):
    let s := x + y;
    let d := x - y;
return;

rule main:
    ** capture result into a single variable
    new r := com(3, 2);
    print r; -- (5, 1)

    ** deconstruction of result into variables: s, d
    new s, d := com(3, 2);
    print (s, d, sep: ","); -- 5, 1

    ** ignore second result using variable "_"
    new a, _ := com(3);
    print a; -- 3
return;
```

**Notes:**
- Multiple results are declared with names and can have initial values.
- A rule with multiple results can be called using the spread operator `*`.
- You can ignore one result using the anonymous variable `_`.
- Rules with multiple results cannot be used directly in expressions.

## Variadic Rules

The last parameter in a parameter list can use the prefix `*` to receive multiple values into an array. This is called a "varargs" parameter.

```bee
rule foo(*bar ∈ [Z]) => (x ∈ Z):
    new c := bar.count();
    if (c == 0) do
        let x := 0;
        exit;
    done;
    for ∀ i ∈ (0.!c) do
        let x += bar[i];
    repeat;
return;

rule main:
    print foo();        -- 0
    print foo(1, 2, 3); -- 6
return;
```

## Early Termination

A rule usually ends with the `return` keyword. However, it can be interrupted using the `exit` keyword to terminate without signaling an error.

```bee
rule name(param ∈ type) => (result ∈ type):
    exit if condition; -- early successful exit
    let result := expression;
return;
```

## Advanced Topics

### Forward Declarations
In Bee, you cannot use an identifier before it is declared. If two rules call each other, you can use a forward declaration.

```bee
rule plus(a, b ∈ Z) => (r ∈ Z); -- forward declaration

rule main:
   print plus(1, 1);
return;

rule plus(a, b ∈ Z) => (r ∈ Z):
  let r := (a + b);
return;
```

### Recursive Rules
Recursive rules call themselves. While functional, they can be inefficient if not optimized.

**Tail Call Optimization (TCO):**
If the last action in a rule is a call to itself, the compiler can optimize it to act like iteration.

```bee
rule tail(n ∈ N, acc ∈ N) => (r ∈ N):
    when (n = 0) do
      let r := acc;
    else
      let r := tail(n-1, acc * n);
    done;
return;
```

### External Rules
External rules allow importing functions from other languages (e.g., C/C++).

```bee
use $bee.lib.cpp.myLib;

rule fib(n ∈ Z) => (x ∈ Z);
  let x := myLib.fib(n);
return;
```

### Closures
A closure is a rule defined inside another rule, often used for encapsulated logic or state.

```bee
rule foo(start: 0 ∈ N, step: 1 ∈ R):
    set .count := [start];
    set .step := [step];

    rule .next() => (r ∈ Z):
       let r := foo.count + foo.step;
       let foo.count := r;
    return;
return;
```

---

[Go back](control.md) | [Read next](functions.md)
