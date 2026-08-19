# Bee-0 — Decisions Log

Every ruling that resolves an ambiguity, contradiction or gap in the upstream Bee design. Each
entry states the conflict, the ruling, and why. These are arguable — that is the point of writing
them down.

**Status key:** `SETTLED` — implement it · `PROVISIONAL` — implement it, but expect to revisit.

No ruling here has been raised with the author. `UPSTREAM-ISSUE.md` is drafted and unsent, so every
decision in this log is one-sided by construction — including the sixteen that deliberately change
the language (D66–D81).

---

## Sources in conflict

Three sources disagree with each other, in this order of authority for Bee-0:

1. **`sagecode.org/projects/bee/` HTML documentation** — the fullest and most recent statement of
   the design. **Normative** unless overridden below.
2. **`demo/*.bee` in the upstream repo** — 34 sample programs. These use a **materially different
   dialect** from the documentation (D11–D18). Treated as source material, not as truth.
3. **The repo README** — goals and design bullets only.

The single most consequential finding of Phase 0 is that source 2 does not implement source 1.

---

## Part A — Rulings from the plan (D1–D10)

### D1 — Array index base · `SETTLED`

**Conflict.** The Collections chapter states array indices start at 1 and uses `(1..10)` to
traverse ten elements. The Processing chapter states indices start at 0, gives max capacity as
`2³²`, and uses `test[0]` for the first element. `bubble_sort.bee` uses `(0.!n)`.

**Ruling.** **0-based.**

**Rationale.** Negative indexing (`a[-1]` for last) is documented in both chapters and only
composes cleanly with 0-based positive indices — with 1-based, `a[1]` and `a[-1]` on a
one-element array would be the same element by two incompatible rules. Slice arithmetic
(`a[n..m]` length = `m-n+1` vs `m-n`) is likewise cleaner. Two of three sources already use 0.
Matrix literals indexed from `[1,1]` are out of scope for Bee-0, so the conflict does not arise.

**Cost.** Contradicts one full chapter of upstream documentation. Must be stated loudly in
user-facing material.

---

### D2 — Memory management · `SETTLED`

**Conflict.** The documentation describes reference sharing (`:=`), deep copy (`::`), boxed
primitives, slices as views into arrays, and closure states allocated on the heap. It never
specifies who frees anything, and there is no `free`, `del` (except on object keys), or scope-exit
rule.

**Ruling.** **Non-atomic reference counting.** No cycle collector in v1. Reference cycles leak,
and this is documented.

**Rationale.** Refcounting is the only option that gives the documented `:=`-shares /
`::`-clones semantics honestly and predictably, with destruction timing the programmer can reason
about. A tracing GC would be more work and would make the language's claimed suitability for
embedded/fixed-point numeric work implausible. Ownership/borrowing would be a different language.
In Bee-0 the only reference types are arrays, lists and strings, and cycles are unconstructable —
there are no objects and no recursive types. So the leak is theoretical until Bee-1.

**Revisited in Bee-2.** Objects arrived, so cycles *are* constructable now — `let a.next := a;`
makes one. The implementation relies on the host's tracing collector, which subsumes reference
counting and reclaims cycles as well. The observable semantics are unchanged and strictly stronger
than the ruling: `:=` shares, `::` clones, and nothing leaks. A native backend would have to
implement this properly, and that is recorded as the one place where the reference implementation
is easier than the real thing.

---

### D3 — Slice invalidation on resize · `SETTLED`

**Conflict.** Slices are views sharing storage with the original array. `++` resize "will reset
the array reference… it will not update any slice or other references you may have to this array."
That describes a dangling view.

**Ruling.** `++` **allocates a new buffer** and rebinds the resized variable to it. Slices and
other references retain a strong reference to the **old** buffer and stay valid, viewing stale
data. No use-after-free is possible.

**Rationale.** Combined with D2 refcounting, this makes the documented behaviour memory-safe
without changing its observable semantics: after `let acopy ++ [0](10)`, the upstream example
prints the modified `acopy` and the unmodified `array`, which is exactly what this ruling
produces. The alternative — invalidating slices — would require a validity flag on every slice
access and would turn a documented example into a runtime error.

**Cost.** Silent aliasing surprise. A resized array is a different object; `a == b` becomes false
where it was true. Diagnose with a warning when a live slice exists at a `++` site and the
compiler can prove it.

---

### D4 — Block terminators · `SETTLED`

**Conflict.** Closers appear as `done`, `repeat`, `cycle`, `rule` and `return` across examples,
sometimes within one file. `local_var.bee` ends a rule with `rule;`. Several loops close with
`cycle;`.

**Ruling.** `done` closes `if` and `start`. `repeat` closes `cycle` and `for`. `return` closes
`rule`. Nothing else closes anything.

**Rationale.** Majority usage in the documentation, and the only assignment that keeps each closer
unambiguous. Accepting `cycle;` as a loop terminator would make `cycle:` … `cycle;` visually
symmetric but collide with a nested loop opener on the same line.

---

### D5 — `when` vs `if` · `SETTLED`

**Conflict.** `when` is documented as the `match`-branch keyword, but appears as a synonym for
`if` in the recursion, hash-map and inclusion examples.

**Ruling.** `if` is the decision keyword. `when` is reserved for `match` (Bee-1) and is rejected
in Bee-0 with a diagnostic pointing at `if`.

---

### D6 — Assertion keywords · `SETTLED`

**Conflict.** `expect`, `pass`, `fail` and `claim` all appear in assertion-like positions. `claim`
is used in two demos but appears nowhere in the 72-keyword list.

**Ruling.** `expect` is the sole Bee-0 assertion. `pass` and `fail` are reserved for `trial`
(Bee-1). `claim` is **not a keyword** and is rejected with a diagnostic suggesting `expect`.

**Rationale.** `pass`/`fail` have trial-specific control-flow meaning (skip to next job / record
error and continue) that is incoherent outside a trial. `claim` is undocumented drift in the demos.

---

### D7 — Statement terminator · `SETTLED`

**Ruling.** `;` is mandatory on every statement. Block-opening lines ending in `do`, `:` or `else`
take none.

**Rationale.** The documentation is inconsistent; several examples omit it. Mandatory is easier to
parse, enables one-line multi-statement forms the docs advertise, and turns a class of typos into
clear errors.

---

### D8 — Integer overflow · `SETTLED`

**Ruling.** Trap. Overflow raises `$value_overflow` and terminates.

**Rationale.** The language's stated priority order puts safety above performance and explicit
above implicit. Silent wrapping is neither.

---

### D9 — `∈` as membership vs type test · `SETTLED`

**Conflict.** `∈` declares types (`new a ∈ Z`), tests types (`expect a ∈ Z`) and tests membership
(`pass if '0' ∈ Digit`, `if x ∈ myList`). The middle two are indistinguishable syntactically —
`Digit` is both a type and a set of values.

**Ruling.** Resolved at compile time by the right operand. If it names a type, `∈` is a type test
(and for range subtypes, a *value-domain* test — `'0' ∈ Digit` checks the character is in
`'0'..'9'`). Otherwise it is membership. A name bound to both a type and a variable in the same
scope is a compile-time error.

**Rationale.** Preserves every documented example. The dual reading of range subtypes is what the
docs actually intend: `type Digit: ('0'..'9') <: A` makes the type *be* the domain.

---

### D10 — Uninitialised variables · `SETTLED`

**Ruling.** Zero-initialised per the type's default (§4.1). Confirms documented behaviour.

---

## Part B — Rulings forced by the demo dialect (D11–D23)

These emerged from reading `demo/*.bee` against the documentation. They were not anticipated in the
plan.

### D11 — Declaration keywords are mandatory · `SETTLED`

**Conflict.** This is the big one. **The demos do not use `new`, `let` or `set` at all.** They use
bare assignment for both declaration and mutation:

```bee
** demo dialect (bubble_sort.bee)
n := length(this);
swap := True ∈ L;

** documented dialect
new n := length(this);
new swap := True ∈ B;
```

`type_inference.bee` additionally uses `store` for constants — a keyword absent from the 72-word
list and from every other source.

**Ruling.** `new`, `set` and `let` are **mandatory**, per the documentation. Bare assignment at
statement position is a compile-time error whose diagnostic suggests the right keyword. `store` is
rejected in favour of `set`.

**Rationale.** Implicit declaration is exactly the Python behaviour where a typo'd assignment
silently creates a new variable instead of updating the intended one. The language's own stated
design principle is "explicit is better than implicit even if it requires more work," and the
documentation devotes a section to the `set`/`new`/`let` distinction as a *feature*. The demos
appear to predate that decision.

**Consequence.** **All nine target demos must be ported.** They are not conformance tests as
written. See `tests/PORTING.md`.

**Upstream question.** Which dialect is current? If the demos are the intended direction, this
ruling inverts and most of §5 of the spec changes.

---

### D12 — Boolean type code · `SETTLED`

**Conflict.** The documentation gives `B` = Boolean and `L` = Lambda. The demos use `L` for logic
values (`swap := True ∈ L`, `store f := False; -- L (logic)`), and one doc example also slips
(`new (q,p):0 ∈ L; -- Logic`).

**Ruling.** `B` is Boolean. `L` is Lambda and is out of scope in Bee-0. `∈ L` on a Boolean is
rejected with a diagnostic suggesting `B`.

**Rationale.** The primitive-type table and the whole `0B0`/`0B1` literal notation are built around
`B`. `L` as Lambda is used consistently throughout the Functions chapter.

---

### D13 — Reference arguments and the `@` sigil · `PROVISIONAL`

**Conflict.** `output_params.bee` calls `pro(a:@x, b:@y)` to pass primitives by reference to boxed
parameters. The `@` sigil is documented as meaning "domain name, e.g. @sagecode.net" — an entirely
different use. `type_inference.bee` calls the same kind of rule *without* `@`: `inc(i,k);`.

**Ruling.** `@x` is the **by-reference argument marker**, mandatory at call sites for boxed
primitive parameters `[T]`. Domain-name literals are out of scope in Bee-0, so there is no clash.

**Rationale.** Silent mutation of a caller's local through an innocuous-looking `f(x)` is the
opposite of the language's explicitness goal. Requiring `@` makes every possible mutation visible
at the call site, which is a genuine improvement on both the docs and C#'s `ref`. The demos
disagree with each other here, so neither can be followed.

**Provisional because:** it repurposes a documented symbol. If domain literals return in Bee-2, a
different marker is needed.

---

### D14 — Parallel assignment · `SETTLED`

**Source.** `bubble_sort.bee` swaps with `(this[i+1], this[i]) := (this[i], this[i+1]);`; the docs
swap with `let p, q := q, p;`.

**Ruling.** Supported, with or without parentheses on the target list. **All** right-hand
expressions are evaluated to values before any assignment. Length mismatch is an error, except a
single right-hand expression broadcasts to all targets (documented: `let x, y := 10.5;`).

---

### D15 — Rule calls as statements require `apply` · `SETTLED`

