# Changelog

All notable changes to this HRMS fork will be documented in this file.

## [v16.0.0b2+mh10] - 2026-01-07

### Fixed

- **[Roster]** Fixed period date calculations in roster management
  - Corrected month offset logic to properly calculate roster periods based on HR Settings Start Day
  - Improved period_start calculation to use selected month (one month back from current month)
  - Enhanced period_end calculation to accurately determine the last day of the period (start_day - 1 of next month)
  - Better handling of edge cases when start_day doesn't exist in a month (e.g., day 31 in February)
  - Updated MonthView component to default to previous month for better UX alignment with fiscal period logic

## [v16.0.0b2+mh9] - 2026-01-06

### Added

- **[HR Settings]** Added configurable Start Day field for custom roster period calculations
  - Select field with options 1-28 for defining roster period start day
  - Includes validation to ensure valid day selection

### Changed

- **[Roster]** Updated roster period handling to use Start Day from HR Settings instead of fiscal year
  - Period calculations now based on HR Settings Start Day configuration
  - Handles edge cases for months with fewer days (e.g., February 31st defaults to last day)
- **[HR Settings]** Changed Start Day field from Date type to Select type with options 1-28

## [v16.0.0b2+mh8] - 2025-12-16

### Added

- **[HR Settings]** Added Probation period field to HR Settings doctype

### Fixed

- **[Employee Advance]** Commented base_paid_amount in APLE (Advanced Payment Ledger Entry) logic due to missing field in Employee Advance doctype
- **[General]** Fixed passing params as dict (bug from beta)

---

## Links

- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [Upstream HRMS Repository](https://github.com/frappe/hrms)
