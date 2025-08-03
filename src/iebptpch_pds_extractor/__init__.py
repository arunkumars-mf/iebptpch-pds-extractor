#!/usr/bin/env python3
"""
IEBPTPCH PDS Extractor - A utility to extract PDS members from IEBPTPCH output files

This package takes an IEBPTPCH output flat file (PDS to PS converted file),
determines the input data format (EBCDIC/ASCII), and extracts all PDS members
to an output directory. If the input is in EBCDIC format, it converts the content
to ASCII (UTF-8).
"""

import re
import os
import sys
import argparse
import codecs
from typing import Optional, List, Tuple

__version__ = "1.0.1"
__author__ = "Arunkumar Selvam"
__email__ = "aruninfy123@gmail.com"

# Export main classes and functions
from .extractor import PDSExtractor, main

__all__ = ['PDSExtractor', 'main']