**Conflict.** The docs specify `apply` for calling a rule and discarding results. The demos call
bare: `sort(test);`, `add;`, `inc(i,k);`, `pro(a:@x, b:@y);`.

**Ruling.** `apply` is mandatory in statement position. Bare `f(x);` is an error with a diagnostic
suggesting `apply f(x);`. A bare identifier with no parentheses and no `apply` (`add;`) is an
error suggesting `apply add();`.

**Rationale.** Without `apply`, `f(x);` is ambiguous with an expression statement, and Bee has no
expression statements. Requiring it also makes discarded results visible.

---

### D16 — `store` keyword · `SETTLED`

**Ruling.** Not a keyword. Rejected, diagnostic suggests `set`. (See D11.)

---

### D17 — Conversion operator · `SETTLED`

**Conflict.** Docs use `:>` throughout. `type_inference.bee` uses `->`
(`t := "23:45" -> T24;`).

**Ruling.** `:>`. `->` is rejected.

**Rationale.** `:>` appears in the operator tables and a dozen examples; `->` appears in one demo,
alongside `T24`/`T12`/`DMY` types that exist nowhere else in the design.

---

### D18 — Rule terminator `rule;` · `SETTLED`

**Conflict.** `local_var.bee` ends `main` with `rule;`. Two collection examples end with `rule;`
too.

**Ruling.** `return;` only. (See D4.)

---

### D19 — Public/system sigils out of scope · `SETTLED`

**Ruling.** Leading `.` (public member) and `$` (system/global) are not valid in Bee-0 identifiers,
because Bee-0 has no modules and therefore no public/private distinction. `$Global.x`
(`local_var.bee`) is rejected. The two system constants in §12 are compiler flags, not identifiers.

---

### D20 — `∀` in `for` · `SETTLED`

**Conflict.** `for ∀ i ∈ (1..10)` in most examples; `for e ∈ M do` and `for x ∈ self.keys()` in
others.

**Ruling.** `∀` is **optional and semantically inert** in a `for` header. Both forms parse
identically.

**Rationale.** Rejecting either form would break documented examples. As an *expression*, `∀` is
a real quantifier (Bee-1); in a `for` header it is decoration.

---

### D21 — `print` with no argument · `SETTLED`

**Ruling.** `print;` flushes the console buffer and emits a newline. Confirms
`repetition_statements.bee` and several doc examples.

---

### D22 — Implicit coercion in string concatenation · `SETTLED`

**Conflict.** The docs require explicit conversion on type mismatch, then freely write
`print "unexpected:" + a;` where `a ∈ Z`, and `print "a =" + self.a;`.

**Ruling.** In `a + b` where either operand is `S`, the other is converted to its default display
representation. This is the **only** implicit conversion besides numeric widening.

**Rationale.** Every I/O example in the corpus depends on it. Restricting it to concatenation with
a string keeps it from leaking into arithmetic.

---

### D23 — Nested comments `|: :|` · `SETTLED`

**Source.** `comments.bee` advertises `|: nested :|`, `|: expression :|` and `|: debug-code :|`
comments, including *inside string literals* — where the demo expects them to be stripped.

**Ruling.** Out of scope for Bee-0. `#`, `##`, `**`, `--` and `+- -+` only.

**Rationale.** Comments that are stripped inside string literals make the lexer's string rule
context-dependent and would silently corrupt any program containing `|:` in text. The feature
needs a design discussion, not an implementation.

---

## Part C — Rulings forced by the lexer (D24–D27)

These emerged in Phase 1. Nothing surfaces a specification contradiction like having to write code
that obeys it.

### D24 — `!=` is identity, not value inequality · `SETTLED`

**Conflict.** My own §2.7 listed `!=` as an ASCII alias for `≠` (value inequality), while §7.5
listed `==`/`!=` as the identity pair. Both cannot be true. Upstream has the same contradiction:
the double-symbols table calls `!=` "not identical (not the same)", but the negation section writes
`x != y; -- equivalent to: ¬(x = y)`, which is value inequality.

**Ruling.** `=`/`≠` compare **values**. `==`/`!=` compare **references**. `!=` is not an alias for
`≠`. The negation prefix `!` composes only with `≡`, `∈` and `≈`.

**Rationale.** Reference identity needs a spelling, and `==`/`!=` is the only pair the design
offers. Making `!=` mean value inequality would leave `==` without a negation.

**Also found:** upstream `reference_transfer.bee` uses `≢`, which appears in no operator table
anywhere. Adopted as a third spelling of `≠≡`.

### D25 — Literal signs are unary operators · `SETTLED`

**Conflict.** §2.5 described integer literals as "decimal, optional sign", which would make the
lexer responsible for deciding whether `a -1` is a subtraction or two tokens.

**Ruling.** A leading `-` or `+` is a unary operator handled by the parser. Literals are unsigned.

**Rationale.** No lexer can make that call without expression context, and the precedence table
already has unary minus at level 2.

### D26 — Box comments open only at the start of a line · `SETTLED`

**Conflict.** A box comment opens with `+-`. Under plain longest-match, `a +-b` — addition of a
negated value — silently becomes a comment that swallows the rest of the file until the next `-+`.

**Ruling.** `+-` opens a box comment only when preceded by nothing but whitespace on its line.

**Rationale.** Matches every real use in the corpus (box comments are always flush-left banners)
and eliminates a silent, catastrophic misparse. The alternative — requiring a space after `+`
in arithmetic — puts the burden on every arithmetic expression to avoid a comment syntax.

### D27 — `--` is a comment only before whitespace · `SETTLED`

**Conflict.** Same shape as D26. Under longest-match, `5--3` becomes `5` followed by a comment.

**Ruling.** `--` opens a comment only when followed by a space, tab, newline or end of file.

**Rationale.** The documentation itself writes the marker as `"-- "` with a trailing space. This
makes `a--b` subtraction and `a -- note` a comment, which is what both readings expect.

**Not fixed:** `**` remains a comment in every position, so `a ** b` comments out the rest of the
line instead of multiplying. Unlike `+-` and `--`, there is no positional rule that saves it, and
`**` is the single most common comment marker in the corpus. Bee has `^` and superscripts for
exponentiation, so nothing is lost — but it is a sharp edge and belongs in user-facing docs.

### D28 — A parenthesised list after `print`/`write`/`read` is an argument list · `SETTLED`

**Conflict.** `print (a, b)` and `print my_list` are the same shape once `my_list` is replaced by
its literal. My own `result_unpacking.expected` requires both readings in one file: `print both`
where `both` is a list outputs `(2,3)`, while `print (n, m)` outputs `2,3`.

**Ruling.** Immediately after `print`, `write` or `read`, a parenthesised comma list is the
**argument list**, never a list literal. To print a literal list, bind it first
(`new l := (1,2,3); print l;`) or double the parentheses (`print ((1,2,3));`).

**Rationale.** The argument-list reading is what every use in the corpus wants, including the
`sep:` named argument (`print (a, b, sep:",")`), which is not expressible as a list literal at all.
The escape hatch costs one pair of parentheses in a case that does not occur in the corpus.

**Cost.** `print` is now genuinely special syntax rather than a rule call, and the parser needs a
flag for "we are directly after an I/O keyword". Documented in §11.1.

### D29 — Parenthesised right-hand sides are arity-driven · `SETTLED`

**Conflict.** `bubble_sort.bee` writes `let (this[i], this[i+1]) := (this[i+1], this[i]);`, while
`type_inference.bee` writes `new v := (1,2,3);`. Both right-hand sides are a parenthesised comma
list. If the first is a list literal, D14's broadcast rule assigns one list to both targets, which
is wrong. If the second is an expression list, `v` never becomes a list.

**Ruling.** Decided by the number of targets:

- **One target** — a parenthesised comma list on the right is a **list literal**.
  `new v := (1,2,3);` binds a three-element list.
- **Two or more targets** — it is an **expression list** for parallel assignment.
  `let x, y := (1,2);` assigns 1 and 2.

Parentheses around the target list are optional and carry no meaning:
`let (a,b) := ...` and `let a,b := ...` are identical.

**Rationale.** Matches every site in the corpus. The alternative — a distinct syntax for tuples —
would require inventing notation the design does not have.

**Cost.** The meaning of the right-hand side depends on the left, so the parser must parse targets
before committing to a reading of the right. Multi-result rule calls stay unambiguous because they
are calls, not parenthesised lists: `new r := com(3,2)` yields a list under the one-target rule,
`new s, d := com(3,2)` destructures. That is exactly what §8.2 documents.

### D30 — Bracket meaning is positional · `SETTLED`

**Gap**, not a conflict: the spec never said how `[` is disambiguated.

**Ruling.** By position:

| Position | Meaning | Example |
|---|---|---|
| after `∈`, `<:`, or in a `type` descriptor | array type | `new a ∈ [Z](10);` |
| immediately after a primary expression | index or slice | `a[i]`, `a[1..3]`, `a[*]` |
| anywhere else an expression may start | array literal | `new a := [1,2,3];` |

"Immediately after" means no intervening whitespace-insensitive token boundary is needed — the
parser treats `[` as a postfix operator whenever the previous construct was a complete primary,
matching the level-1 precedence entry in §7.1.

**Rationale.** This is how the corpus reads, and it is the same rule most bracket-indexed languages
use. Writing it down removes the last place a parser would have to guess.

---

## Part C2 — Rulings forced by the grammar (D31–D35)

Found by writing the tree-sitter grammar before the hand-written parser, exactly as the plan
intended. Each of these is a place where the grammar could not be generated at all until the
ambiguity was resolved.

### D31 — Parameter lists are flat, with leftward type propagation · `SETTLED`

**Conflict.** §8 wrote a parameter as `Identifier ("," Identifier)* [":" default] "∈" type`, so
`(a, b ∈ Z)` is one group of two. But `(x ∈ Z, y: 0 ∈ Z)` is two groups. After reading `a,`
nothing distinguishes "b continues this group" from "b starts a new one" until the `∈` arrives,
which is unbounded lookahead.

**Ruling.** The parameter list is a **flat** comma-separated list of items, each
`[*] name [: default] [∈ type]`. A post-pass propagates each declared type **leftward** over the
preceding untyped items. An item with no type to its right is an error.

**Rationale.** Reproduces every documented signature — `(a, b, c:0 ∈ Z)` gives all three type `Z`
with `c` optional — without lookahead. Results use the same rule.

### D32 — `(x)` is grouping, not a one-element list · `SETTLED`

**Conflict.** `list_literal` accepting one element makes `(x + y)` ambiguous with a one-element
list containing `x + y`. The upstream docs do write `new one:(0);` for a single-element list.

**Ruling.** `()` is the empty list. `(x)` is a **parenthesised expression**. A one-element list is
written `(x,)`.

**Rationale.** Grouping is overwhelmingly the common case — it appears in nearly every demo, while
one-element lists appear once in the whole corpus. The trailing comma is the standard escape and
costs one character.

### D33 — Declaration values are parsed with top-level `∈` suppressed · `SETTLED`

