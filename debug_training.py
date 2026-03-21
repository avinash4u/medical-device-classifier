#!/usr/bin/env python3
"""
Debug the training data matching for NeuroScan AI
"""

import sys
sys.path.append('.')

from extraction_engine import ExtractionEngine
from training_data import TRAINING_EXAMPLES

def debug_training_match():
    """Debug the training data matching logic"""
    
    # Initialize extraction engine
    extractor = ExtractionEngine(TRAINING_EXAMPLES)
    
    # Test with NeuroScan AI
    test_text = "NeuroScan AI analyzes brain imaging data to detect neurological abnormalities."
    text_lower = test_text.lower()
    
    print("Debugging Training Data Match")
    print("=" * 40)
    print(f"Input text: {test_text}")
    print(f"Lower case: {text_lower}")
    print()
    
    # Check each training example
    for example_name, example_data in extractor.training_examples.items():
        raw_input = example_data['raw_input'].lower()
        canonical_object = example_data['canonical_object']
        device_name = canonical_object['device_name'].lower()
        
        print(f"Training Example: {example_name}")
        print(f"  Device Name: '{device_name}'")
        print(f"  Device Name in text: {device_name in text_lower}")
        print(f"  Length check: {len(device_name) > 3}")
        
        if device_name in text_lower and len(device_name) > 3:
            score = 0.3
            print(f"  Score: {score}")
        
        print()

if __name__ == "__main__":
    debug_training_match()
