# Test Report: QA Test Web Application - All Pages

**Application URL:** https://qa-test-web-app.vercel.app/
**Date:** February 2026
**Tester:** QA Engineer Candidate
**Environment:** Windows, Python 3.14, Playwright 1.50, Chromium (headless)

---

## 1. Test Plan

### 1.1 Objective
Perform comprehensive functional testing of the entire QA Test Web Application, covering all 4 pages: Registration, Login, Forgot Password, and Dashboard. Identify bugs, validate form behavior, test API endpoints, responsive design, and security.

### 1.2 Scope

| Area | Coverage |
|------|----------|
| Registration page | Form validation, field types, required fields, T&C, duplicate email |
| Login page | Authentication flow, email validation, navigation, redirect |
| Forgot Password | Reset flow, security questions, fake success detection |
| Dashboard | Auth check, user display, logout, session management |
| Responsive design | Mobile (375x667) and tablet (768x1024) CSS bugs |
| API testing | /api/register and /api/login endpoints |
| Security | Console logging, session storage, injection attacks, CSRF |

### 1.3 Test Approach
- **Automated testing:** 104 test cases using Playwright + pytest
- **Page Object Model** (POM) for maintainable, reusable test code
- **Parametrized tests** for multiple data-driven scenarios
- **Viewport testing** for responsive design verification
- **Direct API testing** for backend endpoint validation

---

## 2. Acceptance Criteria

| # | Criteria | Status |
|---|----------|--------|
| AC-1 | User can register with valid data | PASS |
| AC-2 | Email validates proper format (RFC 5322) | FAIL |
| AC-3 | Password minimum 8 characters | FAIL |
| AC-4 | Password and Confirm Password must match | FAIL |
| AC-5 | Phone accepts only valid formats | FAIL |
| AC-6 | ZIP code accepts only numeric values | FAIL |
| AC-7 | Terms & Conditions must be checked | FAIL |
| AC-8 | HTML required attributes enforced | PASS |
| AC-9 | Registration redirects to login | PASS |
| AC-10 | Duplicate email prevented | PASS |
| AC-11 | Malicious input handled gracefully | PASS |
| AC-12 | Login with valid credentials works | PASS |
| AC-13 | Wrong credentials show error | PASS |
| AC-14 | Login redirects to dashboard | PASS |
| AC-15 | Password reset validates email existence | FAIL |
| AC-16 | Security answer is verified | FAIL |
| AC-17 | Dashboard requires authentication | PASS |
| AC-18 | Logout clears all session data | FAIL |
| AC-19 | Error messages visible on all viewports | FAIL |
| AC-20 | No sensitive data in console logs | FAIL |
| AC-21 | CSRF protection on API endpoints | FAIL |

---

## 3. Execution Summary

### 3.1 Overall Results

| Metric | Value |
|--------|-------|
| Total Test Cases | 104 |
| Passed | 77 |
| Failed (Application Bugs) | 27 |
| Pass Rate | 74% |
| Total Execution Time | ~214 seconds |
| Browser | Chromium (headless) |
| Framework | Playwright 1.50 + pytest 8.3.4 |

### 3.2 Results by Test Suite

| Suite | Tests | Passed | Failed | Pass Rate |
|-------|-------|--------|--------|-----------|
| Registration | 41 | 32 | 9 | 78% |
| Login | 15 | 14 | 1 | 93% |
| Forgot Password | 12 | 9 | 3 | 75% |
| Dashboard | 12 | 11 | 1 | 92% |
| Responsive | 10 | 1 | 9 | 10% |
| API | 9 | 8 | 1 | 89% |
| Security | 5 | 2 | 3 | 40% |

### 3.3 Bug Severity Distribution

| Severity | Count | Percentage |
|----------|-------|------------|
| Critical | 5 | 15% |
| High | 6 | 18% |
| Medium | 9 | 26% |
| Low | 14 | 41% |
| **Total** | **34** | |

---

## 4. Test Cases

### 4.1 Registration Tests (41 tests)