**Conflict.** D9 resolved `∈` as membership-or-type-test semantically, but the same symbol also
*structurally* separates a declaration's value from its annotation. In `set a: 5 ∈ Z;` the parser
cannot tell whether the value is `5` annotated `Z`, or the expression `5 ∈ Z`.

**Ruling.** When parsing the value of a `set`, `new`, parameter or result declaration, `∈` is
suppressed at the top level: it always ends the value and begins the annotation. To use `∈` as a
membership test in an initialiser, parenthesise it: `new flag := (x ∈ list);`.

**Rationale.** The annotation reading is the only one that occurs in the corpus, and the
parenthesised escape is unambiguous.

### D34 — `else if` is always a ladder rung · `SETTLED`

**Conflict.** Bee's own dangling-else. `if a do X else if b do Y done;` can be a two-rung ladder
with one terminator, or an `else` containing a nested if statement with its own terminator. They
differ only in how many `done`s follow, which is not decidable with one token of lookahead.

**Ruling.** `else` immediately followed by `if` is **always** a ladder rung. A plain `else` branch
may not begin with a bare `if` statement; wrap it in a `start` block to nest.

**Rationale.** Nothing is lost. A ladder rung already means exactly what a nested if means, and
needs one fewer terminator. This is the reading every example in the corpus uses.

### D35 — The cast operator has a precedence · `SETTLED`

**Gap.** §7.1's precedence table omitted `:>` entirely, despite `:>` appearing in §4.5, §9 and two
demos. The grammar could not place `x :> Z`.

**Ruling.** `:>` binds **looser than arithmetic and bitwise, tighter than logic and comparison**.
So `a + b :> R` is `(a + b) :> R`, and `a :> R > b` is `(a :> R) > b`. Left-associative.

**Rationale.** A cast almost always applies to a computed value and is almost always compared or
tested afterwards. The revised table is in §7.1.

### D36 — `type` is both a keyword and a built-in · `SUPERSEDED by D87`

**Conflict.** `type X: ...` declares a type (§4.3), and `type(x)` is the introspection built-in
(§11.3). The same word opens both.

**Ruling.** Resolved by one token of lookahead: `type` followed by `(` is the built-in, `type`
followed by an identifier is a declaration.

**Rationale.** The two forms cannot otherwise be confused — a declaration always names something,
a call always parenthesises. Found when `type_inference.bee` was the last demo still failing to
parse in Phase 2.

**Superseded.** D87 renames the built-in to `kind`, so the collision no longer exists and the
lookahead is kept only to diagnose the old spelling.

---

## Part C3 — Rulings forced by the type system (D37–D38)

### D37 — Integer literals are untyped; real literals are not · `SETTLED`

**Gap.** §4.5 says there is no implicit numeric conversion apart from widening in arithmetic. Read
strictly, that makes `new n ∈ N; let n := 1;` an error, because `1` is a `Z` literal and `Z` does
not widen to `N`. It also breaks recursion over naturals: in `fib(n-1)` with `n ∈ N`, mixing `N`
with the `Z` literal `1` promotes to `Z`, and `Z` cannot then be passed back to an `N` parameter.
Every demo that recurses would fail to compile.

**Ruling.** An **integer literal is untyped** until it meets a typed context, at which point it
takes that type if it fits. In arithmetic, an untyped literal takes the other operand's type, so
`n - 1` stays in `N`. A **real literal is typed `R`** and never adapts downward.

**Rationale.** This is the Go/Ada "untyped constant" treatment, and it is the only way the
documented examples compile. Restricting it to integer literals is what keeps
`new n ∈ Z; let n := 10.5;` an error — which is exactly the narrowing §4.5 forbids, and is one of
the conformance tests.

**Cost.** `let n := 3000000000;` on an `N` is accepted statically and traps at runtime if it does
not fit. Range checking of literals against target widths is deferred.

### D38 — `[T]` parameters take an array *or* a boxed primitive · `SETTLED`

**Conflict.** `bubble_sort.bee` declares `rule sort(this ∈ [Z])` and calls `apply sort(test)` where
`test` is an array. `output_params.bee` declares `rule pro(a, b ∈ [N])` and calls
`apply pro(a:@x)` where `x` is a plain `N`. The parameter syntax is identical; the arguments are
not.

**Ruling.** A `[T]` parameter accepts either:

- an **array of T**, passed by reference, written plainly: `apply sort(a);`
- a **primitive T**, boxed at the call site and therefore written `@`: `apply inc(@i);`

The choice is made by the argument's type. Passing a primitive without `@` is E009; passing an
array *with* `@` is E231.

**Rationale.** It is the only reading under which both demos are correct, and it preserves D13's
point: `@` appears exactly when a caller's own local can be modified. An array argument was already
a reference, so `@` there would be noise.

---

## Part C4 — Rulings forced by the interpreter (D39–D41)

### D39 — `new x :: y` is a declaration form · `SETTLED`

**Gap.** §6 lists `::` among the assignment modifiers, and the Processing chapter writes
`new b :: a;` to declare a clone. The grammar in §5 only allowed `:=` after a `new`, so the
documented form did not parse.

**Ruling.** A `new` declaration accepts `::` as well as `:=`. `new b :: a;` declares `b` holding a
deep copy; `new b := a;` declares `b` sharing the reference.

**Rationale.** Without it there is no way to declare a clone in one statement, and the upstream
example is simply rejected. `VarDecl` now records which operator was used.

### D40 — A range descriptor names a domain of the base type · `SETTLED`

**Conflict.** `type Small: (0..9) <: Z;` gave `Small` the type "range of Z", so
`new a: 5 ∈ Small;` failed: a `Z` is not a range. But D9 already depends on the other reading —
`type Digit: ('0'..'9') <: A` is what makes `'0' ∈ Digit` a *value-domain* test.

**Ruling.** A range descriptor in a `type` declaration names a **domain of values of the base
type**. `Small` is a `Z` that happens to be constrained; `Digit` is an `A`. The base type is the
declared super-type when one is given, otherwise the range's element type.

**Rationale.** It is the only reading under which D9's documented examples work, and the only one
under which a variable of the type can hold anything.

**Not implemented:** the constraint is not enforced at runtime. `new a: 99 ∈ Small;` is accepted.
Domain checking needs a runtime representation for subtypes and is deferred.

### D41 — Collection compatibility ignores capacity · `SETTLED`

**Gap.** `[1,2] + [3]` was rejected because `[Z](2)` and `[Z](1)` are different types. Capacity is
part of an array's *type* but should not be part of its *compatibility*.

**Ruling.** Two collections are compatible when their element types are. Capacity is checked at
allocation, never at assignment or concatenation.

**Rationale.** The alternative makes every array operation depend on literal length, so
`let a := b;` between two arrays of different sizes would fail even where the language clearly
intends it to work.

---

## Part C5 — Rulings forced by sets and maps (D42–D46)

### D42 — `{}` is the empty set · `SETTLED`

**Conflict.** `{ }` delimits sets, hash maps *and* objects. An empty one is ambiguous between all
three.

**Ruling.** `{}` is an **empty set**. An empty map needs an annotation: `new m ∈ {S:Z};`. When
objects arrive, an empty object will need one too.

**Rationale.** Sets are the simplest of the three and the only one whose empty form appears in the
corpus. An annotation is a small price in the two rarer cases.

### D43 — `|` inside a collection literal is the builder separator · `SETTLED`

**Conflict.** `{ x | x ∈ (1..3) }` is a set builder, but `|` is also bitwise-or, so `{a | b}` is a
one-element set containing `a | b`. Worse, `|` binds tighter than `∈`, so the builder form parses
as `{(x|x) ∈ (1..3)}` — silently wrong rather than an error.

**Ruling.** Inside `{}` or `[]`, a **top-level `|` is the builder separator**. Bitwise-or in a
collection literal must be parenthesised: `{(1 | 2)}`.

**Rationale.** Builders are documented and common; a bare bitwise-or inside a set literal appears
nowhere. The parser detects a top-level `|` by lookahead and suppresses it as an operator while
parsing the builder head — the same mechanism D33 uses for `∈`.

### D44 — A top-level `:` makes a brace literal a map · `SETTLED`

**Ruling.** `{1:"a"}` is a map; `{1,2}` is a set. The decision is made on the first top-level `:`.
Map builders write their pair parenthesised — `{ (k:v) | ... }` — which the documentation already
does.

### D45 — Maps display as parenthesised pairs · `SETTLED`

**Conflict.** The Collections chapter shows a map as `{'key2':"value2", 'key3':"value3"}`, while
the Builders chapter shows `{(0:0),(2:4),(4:16)}`. Both are upstream.

**Ruling.** `{(k:v),(k:v)}`. Pairs are parenthesised, no spaces.

**Rationale.** It matches the builder chapter, which is the more precise of the two, and it makes
the pair structure visible in nested output.

### D46 — `Δ` is an operator, not a letter · `SETTLED`

**Conflict.** `Δ` appears in the permitted-Greek identifier set *and* as the symmetric-difference
operator. It cannot be both.

**Ruling.** `Δ` is the symmetric-difference operator and is removed from the identifier alphabet.
The other Greek capitals (`Σ Π Ξ Γ Ψ Ω`) remain available as names.

**Rationale.** No corpus identifier uses `Δ`, and the operator has no alternative spelling.

---

## Part C6 — Rulings for Bee-1b (D47–D51)

### D47 — The right operand of `?` is an argument list · `SETTLED`

**Gap.** `"a=#(z) b=#(s)" ? (1, "two")` mixes types, but a parenthesised comma list is a list
literal, and lists are homogeneous. The documented examples do not type-check.

**Ruling.** After `?`, a **written** parenthesised list is the argument list and need not be
homogeneous. Anything else is a single argument, so `"#[*]" ? (array)` sees the whole array rather
than its elements spread.

**Rationale.** Same shape as D28 for `print`, and decided the same way. The distinction between a
written list and a value that happens to be a list is exactly what makes `#[*]` usable.

### D48 — Bare identifier keys make a brace literal an object · `SETTLED`

**Conflict.** The documentation writes maps as `{key1:"value1"}` and objects as `{a1:1, a2:2}`.
These are the same syntax.

**Ruling.** A brace literal whose keys are **bare identifiers** is an **object**; a **map** needs
expression keys — `{"key1":"value1"}` or `{1:"a"}`. In type position, `{a ∈ Z, b ∈ S}` is a
record, `{Z}` a set and `{Z:S}` a map.

**Rationale.** Something has to break, and the map form has a natural repair (quote the key) while
the object form does not — an object's field names are not values. This contradicts the map
examples in the Collections chapter; those keys must now be quoted.

### D49 — `_` in a format picture means a space · `SETTLED`

**Gap.** §18 gives the numeric picture as `#(ap:l.d)` where `p` is padding, "`_` or `0`", without
saying what `_` pads with.

**Ruling.** `_` pads with **spaces**; `0` pads with zeros. The underscore is a visible stand-in for
a space in the picture, not a literal character.

**Rationale.** A literal-underscore reading makes `_` useless — the character could simply be
written. Space padding is what alignment is for.

### D50 — A match branch matches by membership only for real collections · `SETTLED`

