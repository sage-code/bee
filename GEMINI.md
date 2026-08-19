# Execution Constraints
- Process all batch tasks, file conversions, and automated transformations strictly **one file at a time**.
- Insert a mandatory pause or sleep interval of 45 seconds or more between sequential API calls or file write operations to respect free-tier rate limits. 
- Never execute parallel or rapid-fire requests.

If you create a Python script that call Gemini API use time.sleep(10) in Python or sleep 10 in Bash to slow down execution for each API call. If the call process a file increase the sleep time proportional with file size up to 2 minutes.
