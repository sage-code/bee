## Execution

You can execute the public methods of a secondary module in two modes: synchronous mode and asynchronous mode. This is how you can split a large applications into smaller, more manageable parts that can be executed in parallel.


In next module called: "test_module.bee", we create a public rule that delay execution for several seconds using "wait" then it returns a result "r" equal to the argument value "t". So the rule basicity does nothing but wait.


```
--  secondary module: test_module.bee
rule .test(t ∈ Z) => (r ∈ N):
  let  r := t; -- prepare the result
  wait t;      -- wait for t seconds
return;
```


Let's use the module previously defined in synchronous mode.


```
--  main module
use $pro_src.test_module;

alias test = test_module.test;

+--------------------------------
execute test() and append result
at the end of "collect" list
--------------------------------+
rule main:
-- define a collector (list)
   new collect ∈ (N);

   apply collect <+ test(30);
   apply collect <+ test(40);
   apply collect <+ test(10);
   apply collect <+ test(20);
-- the collector is unordered
   print collect; -- (30,40,10,20)
return;
```


Let's use the module previously defined in asynchronous mode. For this we use keywords "begin" to start a process and "wait" for all asynchronous sub-processes to synchronize.


```
--  main module
use $pro_src.test_aspect.(*);

+-----------------------------------------
   execute test() and append result
   at the end of "collect" list
-----------------------------------------+
rule main:
-- define a collector (list)
   new collect ∈ (N);

   begin collect <+ test(30); -- open one thread
   begin collect <+ test(40); -- open one thread
   begin collect <+ test(10); -- open one thread
   begin collect <+ test(20); -- open one thread

   wait; -- stop and wait for the all open threads to finish
-- the collector is ordered
   print collect; -- (10,20,30,40)
return;
```


**Note:** By using begin and wait you can create multi-session applications. Each aspect is executed on a different core, and the application runs them in parallel. The main thread is waiting using resolve keyword for the threads to finish.