**Conflict.** Ranges and sets in a `when` clause should match by membership, so
`when (0..9) do` catches any digit. But strings are element-bearing too, and `when "a" do` must
mean equality, not "contains an a".

**Ruling.** A `when` value matches by **membership** when it is a set, list, array, map or range,
and by **equality** otherwise — including strings.

### D51 — `match` is designed here, not implemented from a specification · `PROVISIONAL`

**Gap.** This is not a conflict but an absence. The upstream `match` chapter is four sentences of
prose, a broken diagram link, and one type declaration. It states that a match has an "all" variant
and a "one" variant, and never shows the syntax of either — no `when`, no `other`, no example.

**Ruling.** `match` is designed to match the rest of the language rather than invented freely:

```bee
match [all|one] selector [label]:
when value, value do
  ...
other
  ...
done [label];
```

- The block opens with a keyword and `:`, branches use `do`, and it closes with `done;` — the same
  shape as `if`, `start` and `cycle` (D4).
- `when` and `other` are the keywords the documentation's own trial chapter uses for "a branch" and
  "everything else", so they carry their existing meaning.
- `all` and `one` are **contextual**: they are only the variant when a selector follows, so a
  variable may still be called `all`. The default is `one`, matching the documented sentence that
  ALL is the variant you opt into.
- Branch values reuse `∈` semantics implicitly (D50) rather than adding pattern syntax the language
  does not have.

**Provisional** because it is a design, not a reading. If upstream later specifies `match`, this
should yield to it.

---

## Part C7 — Rulings for modules (D52–D57)

### D52 — Two path roots, dot-separated · `SETTLED`

**Conflict.** The upstream corpus spells module paths four different ways:
`$bee_lib.folder.module`, `$pro.src.demo_module`, `$pro_src.test_module`, and
`lib_folder/test_module`. Roots, separators and naming are all inconsistent.

**Ruling.** Components are separated by `.`, and there are exactly two roots:

| Root | Resolves to |
|---|---|
| `$pro` | the project root — the directory holding the main module |
| `$lib` | `lib/` under the project root |
| *(none)* | relative to the directory of the module doing the loading |

`$bee_lib`, `$pro_lib`, `$pro_home` and `/` separators are rejected with a diagnostic naming the
two that exist.

**Rationale.** Two roots cover every documented layout: `src/` reached as `$pro.src.x`, `lib/` as
`$lib.x`, and a system library location is meaningless until there is a package manager. A single
separator removes the `.`-versus-`/` question entirely.

### D53 — The public marker is parsed, not lexed · `SETTLED`

**Problem.** A leading `.` marks a public member — `set .PI: 3.14;`, `rule .bar(...)`. But `.` is
also member access, and `.pi` at the start of a line is indistinguishable from `x.pi` to a lexer.

**Ruling.** The marker is handled in the **parser**, as an optional `DOT` immediately after `set`,
`new`, `type` or `rule`. A declaration keyword has just been consumed at that point, so there is
nothing to be ambiguous with.

**Rationale.** No lexer mode flag, no new token, no interaction with member access. The one place
the two readings could collide is the one place a declaration keyword guarantees which is meant.

### D54 — A module is loaded once per program · `SETTLED`

**Ruling.** Modules are cached by resolved path. Two modules that both `use` a third share one
instance, so its module-level state is shared. Circular loading is a compile-time error (E110)
naming the chain.

**Rationale.** The documentation says a library module "can be loaded a single time in another
module" and that loaded modules stay resident. Shared state is the consequence, and it is what
makes a module-level counter behave the way the docs' examples assume.

### D55 — A collision inside `with` is an error · `SETTLED`

**Gap.** `with a, b do` suppresses both qualifiers. If both export the same name, one silently
wins.

**Ruling.** Reported as E116, naming both modules. The programmer qualifies explicitly instead.

**Rationale.** This was flagged as an open question back in Phase 2 and deferred. Silent shadowing
across module boundaries is exactly the kind of implicit behaviour the language's own design
principle rejects.

### D56 — Private members are callable inside their own module · `SETTLED`

**Ruling.** Visibility restricts what a **qualifier** can reach, not what the module can do
internally. A private rule is dispatchable from anywhere in its own file; `hide` likewise only
blocks the importing module's view, so a hidden constant still works inside the module that
declared it.

**Rationale.** The alternative makes private members useless. Found while writing the conformance
project: `hide banner.EDGE` correctly blocked the importer while `banner.shout` kept using `EDGE`
internally.

### D57 — Path components may be keywords · `SETTLED`

**Problem.** Module names come from **file names**, so a file called `other.bee` or `match.bee`
could not be loaded at all — the path parser expected an identifier and `other` is a keyword.

**Ruling.** Inside a `use` path, components may be keywords. If the **implied** qualifier would be
a keyword, an explicit `as` is required (E118).

**Rationale.** A filesystem does not know about Bee's keyword list, and reserving 90-odd filenames
would be a strange constraint. The `as` requirement keeps the qualifier itself unambiguous.

---

## Part C8 — Rulings for Bee-2 (D58–D62)

### D58 — `Q(m,n)`, not `Qm.n` · `SETTLED`

**Problem.** §19 writes container sizes both ways. `Q5.2` cannot be lexed as one token: `Q5` is a
valid identifier, so it arrives as an identifier, a dot and an integer — the same shape as member
access.

**Ruling.** `Q(m,n)`. Bare `Q` means the documented default `Q(14,17)`. `Q5.2` is recognised in
type position purely to produce a diagnostic pointing at the parenthesised form.

### D59 — `begin` defers; `wait` joins in start order · `SETTLED`

**Amended in Bee-2.** Arguments are bound when `begin` runs, not when `wait` does. The first
implementation captured the environment and evaluated the call at `wait`, so four jobs started in a
loop all saw the loop variable's final value — the documented map-reduce example returned 8800
instead of 5050. Found by porting it.


**Conflict.** §21's example starts four jobs and states the results come back "ordered by
completion" — that is, by how long each happens to take. A test asserting that ordering would be
asserting a race.

**Ruling.** `begin` **queues** a call; `wait` runs the queue in **start order**. Coroutines (rules
containing a bare `yield`) are separate: those get real suspend and resume.

**Rationale.** Bee has no shared-memory model, no locks, and no memory ordering — there is nothing
in the design that a truly parallel `begin` could mean. Deterministic ordering keeps every program
using it testable, which a race does not. If real parallelism arrives it needs a memory model
first, and that is a language design question, not an implementation one.

**Cost.** `begin` gives no speedup. It is concurrency's *shape* without its performance, and that
is stated rather than implied.

### D60 — A coroutine is a rule containing a bare `yield` · `SETTLED`

**Gap.** §21 shows `begin test(9)` starting a coroutine and `begin sum(a,b)` starting a job, with
identical syntax. Nothing says which is which.

**Ruling.** A rule whose body contains a bare `yield;` is a **coroutine**; any other rule started
with `begin` is a **job**. The distinction is a property of the callee, not the call site.

**Rationale.** It is the only signal available, it needs no new syntax, and it is checkable
statically. A coroutine also publishes its **final** result when its body ends, not the last value
it yielded — which is what makes the documented terminating-sentinel pattern work.

### D61 — A constructor is a rule whose result is named `self` · `SETTLED`

**Gap.** §15 shows constructors as rules returning `self`, but never says how the compiler knows a
rule is a constructor rather than an ordinary rule that happens to use that name.

**Ruling.** A rule with exactly one result named `self` is a constructor. Its **name is also its
type**, registered in a separate table so the rule and the type do not shadow each other:
`Point(3,4)` is the call, `∈ Point` is the type. A parent is declared on the result —
`=> (self ∈ Child <: Parent)` — and `super(...)` chains to it.

**Rationale.** No new keyword, and it matches every documented constructor. The separate type
registry is what makes `rule Point(...) => (self ∈ Point)` resolvable at all: the annotation names
the type the rule is in the middle of defining.

### D62 — `p\q` is a literal, not two divisions · `SETTLED`

