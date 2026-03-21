#!/usr/bin/env python3
"""
Debug the medical purpose extraction
"""

import sys
sys.path.append('.')

from extraction_engine import ExtractionEngine
from training_data import TRAINING_EXAMPLES

def debug_medical_purpose():
    """Debug the medical purpose extraction"""
    
    # Initialize extraction engine
    extractor = ExtractionEngine(TRAINING_EXAMPLES)
    
    # Test with the problematic case
    test_text = "NeuroScan AI analyzes brain imaging data to detect abnormalities and assist clinicians in interpretation."
    
    print("Debugging medical purpose extraction...")
    print(f"Input text: {test_text}")
    print()
    
    # Check the patterns
    print("Checking purpose examples:")
    for phrase, purpose_value in extractor.patterns.get('purpose_examples', {}).items():
        if phrase in test_text.lower():
            print(f"  MATCH: '{phrase}' -> '{purpose_value}'")
        else:
            print(f"  NO MATCH: '{phrase}'")
    
    print()
    print("Checking specific patterns:")
    text_lower = test_text.lower()
    if 'brain imaging' in text_lower and 'detect abnormalities' in text_lower:
        print("  MATCH: brain imaging + detect abnormalities")
    elif 'brain imaging' in text_lower and 'assist clinicians' in text_lower:
        print("  MATCH: brain imaging + assist clinicians")
    else:
        print("  NO MATCH on specific patterns")
        print(f"    'brain imaging' in text: {'brain imaging' in text_lower}")
        print(f"    'detect abnormalities' in text: {'detect abnormalities' in text_lower}")
        print(f"    'assist clinicians' in text: {'assist clinicians' in text_lower}")
    
    # Test the method directly
    print()
    print("Direct method call result:")
    purpose = extractor._extract_medical_purpose(test_text)
    print(f"  Result: '{purpose}'")

if __name__ == "__main__":
    debug_medical_purpose()
