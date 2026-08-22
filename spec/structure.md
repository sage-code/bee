# Code Structure

This document outlines the architectural organization of Bee applications:

- [Projects](#projects)
- [System Variables](#system-variables)
- [Compiler Directives](#compiler-directives)
- [Global Variables](#global-variables)
- [Modules](#modules)
- [External Code](#external-code)
- [Global Scope](#global-scope)
- [Namespaces](#namespaces)
- [Execution Modes](#execution-modes)

## Projects

A Bee project is a structured directory containing one or more application modules, secondary modules, libraries, and documentation. Applications within a project can execute independently on a single machine or collaborate across an n-tier architecture.

### Recommended Project Layout

The following tree illustrates a project structure containing client and server applications, source modules (`src`), shared libraries (`lib`), and documentation (`doc`):

```text
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

System variables use the `$` prefix. Predefined system variables locate project directories, libraries, or system resources. New system variables can be declared in the main module or configuration files.

| Variable | Environment | Description |
| :---| :---| :---|
| `$bee_home` | `BEE_HOME` | Bee installation root folder |
| `$bee_lib` | `BEE_LIB` | Bee core library folder |
| `$bee_path` | `BEE_PATH` | Bee library search path |
| `$pro_home` | N/A | Current project root folder |
| `$pro_lib` | N/A | Project library folder |
| `$pro_mod` | N/A | Project modules folder |
| `$pro_log` | N/A | Log output directory |



### Compiler Directives

Compiler directives are system variables that control compilation and execution options. These can be configured in compiler configuration files or within the main source file prior to execution.

To distinguish compiler directives from environment variables, system directives use lowercase names while imported environment variables use uppercase names.

| Directive | Default | Description |
| :---| :---| :---|
| `$max_precision` | `0.00001` | Numeric precision tolerance for rational arithmetic |
| `$max_recursion` | `10000` | Maximum call stack recursion depth |
| `$max_iteration` | `0` | Maximum loop iteration count (0 = unlimited) |
| `$loop_timeout` | `60` | Maximum execution time in seconds for a single loop |
| `$log_debug` | `"Off"` | Include debug information and symbols |
| `$log_echo` | `"Off"` | Print statements to console on error |
| `$log_trace` | `"Off"` | Populate `$trace` system variable with execution information |
| `$date_format` | `"DMY"` | Date formatting (`"DMY"` or `"MDY"`) |
| `$time_format` | `"T24"` | Time formatting (`"T24"` or `"T12"`) |
| `$platform` | `"Windows"` | Target platform (`"Windows"`, `"Linux"`, `"Mac"`) |

Notes:
- Compiler directives can only be set in the main module.
- Precision settings apply strictly to rational number operations.

### Global Variables

Global variables are declared outside rule blocks. The following system variables are available at runtime for debugging and introspection:

| Variable | Description |
| :---| :---|
| `$timer` | Duration information for the last executed statement |
| `$stack` | Call stack frame information |
| `$trace` | Execution trace log |
| `$query` | Last executed database query statement |
| `$error` | Active error object |
| `$threads` | Count of active execution threads |
| `$trial` | Trial object containing exception log messages |

Notes:
- System variables are defined globally by the core runtime library.
- Custom global variables can be declared in the main module using `new` or `set`.

## Modules

Bee programs are organized into modular units. A project decomposes into executable entry points (main modules), project-specific subroutines (secondary modules), and shared dependencies (library modules).

### Main Modules

A main module defines `rule main`, serving as the application entry point. A project may contain multiple main modules representing separate application executables. Main modules reside in the project root directory.

Key characteristics:
- Main modules cannot be loaded by other modules.
- Main modules do not export public members.
- A single project can contain multiple main modules.
- Main modules accept command-line parameters in `rule main`.

### Secondary Modules

Secondary modules decompose large application logic into reusable units. They reside in the `src` directory and export public members for use by main modules or other secondary modules.

Key characteristics:
- Specific to the parent project.
- Reside in the `src` directory.
- Export public members using the `.` prefix.
- Do not contain `rule main`.

### Library Modules

Library modules reside in the `lib` directory (or system `$bee_lib`) with a `.bee` extension. They provide shared utility routines and external packages.

Key characteristics:
- Must export public elements for external access.
- Can import other library modules.
- Do not contain `rule main`.
- Are loaded once per module scope.
- Cannot be loaded conditionally inside local block statements.

### Main Rule

The entry point rule is `rule main`, defined strictly within a main module. It accepts command-line parameters and executes automatically upon program launch.

```bee
-- main rule example
rule main(*params ∈ S):
  -- read parameter count
  new c := params.count;
  panic if (c = 0);

  -- print comma-separated parameters
  new i := 0 ∈ Z;
  while (i < c) do
    write params[i];
    let i += 1;
    write "," if (i < c);
  repeat;

  -- print buffer to console
  print;
return;
```

Key observations:
- Input parameter `*params` is a variadic array of strings representing command-line arguments.
- Early program termination can be triggered using `over` (clean exit) or `panic` (error exit).
- Every rule definition terminates with the mandatory keyword `return;`.

## External Code

Reusable library modules are imported from `$bee_lib` or local project paths using `use` directives:

```bee
-- loading modules
use $bee_lib.folder_name.(*);     -- load all modules from directory
use $bee_lib.folder_name.(x,y,z); -- load specific modules x.bee, y.bee, z.bee
```

### Module Qualifiers and Aliases

Dot notation provides qualified access to exported members, preventing symbol name collisions between imported modules.

```bee
-- load a module with a specific qualifier
use $bee_lib.folder_name.module_name as qualifier;

apply qualifier.member_name; -- access member via qualifier
```

Qualifiers can be stripped for local regions using `with` blocks or mapped to short aliases using `alias`:

```bee
use cpp:$runtime.cpp_lib.(*); -- load C++ runtime library
use asm:$runtime.asm_lib.(*); -- load Assembly library
use bee:$runtime.bee_lib.(*); -- load Bee core library
use pro:$program.pro_lib.(*); -- load project library
```


## Global scope


## Global Scope

An application shares a top-level global scope (application scope) where exported variables, constants, and public members from loaded modules are bound.

Key rules:
- Public members of loaded modules are accessible in the global scope.
- Qualified module names prevent symbol collisions across libraries.

## Namespaces

Each module establishes its own namespace. Members defined within a module are either private (default) or public (prefixed with `.`).

```bee
module demo_module:
  -- public constant
  set .pi: 3.14;

  -- private rule
  rule foo(x ∈ N) ∈ N => (x + 1);

  -- public rule
  rule .bar(x, y ∈ N) => (r ∈ N):
    new str := "test";
    let r := x + y;
  return;
```

### Symbol Aliases and Scope Suppression

Aliases bind local identifiers to qualified public members, stripping the qualifier prefix:

```bee
use library as qualifier;
alias new_name: qualifier.member_name;
```

Example demonstrating module imports, qualifiers, aliases, and `with` blocks:

```bee
use $pro.src.demo_module as demo;

alias sum = demo.bar;

rule main:
  -- call rule using qualifier
  new test := demo.bar(1, 1); -- 2

  -- call rule using alias
  new result := sum(1, 1);    -- 2

  -- call rule using 'with' block
  with demo do
    print foo(2);   -- 3
    print bar(2, 1); -- 3
  done;
return;
```

To suppress specific public symbols from an imported library, use `hide`:

```bee
hide qualifier.member_name;
hide qualifier.(reg_exp_pattern);
```

---

[Go back](syntax.md) | [Read next](execution.md)
