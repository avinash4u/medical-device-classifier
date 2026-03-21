#!/usr/bin/env python3
"""
Test the improved device name extraction
"""

import sys
sys.path.append('.')

from extraction_engine import ExtractionEngine
from training_data import TRAINING_EXAMPLES

def test_device_name_extraction():
    """Test the improved device name extraction"""
    
    # Initialize extraction engine
    extractor = ExtractionEngine(TRAINING_EXAMPLES)
    
    # Test with the problematic case
    test_text = "NeuroScan AI analyzes brain imaging data to detect abnormalities and assist clinicians in interpretation."
    
    print("Testing improved device name extraction...")
    print(f"Input text: {test_text}")
    print()
    
    # Test just the device name extraction
    device_name = extractor._extract_device_name(test_text)
    print(f"Extracted device name: '{device_name}'")
    
    # Test full extraction
    print("\nTesting full extraction:")
    result = extractor.extract(test_text)
    
    print("Extraction Results:")
    print("=" * 50)
    for field, value in result.items():
        print(f"{field:25}: {value}")

if __name__ == "__main__":
    test_device_name_extraction()
