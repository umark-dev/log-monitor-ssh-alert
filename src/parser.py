import re
from typing import List, Dict

FAILED_LOGIN_PATTERN = re.compile(
    r"Failed password for (invalid user )?(\S+) from ([\d\.]+) port \d+ ssh2"
)

def parse_failed_logins(log_content: str) -> List[Dict[str, str]]:
    matches = FAILED_LOGIN_PATTERN.findall(log_content)
    failed_attempts = []
    for match in matches:
        failed_attempts.append({
            "username": match[1],
            "ip": match[2]
        })
    return failed_attempts

def parse_failed_logins_from_file(file_path: str) -> List[Dict[str, str]]:
    failed_attempts = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[-1000:]
        content = "".join(lines)
        failed_attempts = parse_failed_logins(content)
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {file_path}")
    except PermissionError:
        print(f"[ERROR] Permission denied: {file_path}")
    except Exception as e:
        print(f"[ERROR] Failed to parse logs: {e}")
    return failed_attempts

def parse_multiple_logs(file_paths: List[str]) -> List[Dict[str, str]]:
    combined_attempts = []
    for path in file_paths:
        combined_attempts.extend(parse_failed_logins_from_file(path))
    return combined_attempts
