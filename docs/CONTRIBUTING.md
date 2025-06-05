# Contributing to Fitness And Diet App

Thank you for your interest in contributing to the Fitness And Diet App! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/your-username/diet_fitness.git
   cd diet_fitness
   ```
3. **Set up the development environment** by following the instructions in the [README.md](../README.md)
4. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

1. **Make your changes** in your feature branch
2. **Write or update tests** to cover your changes
3. **Run the tests** to ensure they pass:
   ```bash
   pytest
   ```
4. **Format your code** using the project's style guidelines
5. **Commit your changes** with a descriptive commit message:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```
6. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a pull request** from your fork to the main repository

## Pull Request Guidelines

When submitting a pull request:

1. **Describe your changes** in detail
2. **Reference any related issues** using the GitHub issue number (e.g., "Fixes #123")
3. **Include screenshots or examples** if applicable
4. **Update documentation** to reflect your changes
5. **Ensure all tests pass**
6. **Be responsive to feedback** and be willing to make changes if requested

## Code Style Guidelines

Please follow these style guidelines when contributing code:

1. **Use consistent indentation** (4 spaces, not tabs)
2. **Follow PEP 8** for Python code
3. **Write descriptive variable and function names**
4. **Add docstrings** to all functions, classes, and modules
5. **Keep functions small and focused** on a single responsibility
6. **Use type hints** where appropriate

## Testing Guidelines

1. **Write unit tests** for all new functionality
2. **Ensure existing tests pass** with your changes
3. **Use pytest** for writing and running tests
4. **Aim for high test coverage** of your code

## Documentation Guidelines

1. **Update the README.md** if your changes affect the installation or usage instructions
2. **Add or update docstrings** for all functions, classes, and modules
3. **Update API documentation** if you change or add endpoints
4. **Create new documentation files** in the docs directory if needed

## Reporting Bugs

When reporting bugs:

1. **Use the GitHub issue tracker**
2. **Describe the bug** in detail
3. **Include steps to reproduce** the bug
4. **Include expected and actual behavior**
5. **Include your environment details** (OS, Python version, etc.)
6. **Include screenshots or logs** if applicable

## Suggesting Features

When suggesting features:

1. **Use the GitHub issue tracker**
2. **Describe the feature** in detail
3. **Explain why the feature would be useful**
4. **Provide examples of how the feature would be used**
5. **Be open to discussion** about the feature

## Branching Strategy

- **main**: The production branch, containing stable code
- **develop**: The development branch, containing code for the next release
- **feature/feature-name**: Feature branches for new features
- **bugfix/bug-name**: Bug fix branches for fixing bugs

## Versioning

We use [Semantic Versioning](https://semver.org/) for versioning:

- **MAJOR** version for incompatible API changes
- **MINOR** version for adding functionality in a backwards-compatible manner
- **PATCH** version for backwards-compatible bug fixes

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](../README.md#license).

## Questions?

If you have any questions about contributing, please open an issue or contact the project maintainers.

Thank you for your contributions!