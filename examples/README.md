# Examples

This directory contains example files and usage scenarios for the IEBPTPCH PDS Extractor.

## Files

- `sample_pds_output.txt` - Sample IEBPTPCH output file (ASCII format)
- `sample_ebcdic_output.txt` - Sample IEBPTPCH output file (EBCDIC format)
- `extract_jcl_example.py` - Python script showing how to extract JCL members
- `extract_cobol_example.py` - Python script showing how to extract COBOL members
- `basic_usage.py` - Basic usage example

## Running Examples

### Command Line Examples

Extract JCL members:
```bash
iebptpch-pds-extractor -i sample_pds_output.txt -o output_jcl -e jcl -v
```

Extract COBOL members from EBCDIC file:
```bash
iebptpch-pds-extractor -i sample_ebcdic_output.txt -o output_cobol -f ebcdic -e cbl -v
```

### Python API Examples

Run the Python examples:
```bash
python extract_jcl_example.py
python extract_cobol_example.py
python basic_usage.py
```

## Sample Data

The sample files contain mock PDS members for demonstration purposes. In a real scenario, you would:

1. Create IEBPTPCH output using JCL on your mainframe
2. Transfer the file to your local system
3. Use this tool to extract individual members
