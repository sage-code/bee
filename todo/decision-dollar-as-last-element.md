# Decision: Use $ to represent the last element in collections

The symbol `$` will be used to represent the last element in arrays and lists. This follows the convention in regular expressions where `$` denotes the end.

## Proposed Usage
- `[$]` refers to the last element of a collection.
- `[$-1]` refers to the element preceding the last.

## Conflict Resolution
- While `$` is currently used for system constants, ambiguity can be avoided by ensuring it is not used in identifiers (e.g., $A or $1 are forbidden as identifiers, so `$` in the context of an index will always represent the last element).

## Affected Files
- `spec/syntax.md` (Update operator table)
- `spec/collections.md` (Add documentation for index operators)
