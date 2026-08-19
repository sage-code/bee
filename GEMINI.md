# Execution Constraints
- Process all batch tasks, file conversions, and automated transformations strictly **one file at a time**.
- Insert a mandatory pause or sleep interval of **at least 5 seconds** between sequential API calls or file write operations to respect free-tier rate limits.
- Never execute parallel or rapid-fire requests.

If you create a Python script that call Gemini API use time.sleep(5) in Python or sleep 5 in Bash to slow down execution.
