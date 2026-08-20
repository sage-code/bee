# Bee Operators

This document enumerates the operators available in the Bee language, categorized by their functionality.

## Delimiters
| Symbol | Description |
| :--- | :--- |
| `+-...-+` | Multi-line boxed comments |
| `#(....)` | String interpolation (placeholder) for operator "?" |
| `(_,_,_)` | Expression | List literal |
| `[_,_,_]` | Index | Array literals | Parameterize types |
| `{_,_,_}` | Enumeration type | Set of values | Hash map |

## Strings
| Symbol | Description |
| :--- | :--- |
| `x` | Back quoted string: regular expression. |
| `'x'` | Single quoted string literal or ASCII code point |
| `"y"` | Double quoted string literal or UTF32 code point |

## Single Symbols
| Symbol | Description |
| :--- | :--- |
| `!` | Negation symbol for relations | Excluded from domain |
| `?` | Template modifier. Associated with string templates |
| `*` | String replication | Varargs prefix | Spread operator | Many something |
| `@` | Domain name | Example @sagecode.net |
| `$` | System constant | Environment variables |
| `&` | String concatenation | number concatenation |
| `#` | Title | String interpolation |
| `∈` | Define variable/constant/result/parameter type |
| `_` | Anonymous variable | Constant value = one space (_ = ' ') |
| `+` | Maximum upper limit for a domain | Unicode notation U+ |
| `-` | Minimum lower limit in a domain | Unicode notation U- |
| `:` | Start a block or define something |
| `:` | Pair-up key-value in: objects, rule parameters, rule arguments, hash-map pairs |
| `;` | End of statement | Statement separator |
| `.` | Decimals for real numbers | Path string concatenation |
| `.` | Membership dot notation | Prefix for public member/attribute |
| `,` | Enumeration of elements | expressions |
| `\|` | Declarative collection builder: set := { x*2 \| x ∈ (0..3)} |
| `\` | Escape character (\n := New Line), (\" = Double Quotes) |

## Numeric Operators
| Symbol | Description |
| :--- | :--- |
| `-` | Change sign, replace "y = -x" with "y = -1*x" |
| `/` | Rational number division |
| `^` | Power symbol used with fractions or expressions |
| `√` | Radical: x√n is equivalent to x^(1/n) |
| `*` | Multiplication alternative |
| `\` | Rational number division |
| `/` | Real number division |
| `×` | Array multiplication | Matrix multiplication |
| `%` | Modulo operator 5 % 2 = 2 |
| `+` | Numeric addition | List append | Matrix addition |
| `-` | Numeric subtraction | Collection difference |
| `±` | Numeric tolerance (use with ≈) |

## Double Symbols
| Symbol | Description |
| :--- | :--- |
| `--` | End of line comments (not in expression) |
| `##` | Single line subtitle comments (no indentation) |
| `**` | Single line comments (allow indentation) |
| `..` | Define range/domain/slice (n..m) | [n..m] |
| `.!` | Define range/domain with excluded limit (n.!m) | [n.!m] |
| `!.` | Define range/domain with excluded limit (n!.m) | [n.!m] |
| `!!` | Define range/domain with excluded limits: (n!!m) | [n.!m] |
| `-.` | Minus infinite domain: instead of [-∞..0] write: [-..0] |
| `.+` | Plus infinite domain: instead of [0..+∞] write: [0..+] |
| `=>` | Define: rule expression | rule result |
| `<-` | Define and generate values in a loop from range or set |
| `<:` | Define subset from set | Specify super-type for a new type |
| `:>` | Data cast pipeline operator / Type conversion |
| `<<` | Shift values of collection to right by removing first elements |
| `>>` | Shift values of collection to left by removing first elements |
| `::` | Deep copy | Clone operator |
| `++` | Extend an array with one or more elements |
| `-=` | Find and delete one element, from a collection |
| `+>` | Append element to beginning of a list |
| `<+` | Append element to end of a list |
| `~=` | Relation operator: regular expression match |
| `>=` | Relation operator: greater then or equal to |
| `<=` | Relation operator: less then or equal to |

## Modifiers
| Symbol | Meaning |
| :--- | :--- |
| `:=` | Modify | (value | reference) |
| `+=` | Increment value |
| `-=` | Decrement value |
| `*=` | Multiplication modifier |
| `/=` | Real division modifier |
| `^=` | Power modifier |
| `√=` | Radical modifier |
| `%=` | Modulo modifier |

## Relation Operators
| Symbol | Meaning |
| :--- | :--- |
| `∈` | check if element belong to collection |
| `=` | equal { compare values or attributes} |
| `≠` | different { compare values or attributes} |
| `≡` | equivalent | { compare values / convert type } |
| `≈` | approximating equal numbers, used with ± like: (x ≈ 4 ± 0.25) |
| `>` | value is greater than: (2 > 1) |
| `<` | value is less than: (1 < 2) |
| `≥` | greater than or equal to |
| `≤` | less than or equal to |

## Collection Operators
| Symbol | Result | Meaning |
| :--- | :--- | :--- |
| `∩` | Set | Intersection between two collections |
| `∪` | Set | Union between two collections |
| `⊂` | Logic | Set is included in superset: "⊂" |
| `⊃` | Logic | Set contain subset: "⊃" |
| `Δ` | Set | Set symmetric difference |
| `$` | Index | Last element of a collection |
| `+` | String | Concatenation between two strings |
| `+` | List | Concatenation between two lists |
| `+` | Array | Concatenation between two arrays |
| `∀` | Element | All: used in collection qualification |
| `∃` | Logic | One: used in collection qualification |

## Logic Operators
| Symbol | Meaning | Notes |
| :--- | :--- | :--- |
| `¬` | NOT | unary operator |
| `∧` | AND | shortcut operator |
| `∨` | OR | shortcut operator |
| `⊕` | XOR | exclusive OR |
| `↓` | NOR | p ↓ q = ¬ (p ∨ q) |
| `↑` | NAND | p ↑ q = ¬ (p ∧ q) |

## Bitwise Operators
| Symbol | Meaning | Notes |
| :--- | :--- | :--- |
| `«` | bit SHIFTL | shift bits to left |
| `»` | bit SHIFTR | shift bits to right |
| `~` | bit NOT | negate all bits |
| `&` | bit AND | execute AND between each bits |
| `|` | bit OR | execute OR between each bits |
| `⊕` | bit XOR | execute XOR between each bits |

## String Operators
| Symbol | Description |
| :--- | :--- |
| `*` | string pattern repetition (right operator must be numeric) |
| `/` | concatenate url or path using / not depending on OS |
| `+` | concatenate two strings as they are preserving trial spaces. |
| `-` | concatenate two strings and trim spaces to a single space. |
| `.` | concatenate strings with "/" on Linux or "\" on Windows. |
| `?` | string format operator, replace "#" with number. |
