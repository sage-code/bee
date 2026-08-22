# Bee Features

Bee is an expressive language that integrates mathematical notation directly into source code. Bee features a clear, keyword-driven syntax with dedicated operators and domain-specific symbols.

| # | Feature Name | How to Implement |
| :---| :---| :---|
| 1 | readable | use English keywords |
| 2 | efficient | use native types |
| 3 | safe | avoid invalid references |
| 4 | modular | reusable modules |
| 5 | explicit | named results & arguments |
| 6 | deterministic | avoid side effects |
| 7 | unicode | Unicode symbols and operators |

## Readable

Bee is designed to be learned as a first programming language for Sage-Code developers. Code examples can be understood quickly due to the following design choices:

- Use short and familiar English keywords;
- Use imperative statements based on verb keywords;
- Use end-of-block keywords rather than curly braces;
- Use mathematical symbols for operators where appropriate;
- Use intuitive data literals for collections;
- Support structured inline comments and code documentation;
- Enable Greek and Cyrillic letters for identifiers.

The result of these choices is demonstrated below. Syntax highlighting identifies keywords, comment styles, and statement structures.

```bee
--  Demo: Fibonacci Sequence
-- declare Fibonacci rule
rule fib(n ∈ N) => (y ∈ N):
  if (n = 1) ∨ (n = 0) do
    let y := 1; -- first value
  else
    let y := fib(n-1) + fib(n-2);
  done;
return;

rule main:
  -- call fib rule using argument 5
  new r := fib(n: 5);
  -- print the result to console
  print r;
return; -- end of module
```

## Efficient

Bee aims for efficiency rather than raw compute overhead. Performance can be obtained using intensive compute resources and distributed computing, whereas efficiency is achieved through better algorithms and native data types. Bee is designed for multi-core CPUs. It enables creating efficient applications using the following techniques and features:

- Native data types;
- Mutable string types;
- Fixed precision arithmetic;
- Fixed-size arrays and matrices;
- Array slicing;
- Lambda expressions;
- Tail recursion;
- Coroutines;
- Concurrency.

## Safe

Bee is designed to be safe yet expressive. To fulfill these goals, the language architecture is built on the following principles and beliefs:

- Safety is more important than raw performance.
- If something can go wrong, eventually it will.
- Potential runtime issues must be prevented at compile time whenever possible.
- Proactive error checks are better than reactive debugging.
- Large problems should be decomposed into smaller modular subroutines.
- Explicit syntax is better than implicit behavior, even if it requires more code.
- Resource efficiency is prioritized over high-overhead abstractions.
- Controlled fixed precision is preferred over unpredictable floating-point rounding.

## Modular

Bee applications are typically compact, often residing in a single source file. However, Bee fully supports multi-file organization for separation of concerns. There are two kinds of modules in a large application: application modules and library modules.

**Bee Modular Design:**

- A Bee program consists of application modules and library modules.
- The entry point module is called the main module and contains `rule main`.
- Secondary modules can be reused across multiple Bee programs.
- Library modules reside in designated Bee library folders.
- External modules can be installed by a package manager in Bee library folders.

`Note:` The main module is the only executable entry point and is not reusable by other modules. Secondary modules can be loaded and their public members executed. Loaded modules remain persistent in memory for the duration of program execution.

## Explicit

Bee is an explicit language: explicit design choices prevent unintended side effects. The following design choices enforce explicit semantics:

- Bee requires explicit data type declarations for all constants, variables, parameters, and rule results, unlike dynamically typed languages.
- Bee allows developers to declare explicit names and types for every return result. This provides clarity when a subroutine produces multiple results.
- Fixed-precision rational numbers (`Q`) allow developers to specify exact decimal precision rather than relying on floating-point approximations.
- Variables and parameters without explicit initializers are automatically set to standard zero default values. Parameters with explicit default values become optional.
- Bee provides three assignment operators: `:` (pair-up), `::` (clone), and `:=` (assign). Developers control variable mutation using `new` (declare variable) and `let` (modify existing variable).
- Primitive type parameters are transferred by value, while composite types and objects are transferred by reference. The same rules apply to result variables.
- Bee does not have raw pointers or pointer arithmetic. However, explicit boxing references `[x]` can be defined for primitive types.

### Deterministic Execution

A deterministic system ensures that given the same input and initial state, the program always produces the same output through the exact same sequence of internal states. In language design, this is critical for reliability, testing, and formal verification.

#### Achieving Determinism

To enforce determinism, the language architecture incorporates the following constraints:

1. **Pure Functions by Default:** Enforce pure functions where outputs depend solely on input parameters, with no reliance on or mutation of shared global state.
2. **Explicit Side-Effect Management:** Operations that perform I/O, interact with system clocks, or rely on external randomness must be explicitly declared (e.g., using `system` or `impure` qualifiers).
3. **Controlled Concurrency:** Disallow un-synchronized shared-memory mutation across threads to eliminate race conditions. Use message-passing models or immutable structures.
4. **Hardware/Platform Abstraction:** Normalize floating-point behavior and integer representations across target architectures (ARM, x86, WebAssembly).
5. **Deterministic Initialization:** The order of global constant evaluation and module initialization is strictly specified by the language standard rather than compiler-dependent heuristics.

## Unicode Symbols

Bee integrates carefully selected Unicode symbols into its syntax to express mathematical and set operations clearly:

- Bee uses Unicode operators: `{ ÷ × ¬ ∧ ∨ ∈ ≤ ≥ ≡ ≠ ≈ ± ⊂ ⊃ ∪ ∩ ↑ ↓ » « ⊕ ⊖ ∀ ∃ }`. Standard ASCII equivalents are supported for key operators.
- Bee uses single uppercase letters for primitive types: `{ A, B, C, D, T, L, U, N, Q, R, S, X, Z, G }`.
- Bee supports selected Greek letters for identifiers and mathematical operators: `{ Σ, Π, Δ, Γ, Λ, Φ, Ψ, Ω, λ, φ, π, α, β, ε, δ, μ, ω }`.
- Bee supports selected Cyrillic letters for identifiers: `{ Б, Г, Д, Ж, И, Л, Ф, Ц, Ч, Ш, Э, Я }`. Full Cyrillic text is supported in string literals.
- Bee supports superscript digits `{ ⁺ ⁻ ⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ }` for power expressions such as `x²` and `xⁿ`. Latin superscript characters `(ᵃ..ᶻ)` are also supported.
- Subscript indices create distinct identifiers: `x₁`, `x₂`, `α₁`, `β₂`.
- Bee uses the `$` sigil for system variables and environment variables to prevent accidental scope shadowing.
- Bee uses starting and ending keyword pairs (`do..done`, `cycle..repeat`, `rule..return`) to delineate code blocks instead of curly braces. Brackets and braces are reserved for data literals (ordinals, sets, hash maps, and objects).

---

[Go back](index.md) | [Read next](syntax.md)