**Problem.** §19 calls `p\q` a *literal notation*, but `\` is also the rational-division operator
at multiplicative precedence. So `1\4 / 1\8` parsed left-to-right as `((1\4) / 1) \ 8` and gave
0.03125 instead of 2.

**Ruling.** Between two **integer literals**, `\` binds at primary precedence and forms a rational
literal. Between anything else it is the operator.

**Rationale.** The documentation's word is "literal", and a literal binds tighter than any
operator. Found by a test asserting `1\4 / 1\8 = 2`.

---

## Part C9 — Ruling from running in a browser (D63)

### D63 — Coroutines are generators, not threads · `SETTLED`

**Problem.** The first implementation (D60) ran each coroutine on a worker thread with a strict
ping-pong handoff. That is correct and deterministic, and it fails completely on a host without
threads:

```
RuntimeError: can't start new thread
```

which is what Pyodide raises, and therefore what the browser playground did.

**Ruling.** A coroutine is a **Python generator**. `yield from` propagates suspension through every
nested frame, which is exactly the stackful behaviour §21 requires, and it needs no threads at all.
Statement execution is a generator; expression evaluation is not, because a bare `yield` is a
statement and can never appear inside an expression.

**Rationale.** The threading version was a correct implementation of the wrong mechanism. Threads
buy nothing here — the handoff was strictly alternating anyway, so there was never any parallelism
to lose — and they cost portability to the one host that matters most for a language nobody has
heard of.

**Also removed:** the 10-second handoff timeout that guarded against a hung tab. With no threads
there is nothing to hang.

**Cost.** Every statement handler that can contain another statement is now a generator, and the
entry points must drive rather than delegate. A `yield` reached outside a coroutine is a runtime
error naming the cause rather than a silent suspension.

---

## Part C10 — A memory model, of sorts (D64)

### D64 — Parallelism requires isolation, not locks · `SETTLED`

**The gap.** The concurrency chapter promises that "each aspect is executed on a different core, and
the application runs them in parallel", and provides **no way to make that safe**. There is no
mutex, no lock, no atomic, no ordering guarantee, no volatile, no channel discipline — the only
concurrency vocabulary in the whole design is `begin`, `wait`, `yield` and a `$threads` count.
D59 therefore made `begin` sequential, because a race is not a testable specification.

Adding locks would be inventing a large piece of language. There is a smaller answer.

**Ruling.** A job may run in parallel **only if it is isolated**: it touches no shared mutable
state, so no interleaving can change its result. Concretely, an isolated rule

- reads and writes no module-level variable (constants are immutable and therefore fine);
- writes through no reference parameter, so it cannot mutate a caller's array, list, set, map or
  object;
- performs no I/O, because the console buffer and stdin are shared;
- starts no coroutine and no further job;
- calls only isolated rules.

Isolation is decided **statically**, by `bee/isolation.py`, with a fixpoint over the call graph so
that recursion does not disqualify a rule and contamination travels the whole chain.

**Rationale.** This is the one condition under which parallelism needs no memory model at all. If a
job cannot observe or affect another, ordering is unobservable, and D59's determinism stops being
an imposition and becomes a fact. It also costs the programmer nothing to check: the analysis is
already written, and `--isolation` reports it.

The upstream map-reduce example passes: `rule sum(a, b ∈ Z) => (r ∈ Z)` accumulates into a local
and returns it, touching nothing shared. That the documentation's own parallel example is isolated
is good evidence the restriction is the right shape.

**Not yet done.** Nothing runs in parallel. The analysis says *which jobs could*, which is the part
that has to be true first. Actual parallel execution belongs in the C backend with pthreads —
the interpreter would gain nothing from it, since the host serialises bytecode anyway, and
coroutines have already had to abandon threads once to survive a browser (D63).

**Cost.** The rule is conservative. A job that only *reads* a module variable is rejected even
though concurrent reads are harmless, because "no other job writes it" is a whole-program property
and this analysis is per-rule. Loosening that is future work, not a correction.

### D65 — Locks are rejected · `SETTLED`

**The question.** D64 restricts parallelism to isolated jobs, which forbids jobs from sharing
mutable data at all. The conventional way to lift that restriction is a mutex, a lock or a
`synchronized` block. Bee should not have one.

**Ruling.** No locks, no mutexes, no atomics, no `synchronized`. If shared mutable state is ever
needed across jobs, it will come from restricting *aliasing* — ownership transfer, channels,
immutability — not from guarding access after the fact.

**Rationale.** Three of the design's own stated priorities point the same way.

- **Safety above performance.** The design says so explicitly, and lists safety first. A lock does
  not make a program safe; it makes a program safe *if the programmer holds it everywhere it is
  needed*, which is a property no compiler checks and no test reliably catches.
- **Explicit above implicit, even at a cost.** A lock is the opposite: the dangerous thing is the
  code you did *not* write. A missing `let` is a compile error in Bee; a missing lock would be a
  race that passes every test until it does not.
- **No pointers, on safety grounds.** This is the decisive one. The design removed pointers and
  pointer arithmetic because they are dangerous, and replaced them with boxing and an explicit `@`
  at the call site so that every possible mutation of a caller's variable is visible where the call
  is written (D13). **A language that removed pointers for safety should not reintroduce data races
  through the side door.** A race is a pointer bug with worse reproduction.

It is also a large amount of new language — a type, a statement form, acquisition order rules,
reentrancy, and a deadlock story — for a design that currently has none of it.

**What replaces it.** D64 for the safe subset today. Beyond that, the shapes worth considering all
restrict aliasing rather than guarding it: making `for ∀` a parallel loop with a checked isolation
requirement (which would also retire D20's "inert" ruling); an ownership-transfer modifier
alongside `:=` and `::`; and channels as a real type, which `producer_consumer.bee` already
simulates with a list. **All three are designs, not readings** — nothing upstream suggests them,
and they belong to the author to accept or refuse.

---

## Part C11 — Bee-3: changes made for safety (D66–D73)

Everything above this point is a *reading* of an existing design, or a decision forced by a gap in
it. This part is different: these are **deliberate changes**, made because Bee-2 had defects that
a language claiming safety as its first priority should not have. Each states what was wrong, what
changed, and what it costs.

### D66 — Comparison binds tighter than logic · `SETTLED` · **breaking**

**Was.** Logic bound tighter, so `a = 1 ∧ b = 2` parsed as `a = (1 ∧ b) = 2` — a chained
comparison of a nonsensical operand. The most ordinary line in programming did not work, and
Bee-2 needed a dedicated diagnostic (E011) to explain why.

**Now.** Comparison binds tighter than `∧` and `∨`, as in C, Java, Python, Go, Rust, JavaScript and
mathematical notation alike. `a = 1 ∧ b = 2` means what it looks like.

**Why it was wrong.** Comparison *produces* the booleans that logic *consumes*. Ordering them the
other way inverts the data flow, so the operands do not exist yet when the operator wants them.

The likely origin is C's most notorious wart — `a & MASK == 0` parsing as `a & (MASK == 0)` — which
Ritchie later called a mistake. Bee applied that shape to `∧`/`∨` as well, making it far worse:
in C only the rare bitwise case bites, in Bee-2 every compound condition did.

Bitwise still binds tighter than comparison, which is the *correct* half of C's arrangement.

**Cost.** Any Bee-2 source relying on the old order changes meaning. Nothing in the corpus did:
every compound condition was already parenthesised, precisely because the old order made bare ones
an error.

### D67 — `**` opens a comment only at the start of a line · `SETTLED` · **breaking**

**Was.** `**` was a comment in every position, so `a ** b` silently commented out the rest of the
line. A reader arriving from Python or Fortran reads that as exponentiation.

**Now.** `**` opens a comment only when nothing but whitespace precedes it on the line — the same
rule D26 and D27 already applied to `+-` and `--`. Mid-line, it is an error naming both readings.

**Cost.** None measured. All 126 `**` comments in the corpus are already flush-left.

### D68 — Every operator has an ASCII spelling · `SETTLED`

**Was.** `∈` was required in every declaration, `∀` and `∃` in every quantifier, `∪`/`∩`/`Δ` for set
algebra. The design's answer to typing them was an APL-style keyboard that does not exist.

**Now.** `in` `is` `union` `inter` `sdiff` `subset` `superset` `root` `forall` `exists` `approx`
`plusminus` `divides` join the existing `and` `or` `not` `xor`, and `===`/`!==` spell `≡`/`≠≡`.
The Unicode forms remain, and remain preferred; they are simply no longer mandatory.

**Why.** This is the largest barrier to anyone trying the language, and it is not a safety
trade-off — a program nobody can type is a program nobody proof-reads. Julia settled this argument
years ago by making its Unicode optional.

### D69 — `==` and `!=` are value equality · `SETTLED` · **breaking**

**Was.** D24 made `==`/`!=` reference identity and `=`/`≠` value equality. Every mainstream
language uses `==` for value equality, so a newcomer writing `a == b` got identity and no warning.

**Now.** `=` `≠` `==` `!=` all compare **values**. Identity is `is`, which reads correctly and
matches Python.

**Cost.** A Bee-2 program using `==` for identity changes meaning silently. Nothing in the corpus
did — identity comparison appears nowhere.

### D70 — Shadowing is an error · `SETTLED` · **breaking**

**Was.** A warning. **Now.** An error.

**Why.** In a language whose stated priority is that the reader should never have to work out what
a line means, requiring them to scan outward for which `x` is in scope is exactly the wrong
default. A warning is advice; safety properties should not be advisory.

**Cost.** One demo needed a rename.

### D71 — Forward declarations, and therefore mutual recursion · `SETTLED`

**Was.** No hoisting and no forward declarations, so mutually recursive rules were **unwritable** —
not awkward, impossible. Pascal solved this in 1970.

**Now.** A rule may be declared with a signature and no body; its definition follows later. A
forward declaration with no matching body is an error (E249).

**Why it matters for safety.** Programmers do not abandon the algorithms they need; they inline
them by hand, and hand-inlined mutual recursion is where bugs live.

### D72 — A `match` must be total · `SETTLED` · **breaking**

**Was.** A `one`-variant match whose selector hit no branch did nothing at all, silently. That is
the classic `switch` bug.

**Now.** `other` is required unless the variant is `all`, which is a filter rather than a
selection and needs no default.

**Cost.** Eight tests gained an `other` branch. Exhaustiveness *inference* — proving a match total
over an ordinal or range subtype without a default — is future work; requiring the branch is the
sound conservative version.

### D73 — A resized array invalidates its slices · `SETTLED` · **breaking**

**Was.** D3 ruled that `++` allocates a new buffer and existing slices keep viewing the **old**
one. That preserved the documented behaviour and was memory-safe in the narrow sense, but it means
a slice silently starts reporting stale data — a use-after-free in every sense except the one a
sanitiser detects.

**Now.** An array carries a version, a slice records the version it was taken at, and using a slice
after its array has been reshaped raises `$out_of_range` naming the cause.

**Why the reversal.** D3 chose to preserve a documented example. That was the right call for an
implementation *of* Bee-2 and the wrong one for a language sold on safety: silent wrong answers are
worse than loud failures, and this was the only place in the language where a value could quietly
become wrong.

### D74 — Comparisons chain, as in mathematics · `SETTLED`

**Was.** Comparison was non-associative: `a < b < c` was rejected, and the user was told to write
`(a < b) ∧ (b < c)`.

**Now.** `a < b < c` means what it means in mathematics — each link tested in order, **each operand
evaluated once**, stopping at the first false link. Exactly Python's semantics.

**Why the old rule was wrong.** Non-associativity exists to stop an ambiguity, and there was none
to stop. The C reading, `(a < b) < c`, compares a `B` with a `Z` and **does not type-check in
Bee** — the language already rejected it for an unrelated and better reason. The rule was guarding
a door that was already locked.

Worse, the mandated workaround is a hazard. `(a < b) ∧ (b < c)` **evaluates `b` twice**, so a
middle operand with side effects runs twice:

```bee
print (1 < bump()) ∧ (bump() < 3);   -- "evaluated" printed twice
print 1 < bump() < 3;                -- printed once
```

For a language that traps overflow and forbids shadowing to force double evaluation on its users
was the wrong trade.

**Also, notation.** Bee's whole argument for `∈`, `∀`, `∃` and set-builders is that programs should
read like the mathematics they encode. `a < b < c` is that same argument, and rejecting it was
inconsistent with the rest of the design.

**Restrictions.** `∈` and `∉` may not appear in a chain (E251): membership is not transitive, so
`a ∈ b ∈ c` has no sensible reading. Every adjacent pair must be comparable, checked separately.

### D75 — Contracts · `SETTLED`

**The gap.** `expect` exists, but it is a statement in a body. A precondition written that way is
invisible to a caller, indistinguishable from ordinary logic, and gone the moment someone edits the
body. Bee had assertions and no way to say what a rule *promises*.

**Ruling.** A rule may carry `require` and `ensure` conditions, written between the signature and
the body:

```bee
rule half(n ∈ Z) => (r ∈ Z):
require n ≥ 0;
require n % 2 = 0;
ensure r * 2 = n;
  let r := n / 2;
