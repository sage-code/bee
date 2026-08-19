# Task: D3 Slice invalidation on resize

Document that `++` allocates a new buffer and rebinds the variable. Slices keep pointing to the old buffer (stale data).

Affected Files: `spec/collections.md`.
