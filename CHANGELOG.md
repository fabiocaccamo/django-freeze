# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.11.1](https://github.com/fabiocaccamo/django-freeze/releases/tag/0.11.1) - 2024-09-21
-   Parse sitemap urls only if needed. #136
-   Bump test requirements.
-   Bump `pre-commit` hooks.

## [0.11.0](https://github.com/fabiocaccamo/django-freeze/releases/tag/0.11.0) - 2024-03-04
-   Fix random files generated. #89
-   Fix `scanner` encoding issue. #117
-   Use `f-strings`.
-   Avoid to execute database queries in settings module.
-   Improve parser code quality and add unit tests. #10
-   Include `sitemap.xml` and `robots.txt`. #1
-   Replace `Black` and `isort` with `Ruff-format`.
-   Bump requirements.
-   Bump `pre-commit` hooks.
-   Bump GitHub actions.

## [0.10.0](https://github.com/fabiocaccamo/django-freeze/releases/tag/0.10.0) - 2023-12-05
-   Add `Python 3.12` support.
-   Add `Django 5.0` support.
-   Speed-up test workflow.
-   Bump requirements.
-   Bump `pre-commit` hooks.

## [0.9.0](https://github.com/fabiocaccamo/django-freeze/releases/tag/0.9.0) - 2022-12-09
-   Add `Python 3.11` support.
-   Add `Django 4.1` support.
-   Add `pre-commit`.
-   Drop `Python < 3.8` and `Django < 2.2` support.

## [0.8.0](https://github.com/fabiocaccamo/django-freeze/releases/tag/0.8.0) - 2022-09-25
-   Drop `Python < 3.7` and `Django < 2.0` support.
-   Use `f-strings`.
-   Replace `print` calls with `logging`.

## [0.7.0](https://github.com/fabiocaccamo/django-freeze/releases/tag/0.7.0) - 2022-09-25
-   Add initial test suite and GitHub CI. #10
-   Add requirements files.
-   Update setup.
-   Format code with Black.