return;
```

- **`require`** is the caller's obligation, checked once the parameters are bound and before any of
  the body has run.
- **`ensure`** is the rule's promise, checked after the body with the results holding the values
  the caller will see. It may name parameters and results together.
- A failure raises `$broken_contract` (105), naming the rule and which condition.
- Contracts are checked on **every** call, including recursive ones.

**Contracts must be free of side effects**, enforced by the isolation analysis (D64): a condition
may only call rules that touch no shared state, perform no I/O and start no work. A check that
changes what it is checking is not a check, and this is exactly the reuse D64 was worth building
for.

**Why this and not something else.** Every other item on the improvement list makes Bee-3 bigger or
faster. This makes it *safer*, which is the whole claim. A precondition in the signature is three
things at once: documentation that cannot drift from the code, a runtime check, and — for anyone
who later wants it — the shape a prover consumes. Ada's road to SPARK started here.

**Not yet.** No `old` values in a postcondition, so a rule cannot say "the result is larger than the
argument *was*" when the argument is boxed and has been modified. No static checking of contracts at
call sites, no inheritance of contracts by constructors, and no way to disable checks in a release
build. Each is worth having; none is needed for contracts to earn their place.

### D76 — Exhaustiveness is inferred where the domain is finite · `SETTLED`

**Was.** D72 required `other` on every `one`-variant match, with no exception. Sound, but it forces
a dead branch onto a match that already covers every case — and a rule you must satisfy even when
it is pointless teaches people to satisfy it reflexively, which is the habit D72 exists to prevent.

**Now.** `other` is required only when the branches cannot be shown to cover the selector's domain.
A domain counts as finite when it is `B`, or a range subtype over at most 1024 integers. Branch
coverage is computed from integer literals, literal ranges and literal collections.

```bee
type Small: (0..3) <: Z;
match v:                   -- total, so no `other` needed
when 0, 1 do  ...
when (2..3) do ...
done;
```

A partial match now says **which values it misses** — `this match does not cover 2, 4, 5` — rather
than only that a default is absent. Anything the analysis cannot decide still requires `other`, so
the rule remains sound.

### D77 — `exact` shows a Q in full · `SETTLED`

**Was.** `Q` displays rounded to `$precision`, so `1\3` prints `0.33334` and two values differing
below precision print identically. For a type whose entire purpose is exactness, having no way to
see the exact value was a real gap.

**Now.** The built-in `exact(q)` returns every fractional digit. A template picture may also ask
for more digits than `$precision`: `"#(r:0.10)" ? (t)`.

```bee
print 1\10;            -- 0.1
print exact(1\10);     -- 0.09999847412109375
```

That second line is the point. One tenth has no finite binary form, so `Q` cannot hold it exactly —
the documentation is right to call `Q` approximate — and now a programmer can *see* which values
are exact and which are not, instead of being told.

The C backend computes the digits in integers rather than through a double: a `Q14.17` needs 17
decimal digits and a double carries about 16, so the float route would lose exactly the property
the type exists for.

### D78 — Only a written module variable is shared state · `SETTLED`

**Was.** D64's isolation analysis rejected any rule that so much as *read* a module variable. Sound,
but too blunt: concurrent reads of something nothing writes cannot race.

**Now.** A module variable that no rule ever assigns is effectively a constant, and reading it keeps
a rule isolated. Only variables something actually writes count as shared mutable state, and the
diagnostic says so: `reads "counter", which another rule writes`.

**Why it is still sound.** "Nothing writes it" is a whole-program property, computed over every
rule in the module before any verdict is reached — not a per-rule guess.

### D79 — A variable read but never written is an error · `SETTLED`

**The gap.** Everything zero-initialises (D10), so a variable you meant to set but forgot reads as
`0` and the program carries on with a wrong answer. There was no analysis at all.

**The tension.** Full definite-assignment analysis — "not yet assigned at *this point*" — would be
the textbook answer and would **break the language**. This is idiomatic Bee:

```bee
new total ∈ Z;
for i ∈ (1..4) do
  let total += i;
repeat;
```

`let total += i` reads `total` before anything has assigned it, and relies on the zero. Accumulators
are everywhere in the corpus. D10 is a deliberate design decision, and it wins.

**Ruling.** An error when a variable is **read and never written anywhere in its scope**. That is
never correct: it is a name typed wrong, or an assignment forgotten entirely.

**Refinements, each forced by a false positive found in the corpus:**

- a loop writes its control variable on every cycle;
- `read x;` writes `x`;
- `begin got <+ f();` writes the collector, and `yield v << f;` writes `v`;
- passing a collection to a rule is a **potential write**, since that is exactly what a reference
  parameter means — `apply drain(queue)` counts as writing `queue`;
- an imported member and an alias already hold their module's value;
- **collections are exempt entirely.** A collection's zero value is *empty*, which is a real value
  programs legitimately declare and then fill or pass along. A numeric or Boolean zero read before
  any assignment is not: it is a forgotten `let` nearly every time.

**Cost.** Weaker than Ada's or Rust's analysis, which reject a read on any path lacking an
assignment. Bee-3 cannot have that without giving up zero-initialisation, and the exchange is not
worth it.

### D80 — Discarding a rule's results must be written down · `SETTLED` · **breaking**

**Was.** `apply value();` silently threw away everything the rule returned. That is how a checked
result becomes an ignored one.

**Now.** An error, unless the discard is explicit:

```bee
apply _ := value();     -- yes, throw them away
```

**Rationale.** The results are the rule's answer. A language that makes `@` visible at the call
site so a caller can see a mutation coming should not let a caller silently drop an answer.
`_` already means "deliberately unused" in a binding list; this extends the same spelling.

### D81 — Ownership transfer · `SETTLED`

**The gap.** D64 keeps parallel jobs safe by forbidding shared mutable state outright, which also
forbids the useful case: handing a job a value it may freely mutate because **nobody else can see
it any more**. D65 ruled out solving this with locks.

**Ruling.** A postfix `!` moves ownership. The source name holds nothing afterwards, and reading it
is an error until it is given a new value.

```bee
new numbers := [1,2,3,4];
print consume(numbers!);   -- ownership moves
print numbers;             -- E257: was moved and no longer holds a value
let numbers := [10,20];    -- a new value revives the name
```

Only owned types move — strings and collections. Moving a scalar is rejected, because scalars are
copied and a move would mean nothing; moving a constant is rejected outright.

**Why this rather than locks.** It restricts *aliasing* instead of guarding *access*, which is the
shape D65 argued for. If nothing else can reach a value, there is nothing to race over and no lock
to forget — and the compiler checks it rather than the programmer remembering.

**Not yet.** The isolation analysis (D64) does not yet take moves into account, so a job given a
moved value still counts as non-isolated. Teaching it that a moved argument is exclusively owned is
the step that would widen parallelism beyond pure jobs.

### D82 — `for ∀` claims independence, and the claim is checked · `SETTLED` · **breaking**

**Was.** D20 ruled `∀` in a `for` header **optional and semantically inert** — both spellings parsed
identically, and the symbol meant nothing. That was the right reading for an implementation of
Bee-2 and an unsatisfying one for a language this deliberate about notation.

**Now.** `for ∀ x ∈ src` asserts that the iterations are **independent**, and the compiler checks
it. An iteration may write only what it owns:

- its own locals, and the loop's control variable;
- an element of a collection **selected by the control variable** — `out[i] := ...` touches a
  different element each time.

It may not do I/O, write anything else it does not own, or call a rule that is not isolated in the
sense of D64.

```bee
for ∀ i ∈ (0.!6) do
  let squares[i] := i * i;      -- independent
repeat;

for ∀ i ∈ (1..4) do
  let total += i;               -- E258: writes something it does not own
repeat;
```

A plain `for` is unrestricted, so nothing is lost: the notation now distinguishes two things that
were previously the same.

**Cost, and it is real.** The upstream demos use `for ∀ i ∈ (0..9) do print a[i];` — a decorative
`∀` over a loop that does I/O, which is now an error. The migration is deleting one character, and
the diagnostic says exactly why, but it does invalidate the most common upstream loop.

**Nothing runs in parallel.** As with D64, the analysis establishes *which* loops could, which is
the part that has to be true before anything else is worth building.

### D83 — `Λ` and `Φ` are constrained `Q` domains · `SETTLED`

**The gap.** The geospatial types were the one part of the graphics chapter (§22) with real content:
longitude, latitude, and a note that 0.00001° is about 1.11 m. `PHASE6.md` declined graphics as
undesigned but flagged this part as specifiable.

**Ruling.** `Λ` is longitude, a `Q(8,17)` constrained to −180..180. `Φ` is latitude, a `Q(7,17)`
constrained to −90..90. Both are predeclared range subtypes, so the domain is enforced at every
store by the machinery D40 and D73 already provide.

```bee
new lon: 2.3522 ∈ Λ;
new bad: 200 ∈ Λ;        -- $out_of_range
```

**Rationale.** A `Q(8,17)` resolves about 7.6×10⁻⁶ degrees, roughly 0.85 m at the equator — better
than the chapter asks for. Making these *domains of an existing type* rather than new numeric kinds
means they inherit exact arithmetic, `≈`/`±` comparison, `exact`, and both backends for free. It is
the strongest evidence so far that `Q` was worth building properly.

`Λ` and `Φ` join the identifier alphabet to make this possible; the geospatial *symbols*
(`• ◉ ↯ ♁`) remain rejected, since they belong to the undesigned part of the chapter.

### D84 — Traits are nominal, and carry contracts · `PROVISIONAL`

**The gap.** Traits and abstract types were the only major documented feature never implemented.
Upstream mentions them and shows `<:`, but never says what a trait *is* — a set of required
signatures, a mixin carrying implementations, or a marker for `∈` tests. Each gives a different
language.

**What upstream does supply**, and what it settles: `generator.bee` declares methods **inside the
constructor**, with `.` marking them public. That is a real constraint, and it forecloses the
alternatives — methods living on the object mean dispatch is member lookup, needing no overloading,
no vtables, and no dispatch concept the language lacks. Bee has exactly one rule per name and this
design does not disturb that.

**Ruling.** A trait names the methods a type must provide, and its body is written as forward
declarations — the shape D71 already gives a signature with no body:

```bee
trait Shape:
  rule area() => (a ∈ R)
  ensure a > 0;
  rule name() => (n ∈ S);
done;

rule Circle(radius ∈ R) => (self ∈ Circle <: Shape):
  new self.radius := radius;
  rule .area() => (a ∈ R):
    let a := 3.14159 * self.radius * self.radius;
  return;
  rule .name() => (n ∈ S):
    let n := "circle";
  return;
