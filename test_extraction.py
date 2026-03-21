#!/usr/bin/env python3
"""
Test script for enhanced LLM-based extraction engine
"""

import os
import sys
sys.path.append('.')

from extraction_engine import ExtractionEngine
from training_data import TRAINING_EXAMPLES

def test_llm_extraction():
    """Test the enhanced LLM-first extraction"""
    
    # Initialize extraction engine
    extractor = ExtractionEngine(TRAINING_EXAMPLES)
    
    # Test with a sample device description
    test_text = """
    CardioBand is a wearable cardiac monitoring device intended for continuous monitoring of heart rate and rhythm in adults. 
    The device consists of a flexible adhesive patch with embedded sensors that connect to a mobile application. 
    CardioBand is intended for use by patients at home and is designed for long-term continuous monitoring. 
    The device monitors vital physiological parameters and assists in clinical diagnosis but does not independently diagnose conditions. 
    It is not intended to support or sustain life.
    """
    
    print("Testing enhanced LLM-first extraction...")
    print(f"Input text: {test_text[:100]}...")
    print()
    
    # Test extraction
    result = extractor.extract(test_text)
    
    print("Extraction Results:")
    print("=" * 50)
    for field, value in result.items():
        print(f"{field:25}: {value}")
    
    print()
    print("Testing completeness check...")
    missing, questions = extractor.check_completeness(result)
    
    if missing:
        print(f"Missing fields: {missing}")
        print("Questions to ask:")
        for field, question in questions.items():
            print(f"  {field}: {question}")
    else:
        print("✅ All required fields present!")
    
    print()
    print("Testing canonical object creation...")
    canonical = extractor.create_canonical_object(result)
    
    print("Canonical Object:")
    print("=" * 50)
    for field, value in canonical.items():
        print(f"{field:25}: {value}")

if __name__ == "__main__":
    test_llm_extraction()