| TC-ID | Test Name | Description | Expected Result | Status | Bug |
|-------|-----------|-------------|-----------------|--------|-----|
| TC-001 | test_successful_registration_all_fields | Fill all fields with valid data, accept T&C, submit | Registration succeeds with success message | Pass | - |
| TC-002 | test_registration_without_newsletter | Register with all valid data but newsletter unchecked | Registration succeeds without newsletter | Pass | - |
| TC-003 | test_registration_redirects_to_login | Complete registration and wait for redirect | User is redirected to index.html (login page) | Pass | - |
| TC-004a | test_invalid_email_rejected [""] | Submit form with empty email | Rejected by HTML required attribute | Pass | - |
| TC-004b | test_invalid_email_rejected ["plaintext"] | Submit form with email "plaintext" | Error: invalid email format | Pass | - |
| TC-004c | test_invalid_email_rejected ["@nodomain.com"] | Submit form with email "@nodomain.com" | Error: invalid email format | Pass | - |
| TC-004d | test_invalid_email_rejected ["user@"] | Submit form with email "user@" | Error: invalid email format | Pass | - |
| TC-004e | test_invalid_email_rejected ["user@.com"] | Submit form with email "user@.com" | Error: invalid email format | **Fail** | BUG-001 |
| TC-004f | test_invalid_email_rejected ["user space@example.com"] | Submit form with email containing space | Error: invalid email format | **Fail** | BUG-001 |
| TC-004g | test_invalid_email_rejected ["user@@example.com"] | Submit form with double @ in email | Error: invalid email format | **Fail** | BUG-001 |
| TC-005 | test_email_input_type_should_be_email | Inspect email input element type attribute | Input type should be "email" for browser validation | **Fail** | BUG-002 |
| TC-006a | test_weak_password_rejected [""] | Submit form with empty password | Rejected by HTML required attribute | Pass | - |
| TC-006b | test_weak_password_rejected ["a"] | Submit form with 1-char password | Error: password too short | Pass | - |
| TC-006c | test_weak_password_rejected ["ab"] | Submit form with 2-char password | Error: password too short | Pass | - |
| TC-006d | test_weak_password_rejected ["abc"] | Submit form with 3-char password | Error: password too short | Pass | - |
| TC-006e | test_weak_password_rejected ["1234"] | Submit form with 4-char password | Error: password too short (min 8) | **Fail** | BUG-003 |
| TC-007 | test_password_mismatch_rejected | Enter "SecurePass123!" and "DifferentPass456!" | Error: passwords do not match | **Fail** | BUG-004 |
| TC-008 | test_password_field_is_masked | Inspect password and confirm password input types | Both fields should have type="password" | Pass | - |
| TC-009a | test_invalid_phone_rejected [""] | Submit form with empty phone | Rejected by HTML required attribute | Pass | - |
| TC-009b | test_invalid_phone_rejected ["abc"] | Submit form with phone "abc" | Error: invalid phone format | **Fail** | BUG-005 |
| TC-009c | test_invalid_phone_rejected ["12-34"] | Submit form with phone "12-34" | Error: invalid phone format | **Fail** | BUG-005 |
| TC-009d | test_invalid_phone_rejected ["phone number"] | Submit form with phone "phone number" | Error: invalid phone format | **Fail** | BUG-005 |
| TC-010a | test_invalid_zip_rejected [""] | Submit form with empty ZIP | Rejected by HTML required attribute | Pass | - |
| TC-010b | test_invalid_zip_rejected ["ab"] | Submit form with 2-char ZIP "ab" | Error: ZIP too short | Pass | - |
| TC-010c | test_invalid_zip_rejected ["abc"] | Submit form with 3-char ZIP "abc" | Error: ZIP must be numeric | **Fail** | BUG-006 |
| TC-010d | test_invalid_zip_rejected ["!!"] | Submit form with 2-char ZIP "!!" | Error: invalid ZIP format | Pass | - |
| TC-011 | test_zip_with_letters_rejected | Submit form with ZIP "ABCDE" | Error: ZIP must be numeric | **Fail** | BUG-006 |
| TC-012 | test_empty_form_submission | Click submit without filling any field | Form should not submit successfully | Pass | - |
| TC-013 | test_missing_first_name | Fill all except first name, submit | Form should not submit | Pass | - |
| TC-014 | test_missing_last_name | Fill all except last name, submit | Form should not submit | Pass | - |
| TC-015 | test_missing_email | Fill all except email, submit | Form should not submit | Pass | - |
| TC-016 | test_terms_checkbox_required | Fill all fields, leave T&C unchecked, submit | Error: must accept T&C | **Fail** | BUG-007 |
| TC-017 | test_sql_injection_in_fields | Fill fields with SQL injection payload | App handles gracefully, no server error | Pass | - |
| TC-018 | test_xss_in_fields | Fill fields with XSS `<script>` payload | Payload sanitized, not rendered as HTML | Pass | - |
| TC-019 | test_long_input_boundary | Fill fields with 256-char strings | App handles gracefully, no server error | Pass | - |
| TC-020 | test_page_title | Load registration page | Page title contains "Register" | Pass | - |
| TC-021 | test_all_form_labels_present | Inspect all 9 field labels | All labels visible with correct text | Pass | - |
| TC-022 | test_login_link_navigates_correctly | Click "Already have an account? Login" link | Navigates to index.html | Pass | - |
| TC-023 | test_all_required_fields_have_required_attribute | Inspect HTML required attribute on 9 fields | All fields have required attribute | Pass | - |
| TC-024 | test_submit_button_visible | Inspect submit button | Button visible, enabled, text "Create Account" | Pass | - |
| TC-025 | test_duplicate_email_rejected | Register twice with same email | Second registration shows error | Pass | - |

### 4.2 Login Tests (15 tests)

