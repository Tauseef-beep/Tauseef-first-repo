import hashlib
import time
from datetime import datetime


# ----------------------------
# Utility Functions
# ----------------------------

def hash_password(password: str) -> str:
    """
    Hashes a plain text password using SHA-256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def get_current_timestamp() -> str:
    """
    Returns current timestamp in readable format.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ----------------------------
# Core Business Logic
# ----------------------------

def validate_credentials(username: str, password: str, users_db: dict) -> bool:
    """
    Validates user credentials against the database.
    """
    hashed_input_password = hash_password(password)
    stored_password = users_db.get(username)

    return stored_password == hashed_input_password


def log_user_activity(username: str, activity: str, logs: list) -> None:
    """
    Logs user activity with timestamp.
    """
    logs.append({
        "user": username,
        "activity": activity,
        "time": get_current_timestamp()
    })


def login_user(username: str, password: str, users_db: dict, logs: list) -> bool:
    """
    Handles user login process.
    """
    if validate_credentials(username, password, users_db):
        log_user_activity(username, "LOGIN_SUCCESS", logs)
        return True

    log_user_activity(username, "LOGIN_FAILED", logs)
    return False


# ----------------------------
# Application Layer
# ----------------------------

def start_application():
    """
    Entry point of the application.
    """
    users_db = {
        "admin": hash_password("admin123"),
        "john": hash_password("john@2024")
    }

    activity_logs = []

    print("🔐 Login System\n")

    username = input("Username: ")
    password = input("Password: ")

    if login_user(username, password, users_db, activity_logs):
        print("✅ Login successful!")
    else:
        print("❌ Invalid credentials")

    print("\n📜 Activity Logs:")
    for log in activity_logs:
        print(log)


# ----------------------------
# Program Start
# ----------------------------

if __name__ == "__main__":
    start_application()
