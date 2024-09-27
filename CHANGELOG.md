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

### Changed

- `JitbAi`'s default model changed to [gpt-4o-mini](https://platform.openai.com/docs/models/gpt-4o-mini)

### Deprecated

### Fixed

- `--debug` log file location is now (reasonably) OS-agnostic
- Fixed some docstring typos

### Removed

### Security

## [1.0.0] - 2024-09-25

### Added

- Initial support for Jackbox Games Joke Boat, Quiplash 2, and Quiplash 3.
- Release of the jitb package as a wheel.

[unreleased]: https://github.com/hark130/jack-in-the-box/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/hark130/jack-in-the-box/releases/tag/v1.0.0
