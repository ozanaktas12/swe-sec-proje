"""
Authentication module — bcrypt password hashing and login.
"""

import bcrypt
from database import get_db, log_security_event


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_user(username: str, password: str, role: str = "user") -> dict:
    db = get_db()
    try:
        pw_hash = hash_password(password)
        db.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, pw_hash, role),
        )
        db.commit()
        return {"success": True, "message": "User created successfully"}
    except Exception as e:
        if "UNIQUE" in str(e):
            return {"success": False, "message": "Username already exists"}
        return {"success": False, "message": str(e)}
    finally:
        db.close()


def authenticate_user(username: str, password: str, ip_address: str = None) -> dict:
    db = get_db()
    try:
        row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if not row or not verify_password(password, row["password_hash"]):
            log_security_event(
                "AUTH_FAILURE", "medium",
                f"Failed login attempt for user: {username}",
                source_ip=ip_address, username=username,
            )
            return {"success": False, "message": "Invalid username or password"}

        log_security_event(
            "AUTH_SUCCESS", "info",
            f"Successful login for user: {username}",
            source_ip=ip_address, username=username,
        )
        return {
            "success": True,
            "user_id": row["id"],
            "username": row["username"],
            "role": row["role"],
        }
    finally:
        db.close()
