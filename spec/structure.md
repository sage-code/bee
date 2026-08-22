# Code Structure


Next you can learn general concepts about Bee applications:

- Project
- Modules
- External Code
- Name space
- Execution

## Projects


A Bee project is a folder with a specific structure. A project contains one or more applications that can run independent of each other on same computer or a group of computers. For example applications can be designed to collaborate with each other into n-tire architecture or can be a group of OS commands for image manipulation.


project tree


Next project tree contains two applications: client/server and show folders where you should put your code (src+lib) and documentation (doc). This is a recommendation but not a hard rule. You can organize your project better if you are experienced developer.


```
$pro_home
  |-- bin
  |   |-- client.exe
  |   |-- server.exe
  |
  |-- src
  |   |-- module1.bee
  |   |-- module2.bee
  |
  |-- lib
  |   |-- library1.bee
  |   |-- library2.bee
  |
  |-- doc
  |   |-- readme.md
  |   |-- index.html
  |
  |-- client.bee
  |-- server.bee
```


### System Variables


System variables are using "$" prefix. There are several predefined system variables available in Bee. These can be used to locate project files or connect to databases. You can define new system variables at the beginning of main module or in configuration files.


| Table |
| --- |
| Variable | Environment | Description |
| $bee_home | BEE_HOME | Bee home folder |
| $bee_lib | BEE_LIB | Bee library home |
| $bee_path | BEE_PATH | Bee library path |
| $pro_home | N/A | Project home folder |
| $pro_lib | N/A | Project library folder |
| $pro_mod | N/A | Project modules folder |
| $pro_log | N/A | Log output folder |



### Compiler directives


Compiler directives are system variables that control the compilation process. You can setup these options in compiler configuration file or in source file. You can not change these options after compilation. They are available for introspection.


System environment variables are using the same prefix "$". So there is a conflict. To avoid this conflict, you should use capital letters for environment variables. Bee is loading only environment variables specific to Bee.


| Table |
| --- |
| Constant | Default | Description |
| $max_precision | 0.00001 | Control numeric precision |
| $max_recursion | 10000 | Control how deep a recursion before give up |
| $max_iteration | 0 | Control how many iterations before give up |
| $loop_timeout | 60 | Control time in seconds before a loop is forced to give up |
| $log_debug | "Off" | Control if debug information is included |
| $log_echo | "Off" | Control if statement is printed to console in case of error |
| $log_trace | "Off" | Control if @trace variable is getting populated with information |
| $date_format | "DMY" / "MDY" | Control date format: DD/MM/YYYY or MM/DD/YYYY |
| $time_format | "T24" / "T12" | Control time format: HH:MM:SS,MS am/pm or HH:MM:SS,MS |
| $platform | "Windows" | Alternative: "Linux", "Mac" is the target platform |


- You can set compiler parameters in the main module but not in secondary modules
- Precision is controlling only rational numbers.;

### Global Variables


Global variables are defined usually at the beginning of a module outside of any rule.


Following system variables are available for debugging:


| Table |
| --- |
| $timer | duration information about last statement |
| $stack | debug information about current call stack |
| $trace | reporting information about statements |
| $query | last query statement |
| $error | last error object |
| $threads | number of active threads |
| $trial | trial object, contain last trial messages |


- System variables are global and are defined in core library;
- You can define your own global variables in main module;
- Prefix "$" is used to improve code readability;

## Modules


As we mentioned already Bee is modular. It means one large project can be split into parts. Each part can contain reusable rules. A module can load several other modules. An application need an entry point that orchestrate the program execution. This is called the "main" module. Below we explain each kind of module:


### Main Modules


Main module contains declarations for the main rule. One project can have one or more main modules. Each main module represent one single application.  Main module is located in the project root folder.


**Notes:**

- The main module can not be loaded, in other modules;
- The main module do not have public members;
- One project can have many main modules;
- The main module can receive parameters;

### Secondary Modules


A good designer will split a large problem into secondary modules. These modules are similar to the main module except they do not have the main rule. One secondary module can be used in one or more relate applications. Secondary modules are located in src folder. These modules can be loaded into other modules to be re-used.


**Notes:**

- Secondary modules are specific to a project;
- Secondary modules should be loaded in other modules;
- Secondary modules usually do not have rule main()
Secondary modules usually have public members;
- Secondary modules usually have public members;

### Library Modules


A library module is a file located in "lib" folder having extension *.bee. It is called simply: module. A library module can load other library modules and can execute its rules multiple times. You can install new libraries by downloading from the internet a package. Lib folder can have multiple sub-folders, where you create or modify a set of related libraries to be distributed for other people using a package creator tool.

- Any library module should have public elements,
- One library module can load multiple other library modules,
- One library module do not contain rule main(),
- One library module can be loaded a single time in another module,
- You can not load a module from a block statement,
- Library modules can be installed in: bee/lib folder for multiple projects

