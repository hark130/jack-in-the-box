# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for manual login (e.g., Twitch-enabled games)
- New `jitb_validation` module to standardize JITB-specific input validation
- Added support for Blather 'Round
- Added `get_web_elements()` to `jitb_selenium`
- Added debug logging for `jitb_webdriver`'s `click_a_button()`

### Changed

- Argument parser now utilizes commands: automatic, manual
- Extricated module-local, private validation functions into `jitb_validation` as appropriate
- All JITB validation is either handled by `hobo.validation` or `jitb_validation`
- Many of the "bad input" exception messages have changed now input validation has changed
- Dialed back on debug logging for `jitb_selenium`'s underlying functionality to "get an element"

### Deprecated

### Fixed

- Exception message on `jitb_webdriver._validate_bool()` when it got promoted to `jitb_validation.validate_bool()`

### Removed

### Security

## [1.1.0] - 2024-12-20

### Added

- Support for Jackbox Party Pack 6 - Dictionarium
- `JitbAi.change_system_content()` to allow game-specific AI content control
- The user may control the `--debug` log file directory using the `TMPDIR` environment variable
- Added Chrome dependency to project documentation
- Added `convert_str_to_int()` to `jitb_misc`
- Added a support for different replacement characters in `jitb_misc.clean_up_string()`
- Added `get_web_element_int()` to `jitb_selenium`
- Extricated copy/paste functionality into `jitb/jitb_webdriver.py` as common-use functionality
- Added a feature to all legacy Jackbox Game classes (`JbgDict`, `JbgJb`, `JbgQ2`, `JbgQ3`) to dynamically read the prompt length and pass that to OpenAI's API

### Changed

- `JitbAi`'s default model changed to [gpt-4o-mini](https://platform.openai.com/docs/models/gpt-4o-mini)
- Moved the `validate_status()` method up to the `jitb/jbgames/jbg_abc.py` abstract class
- Refactored all legacy Jackbox Game classes (`JbgDict`, `JbgJb`, `JbgQ2`, `JbgQ3`) to utilize new common-use `jitb/jitb_webdriver.py` functionality
- Relaxed `JbgQ3`'s requirement to select an Avatar (failed race conditions no longer raise Exceptions)
- Made the legacy Jackbox Game classes more robust by relaxing Exceptions in lieu of debug logging and errors
- Added an optional `exclude` argument to `jitb_webdriver.get_button_choices()` to ignore certain button names
- Refactored `jitb_webdriver.vote_answers()` to take, and pass down, the `exclude` argument
- Refactored the entire `jbg_jb.choose_catchphrase()` call chain to utilize the new `exclude` argument to avoid choosing the "Reset my choices" button

### Fixed

- `--debug` log file location is now (reasonably) OS-agnostic
- Fixed some docstring typos
- Removed some stale comments
- Fixed a BUG(?) in `jitb_webdriver.click_a_button()`
- Made `jitb_webdriver.get_prompt()` more robust
- An edge case BUG in the `JbgJb.choose_catchphrase()` logic/call-chain that allowed the "Reset my choices" button to be selected

### Removed

## [1.0.0] - 2024-09-25

### Added

- Initial support for Jackbox Games Joke Boat, Quiplash 2, and Quiplash 3.
- Release of the jitb package as a wheel.

[unreleased]: https://github.com/hark130/jack-in-the-box/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/hark130/jack-in-the-box/releases/tag/v1.1.0
[1.0.0]: https://github.com/hark130/jack-in-the-box/releases/tag/v1.0.0
