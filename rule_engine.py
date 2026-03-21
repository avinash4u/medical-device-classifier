"""
Rule Engine for Medical Device Classification
Based on MDR 2017 First Schedule
Deterministic rule evaluation - NO LLM involvement
"""

from typing import Dict, List, Tuple
import json


class RuleEngine:
    """
    Classifies medical devices using deterministic rules
    Evaluates D → C → B → A (highest risk first)
    """
    
    def __init__(self):
        self.rules = self._define_rules()
        self.attempts = 0
        self.max_attempts = 2
    
    def _define_rules(self) -> List[Dict]:
        """
        Define classification rules based on MDR 2017
        Each rule returns a class if conditions match
        """
        rules = [
            # CLASS D RULES - Highest Risk
            {
                'id': 'D1',
                'class': 'D',
                'name': 'Implantable CNS/Cardiac/Circulatory Active Device',
                'conditions': lambda obj: (
                    obj.get('implantable') and
                    obj.get('active') and
                    obj.get('body_system') in ['central_nervous_system', 'cardiovascular', 'circulatory']
                ),
                'justification': 'Implantable active device interacting with central nervous system or cardiovascular system'
            },
            {
                'id': 'D2',
                'class': 'D',
                'name': 'Long-term Invasive CNS Device',
                'conditions': lambda obj: (
                    obj.get('invasiveness') == 'surgically_invasive' and
                    obj.get('duration') == 'long_term' and
                    obj.get('body_system') == 'central_nervous_system'
                ),
                'justification': 'Surgically invasive device with long-term contact with central nervous system'
            },
            {
                'id': 'D3',
                'class': 'D',
                'name': 'Active Therapeutic Device delivering energy/substances to CNS',
                'conditions': lambda obj: (
                    obj.get('active') and
                    (obj.get('delivers_energy') or obj.get('delivers_medicinal_substance')) and
                    obj.get('body_system') == 'central_nervous_system'
                ),
                'justification': 'Active device delivering energy or substances to central nervous system'
            },
            {
                'id': 'D4',
                'class': 'D',
                'name': 'Life-supporting/sustaining device',
                'conditions': lambda obj: obj.get('life_supporting'),
                'justification': 'Device intended to support or sustain life'
            },
            
            # CLASS C RULES - High Risk
            {
                'id': 'C1',
                'class': 'C',
                'name': 'Long-term Surgically Invasive Implantable',
                'conditions': lambda obj: (
                    obj.get('invasiveness') == 'surgically_invasive' and
                    obj.get('implantable') and
                    obj.get('duration') == 'long_term'
                ),
                'justification': 'Surgically invasive implantable device intended for long-term use'
            },
            {
                'id': 'C2',
                'class': 'C',
                'name': 'Active device administering medicinal substances',
                'conditions': lambda obj: (
                    obj.get('active') and
                    obj.get('delivers_medicinal_substance') and
                    obj.get('invasiveness') in ['invasive_via_orifice', 'surgically_invasive']
                ),
                'justification': 'Active device delivering medicinal substances via invasive means'
            },
            {
                'id': 'C3',
                'class': 'C',
                'name': 'Device monitoring vital parameters with potential critical decisions',
                'conditions': lambda obj: (
                    obj.get('monitors_vital_parameter') and
                    obj.get('population') in ['neonates', 'Neonates'] and
                    obj.get('use_environment') in ['NICU', 'Neonatal intensive care unit', 'neonatal intensive care unit']
                ),
                'justification': 'Device monitoring vital physiological parameters in neonatal critical care'
            },
            {
                'id': 'C4',
                'class': 'C',
                'name': 'SaMD influencing diagnosis of serious conditions',
                'conditions': lambda obj: (
                    obj.get('active') and
                    'software' in obj.get('generic_category', '').lower() and
                    obj.get('diagnostic_role') == 'assists' and
                    obj.get('body_system') in ['central_nervous_system', 'cardiovascular']
                ),
                'justification': 'Software as Medical Device assisting in diagnosis of serious conditions'
            },
            {
                'id': 'C5',
                'class': 'C',
                'name': 'Short-term surgically invasive reusable surgical instrument',
                'conditions': lambda obj: (
                    obj.get('invasiveness') == 'surgically_invasive' and
                    obj.get('duration') == 'short_term' and
                    not obj.get('implantable')
                ),
                'justification': 'Surgically invasive device for short-term use during surgical procedures'
            },
            {
                'id': 'C6',
                'class': 'C',
                'name': 'Device monitoring vital cardiovascular parameters',
                'conditions': lambda obj: (
                    obj.get('monitors_vital_parameter') and
                    obj.get('body_system') == 'cardiovascular' and
                    obj.get('diagnostic_role') == 'assists'
                ),
                'justification': 'Device monitoring vital cardiovascular parameters and assisting in diagnosis'
            },
            
            # CLASS B RULES - Medium Risk
            {
                'id': 'B1',
                'class': 'B',
                'name': 'Short/medium-term surgically invasive',
                'conditions': lambda obj: (
                    obj.get('invasiveness') == 'surgically_invasive' and
                    obj.get('duration') in ['transient', 'short_term'] and
                    not obj.get('implantable')
                ),
                'justification': 'Surgically invasive device for transient or short-term use'
            },
            {
                'id': 'B2',
                'class': 'B',
                'name': 'Active diagnostic/monitoring device',
                'conditions': lambda obj: (
                    obj.get('active') and
                    (obj.get('monitors_vital_parameter') or obj.get('diagnostic_role') != 'none') and
                    obj.get('invasiveness') == 'non-invasive'
                ),
                'justification': 'Non-invasive active device for monitoring or diagnostic purposes'
            },
            {
                'id': 'B3',
                'class': 'B',
                'name': 'Device modifying biological/chemical composition',
                'conditions': lambda obj: (
                    obj.get('invasiveness') == 'invasive_via_orifice' and
                    obj.get('duration') in ['short_term', 'long_term']
                ),
                'justification': 'Invasive device via body orifice for short or long-term use'
            },
            {
                'id': 'B4',
                'class': 'B',
                'name': 'Long-term skin contact active device',
                'conditions': lambda obj: (
                    obj.get('active') and
                    obj.get('invasiveness') == 'non-invasive' and
                    obj.get('duration') == 'long_term' and
                    obj.get('body_system') == 'skin'
                ),
                'justification': 'Active device with long-term skin contact'
            },
            
            # CLASS A RULES - Low Risk
            {
                'id': 'A1',
                'class': 'A',
                'name': 'Non-invasive transient contact',
                'conditions': lambda obj: (
                    obj.get('invasiveness') == 'non-invasive' and
                    obj.get('duration') == 'transient' and
                    not obj.get('active')
                ),
                'justification': 'Non-invasive passive device with transient contact'
            },
            {
                'id': 'A2',
                'class': 'A',
                'name': 'Non-invasive device channeling/storing body fluids',
                'conditions': lambda obj: (
                    obj.get('invasiveness') == 'non-invasive' and
                    not obj.get('active') and
                    obj.get('body_system') == 'skin'
                ),
                'justification': 'Non-invasive passive device with skin contact only'
            },
            {
                'id': 'A3',
                'class': 'A',
                'name': 'General non-invasive passive device',
                'conditions': lambda obj: (
                    obj.get('invasiveness') == 'non-invasive' and
                    not obj.get('active') and
                    not obj.get('delivers_medicinal_substance')
                ),
                'justification': 'Non-invasive passive device not delivering substances'
            }
        ]
        
        return rules
    
    def classify(self, canonical_obj: Dict) -> Dict:
        """
        Classify device using rule engine
        Returns classification result with justification
        """
        self.attempts += 1
        
        # Evaluate rules in order D → C → B → A
        rule_trace = []
        matched_rule = None
        
        for rule in self.rules:
            try:
                matches = rule['conditions'](canonical_obj)
                rule_trace.append({
                    'rule_id': rule['id'],
                    'rule_name': rule['name'],
                    'matched': matches
                })
                
                if matches and not matched_rule:
                    matched_rule = rule
                    # Don't break - continue to build full trace
            except Exception as e:
                rule_trace.append({
                    'rule_id': rule['id'],
                    'rule_name': rule['name'],
                    'matched': False,
                    'error': str(e)
                })
        
        # Determine result
        if matched_rule:
            classification = matched_rule['class']
            authority = self._get_authority(classification)
            
            return {
                'source': 'rule_engine',
                'class': classification,
                'authority': authority,
                'confidence': 0.95,
                'rule_triggered': matched_rule['id'],
                'rule_name': matched_rule['name'],
                'justification': matched_rule['justification'],
                'rule_trace': rule_trace,
                'attempts': self.attempts
            }
        
        # No rule matched
        if self.attempts < self.max_attempts:
            # Try again (simulating re-evaluation)
            return self.classify(canonical_obj)
        else:
            # After 2 attempts, declare uncertain
            possible_classes = self._suggest_possible_classes(canonical_obj, rule_trace)
            
            return {
                'source': 'rule_engine',
                'class': 'UNCERTAIN',
                'authority': 'Manual Review Required',
                'confidence': 0.0,
                'rule_triggered': None,
                'justification': f'Unable to determine classification after {self.attempts} attempts. Manual review required. The device characteristics do not clearly match any single classification rule.',
                'rule_trace': rule_trace,
                'possible_classes': possible_classes,
                'attempts': self.attempts
            }
    
    def _suggest_possible_classes(self, obj: Dict, trace: List[Dict]) -> List[Dict]:
        """
        Suggest possible classifications based on partial matches
        """
        suggestions = []
        
        # Analyze which rules came closest
        for entry in trace:
            if entry.get('matched'):
                # Find the rule details
                for rule in self.rules:
                    if rule['id'] == entry['rule_id']:
                        suggestions.append({
                            'class': rule['class'],
                            'reason': rule['name'],
                            'confidence': 'partial_match'
                        })
        
        # If no partial matches, suggest based on key characteristics
        if not suggestions:
            if obj.get('invasiveness') == 'surgically_invasive':
                suggestions.append({
                    'class': 'C',
                    'reason': 'Surgically invasive devices are typically Class C or D',
                    'confidence': 'characteristic_based'
                })
            
            if obj.get('active') and obj.get('monitors_vital_parameter'):
                suggestions.append({
                    'class': 'B',
                    'reason': 'Active monitoring devices are typically Class B or C',
                    'confidence': 'characteristic_based'
                })
            
            if obj.get('invasiveness') == 'non-invasive' and not obj.get('active'):
                suggestions.append({
                    'class': 'A',
                    'reason': 'Non-invasive passive devices are typically Class A',
                    'confidence': 'characteristic_based'
                })
        
        return suggestions
    
    def _get_authority(self, classification: str) -> str:
        """
        Determine licensing authority based on classification
        """
        if classification in ['A', 'B']:
            return "State Licensing Authority (CDSCO)"
        elif classification in ['C', 'D']:
            return "Central Licensing Authority (CDSCO)"
        else:
            return "To be determined"
    
    def reset(self):
        """Reset attempt counter"""
        self.attempts = 0