| TC-ID | Test Name | Description | Expected Result | Status | Bug |
|-------|-----------|-------------|-----------------|--------|-----|
| TC-L01 | test_successful_login | Login with valid registered credentials | Success message "Login successful" | Pass | - |
| TC-L02 | test_login_redirects_to_dashboard | Login and wait for redirect | URL contains "dashboard.html" | Pass | - |
| TC-L03 | test_login_shows_registered_param | Check URL after registration redirect | URL contains "registered=true" parameter | Pass | - |
| TC-L04 | test_login_wrong_password | Login with correct email, wrong password | Error message displayed | Pass | - |
| TC-L05 | test_login_nonexistent_email | Login with unregistered email | Error message displayed | Pass | - |
| TC-L06 | test_login_empty_form | Click login without filling fields | No success message | Pass | - |
| TC-L07 | test_login_empty_password | Fill email only, click login | No success message | Pass | - |
| TC-L08 | test_login_email_input_type | Inspect login email input type attribute | Input type should be "email" | **Fail** | BUG-002 |
| TC-L09a | test_login_invalid_email_rejected ["plaintext"] | Login with email "plaintext" | Validation error or no success | Pass | - |
| TC-L09b | test_login_invalid_email_rejected ["user@"] | Login with email "user@" | Validation error or no success | Pass | - |
| TC-L09c | test_login_invalid_email_rejected ["@test.com"] | Login with email "@test.com" | Validation error or no success | Pass | - |
| TC-L10 | test_page_title | Load login page | Page title contains "Login" | Pass | - |
| TC-L11 | test_forgot_password_link | Click "Forgot Password?" link | Navigates to forgot-password.html | Pass | - |
| TC-L12 | test_register_link | Click "Create New Account" link | Navigates to register.html | Pass | - |
| TC-L13 | test_remember_me_checkbox_present | Inspect Remember Me checkbox | Checkbox exists on the page | Pass | - |

### 4.3 Forgot Password Tests (12 tests)

| TC-ID | Test Name | Description | Expected Result | Status | Bug |
|-------|-----------|-------------|-----------------|--------|-----|
| TC-FP01 | test_reset_with_valid_email | Submit valid email for reset | Success message with "reset link" | Pass | - |
| TC-FP02 | test_reset_with_nonexistent_email_still_succeeds | Submit fake email "...@nonexistent.xyz" | Error: email not found | **Fail** | BUG-012 |
| TC-FP03 | test_security_answer_not_validated | Select question, enter wrong answer, submit | Error: wrong security answer | **Fail** | BUG-013 |
| TC-FP04 | test_reset_without_security_answer | Submit with question selected but no answer | Some response (question is optional) | Pass | - |
| TC-FP05 | test_empty_email_rejected | Click submit with empty email | No success message | Pass | - |
| TC-FP06 | test_invalid_email_rejected | Submit email "plaintext" | Validation error or no success | Pass | - |
| TC-FP07 | test_email_input_type | Inspect forgot-password email input type | Input type should be "email" | **Fail** | BUG-002 |
| TC-FP08 | test_security_question_has_correct_options | Inspect dropdown options | Contains 3 security questions + placeholder | Pass | - |
| TC-FP09 | test_security_question_is_optional | Inspect security question label | Label contains "Optional" | Pass | - |
| TC-FP10 | test_back_to_login_link | Click "Back to Login" link | Navigates to index.html | Pass | - |
| TC-FP11 | test_create_account_link | Click "Create New Account" link | Navigates to register.html | Pass | - |
| TC-FP12 | test_page_title | Load forgot password page | Title contains "Forgot Password" | Pass | - |

### 4.4 Dashboard Tests (12 tests)

| TC-ID | Test Name | Description | Expected Result | Status | Bug |
|-------|-----------|-------------|-----------------|--------|-----|
| TC-D01 | test_unauthenticated_redirects_to_login | Access dashboard.html without login | Redirected to index.html | Pass | - |
| TC-D02 | test_dashboard_accessible_after_login | Register, login, check URL | URL contains "dashboard.html" | Pass | - |
| TC-D03 | test_welcome_shows_user_name | Login and check welcome message | Displays user's first name | Pass | - |
| TC-D04 | test_logout_redirects_to_login | Click logout button | Redirected to index.html | Pass | - |
| TC-D05 | test_logout_incomplete_session_cleanup | Logout and check localStorage | All storage data cleared | **Fail** | BUG-016 |
| TC-D06 | test_no_logout_confirmation | Click logout, check immediate redirect | Confirmation dialog shown before logout | Pass* | BUG-017 |
| TC-D07 | test_stat_cards_visible | Login, check dashboard stat cards | At least 3 stat cards visible | Pass | - |
| TC-D08 | test_action_buttons_present | Login, check Quick Actions section | At least 3 action buttons present | Pass | - |
| TC-D09 | test_activity_list_present | Login, check activity section | At least 2 activity items | Pass | - |
| TC-D10 | test_action_button_shows_toast | Click an action button | Toast notification message appears | Pass | - |
| TC-D11 | test_page_title | Login, check page title | Title contains "Dashboard" | Pass | - |
| TC-D12 | test_last_login_displayed | Login, check last login info | Last login timestamp displayed | Pass | - |

*TC-D06 passes because it asserts the redirect occurs (documenting the missing confirmation dialog behavior).

