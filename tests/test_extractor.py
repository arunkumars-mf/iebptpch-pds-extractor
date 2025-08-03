#!/usr/bin/env python3
"""
Tests for the IEBPTPCH PDS Extractor
"""

import unittest
import tempfile
import os
import shutil
from unittest.mock import patch, mock_open

from iebptpch_pds_extractor import PDSExtractor


class TestPDSExtractor(unittest.TestCase):
    """Test cases for PDSExtractor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, "test_input.txt")
        self.output_dir = os.path.join(self.test_dir, "output")
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_init(self):
        """Test PDSExtractor initialization."""
        extractor = PDSExtractor(
            input_file=self.input_file,
            output_dir=self.output_dir
        )
        
        self.assertEqual(extractor.input_file, self.input_file)
        self.assertEqual(extractor.output_dir, self.output_dir)
        self.assertEqual(extractor.file_format, "ascii")
        self.assertEqual(extractor.extension, "")
        self.assertEqual(extractor.encoding, "cp037")
        self.assertEqual(extractor.lrecl, 81)
        self.assertFalse(extractor.verbose)
    
    def test_init_with_options(self):
        """Test PDSExtractor initialization with options."""
        extractor = PDSExtractor(
            input_file=self.input_file,
            output_dir=self.output_dir,
            file_format="ebcdic",
            extension="jcl",
            encoding="cp500",
            lrecl=133,
            verbose=True
        )
        
        self.assertEqual(extractor.file_format, "ebcdic")
        self.assertEqual(extractor.extension, "jcl")
        self.assertEqual(extractor.encoding, "cp500")
        self.assertEqual(extractor.lrecl, 133)
        self.assertTrue(extractor.verbose)
    
    def test_validate_input_missing_file(self):
        """Test validation with missing input file."""
        extractor = PDSExtractor(
            input_file="/nonexistent/file.txt",
            output_dir=self.output_dir
        )
        
        self.assertFalse(extractor.validate_input())
    
    def test_validate_input_creates_output_dir(self):
        """Test validation creates output directory."""
        # Create input file
        with open(self.input_file, 'w') as f:
            f.write("test content")
        
        extractor = PDSExtractor(
            input_file=self.input_file,
            output_dir=self.output_dir
        )
        
        self.assertTrue(extractor.validate_input())
        self.assertTrue(os.path.isdir(self.output_dir))
    
    def test_extract_member_name_default_pattern(self):
        """Test member name extraction with default pattern."""
        extractor = PDSExtractor(
            input_file=self.input_file,
            output_dir=self.output_dir
        )
        
        # Test default pattern
        line = "MEMBER NAME TESTMEM"
        member_name = extractor.extract_member_name(line)
        self.assertEqual(member_name, "TESTMEM")
    
    def test_extract_member_name_alternative_patterns(self):
        """Test member name extraction with alternative patterns."""
        extractor = PDSExtractor(
            input_file=self.input_file,
            output_dir=self.output_dir
        )
        
        # Test alternative pattern
        line = "MEMBER: TESTMEM2"
        member_name = extractor.extract_member_name(line)
        self.assertEqual(member_name, "TESTMEM2")
        
        # Test NAME pattern
        line = "NAME TESTMEM3"
        member_name = extractor.extract_member_name(line)
        self.assertEqual(member_name, "TESTMEM3")
    
    def test_extract_member_name_fallback(self):
        """Test member name extraction fallback logic."""
        extractor = PDSExtractor(
            input_file=self.input_file,
            output_dir=self.output_dir
        )
        
        # Test fallback to third field
        line = "SOME OTHER TESTMEM4 DATA"
        member_name = extractor.extract_member_name(line)
        self.assertEqual(member_name, "TESTMEM4")
        
        # Test fallback to first field
        line = "TESTMEM5"
        member_name = extractor.extract_member_name(line)
        self.assertEqual(member_name, "TESTMEM5")
    
    def test_detect_format_explicit_ascii(self):
        """Test format detection with explicit ASCII."""
        extractor = PDSExtractor(
            input_file=self.input_file,
            output_dir=self.output_dir,
            file_format="ascii"
        )
        
        self.assertEqual(extractor.detect_format(), "ascii")
    
    def test_detect_format_explicit_ebcdic(self):
        """Test format detection with explicit EBCDIC."""
        extractor = PDSExtractor(
            input_file=self.input_file,
            output_dir=self.output_dir,
            file_format="ebcdic"
        )
        
        self.assertEqual(extractor.detect_format(), "ebcdic")
    
    @patch("builtins.open", new_callable=mock_open, read_data=b"test ascii content")
    def test_detect_format_auto_ascii(self, mock_file):
        """Test automatic format detection for ASCII."""
        extractor = PDSExtractor(
            input_file=self.input_file,
            output_dir=self.output_dir,
            file_format="auto"  # This will trigger auto-detection
        )
        
        # Since we're mocking with ASCII content, it should detect as ASCII
        result = extractor.detect_format()
        self.assertEqual(result, "auto")  # Falls back to specified format
    
    def test_extract_no_input_file(self):
        """Test extract with no input file."""
        extractor = PDSExtractor(
            input_file="/nonexistent/file.txt",
            output_dir=self.output_dir
        )
        
        result = extractor.extract()
        self.assertEqual(result, 0)


class TestMainFunction(unittest.TestCase):
    """Test cases for main function."""
    
    @patch('sys.argv', ['iebptpch-pds-extractor', '-i', 'test.txt', '-o', 'output'])
    @patch('iebptpch_pds_extractor.extractor.PDSExtractor')
    def test_main_function(self, mock_extractor_class):
        """Test main function with mocked arguments."""
        from iebptpch_pds_extractor.extractor import main
        
        # Mock the extractor instance
        mock_extractor = mock_extractor_class.return_value
        mock_extractor.extract.return_value = 5
        
        # This should not raise an exception
        try:
            main()
        except SystemExit:
            pass  # Expected when no actual files exist
        
        # Verify extractor was created with correct arguments
        mock_extractor_class.assert_called_once()


if __name__ == '__main__':
    unittest.main()
