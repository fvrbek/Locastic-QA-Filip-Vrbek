# QA Test Application - Comprehensive Test Suite

Automated and manual test suite for the QA Test Web Application at https://qa-test-web-app.vercel.app/

This project contains **104 automated test cases** covering all 4 application pages, using **Python + Playwright + pytest** with the **Page Object Model** design pattern.

**Full test report** with test plan, acceptance criteria, bug reports, and testing metrics is available at [`docs/test_report.md`](docs/test_report.md).

---

## Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Application Under Test](#application-under-test)
- [Test Coverage Summary](#test-coverage-summary)
- [Bug Catalog (34 Bugs Found)](#bug-catalog-34-bugs-found)
- [Test Architecture](#test-architecture)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
- **Python** 3.10 or higher ([download](https://www.python.org/downloads/))
- **Git** ([download](https://git-scm.com/downloads))

### Setup from fresh clone

```bash
# 1. Clone the repository
git clone https://github.com/fvrbek/Locastic-QA-Filip-Vrbek.git
cd Locastic-QA-Filip-Vrbek

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS / Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright browser (Chromium)
playwright install chromium

# 5. Run all tests
python -m pytest

# 6. Open the HTML report
# The report is auto-generated at reports/report.html
```

That's it! All 104 tests will run against the live application.

**Alternative:** You can also run tests without any local setup via GitHub Actions  - go to the **Actions** tab, select **Playwright Tests**, and click **Run workflow**. The HTML report will be available as a downloadable artifact.

---

## Project Structure

```
Locastic - QA - Filip Vrbek/
├── pages/                          # Page Object Model classes
│   ├── base_page.py                # Base class with common methods
│   ├── register_page.py            # Registration page (register.html)
│   ├── login_page.py               # Login page (index.html)
│   ├── forgot_password_page.py     # Forgot Password page (forgot-password.html)
│   └── dashboard_page.py           # Dashboard page (dashboard.html)
├── tests/                          # All automated test cases
│   ├── test_registration.py        # 41 tests - registration form validation
│   ├── test_login.py               # 15 tests - login flow
│   ├── test_forgot_password.py     # 12 tests - password reset flow
│   ├── test_dashboard.py           # 12 tests - dashboard & logout
│   ├── test_responsive.py          # 10 tests - mobile/tablet CSS bugs
│   ├── test_api.py                 # 9 tests  - API endpoint testing
│   └── test_security.py            # 5 tests  - security issues
├── utils/
│   └── test_data.py                # Test data, generators, constants
├── docs/
│   └── test_report.md              # Test report (test plan, acceptance criteria, bug reports, metrics)
├── reports/                        # Auto-generated pytest-html execution reports
├── conftest.py                     # pytest fixtures (page objects, auth flows)
├── pytest.ini                      # pytest configuration
├── requirements.txt                # Python dependencies
└── .gitignore
```

---

## Running Tests

```bash
# Run all tests (generates HTML report automatically)
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test suite
python -m pytest tests/test_registration.py -v
python -m pytest tests/test_login.py -v
python -m pytest tests/test_forgot_password.py -v
python -m pytest tests/test_dashboard.py -v
python -m pytest tests/test_responsive.py -v
python -m pytest tests/test_api.py -v
python -m pytest tests/test_security.py -v

# Run a single test class
python -m pytest tests/test_registration.py::TestEmailValidation -v

# Run a single test
python -m pytest tests/test_registration.py::TestEmailValidation::test_email_input_type_should_be_email -v

# Run in headed mode (see the browser)
python -m pytest --headed

# Run with slow motion (for demos)
python -m pytest --headed --slowmo=500
```

**HTML report** is auto-generated in `reports/` after each run. A sample report is included in the repository. Open it in a browser to preview the format, then rerun tests to generate a fresh one.

---

## Application Under Test

The application has **4 pages**:

| Page | URL | Description |
|------|-----|-------------|
| **Login** | `/index.html` | Email + password login with "Remember Me" |
| **Register** | `/register.html` | 9 form fields + 2 checkboxes for new account |
| **Forgot Password** | `/forgot-password.html` | Email + security question for password reset |
| **Dashboard** | `/dashboard.html` | Authenticated area with stats, actions, activity |

---

## Test Coverage Summary

| Test Suite | File | Tests | Passed | Failed (Bugs) |
|------------|------|-------|--------|----------------|
| Registration | `test_registration.py` | 41 | 32 | 9 |
| Login | `test_login.py` | 15 | 14 | 1 |
| Forgot Password | `test_forgot_password.py` | 12 | 9 | 3 |
| Dashboard | `test_dashboard.py` | 12 | 11 | 1 |
| Responsive | `test_responsive.py` | 10 | 1 | 9 |
| API | `test_api.py` | 9 | 8 | 1 |
| Security | `test_security.py` | 5 | 2 | 3 |
| **TOTAL** | | **104** | **77** | **27** |

**All 27 failures are real application bugs**, not test code issues. An additional 10 bugs (BUG-026 through BUG-035) were found via manual testing and code review, bringing the total to **34 bugs**.

---

## Bug Catalog (34 Bugs Found)

### Critical Severity (5 bugs)

#### BUG-004: Password mismatch validation always returns true
- **Page:** Register
- **Source:** `app.js` -> `validatePasswordMatch()` -> `return true;`
- **Steps:** Enter "Password1" as password, "DifferentPassword" as confirm, submit
- **Expected:** Error "Passwords do not match"
- **Actual:** Registration succeeds with mismatched passwords
- **Test:** `test_registration.py::TestPasswordValidation::test_password_mismatch_rejected`

#### BUG-007: Terms & Conditions checkbox not enforced
- **Page:** Register
- **Source:** `app.js` -> `handleRegister()` (T&C validation is commented out)
- **Steps:** Fill all fields correctly, leave T&C unchecked, submit
- **Expected:** Error "You must accept the terms and conditions"
- **Actual:** Registration succeeds without accepting T&C
- **Test:** `test_registration.py::TestRequiredFields::test_terms_checkbox_required`

#### BUG-012: Forgot password shows fake success for any email
- **Page:** Forgot Password
- **Source:** `app.js` -> `handleForgotPassword()` (no email existence check)
- **Steps:** Enter "nonexistent@fake.xyz", click Send Reset Link
- **Expected:** Error "Email not found"
- **Actual:** Shows "Password reset link has been sent to your email!"
- **Test:** `test_forgot_password.py::test_reset_with_nonexistent_email_still_succeeds`

#### BUG-013: Security answer is never validated
- **Page:** Forgot Password
- **Source:** `app.js` -> `handleForgotPassword()` (security answer completely ignored)
- **Steps:** Select security question, enter any wrong answer, submit
- **Expected:** Validation of answer against stored data
- **Actual:** Shows success regardless of answer
- **Test:** `test_forgot_password.py::test_security_answer_not_validated`

#### BUG-008: Error messages hidden on mobile devices
- **Page:** All forms
- **Source:** `styles.css` -> `@media (max-width: 767px) { .error-message { display: none !important; } }`
- **Steps:** Open any form on mobile viewport, submit with invalid data
- **Expected:** Validation errors visible
- **Actual:** Error messages completely invisible on mobile
- **Test:** `test_responsive.py::test_error_messages_visible_on_mobile`

### High Severity (6 bugs)

#### BUG-001: Weak email validation regex
- **Page:** All forms (register, login, forgot-password)
- **Source:** `app.js` -> `validateEmail()` uses regex `/\S+@\S/`
- **Accepts invalid:** `user@.com`, `user@@example.com`, `user space@example.com`
- **Should use:** RFC 5322 compliant email regex
- **Tests:** `test_registration.py::TestEmailValidation::test_invalid_email_rejected`

#### BUG-003: Password minimum length is 4 characters (should be 8)
- **Page:** Register
- **Source:** `app.js` -> `validatePassword()` checks `password.length >= 4`
- **Steps:** Register with password "1234"
- **Expected:** Rejected (min 8 chars)
- **Actual:** Accepted
- **Test:** `test_registration.py::TestPasswordValidation::test_weak_password_rejected[1234]`

#### BUG-018: Sensitive data logged to browser console
- **Page:** All pages
- **Source:** `app.js` -> multiple `console.log()` statements
- **Logged data:** User emails, session data, authentication status
- **Examples:** `"Attempting login for: user@email.com"`, `"User stored in sessionStorage: email"`
- **Tests:** `test_security.py::test_login_logs_email_to_console`, `test_security.py::test_registration_logs_email_to_console`

#### BUG-019: No CSRF protection on API endpoints
- **Page:** API (`/api/register`, `/api/login`)
- **Source:** `app.js` -> all `fetch()` calls lack CSRF tokens
- **Impact:** Vulnerable to Cross-Site Request Forgery attacks
- **Test:** `test_api.py::test_no_csrf_token_required`

#### BUG-020: Session stored in sessionStorage (not httpOnly cookies)
- **Page:** Login / Dashboard
- **Source:** `app.js` -> `sessionStorage.setItem('currentUser', JSON.stringify(data.user))`
- **Impact:** Session accessible via JavaScript, vulnerable to XSS session theft
- **Test:** `test_security.py::test_session_uses_httponly_cookies`

#### BUG-002: Email input type is "text" on all forms
- **Page:** Register, Login, Forgot Password
- **Source:** HTML `<input type="text">` instead of `<input type="email">`
- **Impact:** No built-in browser email validation (autocomplete, keyboard, format check)
- **Tests:** `test_registration.py::test_email_input_type_should_be_email`, `test_login.py::test_login_email_input_type`, `test_forgot_password.py::test_email_input_type`

### Medium Severity (9 bugs)

#### BUG-005: Phone number accepts alphabetical characters
- **Page:** Register
- **Source:** `app.js` -> `validatePhone()` only checks `phone.length > 0`
- **Accepts:** "abc", "phone number", "12-34" (any non-empty string)
- **Tests:** `test_registration.py::TestPhoneValidation` (3 parametrized tests)

#### BUG-006: ZIP code accepts alphabetical characters
- **Page:** Register
- **Source:** `app.js` -> `validateZipCode()` only checks `zip.length >= 3`
- **Accepts:** "abc", "ABCDE" (any 3+ char string)
- **Tests:** `test_registration.py::TestZipCodeValidation` (2 tests)

#### BUG-009: Submit button reduced height on mobile
- **Page:** All forms (mobile viewport)
- **Source:** `styles.css` -> `.btn-primary { max-height: 35px; margin-bottom: -25px; }`
- **Impact:** Button height is reduced on mobile (~35px vs ~44px on desktop); still visible and functional but inconsistent across viewports
- **Test:** `test_responsive.py::test_submit_button_fully_visible_on_mobile`

#### BUG-023: Download Report button overlay on mobile (Dashboard)
- **Page:** Dashboard (mobile <767px)
- **Source:** CSS class `mobile-hidden-action` activates `button-overlay`
- **Steps:** Log in, access dashboard on mobile viewport, check Quick Actions section
- **Expected:** Download Report button fully accessible
- **Actual:** Button covered by overlay on mobile
- **Test:** `test_responsive.py::TestMobileDashboard::test_download_report_button_not_overlaid_on_mobile`

#### BUG-016: Incomplete session cleanup on logout
- **Page:** Dashboard
- **Source:** `app.js` -> `handleLogout()` only clears `sessionStorage`, not `localStorage`
- **Impact:** User data persists in localStorage after logout
- **Test:** `test_dashboard.py::test_logout_incomplete_session_cleanup`

#### BUG-027: Remember Me checkbox is non-functional
- **Page:** Login
- **Source:** `app.js` -> `handleLogin()` never reads the Remember Me checkbox value
- **Impact:** Session always uses `sessionStorage` (cleared on tab close). Checking "Remember Me" has zero effect  - should use `localStorage` when checked for persistent sessions
- **Test:** Manual observation (not automated)

#### BUG-028: No login attempt rate limiting
- **Page:** Login, API
- **Source:** `/api/login` endpoint
- **Impact:** Unlimited failed login attempts accepted  - no delay, lockout, or CAPTCHA. Enables brute-force password attacks
- **Test:** Manual observation (not automated)

#### BUG-029: Forgot password ignores selected security question
- **Page:** Forgot Password
- **Source:** `app.js` -> `handleForgotPassword()` reads `securityAnswer` but never reads the selected question
- **Impact:** The security question dropdown selection is completely ignored. Related to BUG-013 (answer not validated)
- **Test:** Manual observation (code inspection)

#### BUG-030: Password transmitted as plaintext in API body
- **Page:** Registration, Login
- **Source:** `app.js` -> `handleLogin()`, `handleRegister()` send password as plain JSON text
- **Impact:** Password visible in browser DevTools Network tab and potentially in server logs
- **Test:** Manual observation (DevTools Network tab)

**Note:** BUG-001 (weak email regex) also affects Login and Forgot Password pages with the same validation issue.
See High severity BUG-001 above for full details.

### Low Severity (14 bugs)

#### BUG-010: Street address field overlay on tablet
- **Page:** Register (tablet 768-1024px)
- **Source:** CSS class `tablet-hidden` activates `overlay-image-tablet`
- **Test:** `test_responsive.py::test_address_field_not_overlaid_on_tablet`

#### BUG-011: Newsletter checkbox overlay on mobile
- **Page:** Register (mobile <767px)
- **Source:** CSS class `mobile-hidden-checkbox` activates `overlay-image-small`
- **Test:** `test_responsive.py::test_newsletter_checkbox_not_overlaid_on_mobile`

#### BUG-015: Security question overlay on mobile
- **Page:** Forgot Password (mobile <767px)
- **Source:** CSS class `mobile-hidden-section` activates `overlay-image-security`
- **Test:** `test_responsive.py::test_security_section_not_overlaid_on_mobile`

#### BUG-025: Remember Me checkbox overlay on mobile
- **Page:** Login (mobile <767px)
- **Source:** CSS class `mobile-hidden` activates `overlay-image`
- **Test:** `test_responsive.py::test_remember_me_not_overlaid_on_mobile`

#### BUG-017: No logout confirmation dialog
- **Page:** Dashboard
- **Source:** `app.js` -> `handleLogout()` immediately redirects without confirmation
- **Test:** `test_dashboard.py::test_no_logout_confirmation`

#### BUG-021: Rewards card overlay on tablet (Dashboard)
- **Page:** Dashboard (tablet 768-1024px)
- **Source:** CSS class `mobile-hidden-card` activates `overlay-image-rewards`
- **Test:** `test_responsive.py::TestTabletDashboard::test_rewards_card_not_overlaid_on_tablet`

#### BUG-022: Activity item overlay on tablet (Dashboard)
- **Page:** Dashboard (tablet 768-1024px)
- **Source:** CSS class `tablet-hidden-activity` activates `overlay-image-activity`
- **Test:** `test_responsive.py::TestTabletDashboard::test_activity_item_not_overlaid_on_tablet`

#### BUG-024: Dashboard stat card overlay on tablet
- **Page:** Dashboard (tablet 768-1024px)
- **Source:** CSS class `tablet-hidden-card` activates `overlay-image-dashboard`
- **Steps:** Log in, access dashboard on tablet viewport, check stat cards
- **Expected:** All stat cards fully visible
- **Actual:** Stat card covered by overlay on tablet
- **Test:** `test_responsive.py::TestTabletDashboard::test_dashboard_card_not_overlaid_on_tablet`

#### BUG-026: Required fields lack visual asterisk indicators
- **Page:** Registration (all required fields)
- **Source:** HTML labels for required fields (First Name, Last Name, Email, Phone, Address, City, ZIP, Password, Confirm Password) have no `*` indicator
- **Steps:** Open registration form, inspect field labels
- **Expected:** Required fields have visual `*` next to their label (standard UX convention)
- **Actual:** No asterisks shown  - users cannot tell which fields are mandatory until form submission fails
- **Test:** Manual observation (not automated)

#### BUG-031: No password visibility toggle
- **Page:** Registration, Login
- **Source:** Password input fields in HTML
- **Impact:** No "show/hide password" toggle exists. Users cannot verify typed password, increasing entry errors
- **Test:** Manual observation (not automated)

#### BUG-032: Missing autocomplete attributes on form fields
- **Page:** Registration, Login, Forgot Password
- **Source:** All form input elements
- **Impact:** Missing `autocomplete="email"`, `autocomplete="new-password"`, etc. Password managers and browsers cannot auto-fill reliably
- **Test:** Manual observation (DevTools inspection)

#### BUG-033: Error messages not linked to inputs via aria-describedby
- **Page:** Registration, Login, Forgot Password
- **Source:** Error message elements (e.g., `#emailError`) not associated with inputs
- **Impact:** Screen readers cannot announce validation errors when users focus on a field. Fails WCAG 2.1 SC 1.3.1
- **Test:** Manual observation (DevTools inspection)

#### BUG-034: No skip-to-content navigation link
- **Page:** All 4 pages
- **Source:** All page HTML files
- **Impact:** Keyboard and screen reader users must tab through all elements before reaching content. Fails WCAG 2.1 SC 2.4.1
- **Test:** Manual observation (keyboard navigation)

#### BUG-035: Dashboard action buttons are non-functional
- **Page:** Dashboard
- **Source:** `dashboard.html`, `app.js`
- **Impact:** "Update Profile", "Settings", "Contact Support", "Download Report" buttons only show toast messages  - no actual navigation or functionality
- **Test:** Manual observation (not automated)

---

## Test Architecture

### Page Object Model (POM)
Each page has a dedicated class in `pages/` encapsulating:
- **Locators** - CSS selectors for all interactive elements
- **Actions** - Methods to interact (fill, click, submit)
- **Getters** - Methods to read page state (error messages, attributes)

### Fixtures (`conftest.py`)
| Fixture | Description |
|---------|-------------|
| `register_page` | Opens registration page, returns RegisterPage POM |
| `login_page` | Opens login page, returns LoginPage POM |
| `forgot_password_page` | Opens forgot password page, returns ForgotPasswordPage POM |
| `dashboard_page` | Returns DashboardPage POM (unauthenticated) |
| `registered_user` | Registers a new user via UI, returns credentials dict |
| `authenticated_page` | Register + login, returns (DashboardPage, user_data) |

### Test Data (`utils/test_data.py`)
- `random_email()` - Unique email per test for isolation
- Parametrized invalid data sets for emails, phones, ZIPs, passwords
- Security payloads: SQL injection, XSS
- Viewport sizes: mobile (375x667), tablet (768x1024)
- API endpoint URLs

---

## VS Code Integration

For the best development experience, install the **Playwright Test for VS Code** extension:

```bash
code --install-extension ms-playwright.playwright
```

### Features:
- **Test Explorer** - See all tests in the sidebar, click to run individual tests
- **Run/Debug** - Run tests with breakpoints directly from the editor
- **Pick Locator** - Click elements in the browser to get CSS selectors
- **Record Tests** - Record new test actions by interacting with the app
- **Show Browser** - Toggle headed mode to see tests running

### How to use:
1. Open the project in VS Code
2. Open the Testing sidebar (flask icon)
3. Click the play button next to any test to run it
4. Click the debug button to debug with breakpoints
5. Use "Record new" to create tests by clicking through the app

---

## CI/CD (GitHub Actions)

A GitHub Actions workflow is included at `.github/workflows/tests.yml`:

- **Triggers:** On push/PR to main/master, or manually via **Actions > Playwright Tests > Run workflow**
- **Runs:** Full test suite on Ubuntu with Python 3.12
- **Reports:** Uploads HTML report as artifact (download from Actions tab)

The pipeline runs automatically when you push to GitHub.

---

## Test Execution Output

Running `pytest -v` produces output like this:

```
tests/test_api.py::TestRegisterAPI::test_register_valid_data              PASSED
tests/test_api.py::TestLoginAPI::test_no_csrf_token_required              FAILED
tests/test_dashboard.py::TestDashboardLogout::test_incomplete_cleanup     FAILED
tests/test_forgot_password.py::test_nonexistent_email_still_succeeds      FAILED
tests/test_login.py::TestLoginEmailValidation::test_email_input_type      FAILED
tests/test_registration.py (41 tests)                        32 PASSED, 9 FAILED
tests/test_responsive.py (10 tests)                           1 PASSED, 9 FAILED
tests/test_security.py (5 tests)                              2 PASSED, 3 FAILED

========================= 77 passed, 27 failed in 214s =========================
```

All 27 failures are application bugs, documented in the [Bug Catalog](#bug-catalog-34-bugs-found) above.

The **HTML report** is generated at `reports/report.html` - open in any browser for interactive pass/fail breakdown with stack traces.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Playwright install fails | `playwright install --with-deps chromium` |
| Tests timeout | Server may be slow: `pytest --timeout=60` |
| Python version error | Requires 3.10+: `python --version` |
| Import errors | Ensure you're in project root: `cd "Locastic - QA - Filip Vrbek"` |
| HTML report missing | Check `reports/report.html` after test run |
| VS Code extension not working | Reload VS Code window after installing |