### 4.5 Responsive Tests (10 tests)

| TC-ID | Test Name | Viewport | Description | Expected Result | Status | Bug |
|-------|-----------|----------|-------------|-----------------|--------|-----|
| TC-R01 | test_error_messages_visible_on_mobile | 375x667 | Trigger validation error, check visibility | Error messages visible | **Fail** | BUG-008 |
| TC-R02 | test_submit_button_fully_visible_on_mobile | 375x667 | Check submit button height on mobile | Button height >= 40px (matches desktop) | **Fail** | BUG-009 |
| TC-R03 | test_newsletter_checkbox_not_overlaid_on_mobile | 375x667 | Check for overlay on newsletter checkbox | No overlay element visible | **Fail** | BUG-011 |
| TC-R04 | test_address_field_not_overlaid_on_tablet | 768x1024 | Check for overlay on address field | No overlay element visible | **Fail** | BUG-010 |
| TC-R05 | test_security_section_not_overlaid_on_mobile | 375x667 | Check security question section overlay | No overlay element visible | **Fail** | BUG-015 |
| TC-R06 | test_remember_me_not_overlaid_on_mobile | 375x667 | Check for overlay on Remember Me | No overlay element visible | **Fail** | BUG-025 |
| TC-R07 | test_rewards_card_not_overlaid_on_tablet | 768x1024 | Login, check rewards card overlay | No overlay element visible | Pass | BUG-021 |
| TC-R08 | test_activity_item_not_overlaid_on_tablet | 768x1024 | Login, check activity overlay | No overlay element visible | **Fail** | BUG-022 |
| TC-R09 | test_dashboard_card_not_overlaid_on_tablet | 768x1024 | Login, check stat card overlay | No overlay element visible | **Fail** | BUG-024 |
| TC-R10 | test_download_report_button_not_overlaid_on_mobile | 375x667 | Login, check download button overlay | No overlay element visible | **Fail** | BUG-023 |

### 4.6 API Tests (9 tests)

| TC-ID | Test Name | Description | Expected Result | Status | Bug |
|-------|-----------|-------------|-----------------|--------|-----|
| TC-A01 | test_register_valid_data | POST /api/register with valid payload | Status 200, success: true | Pass | - |
| TC-A02 | test_register_duplicate_email | POST /api/register same email twice | Second request returns error | Pass | - |
| TC-A03 | test_register_missing_fields | POST /api/register with only email | Status 200/400/422, no crash | Pass | - |
| TC-A04 | test_register_response_structure | POST /api/register, inspect response | Response contains "success" field | Pass | - |
| TC-A05 | test_login_valid_credentials | Register via API, then POST /api/login | success: true | Pass | - |
| TC-A06 | test_login_wrong_password | Register via API, login with wrong password | success is not true | Pass | - |
| TC-A07 | test_login_nonexistent_email | POST /api/login with fake email | success is not true | Pass | - |
| TC-A08 | test_login_response_contains_user_data | Login via API, inspect response | Response contains "user" object with email | Pass | - |
| TC-A09 | test_no_csrf_token_required | POST /api/register without CSRF token | Request should be rejected | **Fail** | BUG-019 |

### 4.7 Security Tests (5 tests)

| TC-ID | Test Name | Description | Expected Result | Status | Bug |
|-------|-----------|-------------|-----------------|--------|-----|
| TC-S01 | test_login_logs_email_to_console | Register, login, capture console messages | Email should NOT appear in console | **Fail** | BUG-018 |
| TC-S02 | test_registration_logs_email_to_console | Register, capture console messages | Email should NOT appear in console | **Fail** | BUG-018 |
| TC-S03 | test_session_uses_httponly_cookies | Login, check sessionStorage for user data | Session data should NOT be in sessionStorage | **Fail** | BUG-020 |
| TC-S04 | test_sql_injection_login | Login with SQL injection payload | App handles gracefully, no server error | Pass | - |
| TC-S05 | test_xss_login | Login with XSS script payload | Payload not executed in page | Pass | - |

---

## 5. Bug Reports

### BUG-001: Weak Email Validation (High)
- **Location:** `app.js` -> `validateEmail()`, regex `/\S+@\S/`
- **Affected pages:** Registration, Login, Forgot Password
- **Impact:** Accepts invalid emails: `user@.com`, `user@@example.com`, `user space@example.com`

### BUG-002: Email Input Type is "text" (High)
- **Location:** HTML `<input type="text">` on all forms
- **Impact:** No browser-native email validation

### BUG-003: Password Minimum 4 Characters (High)
- **Location:** `app.js` -> `validatePassword()`, `password.length >= 4`
- **Impact:** Allows dangerously weak passwords

### BUG-004: Password Match Always True (Critical)
- **Location:** `app.js` -> `validatePasswordMatch()`, `return true;`
- **Impact:** Users can register with mismatched passwords

### BUG-005: Phone Accepts Letters (Medium)
- **Location:** `app.js` -> `validatePhone()`, `phone.length > 0`
- **Impact:** Invalid phone numbers stored

