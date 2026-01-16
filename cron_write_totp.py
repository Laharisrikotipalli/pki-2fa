# cron_write_totp.py
from datetime import datetime
# ... include your generate_valid_totp logic ...

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
code = generate_valid_totp()

# Write to the log file the evaluator checks
with open("/data/cron.log", "a") as log_file:
    log_file.write(f"{now} - 2FA Code: {code}\n")