return;
```

- Conformance is **nominal**: a type declares `<: Shape` on its constructor's result, and the
  compiler checks every required method is provided with matching arity. Nothing is satisfied by
  accident, which structural conformance would allow and which the explicitness principle rejects.
- A trait-typed parameter accepts any implementer, dispatching on the object.
- Parameter and result **names must match** the trait's, because the trait's contracts are
  evaluated in the implementation's scope and refer to them.

**The addition, and the reason this is worth having: traits carry contracts.** Whatever a trait
requires or ensures becomes every implementation's obligation, checked on every call, and a
violation is reported **at the trait's own line** — because that is where the promise was made.

**This is not novel, and the original wording here overclaimed.** Ada 2012 already does it:
`Pre'Class` and `Post'Class` on an interface's abstract subprograms are exactly contracts every
implementer inherits, and they are checked the same way. Eiffel has contract inheritance without
traits; Rust has traits without contracts; Go has neither — but Ada has both, and has since 2012.

What is fair to say is narrower: a trait specifying *behaviour* rather than only *shape* is the
natural meeting point of two things Bee-3 already had, and it cost almost nothing because D75 built
the machinery. Bee-3 arrives at Ada's answer independently, which is evidence the answer is right,
not evidence of invention.

**Provisional**, like D51, because it is a design rather than a reading. Upstream gave one worked
example and no statement of intent, so the shape follows the example and the rest is mine.

**Also fixed here.** D61 left a constructor's fields unknown, so *any* member access on a built
object went unchecked — `p.z` on a `Point` compiled fine. The field names are recoverable from the
body: every `new self.x` declares one. A child now inherits its parent's fields too, which is what
made the omission visible.

**Not yet.** No mixins or default implementations, no trait inheritance, and methods are per-object
rather than shared through a table — acceptable at this scale, wasteful at a larger one.

### D85 — A standard library, as built-ins · `SETTLED`

**The gap.** Bee-3 had five built-ins — `length`, `capacity`, `count`, `type`, `exact`. No `abs`,
no `min`, no `sort`, no way to search a string or turn text into a number. Every useful program had
to begin by rebuilding them, which is a larger obstacle than any missing language feature and the
least interesting to fix.

**Ruling.** Twenty-seven library rules, always in scope: `abs min max clamp sign floor ceil round
gcd · ord chr · upper lower trim reverse find contains replace split join · parse_z parse_r ·
sum sorted first last empty`.

**Why built-ins rather than a library written in Bee.** Because **Bee has no generics**. A library
rule `abs(n ∈ Z)` could not also serve `R` or `Q`, so it would need a differently-named copy per
type — `abs_z`, `abs_r`, `abs_q` — which is worse than no library. A built-in is checked by a
*function* rather than a fixed signature, so one `abs` covers every numeric, exactly as `length`
already covered every collection.

This is a workaround for a missing feature, and worth naming as one. If generics arrive, most of
this belongs in Bee source instead.

**Design points.**

- One table (`bee/builtins.py`) holds the signature check *and* the implementation, so the analyser
  and the interpreter cannot disagree about what a rule accepts, and the diagnostic is written
  once: `"abs" does not apply to (S)`.
- `round` goes to the nearer integer with **halves away from zero**, stated rather than inherited
  from a host, and matching how `:>` truncates toward zero.
- `find` returns −1 when the text is absent. A sentinel, which the rest of the language avoids —
  but there is no optional type yet, and inventing one here would be the wrong place for that
  decision.
- The C backend implements 21 of the 27; the rest are refused by name.

**Not included, deliberately.** `random` and `now` are non-deterministic, and every test in this
project depends on programs meaning one thing. They need a seeded generator and a clock injected at
the boundary, which is a design question rather than a missing function.

### D86 — Generics, scoped hard · `PROVISIONAL`

**The gap, made concrete by D85.** Seventeen of the standard library's twenty-seven rules are
built-ins **only because Bee had no generics**. `abs`, `min`, `sorted`, `first` are ordinary Bee
anyone could write in five lines — they live in the implementation's host language because the type
system could not say "any numeric" or "any collection of T". Worse, a user who wanted `median` or
`zip` could not write one *at all*, since their version would be locked to a single element type.

**Ruling.** Type parameters on rules:

```bee
rule first_of[T](items ∈ [T]) => (r ∈ T):
  let r := items[0];
return;

rule doubled[T <: Sized](thing ∈ T) => (n ∈ Z):
  let n := thing.size() * 2;