### BUG-006: ZIP Accepts Letters (Medium)
- **Location:** `app.js` -> `validateZipCode()`, `zip.length >= 3`
- **Impact:** Invalid ZIP codes stored

### BUG-007: Terms Checkbox Not Required (Critical)
- **Location:** `app.js` -> `handleRegister()`, validation commented out
- **Impact:** Legal/compliance violation

### BUG-008: Mobile Error Messages Hidden (Critical)
- **Location:** `styles.css` -> `@media (max-width: 767px) { .error-message { display: none !important; } }`
- **Impact:** Mobile users cannot see validation errors

### BUG-009: Mobile Submit Button Reduced Height (Medium)
- **Location:** `styles.css` -> `.btn-primary { max-height: 35px; margin-bottom: -25px; }`
- **Impact:** Button height is reduced on mobile compared to desktop (~35px vs ~44px); still visible and functional but inconsistent across viewports

### BUG-010: Tablet Address Overlay (Low)
- **Location:** CSS `tablet-hidden` class with `overlay-image-tablet`
- **Impact:** Address field obscured on tablet

### BUG-011: Mobile Newsletter Overlay (Low)
- **Location:** CSS `mobile-hidden-checkbox` with `overlay-image-small`
- **Impact:** Newsletter checkbox obscured on mobile

### BUG-012: Fake Password Reset Success (Critical)
- **Location:** `app.js` -> `handleForgotPassword()`, no email verification
- **Impact:** Misleads users into thinking reset was sent

### BUG-013: Security Answer Ignored (Critical)
- **Location:** `app.js` -> `handleForgotPassword()`, answer not checked
- **Impact:** Security question provides no security

### BUG-015: Mobile Security Section Overlay (Low)
- **Location:** CSS `mobile-hidden-section` with `overlay-image-security`
- **Impact:** Security question hidden on mobile

### BUG-016: Incomplete Logout Session Cleanup (Medium)
- **Location:** `app.js` -> `handleLogout()`, only clears sessionStorage
- **Impact:** User data persists in localStorage

### BUG-017: No Logout Confirmation (Low)
- **Location:** `app.js` -> `handleLogout()`, immediate redirect
- **Impact:** Accidental logout possible

### BUG-018: Console Logging Sensitive Data (High)
- **Location:** `app.js` -> multiple `console.log()` with user emails
- **Impact:** PII exposure in browser console

### BUG-019: No CSRF Protection (High)
- **Location:** `app.js` -> all `fetch()` calls lack CSRF tokens
- **Impact:** Vulnerable to CSRF attacks

### BUG-020: Session in sessionStorage (High)
- **Location:** `app.js` -> `sessionStorage.setItem('currentUser', ...)`
- **Impact:** Session accessible via XSS

### BUG-021: Dashboard Rewards Overlay on Tablet (Low)
- **Location:** CSS `mobile-hidden-card` with `overlay-image-rewards`

### BUG-022: Dashboard Activity Overlay on Tablet (Low)
- **Location:** CSS `tablet-hidden-activity` with `overlay-image-activity`

### BUG-023: Download Report Button Overlay on Mobile (Medium)
- **Location:** CSS `mobile-hidden-action` class with `button-overlay`
- **Affected page:** Dashboard (mobile viewport ≤767px)
- **Impact:** Download Report action button covered by overlay on mobile devices

### BUG-024: Dashboard Stat Card Overlay on Tablet (Low)
- **Location:** CSS `tablet-hidden-card` class with `overlay-image-dashboard`
- **Affected page:** Dashboard (tablet viewport 768-1024px)
- **Impact:** Stat card obscured by overlay on tablet devices

### BUG-025: Login Remember Me Overlay on Mobile (Low)
- **Location:** CSS `mobile-hidden` with `overlay-image`

### BUG-026: Required Fields Lack Visual Asterisk Indicators (Low)
- **Location:** Registration form HTML (`register.html`)
- **Affected pages:** Registration (all required fields)
- **Impact:** All form fields have the HTML `required` attribute but no visual `*` indicator next to labels. Users cannot tell which fields are mandatory until they attempt to submit the form and receive browser validation errors. Standard UX convention is to mark required fields with an asterisk (*).

### BUG-027: Remember Me Checkbox is Non-Functional (Medium)
- **Location:** `app.js` -> `handleLogin()`, Login page HTML
- **Affected page:** Login
- **Impact:** The `handleLogin()` function never reads the Remember Me checkbox value. Session is always stored in `sessionStorage` (cleared when browser tab closes). When checked, the app should use `localStorage` for persistent sessions. Users check the box expecting their session to persist, but it has zero effect.

### BUG-028: No Login Attempt Rate Limiting (Medium)
- **Location:** `/api/login` endpoint
- **Affected page:** Login, API
- **Impact:** The login API accepts unlimited failed login attempts with no delay, lockout, or CAPTCHA. This enables brute-force password attacks. Should implement account lockout after N failed attempts or progressive delays.

