## Execution & Resource Constraints (Free Tier Optimization)

### Rate Limiting & Pacing
- **Sequential Processing:** Execute all batch tasks, file conversions, and API calls strictly **one file at a time**. Never run parallel or rapid-fire requests.
- **Throughput Caps:** Enforce a maximum of **225K TPM** (tokens per minute) and **15 RPM** (requests per minute).
- **Daily Quota Warning:** Halt operations and issue an alert immediately when Requests Per Day (RPD) reaches **450** (buffer before the 500 limit).

### Delay & Sleep Protocol
- **Base Interval:** Insert a mandatory **15-second** pause (`time.sleep(15)` in Python or `sleep 15` in Bash) between sequential API calls or write operations.
- **File-Size Scaling:** For file-processing calls, scale the sleep duration proportionally with file size, capping the pause at **120 seconds (2 minutes)**.

### State Management & Cleanup
- **Obsolete Content Purge:** Delete temporary files, intermediate cache artifacts, and redundant outputs immediately after each task step completes.
- **State Pruning:** Clear conversation history, context windows, and variable caches between batch items to minimize token overhead and prevent context bloat.
- **Error Recovery:** On hitting rate-limit errors (HTTP 429), implement exponential backoff starting at a 60-second delay before retrying.
### Scope & Precision Directives

- **Strict Single-File Boundary:** When instructed to modify a single file, restrict all read, write, and analysis operations exclusively to that named file. 
- **Prohibition of Unsolicited Changes:** Do not refactor, reformat, or alter adjacent files, imports, configurations, or directory structures unless explicitly commanded.
- **Explicit Confirmation:** If a task requires touching secondary dependencies or related files, halt execution and request explicit user authorization before proceeding.
- **Zero Scope Creep:** Confine execution strictly to the literal parameters of the prompt. No proactive optimizations, cleanups, or structural suggestions outside the requested change.
