#!/usr/bin/env python3
"""
IEBPTPCH PDS Extractor - Core extraction functionality

This module contains the PDSExtractor class and main functionality for extracting
PDS members from IEBPTPCH output files.
"""

import re
import os
import sys
import argparse
import codecs
from typing import Optional, List, Tuple


class PDSExtractor:
    """
    A class to extract PDS members from IEBPTPCH output files.
    
    This class handles both ASCII and EBCDIC formatted input files and can
    convert EBCDIC content to ASCII (UTF-8) during extraction.
    """
    
    def __init__(self, input_file: str, output_dir: str, file_format: str = "ascii",
                 extension: str = "", delimiter: str = r'MEMBER\s+NAME\s+(\S+)',
                 encoding: str = "cp037", lrecl: int = 81, verbose: bool = False):
        """
        Initialize the PDSExtractor.
        
        Args:
            input_file: Path to the input IEBPTPCH output file
            output_dir: Directory where extracted members will be saved
            file_format: Input file format ('ascii' or 'ebcdic')
            extension: File extension to add to extracted members (without dot)
            delimiter: Regular expression pattern to identify member names
            encoding: EBCDIC encoding to use for conversion (only used for EBCDIC files)
            lrecl: Logical record length
            verbose: Enable verbose output
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.file_format = file_format
        self.extension = extension
        self.delimiter = delimiter
        self.encoding = encoding
        self.lrecl = lrecl
        self.verbose = verbose
        
        # Member name detection patterns (fallback patterns)
        self.patterns = [
            delimiter,
            r'MEMBER\s+NAME\s+(\S+)',
            r'MEMBER:\s+(\S+)',
            r'NAME\s+(\S+)'
        ]
    
    def validate_input(self) -> bool:
        """Validate input file and output directory."""
        if not os.path.isfile(self.input_file):
            print(f"ERROR: Input file not found: {self.input_file}")
            return False
        
        if not os.path.isdir(self.output_dir):
            try:
                os.makedirs(self.output_dir)
                if self.verbose:
                    print(f"Created output directory: {self.output_dir}")
            except OSError as e:
                print(f"ERROR: Failed to create output directory: {self.output_dir}")
                print(f"       {e}")
                return False
        
        return True
    
    def detect_format(self) -> str:
        """
        Detect if the file is ASCII or EBCDIC.
        Returns 'ascii' or 'ebcdic'.
        """
        # If format is explicitly specified, use that
        if self.file_format.lower() == "ebcdic":
            return "ebcdic"
        elif self.file_format.lower() == "ascii":
            return "ascii"
        
        # Otherwise try to auto-detect
        try:
            with open(self.input_file, 'rb') as f:
                sample = f.read(4096)  # Read a sample of the file
                
            # Check for common EBCDIC characters
            ebcdic_count = 0
            for byte in sample:
                # Check for characters that are common in EBCDIC but rare in ASCII
                if byte in [0x4B, 0x5B, 0x6B, 0x7B, 0xC1, 0xD1, 0xE1, 0xF1]:
                    ebcdic_count += 1
            
            # If more than 10% of the sample contains EBCDIC-specific bytes, assume EBCDIC
            if ebcdic_count > len(sample) * 0.1:
                return "ebcdic"
            else:
                return "ascii"
        except Exception as e:
            if self.verbose:
                print(f"WARNING: Error detecting file format: {e}")
                print(f"         Defaulting to {self.file_format}")
            return self.file_format
    
    def extract_member_name(self, line: str) -> Optional[str]:
        """
        Extract member name from a line using various patterns.
        
        Args:
            line: The line to extract member name from
            
        Returns:
            The extracted member name or None if not found
        """
        # Try regex patterns first
        for pattern in self.patterns:
            matches = re.search(pattern, line)
            if matches and matches.groups():
                return matches.group(1)
        
        # If regex fails, try to parse from line structure
        parts = line.split()
        if len(parts) >= 3:
            return parts[2]
        elif len(parts) >= 1:
            return parts[0]
        
        return None
    
    def extract_members_from_ebcdic(self) -> int:
        """
        Extract PDS members from an EBCDIC file.
        Returns the number of extracted members.
        """
        member_count = 0
        current_outfile = None
        current_member = None
        
        try:
            # Read the entire file into memory
            with open(self.input_file, 'rb') as f:
                content = f.read()
            
            # Try to convert with the specified encoding
            try:
                if self.verbose:
                    print(f"Attempting to decode with {self.encoding} encoding")
                ascii_content = codecs.decode(content, self.encoding)
            except UnicodeDecodeError:
                # Try alternative encodings if the specified one fails
                try:
                    if self.encoding != "cp037":
                        if self.verbose:
                            print(f"Falling back to cp037 encoding")
                        ascii_content = codecs.decode(content, 'cp037')
                    else:
                        if self.verbose:
                            print(f"Falling back to cp500 encoding")
                        ascii_content = codecs.decode(content, 'cp500')
                except UnicodeDecodeError:
                    # If all else fails, replace undecodable characters
                    if self.verbose:
                        print(f"Using {self.encoding} with replacement for undecodable characters")
                    ascii_content = codecs.decode(content, self.encoding, errors='replace')
            
            # Split the content into records based on LRECL
            records = []
            for i in range(0, len(ascii_content), self.lrecl):
                if i + self.lrecl <= len(ascii_content):
                    record = ascii_content[i:i+self.lrecl]
                    records.append(record)
                else:
                    # Handle the last record which might be shorter than LRECL
                    record = ascii_content[i:]
                    records.append(record)
            
            if self.verbose:
                print(f"Processed {len(records)} records with LRECL = {self.lrecl}")
            
            # Process each record
            for record in records:
                if not record:
                    continue
                
                # Check for member name
                member_name = self.extract_member_name(record)
                
                if member_name:
                    # Close previous output file if any
                    if current_outfile:
                        current_outfile.close()
                    
                    current_member = member_name
                    
                    # Add extension if specified
                    if self.extension:
                        output_filename = f"{member_name}.{self.extension}"
                    else:
                        output_filename = member_name
                    
                    output_path = os.path.join(self.output_dir, output_filename)
                    
                    if self.verbose:
                        print(f"Extracting member: {member_name} to {output_path}")
                    
                    current_outfile = open(output_path, 'w', encoding='utf-8')
                    member_count += 1
                elif current_outfile:
                    # Write content record to current output file
                    # Skip the first character which is typically a carriage control character
                    if record and len(record) > 1:
                        content_line = record[1:] + '\n'
                        current_outfile.write(content_line)
        
        except Exception as e:
            print(f"ERROR: Failed to process file: {e}")
            if current_outfile:
                current_outfile.close()
            return member_count
        
        # Close the last output file
        if current_outfile:
            current_outfile.close()
        
        return member_count
    
    def extract_members_from_ascii(self) -> int:
        """
        Extract PDS members from an ASCII file.
        Returns the number of extracted members.
        """
        member_count = 0
        current_outfile = None
        current_member = None
        
        try:
            # Read the file line by line
            with open(self.input_file, 'r', encoding='utf-8') as infile:
                for line in infile:
                    line = line.rstrip('\r\n')
                    
                    if not line:
                        continue
                    
                    # Check for member name
                    member_name = self.extract_member_name(line)
                    
                    if member_name:
                        # Close previous output file if any
                        if current_outfile:
                            current_outfile.close()
                        
                        current_member = member_name
                        
                        # Add extension if specified
                        if self.extension:
                            output_filename = f"{member_name}.{self.extension}"
                        else:
                            output_filename = member_name
                        
                        output_path = os.path.join(self.output_dir, output_filename)
                        
                        if self.verbose:
                            print(f"Extracting member: {member_name} to {output_path}")
                        
                        current_outfile = open(output_path, 'w', encoding='utf-8')
                        member_count += 1
                    elif current_outfile:
                        # Write content line to current output file
                        # Skip the first character which is typically a carriage control character
                        if line and len(line) > 1:
                            content_line = line[1:] + '\n'
                            current_outfile.write(content_line)
        
        except Exception as e:
            print(f"ERROR: Failed to process file: {e}")
            if current_outfile:
                current_outfile.close()
            return member_count
        
        # Close the last output file
        if current_outfile:
            current_outfile.close()
        
        return member_count
    
    def extract(self) -> int:
        """
        Extract PDS members from the input file.
        
        Returns:
            The number of extracted members
        """
        # Validate input
        if not self.validate_input():
            return 0
        
        # Detect or use specified format
        detected_format = self.detect_format()
        if self.verbose:
            print(f"Processing file in {detected_format.upper()} format")
            print(f"Using LRECL = {self.lrecl}")
            if detected_format == "ebcdic":
                print(f"Using EBCDIC encoding: {self.encoding}")
        
        # Extract members based on file format
        if detected_format == "ebcdic":
            return self.extract_members_from_ebcdic()
        else:
            return self.extract_members_from_ascii()


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract PDS members from IEBPTPCH output files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract members from an ASCII file:
  iebptpch-pds-extractor -i input.txt -o output_dir

  # Extract members from an EBCDIC file:
  iebptpch-pds-extractor -i input.txt -o output_dir -f ebcdic

  # Extract JCL files with .jcl extension:
  iebptpch-pds-extractor -i JCL_LIBRARY.txt -o output_dir -e jcl

  # Extract COBOL source files with .cbl extension:
  iebptpch-pds-extractor -i COBOL_LIBRARY.txt -o output_dir -e cbl

  # Extract Assembler source files with .asm extension:
  iebptpch-pds-extractor -i ASM_LIBRARY.txt -o output_dir -e asm

  # Use a specific EBCDIC encoding:
  iebptpch-pds-extractor -i input.txt -o output_dir -f ebcdic -c cp500

  # Use a custom logical record length:
  iebptpch-pds-extractor -i input.txt -o output_dir -f ebcdic -l 133

  # Combine multiple options:
  iebptpch-pds-extractor -i COBOL_LIBRARY.txt -o output_dir -f ebcdic -e cbl -l 133 -v
"""
    )
    parser.add_argument(
        "-i", "--input", 
        required=True,
        help="Input IEBPTPCH output file path"
    )
    parser.add_argument(
        "-f", "--format", 
        choices=["ascii", "ebcdic"], 
        default="ascii",
        help="Input file format (ascii or ebcdic, default: ascii)"
    )
    parser.add_argument(
        "-o", "--output", 
        required=True,
        help="Output directory for extracted PDS members"
    )
    parser.add_argument(
        "-e", "--extension", 
        default="",
        help="File extension to add to extracted members (without dot, e.g., jcl, cbl, asm, proc, pli, rexx, c, inc, msg)"
    )
    parser.add_argument(
        "-d", "--delimiter", 
        default=r'MEMBER\s+NAME\s+(\S+)',
        help="Regular expression pattern to identify member names (default: 'MEMBER\\s+NAME\\s+(\\S+)')"
    )
    parser.add_argument(
        "-c", "--encoding", 
        default="cp037",
        help="EBCDIC encoding to use for conversion (default: cp037)"
    )
    parser.add_argument(
        "-l", "--lrecl", 
        type=int,
        default=81,  # Default to 80 + 1 (first char 'V')
        help="Logical record length (default: 81, which is 80 + 1 for the first character)"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


def main():
    """Main function for command line interface."""
    args = parse_arguments()
    
    # Create extractor instance
    extractor = PDSExtractor(
        input_file=args.input,
        output_dir=args.output,
        file_format=args.format,
        extension=args.extension,
        delimiter=args.delimiter,
        encoding=args.encoding,
        lrecl=args.lrecl,
        verbose=args.verbose
    )
    
    # Extract members
    member_count = extractor.extract()
    
    if member_count > 0:
        print(f"\nExtraction complete. {member_count} members extracted to {args.output}")
    else:
        print("\nNo members were extracted.")
        sys.exit(1)


if __name__ == "__main__":
    main()
