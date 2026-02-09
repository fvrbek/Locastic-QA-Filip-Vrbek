"""Test data for the QA Test Application test suite.

Contains valid/invalid data sets for parametrized tests across all pages:
registration, login, forgot password, and security testing.
"""

import random
import string


def random_email() -> str:
    """Generate a unique random email for test isolation."""
    rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"testuser_{rand}@example.com"


# ──────────────────────────────────────────────
# VALID DATA
# ──────────────────────────────────────────────

VALID_USER = {
    "first_name": "John",
    "last_name": "Doe",
    "email": random_email(),
    "phone": "+385911234567",
    "address": "123 Main Street",
    "city": "Split",
    "zip_code": "21000",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
}

# ──────────────────────────────────────────────
# INVALID EMAIL FORMATS
# Used by: registration, login, forgot-password tests
# The app uses weak regex /\S+@\S/ which accepts many invalid formats
# ──────────────────────────────────────────────

INVALID_EMAILS = [
    "",
    "plaintext",
    "@nodomain.com",
    "user@",
    "user@.com",
    "user space@example.com",
    "user@@example.com",
]

# ──────────────────────────────────────────────
# INVALID PHONE NUMBERS
# BUG: App only checks phone.length > 0, accepts letters
# ──────────────────────────────────────────────

INVALID_PHONES = [
    "",
    "abc",
    "12-34",
    "phone number",
]

# ──────────────────────────────────────────────
# INVALID ZIP CODES
# BUG: App only checks zip.length >= 3, accepts letters
# ──────────────────────────────────────────────

INVALID_ZIPS = [
    "",
    "ab",
    "abc",
    "!!",
]

# ──────────────────────────────────────────────
# WEAK PASSWORDS
# BUG: App accepts passwords >= 4 chars (should be >= 8)
# ──────────────────────────────────────────────

WEAK_PASSWORDS = [
    "",
    "a",
    "ab",
    "abc",
    "1234",
]

# ──────────────────────────────────────────────
# SECURITY PAYLOADS
# ──────────────────────────────────────────────

SQL_INJECTION = "' OR '1'='1'; DROP TABLE users; --"
XSS_PAYLOAD = "<script>alert('XSS')</script>"
LONG_STRING = "a" * 256

# ──────────────────────────────────────────────
# FORGOT PASSWORD DATA
# ──────────────────────────────────────────────

SECURITY_QUESTIONS = [
    ("pet", "What was your first pet's name?"),
    ("city", "What city were you born in?"),
    ("school", "What was your high school name?"),
]

# ──────────────────────────────────────────────
# VIEWPORT SIZES FOR RESPONSIVE TESTING
# ──────────────────────────────────────────────

MOBILE_VIEWPORT = {"width": 375, "height": 667}
TABLET_VIEWPORT = {"width": 768, "height": 1024}
DESKTOP_VIEWPORT = {"width": 1280, "height": 800}

# ──────────────────────────────────────────────
# API ENDPOINTS
# ──────────────────────────────────────────────

API_BASE = "https://qa-test-web-app.vercel.app/api"
API_REGISTER = f"{API_BASE}/register"
API_LOGIN = f"{API_BASE}/login"
