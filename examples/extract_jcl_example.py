#!/usr/bin/env python3
"""
JCL extraction example for IEBPTPCH PDS Extractor

This example demonstrates how to extract JCL members from an IEBPTPCH output file.
"""

import os
import tempfile
from iebptpch_pds_extractor import PDSExtractor


def create_jcl_sample_data():
    """Create sample JCL PDS output data."""
    sample_data = """MEMBER NAME COMPILE
//COMPILE  JOB CLASS=A,MSGCLASS=X,NOTIFY=&SYSUID
//*
//* COBOL COMPILE JCL
//*
//STEP1    EXEC PGM=IGYCRCTL,PARM='OBJECT,MAP,LIST'
//STEPLIB  DD DSN=IGY.SIGYCOMP,DISP=SHR
//SYSLIB   DD DSN=MY.COBOL.COPYLIB,DISP=SHR
//SYSPRINT DD SYSOUT=*
//SYSLIN   DD DSN=&&OBJECT,DISP=(NEW,PASS),
//            UNIT=SYSDA,SPACE=(CYL,(1,1))
//SYSIN    DD DSN=MY.COBOL.SOURCE(PROGRAM1),DISP=SHR
//

MEMBER NAME LINK
//LINK     JOB CLASS=A,MSGCLASS=X,NOTIFY=&SYSUID
//*
//* LINK EDIT JCL
//*
//STEP1    EXEC PGM=IEWL,PARM='MAP,LIST,XREF'
//SYSLIB   DD DSN=CEE.SCEELKED,DISP=SHR
//         DD DSN=MY.LOAD.LIB,DISP=SHR
//SYSPRINT DD SYSOUT=*
//SYSLMOD  DD DSN=MY.LOAD.LIB(PROGRAM1),DISP=SHR
//SYSLIN   DD DSN=&&OBJECT,DISP=(OLD,DELETE)
//

MEMBER NAME BACKUP
//BACKUP   JOB CLASS=A,MSGCLASS=X,NOTIFY=&SYSUID
//*
//* BACKUP DATASETS JCL
//*
//STEP1    EXEC PGM=IEBGENER
//SYSPRINT DD SYSOUT=*
//SYSUT1   DD DSN=MY.SOURCE.LIB,DISP=SHR
//SYSUT2   DD DSN=MY.BACKUP.LIB,
//            DISP=(NEW,CATLG,DELETE),
//            UNIT=TAPE,VOL=SER=BACKUP1
//SYSIN    DD DUMMY
//
"""
    return sample_data


def main():
    """Main function demonstrating JCL extraction."""
    print("IEBPTPCH PDS Extractor - JCL Extraction Example")
    print("=" * 55)
    
    # Create temporary directory for this example
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample input file
        input_file = os.path.join(temp_dir, "jcl_library.txt")
        output_dir = os.path.join(temp_dir, "extracted_jcl")
        
        # Write sample JCL data
        with open(input_file, 'w') as f:
            f.write(create_jcl_sample_data())
        
        print(f"Created sample JCL library file: {input_file}")
        print(f"Output directory: {output_dir}")
        print()
        
        # Create extractor instance for JCL files
        extractor = PDSExtractor(
            input_file=input_file,
            output_dir=output_dir,
            file_format="ascii",
            extension="jcl",  # Add .jcl extension
            verbose=True
        )
        
        # Extract JCL members
        print("Extracting JCL members...")
        member_count = extractor.extract()
        
        print(f"\nJCL extraction completed successfully!")
        print(f"Total JCL members extracted: {member_count}")
        
        # Analyze extracted JCL files
        if os.path.exists(output_dir):
            print(f"\nExtracted JCL files:")
            for filename in sorted(os.listdir(output_dir)):
                filepath = os.path.join(output_dir, filename)
                file_size = os.path.getsize(filepath)
                
                # Count JCL statements
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                    jcl_statements = [line for line in lines if line.strip().startswith('//')]
                    comment_lines = [line for line in lines if line.strip().startswith('//*')]
                
                print(f"  - {filename}")
                print(f"    Size: {file_size} bytes")
                print(f"    Total lines: {len(lines)}")
                print(f"    JCL statements: {len(jcl_statements)}")
                print(f"    Comment lines: {len(comment_lines)}")
                
                # Show job name if present
                for line in lines:
                    if line.strip().startswith('//') and ' JOB ' in line:
                        job_name = line.split()[0][2:]  # Remove '//'
                        print(f"    Job name: {job_name}")
                        break
                print()


if __name__ == "__main__":
    main()
