"""
Database Search Module
Searches CDSCO database for similar devices
Uses semantic similarity + keyword matching
"""

from typing import List, Dict
import re
from difflib import SequenceMatcher


class DatabaseSearch:
    """
    Searches CDSCO database for matching devices
    Uses keyword matching and semantic similarity
    """
    
    def __init__(self):
        self.database = self._load_cdsco_database()
        self.confidence_threshold = 0.6
    
    def _load_cdsco_database(self) -> List[Dict]:
        """
        Load CDSCO device database
        In production, this would load from Excel/CSV
        Using training examples as reference database
        """
        database = [
            {
                'device_name': 'Infusion Pump',
                'generic_category': 'Infusion pump for controlled IV delivery',
                'intended_use': 'Electrically powered device for controlled intravenous delivery of fluids and medications',
                'class': 'C',
                'authority': 'Central Licensing Authority (CDSCO)',
                'keywords': ['infusion', 'pump', 'iv', 'intravenous', 'delivery', 'medication', 'fluid']
            },
            {
                'device_name': 'Adhesive Wound Dressing',
                'generic_category': 'Sterile adhesive dressing',
                'intended_use': 'Sterile dressing for protection of minor wounds and cuts',
                'class': 'A',
                'authority': 'State Licensing Authority (CDSCO)',
                'keywords': ['dressing', 'wound', 'adhesive', 'sterile', 'bandage', 'cut']
            },
            {
                'device_name': 'Deep Brain Stimulator',
                'generic_category': 'Implantable neurostimulation device',
                'intended_use': 'Implantable device delivering electrical stimulation to brain for movement disorders',
                'class': 'D',
                'authority': 'Central Licensing Authority (CDSCO)',
                'keywords': ['brain', 'stimulator', 'implant', 'neurostimulation', 'electrical', 'parkinson']
            },
            {
                'device_name': 'Cardiac Monitor',
                'generic_category': 'Wearable cardiac monitoring device',
                'intended_use': 'Non-invasive device for continuous heart rate monitoring',
                'class': 'B',
                'authority': 'State Licensing Authority (CDSCO)',
                'keywords': ['cardiac', 'heart', 'monitor', 'wearable', 'rate', 'ecg']
            },
            {
                'device_name': 'Orthopedic Implant',
                'generic_category': 'Bone fixation implant',
                'intended_use': 'Surgically implanted device for bone fracture fixation',
                'class': 'C',
                'authority': 'Central Licensing Authority (CDSCO)',
                'keywords': ['orthopedic', 'bone', 'implant', 'fixation', 'screw', 'fracture']
            },
            {
                'device_name': 'Neonatal Monitor',
                'generic_category': 'Neonatal vital signs monitor',
                'intended_use': 'Device for monitoring vital signs in neonatal intensive care',
                'class': 'C',
                'authority': 'Central Licensing Authority (CDSCO)',
                'keywords': ['neonatal', 'neonate', 'infant', 'monitor', 'vital', 'nicu']
            },
            {
                'device_name': 'Clinical Decision Support Software',
                'generic_category': 'Diagnostic software',
                'intended_use': 'Software for analysis of medical imaging to assist diagnosis',
                'class': 'C',
                'authority': 'Central Licensing Authority (CDSCO)',
                'keywords': ['software', 'ai', 'diagnosis', 'imaging', 'analysis', 'decision']
            },
            {
                'device_name': 'Transdermal Drug Delivery System',
                'generic_category': 'Drug delivery patch',
                'intended_use': 'Adhesive patch for transdermal delivery of medication',
                'class': 'A',
                'authority': 'State Licensing Authority (CDSCO)',
                'keywords': ['transdermal', 'patch', 'drug', 'delivery', 'medication', 'adhesive']
            },
            {
                'device_name': 'Surgical Kyphoplasty System',
                'generic_category': 'Vertebral augmentation device',
                'intended_use': 'Surgical device for vertebral compression fracture treatment with cement',
                'class': 'C',
                'authority': 'Central Licensing Authority (CDSCO)',
                'keywords': ['kyphoplasty', 'vertebral', 'spine', 'cement', 'surgical', 'fracture']
            },
            {
                'device_name': 'ECG Analysis Software',
                'generic_category': 'Cardiac diagnostic software',
                'intended_use': 'Software analyzing ECG data to detect arrhythmias',
                'class': 'C',
                'authority': 'Central Licensing Authority (CDSCO)',
                'keywords': ['ecg', 'cardiac', 'arrhythmia', 'software', 'analysis', 'heart']
            }
        ]
        
        return database
    
    def search(self, intended_use: str, canonical_obj: Dict, max_results: int = 5) -> List[Dict]:
        """
        Search database for similar devices
        Returns list of matches with confidence scores
        """
        # Extract keywords from input
        input_keywords = self._extract_keywords(intended_use, canonical_obj)
        
        # Score each database entry
        matches = []
        
        for entry in self.database:
            # Calculate similarity score
            keyword_score = self._keyword_similarity(input_keywords, entry['keywords'])
            text_score = self._text_similarity(intended_use, entry['intended_use'])
            category_score = self._category_similarity(canonical_obj, entry)
            
            # Weighted combination
            confidence = (
                keyword_score * 0.4 +
                text_score * 0.3 +
                category_score * 0.3
            )
            
            if confidence >= self.confidence_threshold:
                matches.append({
                    'device_name': entry['device_name'],
                    'generic_category': entry['generic_category'],
                    'intended_use': entry['intended_use'],
                    'class': entry['class'],
                    'authority': entry['authority'],
                    'confidence': confidence,
                    'keyword_score': keyword_score,
                    'text_score': text_score,
                    'category_score': category_score
                })
        
        # Sort by confidence descending
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        
        return matches[:max_results]
    
    def _extract_keywords(self, text: str, obj: Dict) -> List[str]:
        """Extract relevant keywords from text and canonical object"""
        keywords = []
        
        # From text
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        keywords.extend(words)
        
        # From canonical object
        if obj.get('generic_category'):
            keywords.extend(obj['generic_category'].lower().split())
        
        if obj.get('body_system'):
            keywords.append(obj['body_system'])
        
        if obj.get('implantable'):
            keywords.append('implant')
        
        if obj.get('active'):
            keywords.extend(['active', 'powered'])
        
        if obj.get('monitors_vital_parameter'):
            keywords.extend(['monitor', 'vital'])
        
        # Remove duplicates
        return list(set(keywords))
    
    def _keyword_similarity(self, input_keywords: List[str], db_keywords: List[str]) -> float:
        """Calculate keyword overlap similarity"""
        if not db_keywords:
            return 0.0
        
        matches = sum(1 for kw in input_keywords if kw in db_keywords)
        return matches / len(db_keywords) if db_keywords else 0.0
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using sequence matcher"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _category_similarity(self, obj: Dict, entry: Dict) -> float:
        """Calculate similarity based on classification characteristics"""
        score = 0.0
        checks = 0
        
        # Compare key characteristics that drive classification
        characteristics = [
            'invasiveness',
            'implantable',
            'duration',
            'active',
            'body_system'
        ]
        
        for char in characteristics:
            if char in obj and obj[char]:
                checks += 1
                # This is a simplified check - in production, map entry to canonical format
                if char == 'active' and obj.get('active'):
                    if 'powered' in entry.get('intended_use', '').lower() or 'electrical' in entry.get('intended_use', '').lower():
                        score += 1
                elif char == 'implantable' and obj.get('implantable'):
                    if 'implant' in entry.get('intended_use', '').lower():
                        score += 1
                elif char == 'invasiveness' and obj.get('invasiveness') == 'surgically_invasive':
                    if 'surgical' in entry.get('intended_use', '').lower():
                        score += 1
        
        return score / checks if checks > 0 else 0.0