return;
```

- Parameters are inferred from the arguments; there is no way to write them at the call site.
- A variable appearing twice must agree, widening if both are numeric.
- A **bound** is a trait (D84), and it is what makes members visible: without one, `thing.size()`
  is rejected rather than waved through, because nothing is known about `T`.
- **Monomorphised**: the backend emits one C function per distinct set of type arguments, with the
  concrete types in its signature.

**Deliberately absent**, and this is the point of the ruling: no variance, no higher-kinded types,
no type parameters on *types* or traits, no defaults, no explicit instantiation, no specialisation.
Each is a place where generics systems get subtle, and leaving them undesigned is better than
designing them badly in an afternoon.

**Why monomorphisation.** Bee has no separate compilation and the whole program is available, so
the alternative — passing dictionaries — would buy nothing and cost indirection. The backend
already emitted one C function per rule; now it emits one per instantiation, with names like
`r_first_of__Z2` and `r_first_of__R2`.

**Provisional**, like D51 and D84. This is the largest design act in the log: a type-system feature
invented whole, on a language whose author has seen none of the eighty-five rulings before it.

**What it unlocks, and has not yet done.** Those seventeen built-ins could now be written in Bee
and moved into a library; `bee/builtins.py` and the backend's hand-written C for twenty-one library
rules could largely go. An optional type — the sentinel `find` returns −1 instead of — needs
exactly this and nothing more. Neither is done here.

### D87 — The built-in is `kind`, not `type` · `SETTLED` · **breaking**

**What was wrong.** `type(x)` returned a **string**. In a language that rejects truthiness, forbids
implicit narrowing and makes every mutation visible at the call site, the one introspection
facility answered in text:

```bee
kind(n) = "Z"       -- a typo compiles, and quietly says false
```

Worse, the *checked* way to ask already existed. `n ∈ Z` is a type test resolved at compile time,
and `≡` compares value **and** type. Every question worth asking had a safe answer; `type` offered
an unsafe one alongside.

**Ruling.** The built-in is **`kind`**, and it is documentation rather than introspection: a label
for a human to read. `type(` is diagnosed (E263) and points at it.

**Why the name changed rather than the return type.** Making it return a first-class type value is
the textbook fix and the wrong trade here. It needs types as runtime values, their own equality and
printing, and a decision about storing and passing them — and it would undo D86, which erases types
precisely so the backend can monomorphise. Spending a major feature on *runtime* type inspection,
in a language whose distinctive claim is *static* safety, is backwards.

**Why `kind` specifically.** "Type" is a noun and a verb in English — a kind, and the act of
entering characters — so `type_name`, the obvious rename, reads as "the name you type". `kind` has
only the one sense, does not collide with the keyword, and makes the division visible:

| | |
|---|---|
| `type Point: ...` | declares a kind |
| `n ∈ Z` | asks, and the answer is checked |
| `n ≡ m` | same value **and** same kind |
| `kind(n)` | a label, for printing |

**Cost.** Thirty-six call sites across the corpus, all mechanical. The old spelling produces a
diagnostic naming the new one, so nothing fails silently.

### D88 — `@T` is a boxed parameter, distinct from `[T]` · `SETTLED` · **breaking**

**What was wrong, and it is worse than it looks.** D13 and D38 let a `[T]` parameter accept either
an array of `T` or a boxed `T`, with the argument deciding at run time. That means **the same body
meant two different things**:

```bee
rule pro(a ∈ [N]):
  let a += 1;        -- increments a boxed scalar, or appends to an array
return;

apply pro(@x);       -- x becomes 11
apply pro(arr);      -- arr becomes [0,0,1]
```

Statically the parameter is an array, so `let a += 1` type-checks as an *append*; at run time with
a boxed scalar it *increments*. A rule's meaning depended on its caller, silently.

It also made contracts useless for exactly the rules that need them: `ensure a > 0` compared an
array with a number and was rejected, so a rule that mutates a caller's variable could promise
nothing about it.

**Ruling.** `@T` is a **boxed parameter** — a reference to a caller's `T` that the callee may
write. `[T]` is an array and only an array. Inside the body a boxed parameter **is** its element,
so `let a += 1` increments, and `ensure a > 0` means what it says. The call site still needs `@`,
which is D13 unchanged.

**Rationale.** One spelling could not mean two things without the body's meaning depending on the
caller — and in a language whose principle is that a reader should never have to work out what a
line does, that is the deepest kind of wrong. The notation was already there: `@` marks the
argument, so it should mark the parameter.

**Cost.** Two demos migrated, mechanically. `[T]` given a boxed argument is now an error naming
`@T`.

### D89 — `old n` in a postcondition · `SETTLED`

**The gap.** A postcondition could describe a *result* but not a *change*. `ensure r > n` works for
a pure rule; a rule that mutates its argument had no way to say "larger than it was". Ada has
`'Old` and Eiffel has `old`; contracts without it are limited to the rules that need them least.

**Ruling.** `old n` is what parameter `n` held at entry.

```bee
rule bump(n ∈ @Z):
ensure n = old n + 1;
  let n += 1;
return;
```

**Two restrictions, both deliberate:**

- **`ensure` only.** In a precondition nothing has happened, so `old n` would simply be `n`.
- **A bare parameter name.** `old (n * 2)` invites a question about when the multiplication happens
  that is not worth answering, so it is not allowed.

**Not `n'`,** which is Ada's spelling, because `'` already opens a character literal in Bee and
`n'` would be a lexical hazard.

**Cost, stated rather than hidden.** `old` on a collection is a **deep copy at entry** — O(n) on
every call. Only the parameters a postcondition actually mentions are snapshotted, so a rule pays
only for what it asked for, and the copy uses the same `::` semantics the language already has.
Ada and Eiffel both carry this cost; it is the price of talking about the past.

### D90 — The checks stay on, and now the price is known · `SETTLED`

**The complaint.** Contracts, range domains, index bounds and overflow traps all run always, with
**no measurement and no opt-out**. "Safety above performance" is only an honest claim if somebody
knows what it costs.

**What measuring found first.** Building the benchmark uncovered a divergence that mattered more
than any number: **compiled code did not enforce range domains at all.** The interpreter had
enforced them since D40; the backend never emitted the check. Compiled Bee was *less safe* than
interpreted Bee, and the differential harness had not noticed because no demo ever violated a
domain. That is fixed here, and pinned by a test.

**The measurements**, 60 million iterations, `cc -O2`, best of five, against a noise floor
established by timing one program against a copy of itself:

| Check | Cost |
|---|---|
| contracts | within noise |
| index bounds | within noise |
| range domains | **−17%** — the checked program is *faster* |
| overflow traps | no comparison: never omitted |

**The domain result is not an error.** It reproduces at ±0.2% against a 2% noise floor. Emitting
`bee_domain_z(v, 0, 1000002, ...)` *tells the optimiser the value's range*, and it uses that to
narrow the arithmetic that follows. A safety check that pays for itself by carrying information is
worth knowing about, and it is the opposite of what the complaint assumed.

**Ruling.** `--unchecked=contracts,domains` omits those two when compiling. **Overflow trapping and
index bounds cannot be omitted**, because the measurement gives no reason to: they cost nothing
detectable, and switching them off converts a caught mistake into silent corruption. Asking for
them by name is refused, with that reason.

**Not a language feature.** `--unchecked` is a compiler flag and cannot be written in source: a
library that could disable checks for its caller would be a worse hazard than any it removed.

**What is still unmeasured.** The interpreter, which always checks everything and is not for
performance; and `old` on a large collection (D89), whose deep copy is a real cost that this
benchmark does not exercise.

### D91 — Every diagnostic must be reachable, and tested · `SETTLED`

**The gap.** The compiler emitted 115 numbered diagnostics; 76 were asserted somewhere. The other
**39 had never been produced by a test** — nothing checked they could be reached, that their message
formatted, or that the code around them worked. Untested error paths are where crashes in the crash
handler live.

**What the first run found, before any of the cases were even right:**

- **`E104` crashed the parser.** A superscript like `x⁺⁻²` was accepted by `text.lstrip("+-")`,
  which strips *every* sign, so `"+-2"` passed `isdigit()` on the remainder and then reached
  `int("+-2")` — `ValueError`, no diagnostic, a traceback instead of an error message.
- **`E104`'s own error call was malformed**, passing the code as the message. It would have raised
  `TypeError` had it ever been reached. The diagnostic could never have fired.
- **`E106` had the same malformed call**, found by walking the AST of `parser.py` for every
  `self.error` whose first positional argument looks like a code.
- **`E030` was dead.** "Stray `!`" became unreachable when D81 made a bare `!` the move operator,
  so it always lexes now. Removed.
- **`E011`, `E015` and `E101` were dead**, left behind by D66 and D74 when the conditions they
  described stopped being errors. Removed.

**Ruling.** `tests/diagnostics/` holds the smallest program that provokes each code. The suite also
fails when a diagnostic is added to the compiler with no case, and when a case names a code no
longer emitted — so it cannot fall behind again in either direction.

**Why this rather than a language change.** Every previous time a test was built for something
assumed fine — the example gallery, the WebAssembly modules, the benchmark — it found a real
defect. This was the largest remaining unexamined surface, and it held two crashes and four pieces
of dead code.

### D92 — One place to ask each question about a type · `SETTLED`

**The problem, measured.** `sema.py` held 62 `isinstance` tests against types, `cgen.py` 35,
`interp.py` 10. Most were not dispatch — they were the *same question*, asked inline over and over:
`isinstance(ty.strip(t), ty.Prim) and t.code == "R"` appeared thirteen times.

That is why adding `Boxed` (D88) took three attempts. Every `isinstance(..., ty.Array)` that should
have become `(ty.Array, ty.Boxed)` had to be found by hand, and one was missed entirely — the
backend went on emitting no domain check at all until D90 measured it.

**Ruling.** A small vocabulary in `types.py`: `is_real` `is_integer` `is_natural` `is_alpha`
`is_text` `is_string` `is_boolean` `is_rational` `is_unknown` `is_sequence` `is_collection`
`is_writable_param` `is_callable`, beside the existing `strip` `unbox` `element_of` `is_numeric`
`is_reference`.

Each strips named subtypes, so `is_integer` is true of a `(0..9) <: Z` without the caller
remembering to strip. Forty-six call sites were rewritten to use them.

**The rule, stated so it survives.** A bare `isinstance` against a type is for **dispatch** — doing
different work per kind. It is not for **asking**. If a predicate answers the question, call it.

**Enforced, not merely recommended.** `tests/hygiene/` fails when an inline test reappears — and it
found seven the mechanical rewrite had missed on its first run. It also checks the argument order
of `error()` calls, the mistake that left E104 and E106 unreachable (D91), and puts every module
under a line limit so `sema.py` cannot quietly grow past being readable.

**What this does not do.** It does not shrink `sema.py`, which is still 2,690 lines, and it does
not remove genuine dispatch — 152 type tests remain and most of them are doing real work. It makes
the *next* type cheap, which is the thing D88 proved was expensive.

### D93 — One printer per statement kind, and layout is tested · `SETTLED`

**The problem.** `printer.statement` was a single 215-line chain of twenty-one `isinstance`
branches, growing by roughly fifteen lines per feature. `sema` and `interp` had dispatched on
`st_<NodeType>` since Phase 3; the printer never did.

**Worse, nothing checked its output.** The round-trip test parses, prints, reparses and compares
**trees** — so it catches structural loss, which is how it found missing type parameters in D86.
It cannot see *text*. Indentation, spacing and line breaks were entirely unverified.

**Demonstrated rather than assumed.** Setting `pad = ""` in the print statement's branch — so every
`print` in every program lost its indentation — left **all 119 tests passing**.

**Ruling.** Twenty-one `st_*` functions, dispatched by name, matching `sema` and `interp`. The
longest function in `printer.py` fell from 215 lines to 95.

**And the output is now checked as text**, at two levels:

- a sample program with nesting, whose exact indentation is asserted — that a rule's body is two
  spaces, a nested body four, that `else`, `done` and `repeat` return to the outer level, and that
  `return` is flush left;
- **every demo in the corpus**, for rules that must hold whatever statements appear: no trailing
  whitespace, no tabs, every indent a multiple of two, no blank line at the end.

The corpus sweep matters because the sample cannot exercise every path. A trailing space added to
one `done` slipped past the sample and was caught by the sweep.

**Verified by sabotage.** Each of the three regressions was reintroduced deliberately and the suite
now fails: the outdented `print` (1 failure), a trailing space (3), a one-space indent (38). Before
this ruling, all three passed silently.

### D94 — One handler per command-line mode · `SETTLED`

**The problem.** `cli.main` was 177 lines: twelve mutually exclusive modes as a chain of early
returns, sharing mutable state built along the way. Adding `--unchecked` (D90) meant threading a
set through three of them. **None of the twelve was tested**, because none could be driven without
a subprocess.

**Three bugs were living there.**

- **`--isolation` exited 1 on a mere warning**, and never printed its report. Its guard was
  `if diags:` rather than `if errors:`, so a naming warning suppressed the whole analysis.
- **That warning was printed twice** — once by the shared diagnostic pass, once by the mode's own.
- **`--emit-c` swallowed the source file.** Declared with `nargs="?"`, so `--emit-c program.bee`
  consumed the program as the *output* name and then failed with "the following arguments are
  required: file". This one predates the restructure and had been there since Phase 7.

**Ruling.** A `Session` carries the source, the diagnostics and the streams; each mode is a
function of one `Session` returning a status; a table maps flag to handler. The longest function in
`cli.py` fell from 177 lines to 31.

Output goes through the session rather than `print`, so a test can capture it without a
subprocess — which is what made the mode tests possible at all.

`--emit-c` now requires its filename, and `--show-c` writes to stdout. A flag with an optional
value that silently eats the next argument is a trap, not a convenience.

**Twenty-seven tests**, covering every mode, the exit codes, `--unchecked`'s refusals, and — the
bug that started this — that a warning does not stop `--check`, `--isolation` or `--run`, and is
reported exactly once.

### D95 — The differential harness compares failures too · `SETTLED`

**The problem.** The interpreter and the C backend implement the same semantics twice. `Q`
arithmetic alone lives in `values.py`, `interp.py`, `cruntime.py` and `cgen.py`. They agree only
because the differential harness says so — and the harness **compared standard output and nothing
else**.

So every error path was unchecked. That is precisely how the missing domain check survived until
D90 measured it: no demo violated a domain, so no output ever differed, and compiled code went on
being *less safe* than interpreted code.

**Ruling.** Both implementations now report a failure as `(output, status, message)`, and all three
are compared. A corpus of eighteen deliberately failing programs runs through both: division and
modulo by zero, indices past either end, addition, subtraction and multiplication overflow, values
above and below a domain, a domain checked on an argument, a failed `expect`, a broken
precondition, postcondition and `old`-value promise, `panic`, `over`, output retained before a
failure, and a `Q` too large for its container.

**Four disagreed on the first run** — same failure, different words:

| | Interpreter | Compiled |
|---|---|---|
| above a domain | `200 is above the domain of Small` | `200 is outside the domain of Small` |
| below a domain | `1 is below the domain of Small` | `1 is outside …` |
| on an argument | `99 is above the domain of Small` | `99 is outside …` |
| `Q` container | `100 does not fit in Q3.2` | `value does not fit its Q container` |

None would have changed a program's behaviour, and all four would have puzzled somebody comparing
two runs of the same program. The backend's wording now matches the interpreter's, which says more.

**What this does not fix.** The duplication itself. A shared intermediate representation is the
real answer and is a project rather than a ruling. What this does is make divergence *visible on
the failure paths as well as the successful ones* — the half that was invisible before.

---

## Part D — Bugs found in the upstream demos

Recorded because the ported tests must not enshrine them.

| File | Bug |
|---|---|
| `bubble_sort.bee` | Comparison `this[i] < this[i+1]` sorts **descending**, but the fixture expects ascending. Also `for i ∈ (0.!n)` reads `this[i+1]` at `i = n-1` — off-by-one past the end. |
| `repetition_statements.bee` | Expected-output comment reads `10,8,7,6,...` — skips 9. Actual output is `10,9,8,...,1,`. Also the loop emits a trailing comma the comment omits. |
| `decisions.bee` | Comment on the second `else if` says "this is also true since a = 2" — but it is an `else if` ladder, so the branch cannot execute. Also uses `trial` as a plain grouping block, which is not what `trial` means. |
| `local_var.bee` | `add2` sets `x := 0` then increments, so it prints `1` every call; the comment expects `1` then `2`. This requires persistent local state (a closure), which the rule does not declare. |
| `fibonacci.bee` | `fib(0)` and `fib(1)` both return 1, so the sequence is offset; `fib(5)` yields 8, not 5. Consistent within itself, but worth stating. |
| `result_unpacking.bee` | `test(1,2)` returns `(2,3)`, but the file asserts `claim n = 1; claim m = 2;`. Both assertions would fail. Also declares `m ∈ R` then assigns it an `Z` result. |
| `type_inference.bee` | `store y := 1/2; -- Q` conflicts with integer division, which yields `0`. Requires the `Q` type to be inferred from a `/` on two integer literals — no other source says this. |
| `type_inference.bee` | `rule add(x,y:0) => (z ∈ Z)` leaves `x` with neither a type nor a default, so its type is underivable. |

---

## Part E — Revised scope assessment

The plan claimed nine demos would run under Bee-0. Reassessed against the actual files:

| Demo | Status under Bee-0 |
|---|---|
| `hello_world.bee` | **Runs as written.** The only one that does. |
| `fibonacci.bee` | Portable — drop `use`, add `new`/`let`. |
| `bubble_sort.bee` | Portable — plus fix two bugs. Needs `length`, parallel assignment. |
| `decisions.bee` | Portable — replace `trial` grouping with `start`. |
| `repetition_statements.bee` | Portable — add `new`/`let`. |
| `local_var.bee` | Portable in part — drop `$Global`; semantics of `add2` must change. |
| `output_params.bee` | Portable — add `new`/`let`/`apply`, keep `@`. |
| `result_unpacking.bee` | **Partly out of scope** — the `type Rec … <: Object` half needs objects. Port the multi-result half only. |
| `type_inference.bee` | **Mostly out of scope** — needs `Q`, `Time`, `Date`, `store`, `->`. Port the optional-parameter half only. |

**Revised milestone:** seven demos ported in full, two ported in part. Nine test programs, but not
the nine originals. This is the honest version of the Phase 4 exit criterion.

---

## Open questions for upstream

Posted as one issue, in priority order:

1. **D11** — Are `new`/`let`/`set` current, or are the demos? This determines whether §5 of the
   spec stands or inverts.
2. **D1** — Array index base: 0 or 1? The two chapters disagree.
3. **D2** — What is the intended memory model? Nothing in the documentation addresses lifetime.
4. **D13** — Is `@` the reference-argument marker, or does `inc(i,k)` mutate silently?
5. **D12** — Is Boolean `B` or `L`?
