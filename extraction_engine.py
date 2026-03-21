"""
Extraction Engine for Medical Device Intended Use
Uses training examples to extract and normalize fields
"""

import re
import json
import os
from typing import Dict, List, Tuple, Optional
from training_data import (
    TRAINING_EXAMPLES, 
    REQUIRED_FIELDS, 
    CLASSIFICATION_CRITICAL_FIELDS,
    FIELD_CLARIFICATION_QUESTIONS
)


class ExtractionEngine:
    """
    Extracts structured fields from intended use text
    Uses training examples as reference, NOT LLM for core extraction
    """
    
    def __init__(self, training_examples: Dict):
        self.training_examples = training_examples
        self.patterns = self._build_extraction_patterns()
    
    def _build_extraction_patterns(self) -> Dict:
        """Build regex and keyword patterns from training examples"""
        patterns = {}
        
        # Learn device name patterns from training data
        device_name_patterns = [r'Device Name:\s*([^\n.]+)', r'Product Name:\s*([^\n.]+)']
        for example_name, example_data in self.training_examples.items():
            raw_input = example_data['raw_input']
            device_name = example_data['canonical_object']['device_name']
            
            # Create pattern from this specific example
            if device_name in raw_input:
                # Find the device name in context
                idx = raw_input.find(device_name)
                context_start = max(0, idx - 20)
                context_end = min(len(raw_input), idx + len(device_name) + 20)
                context = raw_input[context_start:context_end]
                
                # Create a pattern from this context
                pattern = re.escape(device_name)
                device_name_patterns.append(pattern)
        
        patterns['device_name'] = device_name_patterns
        
        # Learn population patterns from training data
        population_examples = {}
        for example_data in self.training_examples.values():
            pop = example_data['canonical_object']['population']
            raw = example_data['raw_input'].lower()
            if pop.lower() in raw:
                population_examples[pop] = raw
        
        patterns['population_examples'] = population_examples
        
        # Learn structure/function patterns
        structure_examples = {}
        for example_data in self.training_examples.values():
            struct = example_data['canonical_object']['structure_function']
            raw = example_data['raw_input'].lower()
            # Look for key phrases from structure_function in raw input
            key_phrases = struct.lower().split()[:3]  # First 3 words
            for phrase in key_phrases:
                if phrase in raw and len(phrase) > 3:
                    structure_examples[phrase] = struct
        
        patterns['structure_examples'] = structure_examples
        
        # Learn medical purpose patterns
        purpose_examples = {}
        for example_data in self.training_examples.values():
            purpose = example_data['canonical_object']['medical_purpose']
            raw = example_data['raw_input'].lower()
            key_phrases = purpose.lower().split()[:3]  # First 3 words
            for phrase in key_phrases:
                if phrase in raw and len(phrase) > 3:
                    purpose_examples[phrase] = purpose
        
        patterns['purpose_examples'] = purpose_examples
        
        # Keep existing keyword-based patterns for other fields
        patterns['invasiveness'] = {
            'non-invasive': ['non-invasive', 'contactless', 'wearable', 'adhesive', 'skin contact', 'external'],
            'invasive_via_orifice': ['invasive', 'catheter', 'endoscope', 'intravascular', 'via orifice'],
            'surgically_invasive': ['surgically', 'surgical', 'implant', 'intracranial', 'deep brain']
        }
        patterns['implantable'] = {
            True: ['implant', 'permanently', 'long-term implant', 'remains in place', 'surgically implanted'],
            False: ['wearable', 'adhesive', 'single-use', 'transient', 'temporary']
        }
        patterns['duration'] = {
            'transient': ['transient', 'single-use', 'episode', '<60 min'],
            'short_term': ['short-term', 'up to 72 hours', '<30 days'],
            'long_term': ['long-term', 'continuous', 'permanent', '>30 days', 'chronic']
        }
        patterns['active'] = {
            True: ['electrically powered', 'active', 'programmable', 'powered', 'electric'],
            False: ['passive', 'sterile', 'adhesive', 'mechanical', 'non-powered']
        }
        
        # Add missing patterns for other fields
        patterns['delivers_medicinal_substance'] = {
            True: ['deliver medication', 'drug delivery', 'medicinal substance', 'pharmaceutical', 'infusion'],
            False: []
        }
        patterns['delivers_energy'] = {
            True: ['electrical stimulation', 'energy', 'radiation', 'laser', 'radiofrequency', 'ultrasound'],
            False: []
        }
        patterns['monitors_vital_parameter'] = {
            True: ['monitor', 'measure', 'vital', 'heart rate', 'respiratory rate', 'blood pressure', 'ECG'],
            False: []
        }
        patterns['body_system'] = {
            'cardiovascular': ['heart', 'cardiac', 'vascular', 'blood'],
            'respiratory': ['respiratory', 'breathing', 'lung', 'airway'],
            'central_nervous_system': ['brain', 'neural', 'CNS', 'neurological', 'deep brain'],
            'skeletal': ['bone', 'orthopedic', 'vertebral', 'fracture', 'skeletal'],
            'skin': ['skin', 'dermal', 'wound', 'superficial']
        }
        patterns['diagnostic_role'] = {
            'none': ['not diagnostic', 'does not diagnose'],
            'assists': ['assist', 'support clinical', 'aid in', 'help identify'],
            'independent': ['diagnose', 'diagnostic decision', 'independently establish']
        }
        patterns['life_supporting'] = {
            True: ['life-supporting', 'life-sustaining', 'critical to life'],
            False: ['not life-supporting', 'does not support life']
        }
        
        return patterns
    
    def extract(self, text: str) -> Dict:
        """
        Extract fields using three-tier hierarchy:
        1. Training data set (highest priority)
        2. LLM extraction (second priority)
        3. Regex patterns (final fallback)
        """
        print(f"DEBUG: Starting three-tier extraction with text: {text[:100]}...")
        extracted = {}
        
        # Tier 1: Training data set - highest priority
        print("DEBUG: Tier 1 - Trying training data set extraction...")
        training_result = self._extract_from_training_data(text)
        if training_result:
            extracted = training_result
            print("DEBUG: Training data extraction successful")
        else:
            print("DEBUG: No training data match found")
            
            # Tier 2: LLM extraction - second priority
            print("DEBUG: Tier 2 - Trying LLM extraction...")
            llm_result = self._llm_extract_all_fields(text)
            if llm_result:
                extracted = llm_result
                print("DEBUG: LLM extraction successful")
            else:
                print("DEBUG: LLM extraction failed")
                
                # Tier 3: Regex patterns - final fallback
                print("DEBUG: Tier 3 - Using regex pattern fallback...")
                extracted = self._pattern_extract_all_fields(text)
        
        # Validate and enhance with keyword matching for critical fields
        extracted = self._validate_and_enhance_extraction(extracted, text)
        
        print(f"DEBUG: Final extraction complete: {extracted}")
        return extracted
    
    def _extract_from_training_data(self, text: str) -> Optional[Dict]:
        """
        Extract fields by finding exact or very similar matches in training data set
        This is the highest priority extraction method
        """
        text_lower = text.lower()
        best_match = None
        best_score = 0
        
        print("DEBUG: Searching training data for matches...")
        
        for example_name, example_data in self.training_examples.items():
            raw_input = example_data['raw_input'].lower()
            canonical_object = example_data['canonical_object']
            
            # Calculate similarity score
            score = 0
            
            # Exact match check
            if text_lower == raw_input:
                print(f"DEBUG: Exact match found with: {example_name}")
                return canonical_object.copy()
            
            # High similarity check (80%+ words in common)
            text_words = set(text_lower.split())
            input_words = set(raw_input.split())
            
            if text_words and input_words:
                common_words = text_words.intersection(input_words)
                similarity = len(common_words) / max(len(text_words), len(input_words))
                
                if similarity > 0.8:  # 80% similarity threshold
                    score = similarity
                    if score > best_score:
                        best_score = score
                        best_match = example_name
                        print(f"DEBUG: High similarity match ({score:.2f}) with: {example_name}")
            
            # Check for device name match
            device_name = canonical_object['device_name'].lower()
            if device_name in text_lower and len(device_name) > 3:
                score = max(score, 0.8)  # Give high score for device name match
                if score > best_score:
                    best_score = score
                    best_match = example_name
                    print(f"DEBUG: Device name match with: {example_name} (score: {score})")
        
        # If we found a good match, return the canonical object
        if best_match and best_score > 0.5:  # Lowered threshold from 0.7 to 0.5
            print(f"DEBUG: Using best training match: {best_match} (score: {best_score:.2f})")
            return self.training_examples[best_match]['canonical_object'].copy()
        
        print("DEBUG: No suitable training data match found")
        return None
    
    def _llm_extract_all_fields(self, text: str) -> Optional[Dict]:
        """Use LLM to extract all fields in one call for better context"""
        try:
            import google.generativeai as genai
            
            # Get API key from environment
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                print("DEBUG: GEMINI_API_KEY not found in environment")
                return None
                
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Comprehensive prompt for all fields
            prompt = f"""
You are a medical device regulatory expert. Extract ALL classification-critical fields from this text.
Return ONLY valid JSON with these exact fields:

{{
  "device_name": "string",
  "structure_function": "string", 
  "medical_purpose": "string",
  "population": "string",
  "intended_user": "string",
  "use_environment": "string",
  "invasiveness": "non-invasive|invasive_via_orifice|surgically_invasive",
  "implantable": true/false,
  "duration": "transient|short_term|long_term",
  "body_system": "cardiovascular|respiratory|central_nervous_system|skeletal|skin|other",
  "active": true/false,
  "delivers_medicinal_substance": true/false,
  "delivers_energy": true/false,
  "monitors_vital_parameter": true/false,
  "diagnostic_role": "none|assists|independent",
  "life_supporting": true/false
}}

Guidelines:
- Be precise and conservative
- If uncertain, choose the lower risk option
- Use exact values from the enum options
- device_name: Just the name, no description
- structure_function: Physical components and how they work
- medical_purpose: What it does medically
- population: Who it's for (adults, neonates, etc.)
- intended_user: Who operates it
- use_environment: Where it's used

Text: {text}

JSON:"""
            
            print(f"DEBUG: Calling Gemini for comprehensive extraction...")
            
            response = model.generate_content(prompt)
            result = response.text.strip()
            
            print(f"DEBUG: Gemini response: {result[:200]}...")
            
            # Parse JSON response
            import json
            try:
                # Clean up response
                result = re.sub(r'^.*?{', '{', result, flags=re.DOTALL)
                result = re.sub(r'}.*$', '}', result, flags=re.DOTALL)
                
                extracted = json.loads(result)
                
                # Validate required fields
                if self._validate_llm_extraction(extracted):
                    print("DEBUG: LLM extraction validated successfully")
                    return extracted
                else:
                    print("DEBUG: LLM extraction validation failed")
                    return None
                    
            except json.JSONDecodeError as e:
                print(f"DEBUG: JSON parsing error: {e}")
                return None
                
        except ImportError:
            print("DEBUG: Google Generative AI not available")
            return None
        except Exception as e:
            print(f"DEBUG: Gemini API error: {e}")
            return None
    
    def _validate_llm_extraction(self, extracted: Dict) -> bool:
        """Validate LLM extraction results"""
        required_fields = ['device_name', 'structure_function', 'medical_purpose']
        
        for field in required_fields:
            if not extracted.get(field) or len(extracted.get(field, '')) < 3:
                return False
        
        # Validate enum fields
        valid_invasiveness = ['non-invasive', 'invasive_via_orifice', 'surgically_invasive']
        if extracted.get('invasiveness') and extracted['invasiveness'] not in valid_invasiveness:
            return False
            
        valid_duration = ['transient', 'short_term', 'long_term']
        if extracted.get('duration') and extracted['duration'] not in valid_duration:
            return False
            
        valid_diagnostic = ['none', 'assists', 'independent']
        if extracted.get('diagnostic_role') and extracted['diagnostic_role'] not in valid_diagnostic:
            return False
        
        return True
    
    def _pattern_extract_all_fields(self, text: str) -> Dict:
        """Fallback pattern-based extraction"""
        text_lower = text.lower()
        extracted = {}
        
        # Use existing pattern-based methods
        extracted['device_name'] = self._extract_device_name(text)
        extracted['structure_function'] = self._extract_structure_function(text)
        extracted['medical_purpose'] = self._extract_medical_purpose(text)
        extracted['population'] = self._extract_population(text)
        extracted['intended_user'] = self._extract_user(text)
        extracted['use_environment'] = self._extract_environment(text)
        
        # Classification fields via keyword matching
        extracted['invasiveness'] = self._match_keywords(text_lower, self.patterns['invasiveness'])
        extracted['implantable'] = self._match_keywords(text_lower, self.patterns['implantable'])
        extracted['duration'] = self._match_keywords(text_lower, self.patterns['duration'])
        extracted['body_system'] = self._match_keywords(text_lower, self.patterns['body_system'])
        extracted['active'] = self._match_keywords(text_lower, self.patterns['active'])
        extracted['delivers_medicinal_substance'] = self._match_keywords(text_lower, self.patterns['delivers_medicinal_substance'])
        extracted['delivers_energy'] = self._match_keywords(text_lower, self.patterns['delivers_energy'])
        extracted['monitors_vital_parameter'] = self._match_keywords(text_lower, self.patterns['monitors_vital_parameter'])
        extracted['diagnostic_role'] = self._match_keywords(text_lower, self.patterns['diagnostic_role'])
        extracted['life_supporting'] = self._match_keywords(text_lower, self.patterns['life_supporting'])
        
        # Infer generic category
        extracted['generic_category'] = self._infer_category(extracted)
        
        return extracted
    
    def _validate_and_enhance_extraction(self, extracted: Dict, text: str) -> Dict:
        """Validate and enhance extraction with keyword matching"""
        text_lower = text.lower()
        
        # Ensure generic category
        if not extracted.get('generic_category'):
            extracted['generic_category'] = self._infer_category(extracted)
        
        # Enhance boolean fields with keyword validation
        boolean_fields = ['implantable', 'active', 'delivers_medicinal_substance', 
                          'delivers_energy', 'monitors_vital_parameter', 'life_supporting']
        
        for field in boolean_fields:
            if field in self.patterns:
                keyword_result = self._match_keywords(text_lower, self.patterns[field])
                if keyword_result is not None and extracted.get(field) is None:
                    extracted[field] = keyword_result
        
        # Enhance enum fields with keyword validation
        enum_fields = ['invasiveness', 'duration', 'body_system', 'diagnostic_role']
        
        for field in enum_fields:
            if field in self.patterns and not extracted.get(field):
                keyword_result = self._match_keywords(text_lower, self.patterns[field])
                if keyword_result:
                    extracted[field] = keyword_result
        
        return extracted
    
    def _extract_device_name(self, text: str) -> str:
        """Extract device name using learned patterns from training data"""
        # Remove "RAW INPUT" prefix if present
        text = re.sub(r'^RAW INPUT\s*', '', text, flags=re.IGNORECASE).strip()
        
        # First try explicit "Device Name:" pattern
        match = re.search(r'Device Name:\s*([^\n.]+)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Try to find a capitalized phrase at the beginning of the text
        # Look for patterns like "DeviceName action..." or "DeviceName is..."
        beginning_patterns = [
            r'^([A-Z][a-zA-Z0-9\s-]{3,50})\s+(?:analyzes|assists|detects|monitors|measures|treats|diagnoses|is)',
            r'^([A-Z][a-zA-Z0-9\s-]{3,50})(?=\s+(?:analyzes|assists|detects|monitors|measures|treats|diagnoses|is))',
            r'^([A-Z][a-zA-Z0-9\s-]{3,50})',
        ]
        
        for pattern in beginning_patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
                if len(name.split()) <= 6: # Allow slightly longer names at the beginning
                    return name

        # Additional patterns for device names followed by action verbs
        action_patterns = [
            r'([A-Z][a-zA-Z0-9\s-]{3,30})\s+(?:analyzes|assists|detects|monitors|measures|treats|diagnoses)',
            r'([A-Z][a-zA-Z0-9\s-]{3,30})\s+is\s+(?:analyzing|assisting|detecting|monitoring|measuring|treating|diagnosing)',
            r'([A-Z][a-zA-Z0-9\s-]{3,30})\s+(?:provides|delivers|offers|generates)',
        ]
        
        for pattern in action_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name.split()) <= 4:  # Reasonable length for device name
                    return name

        # Additional fallback: look for capitalized device names before "is intended"
        match = re.search(r'([A-Z][a-zA-Z0-9\s-]{3,30})\s+is\s+intended\s+for', text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name.split()) <= 4:
                return name
        
        # Fallback: look for [Name] is a [device] pattern anywhere in text
        match = re.search(r'([A-Z][a-zA-Z0-9\s-]{3,30})\s+is\s+(?:a|an|intended)', text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name.split()) <= 4:  # Reasonable length for device name
                return name
        
        # Try patterns learned from training data last (they might be problematic)
        for pattern in self.patterns['device_name']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and match.groups():
                return match.group(1).strip()
        
        # LLM fallback as last resort
        return self._llm_extract_device_name(text)
    
    def _llm_extract_device_name(self, text: str) -> str:
        """Use Gemini to extract device name as fallback"""
        try:
            import google.generativeai as genai
            
            # Get API key from environment
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                print("DEBUG: GEMINI_API_KEY not found in environment")
                return ""
                
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Simple prompt for device name extraction
            prompt = f"""
Extract ONLY the device name from this text. Return just the device name, no explanation.

Text: {text}

Device Name:"""
            
            print(f"DEBUG: Calling Gemini for device_name with text: {text[:100]}...")
            
            # Use Gemini
            response = model.generate_content(prompt)
            device_name = response.text.strip()
            
            print(f"DEBUG: Gemini response for device_name: {device_name}")
            
            # Clean up the response
            device_name = re.sub(r'["\']', '', device_name)
            device_name = re.sub(r'^.*?:\s*', '', device_name)  # Remove field name prefix
            
            # Validate result
            if len(device_name.split()) <= 6 and len(device_name) > 3:
                print(f"DEBUG: Validated device_name: {device_name}")
                return device_name
            else:
                print(f"DEBUG: Invalid device_name length: {len(device_name.split())}")
                
        except ImportError:
            print("DEBUG: Google Generative AI not available")
            pass
        except Exception as e:
            print(f"DEBUG: Gemini API error for device_name: {e}")
            pass
        
        return ""
    
    def _extract_structure_function(self, text: str) -> str:
        """Extract structure and function using learned patterns from training data"""
        # First try to match structure patterns from training examples
        for phrase, struct_value in self.patterns.get('structure_examples', {}).items():
            if phrase in text.lower():
                return struct_value
        
        # Fallback to basic patterns
        patterns = [
            r'(?:consists of|utilizes|features?)\s+([^.]+)',
            r'([^.]*?(?:sensor|system|device|technology|mechanism)[^.]*?)(?:\.|and|for)',
            r'(?:device|system)\s+([^.]*?(?:under|beneath|using|with)[^.]*?)(?:\.|and)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                structure = match.group(1).strip()
                # Clean up and limit length
                structure = re.sub(r'\s+', ' ', structure)
                if len(structure) < 100 and len(structure) > 10:
                    return structure
        
        # LLM fallback
        return self._llm_extract_field(text, "structure and function", "device structure, components, and how it works")
    
    def _extract_medical_purpose(self, text: str) -> str:
        """Extract medical purpose using learned patterns from training data"""
        text_lower = text.lower()
        
        # Look for specific patterns in the current text FIRST
        if 'brain imaging' in text_lower and 'detect abnormalities' in text_lower:
            return "Detection of brain abnormalities from imaging data"
        elif 'brain imaging' in text_lower and 'assist clinicians' in text_lower:
            return "Assistance in interpretation of brain imaging data"
        elif 'heart rate' in text_lower and 'monitor' in text_lower:
            return "Monitoring of heart rate and rhythm"
        elif 'cardiac' in text_lower and 'monitor' in text_lower:
            return "Cardiac monitoring and rhythm analysis"
        
        # Then try to match purpose patterns from training examples
        for phrase, purpose_value in self.patterns.get('purpose_examples', {}).items():
            if phrase in text_lower:
                return purpose_value
        
        # Fallback to basic patterns
        patterns = [
            r'intended (?:for|to)\s+([^.]+(?:measure|monitor|detect|diagnose|treat|deliver)[^.]*?)\s*(?:\.|and|or)',
            r'for (?:the )?([^.]*?(?:measurement|monitoring|detection|diagnosis|treatment|delivery)[^.]*?)\s*(?:\.|and|or)',
            r'(?:purpose|function):\s*([^.]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                purpose = match.group(1).strip()
                # Clean up common issues
                purpose = re.sub(r'\s+', ' ', purpose)
                if len(purpose) < 150 and len(purpose) > 10:
                    return purpose
        
        # LLM fallback
        return self._llm_extract_field(text, "medical purpose", "what the device does medically")
    
    def _llm_extract_field(self, text: str, field_name: str, description: str) -> str:
        """Use Gemini to extract specific field as fallback"""
        try:
            import google.generativeai as genai
            
            # Get API key from environment
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                print(f"DEBUG: GEMINI_API_KEY not found in environment")
                return ""
                
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Simple prompt for field extraction
            prompt = f"""
Extract ONLY the {field_name} from this medical device text. {description}.
Return just the {field_name}, no explanation.

Text: {text}

{field_name.title()}:"""
            
            print(f"DEBUG: Calling Gemini for {field_name} with text: {text[:100]}...")
            
            # Use Gemini
            response = model.generate_content(prompt)
            result = response.text.strip()
            
            print(f"DEBUG: Gemini response for {field_name}: {result}")
            
            # Clean up the response
            result = re.sub(r'["\']', '', result)
            result = re.sub(r'^.*?:\s*', '', result)  # Remove field name prefix
            
            # Validate result
            if len(result) > 3 and len(result) < 200:
                print(f"DEBUG: Validated {field_name}: {result}")
                return result
            else:
                print(f"DEBUG: Invalid {field_name} length: {len(result)}")
                
        except ImportError:
            print("DEBUG: Google Generative AI not available")
            pass
        except Exception as e:
            print(f"DEBUG: Gemini API error for {field_name}: {e}")
            pass
        
        return ""
    
    def _extract_population(self, text: str) -> str:
        """Extract population using learned patterns from training data"""
        # First try to match exact population values from training examples
        for pop_value, raw_text in self.patterns.get('population_examples', {}).items():
            if pop_value.lower() in text.lower():
                return pop_value
        
        # Fallback to simple keyword detection
        text_lower = text.lower()
        if 'neonate' in text_lower:
            return "Neonates"
        elif 'pediatric' in text_lower:
            return "Pediatric patients"
        elif 'adult' in text_lower:
            return "Adults"
        elif 'patient' in text_lower:
            return "Patients"
        
        return ""
    
    def _extract_user(self, text: str) -> str:
        """Extract intended user using learned patterns from training data"""
        # First try to match exact user values from training examples
        text_lower = text.lower()
        
        # Check for surgical context -> Orthopedic surgeons
        if 'orthopedic surgery' in text_lower or 'orthopedic' in text_lower and 'surgery' in text_lower:
            return "Orthopedic surgeons"
        
        # Check for surgical context general -> Surgeons
        if 'surgery' in text_lower or 'surgical' in text_lower:
            return "Surgeons"
        
        # Check for NICU context -> NICU clinicians
        if 'nicu' in text_lower or 'neonatal intensive care' in text_lower:
            return "NICU clinicians"
        
        # Check for hospital/clinical context
        if 'hospital' in text_lower or 'clinical' in text_lower:
            if 'licensed' in text_lower or 'physician' in text_lower:
                return "Licensed physicians"
            else:
                return "Healthcare professionals"
        
        # Check for self-use keywords
        if 'self-use' in text_lower or ('patient' in text_lower and 'home' in text_lower):
            return "Patients (self-use)"
        
        # Fallback to basic patterns
        user_patterns = [
            r'(?:operated|used) by ([^.]+)',
            r'for use by ([^.]+)',
            r'intended for ([^.]+) in ',
        ]
        
        for pattern in user_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_environment(self, text: str) -> str:
        """Extract use environment"""
        environments = ['hospital', 'home', 'clinic', 'operating room', 'NICU', 'ICU', 'clinical']
        text_lower = text.lower()
        
        for env in environments:
            if env in text_lower:
                return env.title()
        return ""
    
    def _match_keywords(self, text: str, keyword_dict: Dict) -> any:
        """Match text against keyword dictionary"""
        if not keyword_dict:
            return None
        
        # Count matches for each option
        scores = {}
        for key, keywords in keyword_dict.items():
            if not keywords:  # Empty list means no keywords = default False
                continue
            score = sum(1 for kw in keywords if kw.lower() in text)
            if score > 0:
                scores[key] = score
        
        if scores:
            # Return key with highest score
            return max(scores, key=scores.get)
        
        # For boolean fields, default to False/unknown
        if True in keyword_dict or False in keyword_dict:
            return None  # Unknown
        
        return None
    
    def _infer_category(self, extracted: Dict) -> str:
        """Infer generic category from extracted fields"""
        name = extracted.get('device_name', '').lower()
        structure = extracted.get('structure_function', '').lower()
        
        categories = {
            'monitor': ['monitor', 'monitoring', 'sensor'],
            'pump': ['pump', 'infusion'],
            'implant': ['implant', 'screw', 'bone'],
            'dressing': ['dressing', 'bandage'],
            'patch': ['patch'],
            'software': ['software', 'AI', 'algorithm'],
            'stimulator': ['stimulator', 'stimulation'],
        }
        
        combined = name + ' ' + structure
        
        for cat, keywords in categories.items():
            if any(kw in combined for kw in keywords):
                return cat.title()
        
        return "Medical Device"
    
    def check_completeness(self, extracted: Dict) -> Tuple[List[str], Dict]:
        """
        Check if all required and classification-critical fields are present
        Returns: (list of missing fields, dict of clarification questions)
        """
        missing = []
        questions = {}
        
        # Check required fields
        for field in REQUIRED_FIELDS:
            if not extracted.get(field) or extracted.get(field) == "":
                missing.append(field)
                if field in FIELD_CLARIFICATION_QUESTIONS:
                    questions[field] = FIELD_CLARIFICATION_QUESTIONS[field]
        
        # Check classification-critical fields
        for field in CLASSIFICATION_CRITICAL_FIELDS:
            value = extracted.get(field)
            if value is None or value == "" or value == "unknown":
                missing.append(field)
                if field in FIELD_CLARIFICATION_QUESTIONS:
                    questions[field] = FIELD_CLARIFICATION_QUESTIONS[field]
        
        return missing, questions
    
    def create_canonical_object(self, extracted: Dict) -> Dict:
        """
        Create canonical classification object from extracted data
        Ensures all fields are properly formatted
        """
        canonical = {
            'device_name': extracted.get('device_name', ''),
            'generic_category': extracted.get('generic_category', ''),
            'structure_function': extracted.get('structure_function', ''),
            'medical_purpose': extracted.get('medical_purpose', ''),
            'population': extracted.get('population', ''),
            'intended_user': extracted.get('intended_user', ''),
            'use_environment': extracted.get('use_environment', ''),
            'invasiveness': extracted.get('invasiveness', ''),
            'implantable': bool(extracted.get('implantable', False)),
            'duration': extracted.get('duration', ''),
            'body_system': extracted.get('body_system', ''),
            'active': bool(extracted.get('active', False)),
            'delivers_medicinal_substance': bool(extracted.get('delivers_medicinal_substance', False)),
            'delivers_energy': bool(extracted.get('delivers_energy', False)),
            'monitors_vital_parameter': bool(extracted.get('monitors_vital_parameter', False)),
            'diagnostic_role': extracted.get('diagnostic_role', 'none'),
            'life_supporting': bool(extracted.get('life_supporting', False))
        }
        
        return canonical
    
    def generate_intended_use(self, canonical: Dict) -> str:
        """
        Generate formal intended use statement from canonical object
        Follows the structure seen in training examples
        """
        parts = []
        
        # Opening: Device name and classification
        device_name = canonical['device_name']
        
        # Build descriptors
        descriptors = []
        
        # Invasiveness
        if canonical['invasiveness']:
            descriptors.append(canonical['invasiveness'].replace('_', ' '))
        
        # Active/passive
        if canonical['active']:
            descriptors.append('electrically powered')
        
        # Generic category
        if canonical['generic_category']:
            descriptors.append(canonical['generic_category'].lower())
        
        # Opening sentence
        opening = f"{device_name} is a {', '.join(descriptors)} device intended for"
        
        # Medical purpose
        purpose = canonical['medical_purpose']
        if purpose:
            opening += f" {purpose}"
        
        # Population
        if canonical['population']:
            opening += f" in {canonical['population']}"
        
        parts.append(opening + ".")
        
        # Structure and function
        if canonical['structure_function']:
            parts.append(canonical['structure_function'] + ".")
        
        # Duration and implant status
        duration_stmt = []
        if canonical['implantable']:
            duration_stmt.append("is implanted")
            if canonical['duration']:
                duration_stmt.append(f"and intended to remain in place {canonical['duration'].replace('_', '-')}")
        elif canonical['duration']:
            duration_stmt.append(f"is intended for {canonical['duration'].replace('_', '-')} use")
        
        if duration_stmt:
            parts.append("The device " + " ".join(duration_stmt) + ".")
        
        # User and environment
        user_env = []
        if canonical['intended_user']:
            user_env.append(f"for use by {canonical['intended_user']}")
        if canonical['use_environment']:
            user_env.append(f"in {canonical['use_environment']} settings")
        
        if user_env:
            parts.append("It is intended " + " ".join(user_env) + ".")
        
        # Key characteristics
        characteristics = []
        
        if canonical['delivers_medicinal_substance']:
            characteristics.append("delivers a medicinal substance")
        
        if canonical['delivers_energy']:
            characteristics.append("delivers energy")
        
        if canonical['monitors_vital_parameter']:
            characteristics.append("monitors a vital physiological parameter")
        
        # Diagnostic role
        if canonical['diagnostic_role'] == 'assists':
            characteristics.append("assists in clinical diagnosis")
        elif canonical['diagnostic_role'] == 'independent':
            characteristics.append("provides independent diagnostic conclusions")
        elif canonical['diagnostic_role'] == 'none':
            characteristics.append("does not independently diagnose conditions")
        
        # Life supporting
        if not canonical['life_supporting']:
            characteristics.append("is not intended to support or sustain life")
        
        if characteristics:
            parts.append("The device " + ", ".join(characteristics[:-1]) + (" and " if len(characteristics) > 1 else "") + characteristics[-1] + ".")
        
        return " ".join(parts)
