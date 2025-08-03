# Contributing to IEBPTPCH PDS Extractor

Thank you for your interest in contributing to the IEBPTPCH PDS Extractor! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (Python version, OS, etc.)
- Sample input files (if possible and not confidential)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- A clear, descriptive title
- Detailed description of the proposed feature
- Use cases and benefits
- Any implementation ideas you might have

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation as needed
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/arunkumars-mf/iebptpch-pds-extractor.git
   cd iebptpch-pds-extractor
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

4. Run tests:
   ```bash
   python -m pytest tests/
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and reasonably sized
- Add type hints where appropriate

## Testing

- Write tests for new functionality
- Ensure existing tests continue to pass
- Test with both ASCII and EBCDIC input files
- Test error conditions and edge cases

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions and classes
- Update examples if the API changes
- Keep CHANGELOG.md updated

## Commit Messages

Use clear, descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when applicable

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Contact the maintainer at aruninfy123@gmail.com

Thank you for contributing!