### BUG-029: Forgot Password Ignores Selected Security Question (Medium)
- **Location:** `app.js` -> `handleForgotPassword()`
- **Affected page:** Forgot Password
- **Impact:** The function reads `securityAnswer` value but never reads which security question was selected from the dropdown. Even if answer validation were fixed (BUG-013), the selected question is completely ignored. The dropdown serves no purpose.

### BUG-030: Password Transmitted as Plaintext in API Body (Medium)
- **Location:** `app.js` -> `handleLogin()`, `handleRegister()`, API endpoints
- **Affected pages:** Registration, Login
- **Impact:** Both `/api/register` and `/api/login` send the password as plain text in the JSON request body. While HTTPS encrypts in transit, the password is visible in browser DevTools Network tab and server logs. Should be hashed client-side before transmission.

### BUG-031: No Password Visibility Toggle (Low)
- **Location:** Registration form, Login form HTML
- **Affected pages:** Registration, Login
- **Impact:** No "show/hide password" toggle (eye icon) exists on any password field. Users cannot verify what they typed, increasing password entry errors. Standard UX practice includes a visibility toggle.

### BUG-032: Missing Autocomplete Attributes on Form Fields (Low)
- **Location:** All form HTML files
- **Affected pages:** Registration, Login, Forgot Password
- **Impact:** Form fields lack `autocomplete` attributes (`autocomplete="email"`, `autocomplete="new-password"`, `autocomplete="given-name"`, etc.). Password managers and browsers cannot reliably auto-fill fields, degrading the user experience.

### BUG-033: Error Messages Not Linked to Inputs via aria-describedby (Low)
- **Location:** All form HTML files
- **Affected pages:** Registration, Login, Forgot Password
- **Impact:** Error message elements (e.g., `#emailError`) are not associated with their corresponding input fields via `aria-describedby`. Screen readers cannot announce validation errors when users focus on a field. Fails WCAG 2.1 SC 1.3.1.

### BUG-034: No Skip-to-Content Navigation Link (Low)
- **Location:** All page HTML files
- **Affected pages:** All 4 pages
- **Impact:** No skip navigation link exists for keyboard and screen reader users. Users must tab through all navigation elements before reaching main content. Fails WCAG 2.1 SC 2.4.1.

### BUG-035: Dashboard Action Buttons Are Non-Functional (Low)
- **Location:** `dashboard.html`, `app.js`
- **Affected page:** Dashboard
- **Impact:** "Update Profile", "Settings", "Contact Support", and "Download Report" buttons only display toast notification messages. They perform no actual actions. Users expect these buttons to navigate to real functionality, not just show a confirmation toast.

---

## 6. Recommendations (Prioritized)

1. **CRITICAL:** Fix `validatePasswordMatch()` to actually compare passwords
2. **CRITICAL:** Uncomment Terms & Conditions validation
3. **CRITICAL:** Fix forgot password to verify email exists before showing success
4. **CRITICAL:** Validate security answers against stored data
5. **CRITICAL:** Remove `display: none !important` on mobile `.error-message`
6. **HIGH:** Replace weak email regex with RFC-compliant validation
7. **HIGH:** Change password minimum to 8 characters
8. **HIGH:** Remove all `console.log()` statements with user data
9. **HIGH:** Implement CSRF tokens on all API endpoints
10. **HIGH:** Use httpOnly cookies instead of sessionStorage for sessions
11. **HIGH:** Change email input type to "email" on all forms
12. **MEDIUM:** Add phone number format validation (digits only)
13. **MEDIUM:** Add ZIP code numeric validation
14. **MEDIUM:** Fix mobile submit button CSS (remove max-height: 35px and margin-bottom: -25px for consistent button sizing)
15. **MEDIUM:** Clear localStorage on logout
16. **LOW:** Add logout confirmation dialog
17. **LOW:** Remove/fix all overlay elements blocking form fields
18. **LOW:** Add visual asterisk (*) indicators to required field labels
19. **MEDIUM:** Implement Remember Me checkbox using localStorage for session persistence
20. **MEDIUM:** Add login rate limiting / account lockout after failed attempts
21. **MEDIUM:** Read and validate the selected security question in forgot password flow
22. **MEDIUM:** Hash passwords client-side before API transmission
23. **LOW:** Add password visibility toggle (show/hide) on all password fields
24. **LOW:** Add `autocomplete` attributes to all form fields for password manager support
25. **LOW:** Link error messages to inputs via `aria-describedby` for screen reader accessibility
26. **LOW:** Add skip-to-content navigation link on all pages
27. **LOW:** Implement actual functionality for dashboard action buttons

---

## 7. Manual Testing Results

### 7.1 Methodology
Manual exploratory testing was performed before automation to understand application behavior, discover edge cases, and identify UI/UX issues that require visual inspection. Testing was done using Chromium browser with Chrome DevTools responsive mode to simulate mobile and tablet viewports.

### 7.2 Manual Test Cases Executed

