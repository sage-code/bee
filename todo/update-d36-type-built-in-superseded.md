# Task: D36 `type` is both keyword and built-in (Superseded)

Document that the collision between `type` as a keyword and `type()` as a built-in has been resolved by D87, which renamed the built-in to `kind`. The old `type()` is now deprecated and issues a diagnostic.

Affected Files: `spec/types.md`, `spec/syntax.md`
