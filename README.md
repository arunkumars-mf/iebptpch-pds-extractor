# IEBPTPCH PDS Extractor

[![PyPI version](https://img.shields.io/pypi/v/iebptpch-pds-extractor.svg)](https://pypi.org/project/iebptpch-pds-extractor/)
[![Python versions](https://img.shields.io/pypi/pyversions/iebptpch-pds-extractor.svg)](https://pypi.org/project/iebptpch-pds-extractor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command line utility and Python library to extract PDS members from IEBPTPCH output files. This tool can handle both ASCII and EBCDIC formatted input files and convert EBCDIC content to ASCII (UTF-8) during extraction.

## Overview

This utility processes output files created by the IBM IEBPTPCH utility, which converts Partitioned Data Sets (PDS) to sequential files. The typical workflow is:

1. **Create IEBPTPCH output** using JCL (see [Creating IEBPTPCH Output](#creating-iebptpch-output))
2. **Transfer the file** from mainframe to your local system
3. **Extract individual members** using this Python utility

## Installation

### From PyPI (Recommended)

```bash
pip install iebptpch-pds-extractor
```

### From Source

```bash
git clone https://github.com/arunkumars-mf/iebptpch-pds-extractor.git
cd iebptpch-pds-extractor
pip install .
```

### Development Installation

```bash
git clone https://github.com/arunkumars-mf/iebptpch-pds-extractor.git
cd iebptpch-pds-extractor
pip install -e .
```

## Creating IEBPTPCH Output

Use this JCL to convert your PDS to a sequential file suitable for this extractor:

```jcl
//PDSEXTJ JOB 'PDS 2 PS',CLASS=A,MSGCLASS=X,NOTIFY=&SYSUID
//*
//IEBPTPCH EXEC PGM=IEBPTPCH
//*
//SYSUT1 DD DISP=SHR,DSN=<YOUR.SOURCE.LIBRARY>
//*
//SYSUT2 DD DSN=<YOUR.SOURCE.LIBRARY.PS>,
//          DISP=(NEW,CATLG,DELETE),UNIT=SYSDA,
//          SPACE=(CYL,(5,5),RLSE)
//*
//SYSPRINT DD SYSOUT=*
//SYSIN DD *
 PUNCH TYPORG=PO
/*
```

**Replace:**
- `<YOUR.SOURCE.LIBRARY>` with your actual PDS name
- `<YOUR.SOURCE.LIBRARY.PS>` with your desired output dataset name

**Notes:**
- The `PUNCH TYPORG=PO` control statement tells IEBPTPCH to process a partitioned dataset
- The output file will contain all PDS members with member name headers
- Transfer this output file to your local system for processing with this Python utility

## Features

- Extract individual PDS members from IEBPTPCH output files
- Support for both ASCII and EBCDIC input formats
- Automatic format detection with manual override option
- Configurable EBCDIC encoding (default: cp037) with automatic fallback to alternative encodings
- Add custom file extensions to extracted members
- Customizable member name detection pattern with multiple fallback patterns
- Support for logical record length (LRECL) processing
- Robust error handling and encoding fallback mechanisms
- Multiple member name detection patterns for improved compatibility
- Both command-line interface and Python API
- Cross-platform compatibility (Windows, macOS, Linux)

## Command Line Usage

After installation, the `iebptpch-pds-extractor` command will be available:

```bash
iebptpch-pds-extractor -i INPUT_FILE -o OUTPUT_DIRECTORY [options]
```

### Required Arguments

- `-i, --input`: Input IEBPTPCH output file path
- `-o, --output`: Output directory for extracted PDS members

### Optional Arguments

- `-f, --format`: Input file format (`ascii` or `ebcdic`, default: `ascii`)
- `-e, --extension`: File extension to add to extracted members (without dot)
- `-d, --delimiter`: Regular expression pattern to identify member names (default: `MEMBER\s+NAME\s+(\S+)`)
- `-c, --encoding`: EBCDIC encoding to use for conversion (default: `cp037`, only used when format is `ebcdic`)
- `-l, --lrecl`: Logical record length (default: 81, which is 80 + 1 for the first character)
- `-v, --verbose`: Enable verbose output

## Examples

### Basic Usage

Extract members from an ASCII file:

```bash
iebptpch-pds-extractor -i input.txt -o output_dir
```

### EBCDIC Input

Extract members from an EBCDIC file:

```bash
iebptpch-pds-extractor -i input.txt -o output_dir -f ebcdic
```

### Add File Extensions

Extract members and add file extensions based on content type:

#### JCL Files
```bash
iebptpch-pds-extractor -i JCL_LIBRARY.txt -o output_dir -e jcl
```

#### COBOL Source Files
```bash
iebptpch-pds-extractor -i COBOL_LIBRARY.txt -o output_dir -e cbl
```

#### Assembler Source Files
```bash
iebptpch-pds-extractor -i ASM_LIBRARY.txt -o output_dir -e asm
```

#### Other File Types
```bash
# Procedures
iebptpch-pds-extractor -i PROC_LIBRARY.txt -o output_dir -e proc

# PL/I Source Files
iebptpch-pds-extractor -i PLI_LIBRARY.txt -o output_dir -e pli

# REXX Scripts
iebptpch-pds-extractor -i REXX_LIBRARY.txt -o output_dir -e rexx

# Include Files
iebptpch-pds-extractor -i INCLUDE_LIBRARY.txt -o output_dir -e inc
```

### Advanced Options

Custom EBCDIC encoding:
```bash
iebptpch-pds-extractor -i input.txt -o output_dir -f ebcdic -c cp500
```

Custom delimiter pattern:
```bash
iebptpch-pds-extractor -i input.txt -o output_dir -d "^MEMBER:\s+(\S+)"
```

Custom LRECL:
```bash
iebptpch-pds-extractor -i input.txt -o output_dir -f ebcdic -l 133
```

Combining options:
```bash
iebptpch-pds-extractor -i COBOL_LIBRARY.txt -o output_dir -f ebcdic -e cbl -l 133 -v
```

## Python API Usage

You can also use the extractor programmatically:

```python
from iebptpch_pds_extractor import PDSExtractor

# Create extractor instance
extractor = PDSExtractor(
    input_file="path/to/input.txt",
    output_dir="path/to/output",
    file_format="ascii",  # or "ebcdic"
    extension="jcl",      # optional file extension
    verbose=True
)

# Extract members
member_count = extractor.extract()
print(f"Extracted {member_count} members")
```

### API Parameters

- `input_file` (str): Path to the input IEBPTPCH output file
- `output_dir` (str): Directory where extracted members will be saved
- `file_format` (str): Input file format ('ascii' or 'ebcdic', default: 'ascii')
- `extension` (str): File extension to add to extracted members (default: '')
- `delimiter` (str): Regular expression pattern to identify member names
- `encoding` (str): EBCDIC encoding to use for conversion (default: 'cp037')
- `lrecl` (int): Logical record length (default: 81)
- `verbose` (bool): Enable verbose output (default: False)

## Supported EBCDIC Encodings

### Common EBCDIC Encodings
- `cp037` - IBM EBCDIC US/Canada (default)
- `cp500` - IBM EBCDIC International
- `cp1047` - IBM EBCDIC Latin-1/Open Systems

### Country-specific EBCDIC Encodings
- `cp273` - IBM EBCDIC Germany
- `cp277` - IBM EBCDIC Denmark/Norway
- `cp278` - IBM EBCDIC Finland/Sweden
- `cp280` - IBM EBCDIC Italy
- `cp284` - IBM EBCDIC Spain
- `cp285` - IBM EBCDIC UK
- `cp297` - IBM EBCDIC France
- And many more...

For a complete list, see the [Python codecs documentation](https://docs.python.org/3/library/codecs.html#standard-encodings).

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses standard library only)

## How It Works

1. The script reads the input file in binary mode
2. If the format is EBCDIC, it converts each line to ASCII using the specified encoding
3. It processes the content based on the specified LRECL (logical record length)
4. It identifies member names using the provided delimiter pattern
5. For each member, it creates a new file in the output directory
6. Content lines are written to the appropriate member file, with the first character (carriage control) removed

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## Support

- **Issues**: [GitHub Issues](https://github.com/arunkumars-mf/iebptpch-pds-extractor/issues)
- **Documentation**: [Project Documentation](https://github.com/arunkumars-mf/iebptpch-pds-extractor#readme)
- **Examples**: [Examples Directory](examples/)

## Related Projects

- [COBOL Copybook to JSON](https://github.com/arunkumars-mf/cobol-copybook-to-json) - Convert COBOL copybooks to JSON schema format
