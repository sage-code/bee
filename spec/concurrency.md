
# Bee Concurrence


### Multi threading


Bee has capability to run in parallel multiple instances of a rule. For this we need to start a rule asynchronously and run other rules or the same rule in a parallel thread. This is called multi-threading application. For this we introduce new kwyeords:


| Table |
| --- |
| keyword | description |
| begin | call a rule asynchronously and create a new thread |
| wait | suspend a thread for specific number of seconds |
| yield | suspend current thread and give priority to other threads |



Asynchronous call can be done using a control cycle and keyword  "begin". This is significant because a rule need parameters. By using keyword "begin" we initiate one rule "test" 4 times but this rule does absolutely nothing, just wait about 30 seconds.


```
-- suspend n seconds
rule test:
    wait 10 + i*5;
return;
-- prepare for execution 4 threads
rule main:
    for ∀ i ∈ (1..4) do
       begin test(i);
    repeat;
    wait; -- wait for other threads to finish;
return;
```


A big problem in asynchronous call is to capture the results of a rule that run in parallel mode. In the next example we use map-reduce design pattern to create sum of numbers in parallel. The results are captured into a list. Then we reduce the results by making sum of sums and create the output.


Map-Reduce Pattern


```-- suspend n seconds
rule sum(a, b ∈ Z) => (r ∈ Z):
  cycle:
    new i := 0
  for ∀ i ∈ (a..b) do
    let r += i;
  repeat;
return;
-- prepare for execution on 4 threads
rule main:
    new results <: List; -- partial sum collection
-- use a mapping technigue to split data in 4 equal batches
    cycle:
        new i ∈ N;
    for ∀ i ∈ (1.!100:25) do
        begin test(i,i+25) +> results;
    repeat;
    wait; -- wait for other threads to finish;
    new output ∈ Z;
-- reduce results into output
    for ∀ partial ∈ results do
       let output += partial;
    repeat;
    print output; -- 5050
    expect output = 5050;
return;
```


Note: There is a smarter way of doing this sum using a formula: (1+100)*50 = 5050. But of course we pretend we don't know this and do it in the hard way. The point is we have done it in parallel on a multithread application.


# Bee Coroutines


## Coroutines


Coroutines are rules that can be suspended with all states ready then resumed on demand multiple times. Each time we resume a coroutine this can produce one result that we capture. So a coroutine can produce multiple results until finishes.


Coroutines can be used as a branch of main thread. This is not yet running in parallel but is an example for how a rule can play as a coroutine.

- you need only one coroutine to create a side branch,
- call a branch using  "begin" and suspended using  "yield",
- resume a coroutine using yield plus routine name.

```
rule test(n ∈ N) => (result ∈ N):
-- can generate n numbers
  cycle:
    new i ∈ N;
  for ∀ i ∈ (1..n) do
    let result := i;
-- suspend execution
    yield; -- wait for the main thread
  cycle;
  result = 0; -- finalization signal
return;

rule main:
-- start secondary process
    begin test(9)     -- initialize coroutine
    cycle:
      new  r ∈ N;  -- result reference
    do
      yield r <- test;  -- capture next result
      write (r, ",");
    repeat if r > 0;

    print;  -- 0,1,2,3,4,5,6,7,8,9,
return
```


Note:&In the example above, the program is still working in serial mode, except that has a branch running on a separated thread. When the coroutine function the main thread is on hold, and when the main thread function the coroutine is waiting.


## Producer consumer
Producer consumer patern is using coroutines that can work in palallel in asynchronous mode. That means we start coroutines and do not wait to finish but let the main thread to continue. A producer is preparing the work and the consumer is doing the work.
If you do not know how this works, take a look to the diagram below. We have one rule called "producer" one list that act as queue and a routine called "consumer". The queue has a limited capacity. We can use same consumer twice, if we do then the application is also multi-threading..



Producer Consumer Diagram

Notes:

for this you need two rules: one is producer and other is consumer,
the main thread is starting threads using begin ,
producer is a dispatcher that distribute the work,
producer is usually working on a single thread;
consumer is a worker that resolve a task given by the producer;
consumer is usually working on multiple threads;

Example:
Info: This example is complex so we have chosen to keep it on GitHub with the Bee project. If you want to visualize it you need Notepad++ and color syntax highlighter. Go back to index page and follow the instructions at the bottom of the page.
Read more:
Graphics


Producer consumer patern is using coroutines that can work in palallel in asynchronous mode. That means we start coroutines and do not wait to finish but let the main thread to continue. A producer is preparing the work and the consumer is doing the work.


If you do not know how this works, take a look to the diagram below. We have one rule called "producer" one list that act as queue and a routine called "consumer". The queue has a limited capacity. We can use same consumer twice, if we do then the application is also multi-threading.


Producer Consumer Diagram

- for this you need two rules: one is producer and other is consumer,
- the main thread is starting threads using begin ,
- producer is a dispatcher that distribute the work,
- producer is usually working on a single thread;
- consumer is a worker that resolve a task given by the producer;
- consumer is usually working on multiple threads;

---

[Go back](processing.md) | [Read next](graphics.md)
