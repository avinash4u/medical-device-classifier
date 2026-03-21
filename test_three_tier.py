#!/usr/bin/env python3
"""
Test the three-tier extraction system: Training Data -> LLM -> Regex Patterns
"""

import sys
sys.path.append('.')

from extraction_engine import ExtractionEngine
from training_data import TRAINING_EXAMPLES

def test_three_tier_extraction():
    """Test the three-tier extraction hierarchy"""
    
    # Initialize extraction engine
    extractor = ExtractionEngine(TRAINING_EXAMPLES)
    
    print("Testing Three-Tier Extraction System")
    print("=" * 50)
    print("Priority Order:")
    print("1. Training Data Set")
    print("2. LLM Extraction")
    print("3. Regex Patterns")
    print()
    
    # Test 1: Exact match from training data (should use Tier 1)
    print("Test 1: Exact training data match")
    test_text_1 = "CardioBand is a wearable device intended to continuously monitor heart rate and transmit data to a mobile application. It is designed for use in home environments."
    
    print(f"Input: {test_text_1}")
    result_1 = extractor.extract(test_text_1)
    
    print("Result:")
    print(f"  Device Name: {result_1.get('device_name', 'N/A')}")
    print(f"  Medical Purpose: {result_1.get('medical_purpose', 'N/A')}")
    print(f"  Body System: {result_1.get('body_system', 'N/A')}")
    print()
    
    # Test 2: Similar but not exact (should use Tier 1 if similarity > 80%)
    print("Test 2: High similarity training data match")
    test_text_2 = "CardioBand wearable device monitors heart rate and transmits data to mobile app for home use."
    
    print(f"Input: {test_text_2}")
    result_2 = extractor.extract(test_text_2)
    
    print("Result:")
    print(f"  Device Name: {result_2.get('device_name', 'N/A')}")
    print(f"  Medical Purpose: {result_2.get('medical_purpose', 'N/A')}")
    print(f"  Body System: {result_2.get('body_system', 'N/A')}")
    print()
    
    # Test 3: No training match (should fall back to Tier 2 LLM, then Tier 3 regex)
    print("Test 3: No training data match (fallback to LLM -> Regex)")
    test_text_3 = "NeuroPulse DBS is an implantable neurostimulation device for deep brain stimulation in Parkinson's disease patients."
    
    print(f"Input: {test_text_3}")
    result_3 = extractor.extract(test_text_3)
    
    print("Result:")
    print(f"  Device Name: {result_3.get('device_name', 'N/A')}")
    print(f"  Medical Purpose: {result_3.get('medical_purpose', 'N/A')}")
    print(f"  Body System: {result_3.get('body_system', 'N/A')}")
    print()
    
    # Test 4: Device name match from training data
    print("Test 4: Device name match from training data")
    test_text_4 = "NeuroScan AI analyzes brain imaging data to detect neurological abnormalities."
    
    print(f"Input: {test_text_4}")
    result_4 = extractor.extract(test_text_4)
    
    print("Result:")
    print(f"  Device Name: {result_4.get('device_name', 'N/A')}")
    print(f"  Medical Purpose: {result_4.get('medical_purpose', 'N/A')}")
    print(f"  Body System: {result_4.get('body_system', 'N/A')}")
    print()
    
    print("Three-tier extraction test completed!")

if __name__ == "__main__":
    test_three_tier_extraction()