### Main rule

A module can define "rules". These are sub-programs that can be executed on demand. One special rule is the main rule that can be defined only in the main module. This rule can receive multiple parameters and is automatically executed when a program starts.


```
--  main rule
rule main(*params ∈ S):
-- read the number of parameters
   new c := params.count;
   panic if (c = 0);
-- print comma separated parameters
   new i:= 0 ∈ Z;
   while (i < c) do
     write params[i];
     let i += 1;
     write "," if (i < c);
   repeat;
-- print the buffer to console
   print;
return;
```


Do not try to understand this example right now. It is just a warming-up code!

- This program has a single module, that is main module;
- Input parameter  *params is an array of strings;
- Early program termination can be trigger using: over or panic;
- Any rule is ending with mandatory keyword: "return";

## External code


Library modules that are reusable for multiple projects can be imported in Bee "lib" sub-folder. This folder is available in Bee as a system constant called: $bee_lib. You can install a set of libraries in a sub-folder of "$bee_lib". Then you can reuse external library by using "load" keyword. The folders can be concatenated using "." string operator.


```
--  loading modules
use $bee_lib.folder_name.(*);     -- load all modules from folder
use $bee_lib.folder_name.(x,y,z); -- load modules x.bee, y.bee and z.bee
```

- using.(*) all modules from a folder are loaded in local scope;
- using.(x,y,z) only some modules are loaded in local scope;
- loaded modules, will merge all public elements in global scope;

Qualifier Bee can use  "dot notation" to locate external members. This technique is used to avoid name collision if one library has names that collide with other library.


```
--  load a single module and create a qualifier
use  $bee_lib.folder_name.module_name as qualifier; -- load a single module
...
apply qualifier.member_name; -- using dot notation with qualifier
...
```


1. A module can be loaded using a qualifier multiple times. However I do not see a useful use-case for this feature yet. I think is unusual to have same module loaded twice. It will be a waste of resources to do this.


2. All public members must use the specified qualifier or you can use "with" block to suppress the qualifier for a region of code. Using "with" is useful but sometimes not good enough so we have also invented the "alias".


```
#load examples
use cpp:$runtime.cpp_lib.(*); -- load cpp library
use asm:$runtime.asm_lib.(*); -- load asm library
use bee:$runtime.bee_lib.(*); -- load bee core library
use pro:$program.pro_lib.(*); -- load project library
```


## Global scope


One application has a global scope where variables and constants are allocated. Each secondary module can contribute with global variables and public elements that can be merged in this single scope. Global scope can be also called application scope;

- Global scope helps to use public identifiers from loaded modules;
- When a module is loaded, its public members are defined in the global scope;
- Public members of other modules can be used with quialifier.;

## Name space


A module has its own scope, that is called name-space where you can define members and statements. Module scope can contain public or private members. Public members start with "." while private members do not have any prefix or suffix.


```
#define a module
module demo_module:
-- public constant
set .pi: 3.14;
-- expression rule foo is private
rule foo(x ∈ N) ∈ N => (x + 1);
-- block rule bar is public
rule .bar(x, y ∈ N) => (r ∈ N):
-- define local variable
  new str := "test";
  ...
-- assign the result
  let r := x + y; -- r, x, y are locals
return;
```


The main module can load numerous secondary modules or libraries. After loading, all public elements of a library can be accessed on demand using dot notation. You can not have collisions of names, except if you use "with" blocks. To simplify the code you can use "alias" statement and can rename a rule belonging to loaded modules.


**Aliases:**


You can create an alias for a specific member to eliminate the qualifier. This rule can be used to "merge" public members into current scope. A member can have one single alias in a module. If you do it multiple times, only the last alias is used. It is a bad practice to change the alias of a member.


```-- import library module
use library as qualifier
-- create alias for a particular member
alias new_name: qualifier.member_name;
```


This example demonstrate how to use a rule from a module named "module_name"


```
#define program name
-- loading a module with qualifier
use $pro.src.demo_module as demo;
-- give alias to module rule
alias sum = demo.bar;
-- define main rule
rule main:
-- call rule using qualifier
    new test := demo.bar(1,1); -- 2
-- call rule using alias
    new result := sum(1,1); -- 2
-- call rule using "with" block
    with demo do
         print foo(2);   -- 3
         print bar(2,1); -- 3
    done;
return;
```


Hiding: To hide a public member instead of making an alias you can use keyword "hide". You can hide any public members from a loaded module. If you use a regular expression you can hide several public members that use a specific pattern.


```
hide qualifier.member_name;
hide qualifier.(reg_exp_pattern);
```


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


---

[Go back](syntax.md) | [Read next](types.md)
