# Control Flow

Bee provides the following block statements:

| Name | Description |
| :--- | :--- |
| `start` | Named block with local scope |
| `with` | Qualifier suppression block |
| `if` / `else` | Decision fork |
| `ladder` | Multi-path decision structure |
| `cycle` | Unconditional repetitive block |
| `for` | Iterative block with local scope |
| `match` | Multi-path value selector |
| `trial` | Exception handler block |

## Start
We occasionally use a block of code with a local scope via the `start` keyword. The label is optional.

```bee
start [label]:
  -- local variables
do
  -- executable block
done [label];
```

## With
Starts a "qualifier suppression block," eliminating the need for explicit module qualifiers within an anonymous local scope.

```bee
-- using qualifier suppressor
use lib_folder/test_module as test;

rule main:
  new x := 2;
  with test do
    -- calls inc() without test. qualifier
    expect x == 3;
    print inc(x);
  done;
return;
```

## If-Else
The `if` and `do` keywords create tasks executed conditionally.

### Conditional Branch
```bee
if condition do
  -- statements
done;
```

### Two-ways Conditional
```bee
if condition do
  -- true branch
else
  -- false branch
done;
```

## Decision Ladder
A cascade of decisions using `if` and `else if` chains.

```bee
-- decision ladder
start test:
  new a ∈ Z;
  read("a = ", a);
  if a = 0 do
    print "a = 0";
  else if a > 0 do
    print "a > 0";
  else if a < 0 do
    print "a < 1";
  else
    print "unexpected: " + a;
done test;
```

## Cycle
Repetitive blocks using the `cycle` keyword.

### Infinite Cycle
```bee
cycle [label]:
  -- local variables
do
  -- repetitive block
repeat [label];
```

### Conditional Run
```bee
cycle:
  -- local variables
do
  -- repetitive block
  [redo if condition1];
  [stop if condition2];
repeat [if condition3];
```

### While Condition
```bee
cycle [label]:
  -- define local variables
while start_condition do
  -- first repetitive block
  [stop if condition]; -- break the cycle
  [redo if condition]; -- restart the cycle
then
  -- non-repetitive block
repeat [label];
```

## For
An iterative cycle controlled by a domain or collection.

```bee
cycle [label]:
  -- local variables
  new i ∈ N;
for ∀ i ∈ (min..max:rate) do
  -- repetitive block
  [next if condition]; -- fast forward
  [stop if condition]; -- early transfer
[then]
  -- non-repetitive block
repeat [label];
```

## Match
A multi-path selector based on a series of blocks.

```bee
match select [all] | [one]:
  when v1 do
    -- first path
  when v1, v2 do
    -- second path
  other
    -- default path
done;
```

## Trial
The exception handler block for managing complex, multi-step processes.

```bee
trial [label]:
  -- initial or default statements
try [code1]:
  -- step 1
  fail {code, message} if condition;
try [code2]:
  -- step 2
  raise {code, message} if condition;
case $error.code = code do
  -- handle specific error
  resume;
miss
  -- handle all other errors
  raise;
final
  -- cleanup region
done [label];
```
