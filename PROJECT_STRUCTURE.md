# Project Structure

This document describes the structure and organization of the IEBPTPCH PDS Extractor project.

## Directory Structure

```
iebptpch_pds_extractor/
├── src/
│   └── iebptpch_pds_extractor/
│       ├── __init__.py          # Package initialization and exports
│       └── extractor.py         # Main PDSExtractor class and CLI
├── tests/
│   ├── __init__.py              # Test package initialization
│   └── test_extractor.py        # Unit tests for extractor functionality
├── examples/
│   ├── README.md                # Examples documentation
│   ├── basic_usage.py           # Basic usage example
│   ├── extract_jcl_example.py   # JCL extraction example
│   └── extract_cobol_example.py # COBOL extraction example
├── docs/
│   └── README.md                # Documentation index
├── dist/                        # Built distributions (created by build)
├── build/                       # Build artifacts (created by build)
├── pyproject.toml               # Modern Python project configuration
├── setup.py                     # Legacy setup script (for compatibility)
├── README.md                    # Main project documentation
├── LICENSE                      # MIT license
├── CHANGELOG.md                 # Version history and changes
├── CONTRIBUTING.md              # Contribution guidelines
├── PUBLISHING.md                # Publishing and release guide
├── PROJECT_STRUCTURE.md         # This file
├── MANIFEST.in                  # Additional files to include in distribution
└── .gitignore                   # Git ignore patterns
```

## Key Files Description

### Core Package Files

- **`src/iebptpch_pds_extractor/__init__.py`**
  - Package initialization
  - Version information
  - Main exports (PDSExtractor, main)
  - Package metadata

- **`src/iebptpch_pds_extractor/extractor.py`**
  - PDSExtractor class implementation
  - Command-line interface (main function)
  - Argument parsing
  - Core extraction logic

### Configuration Files

- **`pyproject.toml`**
  - Modern Python project configuration
  - Build system requirements
  - Project metadata
  - Entry points for console scripts
  - Tool configurations

- **`setup.py`**
  - Legacy setup script for backward compatibility
  - Mirrors pyproject.toml configuration
  - Used by older build tools

### Documentation Files

- **`README.md`**
  - Main project documentation
  - Installation instructions
  - Usage examples
  - Feature descriptions

- **`CHANGELOG.md`**
  - Version history
  - Feature additions
  - Bug fixes
  - Breaking changes

- **`CONTRIBUTING.md`**
  - Contribution guidelines
  - Development setup
  - Code style requirements
  - Pull request process

### Testing and Examples

- **`tests/`**
  - Unit tests for all functionality
  - Test fixtures and utilities
  - Coverage for edge cases

- **`examples/`**
  - Practical usage examples
  - Sample data files
  - Different use case demonstrations

## Package Architecture

### Class Hierarchy

```
PDSExtractor
├── __init__(input_file, output_dir, **options)
├── validate_input() -> bool
├── detect_format() -> str
├── extract_member_name(line) -> Optional[str]
├── extract_members_from_ascii() -> int
├── extract_members_from_ebcdic() -> int
└── extract() -> int
```

### Module Dependencies

```
iebptpch_pds_extractor/
├── __init__.py
│   └── imports: extractor.PDSExtractor, extractor.main
└── extractor.py
    └── imports: re, os, sys, argparse, codecs, typing
```

### Entry Points

The package provides one console script entry point:
- `iebptpch-pds-extractor` → `iebptpch_pds_extractor:main`

## Build Artifacts

When building the package, the following artifacts are created:

### Source Distribution (`sdist`)
- `dist/iebptpch-pds-extractor-X.X.X.tar.gz`
- Contains all source files
- Can be built on any compatible platform

### Wheel Distribution (`bdist_wheel`)
- `dist/iebptpch_pds_extractor-X.X.X-py3-none-any.whl`
- Pre-built binary distribution
- Faster installation
- Platform-independent (pure Python)

## Development Workflow

### Setting Up Development Environment

1. Clone repository
2. Create virtual environment
3. Install in development mode: `pip install -e .`
4. Run tests: `python -m pytest tests/`

### Making Changes

1. Create feature branch
2. Make changes
3. Add/update tests
4. Update documentation
5. Run tests
6. Submit pull request

### Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Build package
5. Test on TestPyPI
6. Create Git tag
7. Publish to PyPI
8. Create GitHub release

## Design Principles

### Modularity
- Clear separation between CLI and API
- Reusable PDSExtractor class
- Minimal dependencies

### Robustness
- Comprehensive error handling
- Multiple fallback strategies
- Encoding detection and fallback

### Usability
- Simple command-line interface
- Comprehensive documentation
- Practical examples

### Maintainability
- Clean code structure
- Comprehensive tests
- Clear documentation

## Future Enhancements

Potential areas for expansion:
- GUI interface
- Additional input formats
- Batch processing capabilities
- Configuration file support
- Plugin architecture for custom processors
