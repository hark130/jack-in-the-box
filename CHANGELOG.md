# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for Jackbox Party Pack 6 - Dictionarium
- `JitbAi.change_system_content()` to allow game-specific AI content control
- The user may control the `--debug` log file directory using the `TMPDIR` environment variable
- Added Chrome dependency to project documentation
- Added `convert_str_to_int()` to `jitb_misc`
- Added a support for different replacement characters in `jitb_misc.clean_up_string()`
- Added `get_web_element_int()` to `jitb_selenium`
- Extricated copy/paste functionality into `jitb/jitb_webdriver.py` as common-use functionality

### Changed

- Moved the `validate_status()` method up to the `jitb/jbgames/jbg_abc.py` abstract class
- Refactored all legacy Jackbox Games clasess (`JbgDict`, `JbgJb`, `JbgQ2`, `JbgQ3`) to utilize new common-use `jitb/jitb_webdriver.py` functionality
- Relaxed `JbgQ3`'s requirement to select an Avatar (failed race conditions no longer raise Exceptions)

### Deprecated

### Fixed

- `--debug` log file location is now (reasonably) OS-agnostic
- Fixed some docstring typos
- Removed some stale comments

### Removed

### Security

## [1.0.0] - 2024-09-25

### Added

- Initial support for Jackbox Games Joke Boat, Quiplash 2, and Quiplash 3.
- Release of the jitb package as a wheel.

[unreleased]: https://github.com/hark130/jack-in-the-box/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/hark130/jack-in-the-box/releases/tag/v1.0.0
