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

### Deprecated

### Fixed

- `--debug` log file location is now (reasonably) OS-agnostic
- Fixed some docstring typos
- Removed some stale comments
- Fixed a BUG(?) in `jitb_webdriver.click_a_button()`
- Made `jitb_webdriver.get_prompt()` more robust
- An edge case BUG in the `JbgJb.choose_catchphrase()` logic/call-chain that allowed the "Reset my choices" button to be selected

### Removed

### Security

## [1.0.0] - 2024-09-25

### Added

- Initial support for Jackbox Games Joke Boat, Quiplash 2, and Quiplash 3.
- Release of the jitb package as a wheel.

[unreleased]: https://github.com/hark130/jack-in-the-box/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/hark130/jack-in-the-box/releases/tag/v1.0.0