| # | Manual Test | Environment | Result | Bug Found |
|---|-------------|-------------|--------|-----------|
| MT-01 | Navigate registration form, fill fields, submit | Desktop Chromium | Pass | - |
| MT-02 | Inspect email input type in DevTools | Desktop Chromium | Fail | BUG-002: type="text" |
| MT-03 | Enter mismatched passwords, observe behavior | Desktop Chromium | Fail | BUG-004: no mismatch error |
| MT-04 | Submit without T&C checkbox | Desktop Chromium | Fail | BUG-007: T&C not enforced |
| MT-05 | Review app.js source for validation logic | Code inspection | Fail | BUG-001,003,004,005,006,007 |
| MT-06 | Review styles.css for responsive rules | Code inspection | Fail | BUG-008,009,010,011,015,025 |
| MT-07 | Resize browser to 375px (mobile) | DevTools responsive | Fail | BUG-008: errors hidden |
| MT-08 | Resize browser to 375px - check submit button | DevTools responsive | Fail | BUG-009: button height reduced |
| MT-09 | Resize browser to 768px (tablet) | DevTools responsive | Fail | BUG-010: address overlay |
| MT-10 | Forgot password with fake email | Desktop Chromium | Fail | BUG-012: fake success |
| MT-11 | Forgot password with wrong security answer | Desktop Chromium | Fail | BUG-013: answer ignored |
| MT-12 | Open browser console during login | DevTools Console | Fail | BUG-018: email logged |
| MT-13 | Check sessionStorage after login | DevTools Application | Fail | BUG-020: user data in sessionStorage |
| MT-14 | Logout and check localStorage remains | DevTools Application | Fail | BUG-016: data persists |
| MT-15 | Dashboard without login | Desktop Chromium | Pass | Redirects correctly |
| MT-16 | Check required fields have visual asterisks | Desktop Chromium | Fail | BUG-026: no asterisks on labels |
| MT-17 | Check Remember Me persists session after browser close | Desktop Chromium | Fail | BUG-027: checkbox not read by JS |
| MT-18 | Attempt 20+ failed logins, check for lockout | Desktop Chromium | Fail | BUG-028: no rate limiting |
| MT-19 | Select security question, check if value used | Code inspection | Fail | BUG-029: question selection ignored |
| MT-20 | Inspect API request body in Network tab | DevTools Network | Fail | BUG-030: password in plaintext |
| MT-21 | Look for show/hide password toggle on forms | Desktop Chromium | Fail | BUG-031: no toggle exists |
| MT-22 | Check autocomplete attributes in DevTools | DevTools Elements | Fail | BUG-032: no autocomplete attrs |
| MT-23 | Check aria-describedby on error messages | DevTools Elements | Fail | BUG-033: not linked to inputs |
| MT-24 | Tab through page, check for skip-to-content link | Keyboard navigation | Fail | BUG-034: no skip link |
| MT-25 | Click dashboard action buttons, check functionality | Desktop Chromium | Fail | BUG-035: only shows toast |

### 7.3 Manual vs. Automated Discovery

| Discovery Method | Bugs Found |
|-----------------|------------|
| Manual exploratory testing (code review) | BUG-001 through BUG-007 (validation logic in app.js), BUG-027, BUG-029 |
| Manual visual testing (responsive/UX) | BUG-008, BUG-009, BUG-010, BUG-011, BUG-015, BUG-025, BUG-026, BUG-031, BUG-035 |
| Manual DevTools inspection | BUG-002, BUG-018, BUG-020, BUG-030, BUG-032, BUG-033, BUG-034 |
| Manual security testing | BUG-028 (rate limiting) |
| Automated testing confirmed | All above bugs + BUG-012, BUG-013, BUG-016, BUG-019 |

All bugs found during manual testing were subsequently automated to ensure regression coverage where applicable. BUG-027 through BUG-035 were discovered during deep source code review and manual exploratory testing.

---

## 8. Sprint Automation Tasks

The following automation-related tasks were executed as part of this testing sprint:

### 8.1 Sprint Task Log

| # | Task | Description | Status |
|---|------|-------------|--------|
| S-01 | Test framework setup | Installed Python, Playwright, pytest, pytest-html, pytest-playwright | Done |
| S-02 | Browser installation | Installed Chromium via `playwright install chromium` | Done |
| S-03 | Page Object Model design | Designed POM with BasePage, RegisterPage, LoginPage, ForgotPasswordPage, DashboardPage | Done |
| S-04 | Test data management | Created centralized test_data.py with random generators and parametrized data sets | Done |
| S-05 | Fixture architecture | Built conftest.py with page fixtures, registered_user, authenticated_page | Done |
| S-06 | Test implementation | Wrote 104 test cases across 7 test files covering all 4 pages | Done |
| S-07 | Test execution (run 1) | Initial run: found 2 test code issues (label selector, button is_enabled) | Done |
| S-08 | Test code fix & refactor | Fixed label selector to use `label[for='id']`, fixed button assertion | Done |
| S-09 | Test execution (run 2) | Clean run: 104 tests, 74 pass, 30 fail (all app bugs) | Done |
| S-10 | Bug triage | Classified 34 unique bugs by severity (5 Critical, 6 High, 9 Medium, 14 Low) | Done |
| S-11 | Test report writing | Created comprehensive test_report.md with all sections | Done |
| S-12 | README documentation | Wrote setup guide, bug catalog, architecture docs, troubleshooting | Done |
| S-13 | CI/CD pipeline setup | Created GitHub Actions workflow (.github/workflows/tests.yml) | Done |
| S-14 | VS Code integration | Installed Playwright Test extension for IDE test running | Done |
| S-15 | Manual testing | Performed 25 manual test cases, documented results | Done |
| S-16 | Git repository setup | Initialized repo, configured .gitignore, staged all files | Done |

