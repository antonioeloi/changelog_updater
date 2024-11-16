# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - YYYY-MM-DD

### Added

### Fixed

### Changed

### Removed

## [7.1.3.2] - 2024-02-13

### Fixed

- Fix Active Record query cache handling with multi-database applications - [#RAILS-1234](https://app.clickup.com/t/82723/RAILS-1234)

## [7.1.3.1] - 2024-02-08

### Fixed

- Ensure correct handling of timezone-aware attributes in forms - [#RAILS-5678](https://app.clickup.com/t/82723/RAILS-5678)

## [7.1.3] - 2024-02-01

### Added

- Add support for custom serializers in Action Cable - [#RAILS-9012](https://app.clickup.com/t/82723/RAILS-9012)

### Changed

- Improve performance of Active Record connection pool management - [#RAILS-3456](https://app.clickup.com/t/82723/RAILS-3456)

## [7.1.2] - 2024-01-25

### Fixed

- Fix regression in Active Storage variant tracking - [#RAILS-7890](https://app.clickup.com/t/82723/RAILS-7890)

## [7.1.1] - 2024-01-10

### Added

- Add built-in support for JSON:API serialization - [#RAILS-2345](https://app.clickup.com/t/82723/RAILS-2345)

### Changed

- Update Active Support's TimeZone data - [#RAILS-6789](https://app.clickup.com/t/82723/RAILS-6789)

## [7.1.0] - 2023-12-15

### Added

- Introduce new testing helpers for Action Mailer - [#RAILS-1111](https://app.clickup.com/t/82723/RAILS-1111)
- Add support for async queries in Active Record - [#RAILS-2222](https://app.clickup.com/t/82723/RAILS-2222)

### Changed

- Improve error messages for routing conflicts - [#RAILS-3333](https://app.clickup.com/t/82723/RAILS-3333)

### Removed

- Remove deprecated `rails/all` require - [#RAILS-4444](https://app.clickup.com/t/82723/RAILS-4444)

[Unreleased]: https://github.com/rails/rails/compare/v7.1.3.2...HEAD
[7.1.3.2]: https://github.com/rails/rails/-/tree/v7.1.3.2
[7.1.3.1]: https://github.com/rails/rails/-/tree/v7.1.3.1
[7.1.3]: https://github.com/rails/rails/-/tree/v7.1.3
[7.1.2]: https://github.com/rails/rails/-/tree/v7.1.2
[7.1.1]: https://github.com/rails/rails/-/tree/v7.1.1
[7.1.0]: https://github.com/rails/rails/-/tree/v7.1.0
