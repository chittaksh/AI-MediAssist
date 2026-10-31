import logging
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "data" / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 1. Configure the logging system
logging.basicConfig(
    filename=LOG_DIR / f"app-{date.today().strftime('%Y-%m-%d')}.log",          # Saves logs to a file named 'app.log'
    filemode="a",                # 'a' appends to the file, 'w' overwrites it each run
    level=logging.DEBUG,         # Sets the lowest threshold level to capture
    format="{asctime} - {levelname} - {message}",  # Output format layout
    style="{"                    # Enables modern curly-brace string formatting
)