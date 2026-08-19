
# Bee Purpose


# Bee Features


Bee is a disruptive strange looking language that will bring Math notation into the source code. Bee has some uncommon keywords, operators and symbols. We have made an effort to maximize these features:


| Table |
| --- |
| # | Feature | How |
| 0 | readable | use English keywords |
| 1 | efficient | use native types |
| 2 | safe | avoid invalid references |
| 3 | modular | reusable modules |
| 4 | explicit | named results & arguments |
| 5 | disruptive | unusual syntax choices |



## Readable


Bee is designed to be learn as first programming language for Sage-Code developers. We think that you can learn Bee by reading code examples in one week. Next design choices will make Bee code easier to read therefore easier to learn:

- Use short and familiar English keywords;
- Use imperative statements based on verb keywords;
- Use end of block keywords not curly brackets;
- Use best operator symbols possible similar to Math;
- Use comprehensive data literals for collections;
- Enable comprehensive comments and code documentation;
- Enable Greek and Cyrillic letters for identifiers;

The result of these choices is demonstrate below. You can observe different comment notations enable different color. Syntax colorizer is able to identify also the keywords and highlight every statement.


```
# Demo: Fibonacci Sequence

** declare Fibonacci rule
rule fib(n ∈ N) => (y ∈ N):
  if (n = 1) ∨ (n = 0) do
    let y := 1; -- first value
  else
    let y := fib(n-1) + fib(n-2);
  done;
return;

rule main:
   ** call fib rule using argument 5
   new r := fib(n: 5);

   ** print the result to console
   print r;
return; -- end of module
```


## Efficient


Bee is aiming for efficiency not performance. There is a difference, performance can be obtained using intensive computer resources and distributed computing. Efficiency is achieved using better algorithms and data types. Bee is designed for multi-core CPU. It enable you to create efficient applications using following techniques and features:

- Use native data types;
- Use mutable string types;
- Use fixed precision arithmetic;
- Use fixed size arrays and matrices;
- Enable array slicing;
- Enable lambda expressions;
- Enable tail recursion;
- Enable coroutines;
- Enable concurrency;

## Safe


Bee is designed to be a safe but also comprehensive. To fulfill these goals we setup a runway architecture based on next principles and believes. Some of these principles create real challange for our design.

- Safety is more important than performance.
- If something can go wrong, eventually it will,
- If you already know it can be a problem, prevent it,
- It is better to be proactive than reactive,
- Sometimes if you try a second time it may work,
- There are more than one ways to resolve a problem,
- If your problem is large, split it into parts,
- Explicit is better than implicit even if require more work,
- Efficiency is more important than high cost performance,
- Good precision is more important than perfect precision,

## Modular


Bee applications are usually small, based on single source file. However Bee enable usage of multiple files for separation of concerns. There are 2 kind of modules in a large application: application modules and library modules.


Bee modular design

- Bee program consist of application modules and library modules
- Main program is called main module and contains rule: main
- Secondary modules can be reused in multiple Bee programs
- Library modules are modules installed in Bee library folders
- External modules can be installed by a package manager in Bee library folders

Note: Main module is the only executable module and is not reusable. Secondary modules can be loaded and public members can be executed from main() rule. Loaded modules are persistent in memory and can not be "unloaded" until the program ends. Bee has this limitation, it has to be small to be loaded in memory.


## Explicit


Bee is an explicit language: We believe explicit is better than implicit. For this we try to give as much control to developers as possible. Next design choices make Bee an explicit language:

- Bee require declarations of data types for all elements: constants, variables, parameters and results. Unlike dynamic languages that use implicit data types that can be changed in the same scope.
- Most languages do not have a name for result variables in functions. Bee allow developers to declare explicit names and types for every result. This is helpful when a subroutine has multiple results.
- Precision is implicit and maximum possible in most other languages, forcing the computation of multiple decimals that are not necessary. In Bee you can define rational numbers that have fixed number of decimals therefore precision is explicit.
- Variables and parameters are automatically initialized with zero value when there is no explicit initialization. Also, if a parameter has explicit initial value it becomes optional.
- Bee has three assignment operators: ":", "::" and ":=". First is called "pair up". Second is called "clone", thread is called "assign". Developers can control what assignment operator actually do by using keywords: "make" to declare a new variable and "alter" to modify an existing variable.
- In a rule, primitive type parameters are transferred by value while composite type parameters and objects are transferred by reference. Same rule apply for result variables.
- Bee do not have pointers nor pointer arithmetic. However you can define references to primitive types using explicit boxing operator [x] that are as good as pointers.

## Disruptive


We have try and failed to create a consistend language because the people who invented Unicode symbols have done such a mess. Some symbols are duplicated, some are not ordered, some are missing. Sometimes the unicode symbol look like a Latin letter. We have done our best to select the most useful symbols.

- Bee use Unicode operators: { ÷ × ¬ ∧ ∨ ∈ ≤ ≥ ≡ ≠ ≈ ± ⊂ ⊃ ∪ ∩ ↑ ↓ » « ⊕ ⊖ ∀ ∃}. We have alternative ASCII 2 symbols for some of these but not all. This is why Bee looks inconsistent & disruptive:
- Bee use one single letter for primitive types: {A B C D T L U N Q R S X Z}, we have not used Unicode symbols: { ℂ ℍ ℕ ℙ ℚ ℝ ℤ } despite aparent inconsistency.
- Bee support some Greek letters and symbols. These can be used as identifiers or operators: { Σ Π Δ Γ Λ Φ Ψ Ω, λ φ π α β ε δ μ ω }
- Bee support Cyrilic letters: {Б Г Д Ж И Л Ф Ц Ч Ш Э Я}. We do not support all Cyrikic alphabet for identifiers but you can use them in strings.
- Bee support superscript numbers: {⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹}. We recognize superscript as power: x^² and x^ⁿ. You can also use any Latin superscript characters: (ᵃ..ᶻ).
- Subscript indices can be used to create identifiers starting with a letter and use a suffix: (x₁, x₂, α₁, β₂) are some valid identifiers in Bee.
- Bee use Unicode symbols for geometric types. These symbols are intuitive and make geometric types shorter. For example: ∠ = Angle, ⊡ = Dot, ◷ = Arc. Many other shapes are recognized.
- Bee define the "if" statement differently than most other languages. The "if" keyword is used as a conditional for other statements or in lambda expressions.
- Bee use sigils: "$" for system variables. These are globals and we import all environment variables and configuration variables into the execution. Protecting these variables with a sigil is preventing overriding by mistake.
- Bee use starting and ending keywords to define blocks of code, not curly brackets. This eliminate the nested bracket nightmares and improve visual aspect of the code. We can use brackets for data literals: ordinals, sets, hash tables and objects.

Read next:
Bee Syntax
