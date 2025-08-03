# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-08-03

### Added
- New section in README explaining advantages over FTP clients
- Migration-focused benefits highlighting one-time binary transfer approach
- Comparison with traditional FTP client workflows
- Emphasis on encoding preservation and verification capabilities

### Changed
- Improved PyPI badges using shields.io for faster updates
- Enhanced documentation with practical migration scenarios

## [1.0.0] - 2025-08-03

### Added
- Initial release of IEBPTPCH PDS Extractor
- Support for extracting PDS members from IEBPTPCH output files
- Support for both ASCII and EBCDIC input formats
- Automatic format detection with manual override option
- Configurable EBCDIC encoding (default: cp037) with automatic fallback
- Custom file extensions for extracted members
- Customizable member name detection patterns with multiple fallback patterns
- Support for logical record length (LRECL) processing
- Robust error handling and encoding fallback mechanisms
- Command-line interface with comprehensive options
- Class-based API for programmatic usage
- Comprehensive documentation and examples
- Support for various mainframe file types (JCL, COBOL, Assembler, PL/I, REXX, etc.)
- Verbose output option for debugging
- Cross-platform compatibility (Windows, macOS, Linux)

### Features
- **Multi-format Support**: Handles both ASCII and EBCDIC input files
- **Automatic Detection**: Intelligently detects file format when not specified
- **Encoding Flexibility**: Supports 25+ EBCDIC encodings with automatic fallback
- **Pattern Matching**: Multiple member name detection patterns for improved compatibility
- **File Extensions**: Configurable file extensions for different source types
- **LRECL Support**: Proper handling of logical record lengths
- **Error Recovery**: Robust error handling with graceful degradation
- **No Dependencies**: Uses only Python standard library

### Supported File Types
- JCL (Job Control Language) files
- COBOL source files
- Assembler source files
- PL/I source files
- REXX scripts
- C source files
- Include files
- Procedure files
- Message files
- And more...
