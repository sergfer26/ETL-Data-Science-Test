#!/usr/bin/env python3
"""
Test script to demonstrate the parse_txt_file_to_dicts function
"""
import sys
import os

# Add src directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import parse_txt_file_to_dicts

def test_parse_function():
    """Test the parsing function with reporte_1.txt"""
    file_path = 'files/reporte_1.txt'
    
    # Parse the file
    dicts = parse_txt_file_to_dicts(file_path)
    
    print(f"Found {len(dicts)} records\n")
    print("=" * 80)
    
    # Display each record
    for idx, record in enumerate(dicts, 1):
        print(f"\nRecord {idx}:")
        print("-" * 40)
        for key, value in record.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    test_parse_function()
