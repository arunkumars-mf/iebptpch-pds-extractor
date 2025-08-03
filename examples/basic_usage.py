#!/usr/bin/env python3
"""
Basic usage example for IEBPTPCH PDS Extractor

This example demonstrates how to use the PDSExtractor class programmatically.
"""

import os
import tempfile
from iebptpch_pds_extractor import PDSExtractor


def create_sample_data():
    """Create sample IEBPTPCH output data for demonstration."""
    sample_data = """MEMBER NAME HELLO
//HELLO    JOB CLASS=A,MSGCLASS=X
//STEP1    EXEC PGM=IEFBR14
//

MEMBER NAME WORLD  
//WORLD    JOB CLASS=A,MSGCLASS=X
//STEP1    EXEC PGM=IEFBR14
//SYSPRINT DD SYSOUT=*
//

MEMBER NAME TEST
//TEST     JOB CLASS=A,MSGCLASS=X
//STEP1    EXEC PGM=HELLO
//STEPLIB  DD DSN=MY.LOAD.LIB,DISP=SHR
//SYSPRINT DD SYSOUT=*
//
"""
    return sample_data


def main():
    """Main function demonstrating basic usage."""
    print("IEBPTPCH PDS Extractor - Basic Usage Example")
    print("=" * 50)
    
    # Create temporary directory for this example
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample input file
        input_file = os.path.join(temp_dir, "sample_pds.txt")
        output_dir = os.path.join(temp_dir, "extracted_members")
        
        # Write sample data
        with open(input_file, 'w') as f:
            f.write(create_sample_data())
        
        print(f"Created sample input file: {input_file}")
        print(f"Output directory: {output_dir}")
        print()
        
        # Create extractor instance
        extractor = PDSExtractor(
            input_file=input_file,
            output_dir=output_dir,
            file_format="ascii",
            extension="jcl",  # Add .jcl extension to extracted files
            verbose=True
        )
        
        # Extract members
        print("Extracting PDS members...")
        member_count = extractor.extract()
        
        print(f"\nExtraction completed successfully!")
        print(f"Total members extracted: {member_count}")
        
        # List extracted files
        if os.path.exists(output_dir):
            print(f"\nExtracted files:")
            for filename in sorted(os.listdir(output_dir)):
                filepath = os.path.join(output_dir, filename)
                file_size = os.path.getsize(filepath)
                print(f"  - {filename} ({file_size} bytes)")
                
                # Show first few lines of each file
                print(f"    Content preview:")
                with open(filepath, 'r') as f:
                    lines = f.readlines()[:3]  # First 3 lines
                    for line in lines:
                        print(f"      {line.rstrip()}")
                    if len(lines) > 3:
                        print(f"      ... ({len(lines)} total lines)")
                print()


if __name__ == "__main__":
    main()
