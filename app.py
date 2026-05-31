"""
MiniShop — E-commerce product search with SQL Injection protection.

A simple online store where the search module is protected by a WAF
and parameterised queries (Secure Mode) or intentionally vulnerable
(String concatenation in Vulnerable Mode for demonstration).
"""

from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, g,
)
from database import get_db, init_db, log_security_event
from security.auth import create_user, authenticate_user
from security.waf import analyze_input
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue shopping.", "warning")
            return redirect(url_for("login"))
        g.user = {
            "user_id": session["user_id"],
            "username": session.get("username"),
            "role": session.get("role"),
        }
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if g.user["role"] != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("shop"))
        return f(*args, **kwargs)
    return wrapper


def _client_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr)


def _search_products(query, category, secure_mode):
    """Run product search — secure (parameterised) or vulnerable (concat)."""
    products = []
    error = None
    vulnerable_query = ""
    safe_query = ""
    waf_result = analyze_input(query) if query else None

    db = get_db()
    if query:
        if secure_mode:
            sql = "SELECT * FROM products WHERE name LIKE ? OR description LIKE ?"
            params = [f"%{query}%", f"%{query}%"]
            if category:
                sql += " AND category = ?"
                params.append(category)
            safe_query = f"{sql}  |  params = {params}"
            try:
                products = [dict(r) for r in db.execute(sql, params).fetchall()]
            except Exception as exc:
                error = str(exc)
        else:
            sql = f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
            if category:
                sql += f" AND category = '{category}'"
            vulnerable_query = sql
            log_security_event(
                "VULNERABLE_QUERY", "warning",
                "Vulnerable query executed (secure mode OFF)",
                source_ip=_client_ip(),
                username=session.get("username"),
                payload=sql,
            )
            try:
                products = [dict(r) for r in db.execute(sql).fetchall()]
            except Exception as exc:
                error = str(exc)
    else:
        sql = "SELECT * FROM products"
        params = []
        if category:
            sql += " WHERE category = ?"
            params.append(category)
        sql += " ORDER BY name"
        products = [dict(r) for r in db.execute(sql, params).fetchall()]

    db.close()

    waf_details = None
    if waf_result:
        waf_details = {
            "is_malicious": waf_result.is_malicious,
            "severity": waf_result.severity,
            "attack_type": waf_result.attack_type,
            "details": waf_result.details,
        }

    return products, error, vulnerable_query, safe_query, waf_details


@app.before_request
def before_request_hook():
    exempt = ("/login", "/logout", "/register", "/static")
    if any(request.path.startswith(p) for p in exempt):
        return None

    if session.get("secure_mode", True) and request.method in ("GET", "POST"):
        for value in list(request.args.values()) + list(request.form.values()):
            result = analyze_input(str(value))
            if result.is_malicious:
                log_security_event(
                    result.attack_type, result.severity,
                    f"WAF blocked malicious input: {result.matched_pattern}",
                    source_ip=_client_ip(),
                    username=session.get("username"),
                    payload=str(value),
                    blocked=True,
                )
                return render_template(
                    "blocked.html",
                    attack_type=result.attack_type,
                    severity=result.severity,
                    details=result.details,
                ), 403


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("shop"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        result = authenticate_user(username, password, _client_ip())
        if result["success"]:
            session["user_id"] = result["user_id"]
            session["username"] = result["username"]
            session["role"] = result["role"]
            session.setdefault("secure_mode", True)
            flash(f"Welcome to MiniShop, {result['username']}!", "success")
            return redirect(url_for("shop"))
        flash(result["message"], "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        errors = []
        if len(username) < 3:
            errors.append("Username must be at least 3 characters.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("register.html")

        result = create_user(username, password)
        if result["success"]:
            flash("Account created! You can now log in.", "success")
            return redirect(url_for("login"))
        flash(result["message"], "danger")
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("See you next time!", "info")
    return redirect(url_for("login"))


@app.route("/shop")
@login_required
def shop():
    query = request.args.get("q", "")
    category = request.args.get("category", "")
    secure_mode = session.get("secure_mode", True)

    products, error, vulnerable_query, safe_query, waf_details = _search_products(
        query, category, secure_mode,
    )

    return render_template(
        "shop.html",
        query=query,
        category=category,
        products=products,
        error=error,
        secure_mode=secure_mode,
        vulnerable_query=vulnerable_query,
        safe_query=safe_query,
        waf_result=waf_details,
    )


@app.route("/admin/security")
@admin_required
def admin_security():
    db = get_db()
    recent_events = [dict(r) for r in db.execute(
        "SELECT * FROM security_logs ORDER BY timestamp DESC LIMIT 10"
    ).fetchall()]
    blocked_count = db.execute(
        "SELECT COUNT(*) FROM security_logs WHERE blocked = 1"
    ).fetchone()[0]
    db.close()

    return render_template(
        "admin_security.html",
        recent_events=recent_events,
        blocked_count=blocked_count,
        secure_mode=session.get("secure_mode", True),
    )


@app.route("/toggle-mode", methods=["POST"])
@admin_required
def toggle_mode():
    session["secure_mode"] = not session.get("secure_mode", True)
    mode = "Secure" if session["secure_mode"] else "Vulnerable"
    log_security_event(
        "MODE_CHANGE", "info",
        f"Mode changed to {mode} by {session.get('username')}",
        source_ip=_client_ip(),
        username=session.get("username"),
    )
    flash(f"Search module switched to {mode} Mode", "info")
    return redirect(request.referrer or url_for("admin_security"))


@app.route("/admin/logs")
@admin_required
def security_logs():
    db = get_db()
    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    total = db.execute("SELECT COUNT(*) FROM security_logs").fetchone()[0]
    logs = [dict(r) for r in db.execute(
        "SELECT * FROM security_logs ORDER BY timestamp DESC LIMIT ? OFFSET ?",
        [per_page, offset],
    ).fetchall()]
    db.close()

    return render_template(
        "security_logs.html",
        logs=logs, page=page, per_page=per_page, total=total,
        total_pages=(total + per_page - 1) // per_page,
    )


@app.errorhandler(404)
def not_found(_):
    return render_template("error.html", code=404, message="Page not found"), 404


@app.errorhandler(500)
def server_error(_):
    return render_template("error.html", code=500, message="Internal server error"), 500


if __name__ == "__main__":
    init_db()
    create_user("admin", "Admin123!", role="admin")
    print("\n  MiniShop — admin / Admin123!")
    print("  Open http://127.0.0.1:5000 in your browser.\n")
    app.run(debug=True, host="127.0.0.1", port=5000)