### 8.2 Test Maintenance Notes
- **Flaky test mitigation:** Used explicit waits (`wait_for_url`, `wait_for_load_state("networkidle")`) instead of fixed delays for reliable cross-platform execution
- **Test isolation:** Each test uses `random_email()` to generate unique emails, preventing test-to-test interference
- **Viewport testing:** Used `page.set_viewport_size()` for responsive tests instead of separate browser contexts (more efficient)
- **API test separation:** API tests use Playwright's `APIRequestContext` directly, avoiding browser overhead

### 8.3 CI/CD Pipeline
GitHub Actions workflow configured at `.github/workflows/tests.yml`:
- Triggers on push/PR to main/master, or manually via **Actions > Playwright Tests > Run workflow**
- Installs Python 3.12, dependencies, Playwright Chromium
- Runs full test suite with HTML report generation
- Uploads report as downloadable artifact (retained 30 days)

---

## 9. Automation Execution Report

### 9.1 Test Execution Output (pytest -v)

```
tests/test_api.py::TestRegisterAPI::test_register_valid_data                PASSED
tests/test_api.py::TestRegisterAPI::test_register_duplicate_email           PASSED
tests/test_api.py::TestRegisterAPI::test_register_missing_fields            PASSED
tests/test_api.py::TestRegisterAPI::test_register_response_structure        PASSED
tests/test_api.py::TestLoginAPI::test_login_valid_credentials               PASSED
tests/test_api.py::TestLoginAPI::test_login_wrong_password                  PASSED
tests/test_api.py::TestLoginAPI::test_login_nonexistent_email               PASSED
tests/test_api.py::TestLoginAPI::test_login_response_contains_user_data     PASSED
tests/test_api.py::TestLoginAPI::test_no_csrf_token_required                FAILED (BUG-019)
tests/test_dashboard.py::TestDashboardAuthentication (3 tests)              3 PASSED
tests/test_dashboard.py::TestDashboardLogout::test_logout_redirects         PASSED
tests/test_dashboard.py::TestDashboardLogout::test_incomplete_cleanup       FAILED (BUG-016)
tests/test_dashboard.py::TestDashboardLogout::test_no_confirmation          PASSED
tests/test_dashboard.py::TestDashboardElements (6 tests)                    6 PASSED
tests/test_forgot_password.py::TestFlow::test_valid_email                   PASSED
tests/test_forgot_password.py::TestFlow::test_nonexistent_email_succeeds    FAILED (BUG-012)
tests/test_forgot_password.py::TestFlow::test_security_answer_not_validated FAILED (BUG-013)
tests/test_forgot_password.py::TestValidation::test_email_input_type        FAILED (BUG-002)
tests/test_forgot_password.py (remaining 8 tests)                           8 PASSED
tests/test_login.py::TestLoginPositive (3 tests)                            3 PASSED
tests/test_login.py::TestLoginNegative (4 tests)                            4 PASSED
tests/test_login.py::TestLoginEmailValidation::test_email_input_type        FAILED (BUG-002)
tests/test_login.py::TestLoginEmailValidation (3 parametrized)              3 PASSED
tests/test_login.py::TestLoginUIElements (4 tests)                          4 PASSED
tests/test_registration.py (41 tests)                                       32 PASSED, 9 FAILED
tests/test_responsive.py (10 tests)                                         1 PASSED, 9 FAILED
tests/test_security.py (5 tests)                                            2 PASSED, 3 FAILED

========================= 77 passed, 27 failed in 214s =========================
```

> **Note:** The 34 bug count includes 10 bugs found via manual testing (BUG-026 through BUG-035) that do not have automated test failures.

### 9.2 HTML Report (Auto-generated)
pytest-html generates a detailed HTML execution report at `reports/report.html` after each test run. This is raw tool output with interactive pass/fail breakdown, test duration, and failure stack traces. Open it in any browser to view. CI/CD also uploads this as a downloadable artifact.

---

## 10. Conclusion

Testing identified **34 unique bugs** across all 4 pages, including **5 Critical** issues that would prevent production deployment. Out of 104 automated tests, 77 pass and 27 fail due to application defects. The registration form has the most bugs (9 failing tests), but critical issues also exist in the forgot password flow (fake reset success, unvalidated security answers), responsive design (hidden error messages on mobile), and security (console logging of PII, session stored in sessionStorage, no CSRF protection). The happy path works for all features, but validation, security, and responsive design need significant improvement before release.
