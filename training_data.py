"""
Training examples for the medical device classification system
Based on the provided documentation
"""

TRAINING_EXAMPLES = {
    "CardioBand Wearable Monitor": {
        "raw_input": """CardioBand is a wearable device intended to continuously monitor heart rate and transmit data to a mobile application.
It is designed for use in home environments.""",
        "canonical_object": {
            "device_name": "CardioBand",
            "generic_category": "Wearable cardiac monitor",
            "structure_function": "Wearable sensor measuring heart rate and transmitting data wirelessly",
            "medical_purpose": "Continuous monitoring of heart rate",
            "population": "Adults with cardiac arrhythmia",
            "intended_user": "Patients (self-use)",
            "use_environment": "Home",
            "invasiveness": "non-invasive",
            "implantable": False,
            "duration": "long_term",
            "body_system": "cardiovascular",
            "active": True,
            "delivers_medicinal_substance": False,
            "delivers_energy": False,
            "monitors_vital_parameter": True,
            "diagnostic_role": "assists",
            "life_supporting": False
        },
        "expected_class": "B",
        "intended_use": "CardioBand is a non-invasive, electrically powered wearable cardiac monitoring device intended for the continuous measurement of heart rate in adult patients with cardiac arrhythmias. The device consists of a wearable sensor that transmits heart rate data wirelessly to a mobile application. It is intended for long-term use on intact skin and is designed for self-use by patients in home environments. The device monitors a vital physiological parameter and provides alerts to support clinical awareness but does not independently diagnose medical conditions, initiate therapy, or support or sustain life."
    },
    
    "PainRelief Patch": {
        "raw_input": """PainRelief Patch is an adhesive device intended to deliver medication through the skin for pain management in adults.""",
        "canonical_object": {
            "device_name": "PainRelief Patch",
            "generic_category": "Transdermal drug delivery patch",
            "structure_function": "Adhesive patch with integrated drug reservoir for transdermal delivery",
            "medical_purpose": "Delivery of analgesic medication for pain management",
            "population": "Adults",
            "intended_user": "Patients (self-use)",
            "use_environment": "Home",
            "invasiveness": "non-invasive",
            "implantable": False,
            "duration": "short_term",
            "body_system": "skin",
            "active": False,
            "delivers_medicinal_substance": True,
            "delivers_energy": False,
            "monitors_vital_parameter": False,
            "diagnostic_role": "none",
            "life_supporting": False
        },
        "expected_class": "A",
        "intended_use": "PainRelief Patch is a non-invasive, single-use transdermal drug delivery device intended for the controlled delivery of analgesic medication through intact skin for the management of pain in adult patients. The device consists of an adhesive patch with an integrated drug reservoir designed for short-term application of up to 72 hours. It is intended for self-use by patients in home environments. The device delivers a medicinal substance but does not independently diagnose conditions, initiate therapy decisions, or support or sustain life."
    },
    
    "OrthoFix Bone Screw": {
        "raw_input": """OrthoFix Bone Screw is intended for fixation of bone fractures during orthopedic surgery.""",
        "canonical_object": {
            "device_name": "OrthoFix Bone Screw",
            "generic_category": "Orthopedic bone fixation implant",
            "structure_function": "Metallic screw providing internal fixation of fractured bone",
            "medical_purpose": "Stabilization and fixation of bone fractures",
            "population": "Adults",
            "intended_user": "Orthopedic surgeons",
            "use_environment": "Hospital operating room",
            "invasiveness": "surgically_invasive",
            "implantable": True,
            "duration": "long_term",
            "body_system": "skeletal",
            "active": False,
            "delivers_medicinal_substance": False,
            "delivers_energy": False,
            "monitors_vital_parameter": False,
            "diagnostic_role": "none",
            "life_supporting": False
        },
        "expected_class": "C",
        "intended_use": "OrthoFix Bone Screw is a surgically invasive, implantable orthopedic device intended for the internal fixation and stabilization of bone fractures in adult patients. The device is implanted during surgical procedures and is intended to remain in place long-term to provide structural support during bone healing. It is intended for use by qualified orthopedic surgeons in hospital operating room settings. The device is passive and does not deliver energy or medicinal substances, nor is it intended to support or sustain life."
    },
    
    "NeuroScan AI": {
        "raw_input": """NeuroScan AI analyzes brain imaging data to detect abnormalities and assist clinicians in interpretation.""",
        "canonical_object": {
            "device_name": "NeuroScan AI",
            "generic_category": "Radiological image analysis software",
            "structure_function": "Software analyzing brain imaging data for abnormal patterns",
            "medical_purpose": "Assist in detection of neurological abnormalities",
            "population": "Adults undergoing brain imaging",
            "intended_user": "Licensed clinicians",
            "use_environment": "Hospital and clinical settings",
            "invasiveness": "non-invasive",
            "implantable": False,
            "duration": "transient",
            "body_system": "central_nervous_system",
            "active": True,
            "delivers_medicinal_substance": False,
            "delivers_energy": False,
            "monitors_vital_parameter": False,
            "diagnostic_role": "assists",
            "life_supporting": False
        },
        "expected_class": "C",
        "intended_use": "NeuroScan AI is a non-invasive, software-based medical device intended to analyze adult brain imaging data to assist licensed clinicians in the identification of neurological abnormalities. The software processes radiological inputs and provides analytical outputs to support clinical interpretation in hospital and clinical settings. The device does not independently establish a diagnosis, initiate treatment, or support or sustain life."
    },
    
    "NeoBreath Monitor": {
        "raw_input": """NeoBreath is a bedside monitor intended to measure respiratory rate in neonates in hospital settings.""",
        "canonical_object": {
            "device_name": "NeoBreath",
            "generic_category": "Neonatal respiratory monitor",
            "structure_function": "Contactless sensor system measuring respiratory motion",
            "medical_purpose": "Continuous monitoring of respiratory rate and apnea detection",
            "population": "Neonates",
            "intended_user": "Healthcare professionals",
            "use_environment": "Neonatal intensive care unit",
            "invasiveness": "non-invasive",
            "implantable": False,
            "duration": "long_term",
            "body_system": "respiratory",
            "active": True,
            "delivers_medicinal_substance": False,
            "delivers_energy": False,
            "monitors_vital_parameter": True,
            "diagnostic_role": "assists",
            "life_supporting": False
        },
        "expected_class": "C",
        "intended_use": "NeoBreath is a non-invasive, electrically powered neonatal monitoring device intended for the continuous measurement of respiratory rate and detection of apnea events in neonates admitted to neonatal intensive care units. The device utilizes contactless sensing technology and provides alarm notifications to support clinical monitoring by healthcare professionals. The device monitors a vital physiological parameter but does not independently diagnose conditions, initiate therapy, or support or sustain life."
    },
    
    "MediFlow Pro Infusion Pump": {
        "raw_input": """Device Name: MediFlow Pro Infusion Pump

Intended Use

The MediFlow Pro Infusion Pump is an electrically powered, programmable infusion device intended to deliver controlled volumes of intravenous fluids, medications, blood products, and parenteral nutrition to patients.

The device utilizes a peristaltic pumping mechanism with integrated pressure and flow sensors to ensure accurate and safe delivery rates.

It is indicated for use in adult and pediatric patients requiring intravenous therapy.

The device is intended to be operated by trained healthcare professionals in hospital and clinical environments.

The device provides short-term and continuous infusion therapy via vascular access devices.

It is not intended to independently sustain life in critical care situations without appropriate monitoring.""",
        "canonical_object": {
            "device_name": "MediFlow Pro Infusion Pump",
            "generic_category": "Infusion Pump",
            "structure_function": "Electrically powered programmable peristaltic infusion pump",
            "medical_purpose": "Controlled IV administration of fluids and medications",
            "population": "Adult and pediatric patients",
            "intended_user": "Healthcare professionals",
            "use_environment": "Hospital / clinical settings",
            "invasiveness": "invasive_via_orifice",
            "implantable": False,
            "duration": "short_term",
            "body_system": "vascular system",
            "active": True,
            "delivers_medicinal_substance": True,
            "delivers_energy": False,
            "monitors_vital_parameter": False,
            "diagnostic_role": "none",
            "life_supporting": False
        },
        "expected_class": "C",
        "intended_use": "MediFlow Pro Infusion Pump is an electrically powered, programmable infusion device intended to deliver controlled volumes of intravenous fluids, medications, blood products, and parenteral nutrition to adult and pediatric patients requiring intravenous therapy. The device utilizes a peristaltic pumping mechanism with integrated pressure and flow sensors to ensure accurate delivery rates. It is intended to be operated by trained healthcare professionals in hospital and clinical environments and provides short-term continuous infusion therapy via vascular access devices."
    },
    
    "DermalCare Wound Dressing": {
        "raw_input": """Device Name: DermalCare Sterile Wound Dressing

Intended Use

DermalCare Sterile Wound Dressing is a sterile, single-use adhesive dressing intended to cover and protect minor cuts, abrasions, and superficial wounds.

The dressing consists of a non-woven absorbent pad attached to a hypoallergenic adhesive backing.

It is intended to absorb exudate and provide a protective barrier against external contaminants.

The device is intended for use on intact or superficially broken skin in the general population.

The product is suitable for use in home, clinic, or first-aid settings and may be applied by healthcare professionals or laypersons.

The dressing is non-invasive and intended for transient use.""",
        "canonical_object": {
            "device_name": "DermalCare Sterile Wound Dressing",
            "generic_category": "Adhesive wound dressing",
            "structure_function": "Sterile absorbent adhesive dressing",
            "medical_purpose": "Protection of minor superficial wounds",
            "population": "General population",
            "intended_user": "Healthcare professionals or laypersons",
            "use_environment": "Home / clinic / first-aid",
            "invasiveness": "non-invasive",
            "implantable": False,
            "duration": "transient",
            "body_system": "skin",
            "active": False,
            "delivers_medicinal_substance": False,
            "delivers_energy": False,
            "monitors_vital_parameter": False,
            "diagnostic_role": "none",
            "life_supporting": False
        },
        "expected_class": "A",
        "intended_use": "DermalCare Sterile Wound Dressing is a sterile, single-use adhesive dressing intended to cover and protect minor cuts, abrasions, and superficial wounds. The dressing consists of a non-woven absorbent pad attached to a hypoallergenic adhesive backing and is intended to absorb exudate and provide a protective barrier against external contaminants. The device is intended for use on intact or superficially broken skin in the general population and is suitable for use in home, clinic, or first-aid settings by healthcare professionals or laypersons."
    },
    
    "NeuroPulse DBS System": {
        "raw_input": """Device Name: NeuroPulse DBS System

Intended Use

NeuroPulse DBS System is an implantable neurostimulation device intended to deliver programmable electrical stimulation to specific regions of the deep brain for the treatment of movement disorders such as Parkinson's disease, essential tremor, and dystonia.

The system consists of implantable intracranial electrodes, an implantable pulse generator, and external programming software.

The device is intended for use in adult patients diagnosed with medically refractory movement disorders.

The device is surgically implanted and provides long-term therapy.

Implantation and programming must be performed by qualified neurosurgeons and neurologists in hospital settings.

The device continuously delivers electrical impulses and may be adjusted non-invasively post-implantation.""",
        "canonical_object": {
            "device_name": "NeuroPulse DBS System",
            "generic_category": "Implantable deep brain stimulator",
            "structure_function": "Implantable pulse generator delivering electrical stimulation",
            "medical_purpose": "Treatment of movement disorders",
            "population": "Adults with Parkinson's / tremor / dystonia",
            "intended_user": "Neurosurgeons / neurologists",
            "use_environment": "Hospital",
            "invasiveness": "surgically_invasive",
            "implantable": True,
            "duration": "long_term",
            "body_system": "central_nervous_system",
            "active": True,
            "delivers_medicinal_substance": False,
            "delivers_energy": True,
            "monitors_vital_parameter": False,
            "diagnostic_role": "none",
            "life_supporting": False
        },
        "expected_class": "D",
        "intended_use": "NeuroPulse DBS System is an implantable neurostimulation device intended to deliver programmable electrical stimulation to specific regions of the deep brain for the treatment of movement disorders such as Parkinson's disease, essential tremor, and dystonia in adult patients with medically refractory conditions. The system consists of implantable intracranial electrodes, an implantable pulse generator, and external programming software. The device is surgically implanted and provides long-term therapy, and must be implanted and programmed by qualified neurosurgeons and neurologists in hospital settings."
    },
    
    "SpineRestore Kyphoplasty Kit": {
        "raw_input": """Device Name: SpineRestore Balloon Kyphoplasty Kit

Intended Use

SpineRestore Balloon Kyphoplasty Kit is intended for the minimally invasive treatment of vertebral compression fractures caused by osteoporosis or trauma.

The system includes inflatable bone tamps, cement delivery instruments, and bone cement.

The device is intended to restore vertebral body height and reduce pain.

It is used by trained orthopedic surgeons or interventional radiologists in hospital operating rooms.

The device is intended for short-term invasive use during a surgical procedure.

Bone cement remains implanted permanently.""",
        "canonical_object": {
            "device_name": "SpineRestore Balloon Kyphoplasty Kit",
            "generic_category": "Balloon kyphoplasty system",
            "structure_function": "Balloon catheter with cement stabilization",
            "medical_purpose": "Restoration of vertebral height and fracture stabilization",
            "population": "Adults with vertebral compression fractures",
            "intended_user": "Orthopedic surgeons / interventional radiologists",
            "use_environment": "Hospital operating room",
            "invasiveness": "surgically_invasive",
            "implantable": True,
            "duration": "long_term",
            "body_system": "skeletal",
            "active": False,
            "delivers_medicinal_substance": False,
            "delivers_energy": False,
            "monitors_vital_parameter": False,
            "diagnostic_role": "none",
            "life_supporting": False
        },
        "expected_class": "C",
        "intended_use": "SpineRestore Balloon Kyphoplasty Kit is intended for the minimally invasive treatment of vertebral compression fractures caused by osteoporosis or trauma. The system includes inflatable bone tamps, cement delivery instruments, and bone cement. The device is intended to restore vertebral body height and reduce pain and is used by trained orthopedic surgeons or interventional radiologists in hospital operating rooms. Bone cement remains implanted permanently for long-term structural support."
    },
    
    "CardioRisk AI": {
        "raw_input": """Device Name: CardioRisk AI

Intended Use

CardioRisk AI is a clinical decision support software intended to analyze electrocardiogram (ECG) recordings and patient demographic data to identify patterns suggestive of atrial fibrillation and other cardiac arrhythmias.

The software provides risk stratification and alerts to assist physicians in diagnosis.

It is not intended to independently diagnose or replace clinical judgment.

The software is intended for use by licensed healthcare professionals in hospitals and clinics.

The system does not directly interface with patients.""",
        "canonical_object": {
            "device_name": "CardioRisk AI",
            "generic_category": "Clinical decision support software",
            "structure_function": "Software analyzing ECG data",
            "medical_purpose": "Assist in identification of cardiac arrhythmias",
            "population": "Adults undergoing ECG",
            "intended_user": "Licensed physicians",
            "use_environment": "Hospital / clinic",
            "invasiveness": "non-invasive",
            "implantable": False,
            "duration": "transient",
            "body_system": "cardiovascular",
            "active": True,
            "delivers_medicinal_substance": False,
            "delivers_energy": False,
            "monitors_vital_parameter": True,
            "diagnostic_role": "assists",
            "life_supporting": False
        },
        "expected_class": "C",
        "intended_use": "CardioRisk AI is a clinical decision support software intended to analyze electrocardiogram (ECG) recordings and patient demographic data to identify patterns suggestive of atrial fibrillation and other cardiac arrhythmias. The software provides risk stratification and alerts to assist physicians in diagnosis but is not intended to independently diagnose or replace clinical judgment. The software is intended for use by licensed healthcare professionals in hospitals and clinics."
    },
    
    "NeoWave BCG Monitor": {
        "raw_input": """Device Name: NeoWave BCG Monitor

Intended Use

NeoWave BCG Monitor is a non-contact neonatal monitoring system intended to measure heart rate, respiratory rate, and gross body movement in neonates admitted to neonatal intensive care units.

The system utilizes ballistocardiography sensors integrated into a mattress platform placed beneath the infant.

It is intended to provide continuous monitoring and trend analysis.

The device is intended for use by trained clinical staff in NICU settings.

The device does not provide diagnostic decisions and is not intended to replace standard ECG or pulse oximetry monitoring.

The device does not contact the infant's skin.""",
        "canonical_object": {
            "device_name": "NeoWave BCG Monitor",
            "generic_category": "Neonatal physiological monitor",
            "structure_function": "Contactless BCG sensor under mattress",
            "medical_purpose": "Continuous monitoring of HR and RR",
            "population": "Neonates",
            "intended_user": "NICU clinicians",
            "use_environment": "NICU",
            "invasiveness": "non-invasive",
            "implantable": False,
            "duration": "long_term",
            "body_system": "cardiorespiratory",
            "active": True,
            "delivers_medicinal_substance": False,
            "delivers_energy": False,
            "monitors_vital_parameter": True,
            "diagnostic_role": "assists",
            "life_supporting": False
        },
        "expected_class": "C",
        "intended_use": "NeoWave BCG Monitor is a non-contact neonatal monitoring system intended to measure heart rate, respiratory rate, and gross body movement in neonates admitted to neonatal intensive care units. The system utilizes ballistocardiography sensors integrated into a mattress platform and is intended to provide continuous monitoring and trend analysis. The device is intended for use by trained clinical staff in NICU settings and does not provide diagnostic decisions."
    }
}


# Field definitions and completeness rules
REQUIRED_FIELDS = [
    'device_name',
    'structure_function',
    'medical_purpose',
    'population',
    'intended_user',
    'use_environment'
]

CLASSIFICATION_CRITICAL_FIELDS = [
    'invasiveness',
    'implantable',
    'duration',
    'body_system',
    'active',
    'delivers_medicinal_substance',
    'delivers_energy',
    'monitors_vital_parameter',
    'diagnostic_role',
    'life_supporting'
]

FIELD_CLARIFICATION_QUESTIONS = {
    'population': {
        'question': 'Who is the intended patient population?',
        'type': 'text',
        'help': 'E.g., "Adults", "Pediatric patients", "Neonates", "General population"',
        'examples': ['Adults', 'Pediatric patients', 'Neonates', 'Pregnant women', 'General population']
    },
    'intended_user': {
        'question': 'Who operates or uses the device?',
        'type': 'text',
        'help': 'E.g., "Healthcare professionals", "Patients (self-use)", "Licensed physicians"',
        'examples': ['Healthcare professionals', 'Patients (self-use)', 'Trained specialists', 'Laypersons']
    },
    'use_environment': {
        'question': 'Where is the device intended to be used?',
        'type': 'text',
        'help': 'E.g., "Hospital", "Home", "Clinic", "Operating room"',
        'examples': ['Hospital', 'Home', 'Clinic', 'Operating room', 'NICU', 'Emergency room']
    },
    'invasiveness': {
        'question': 'What is the invasiveness level of the device?',
        'type': 'select',
        'options': ['non-invasive', 'invasive_via_orifice', 'surgically_invasive'],
        'help': 'Non-invasive (skin contact only), invasive via orifice (natural openings), or surgically invasive'
    },
    'implantable': {
        'question': 'Is the device implantable (remains in body >30 days)?',
        'type': 'boolean',
        'help': 'True if device or any part remains implanted long-term'
    },
    'duration': {
        'question': 'What is the intended duration of use?',
        'type': 'select',
        'options': ['transient', 'short_term', 'long_term'],
        'help': 'Transient (<60 min), Short-term (30 days), Long-term (>30 days)'
    },
    'body_system': {
        'question': 'Which body system does the device primarily interact with?',
        'type': 'text',
        'help': 'E.g., "cardiovascular", "respiratory", "central_nervous_system", "skeletal", "skin"',
        'examples': ['cardiovascular', 'respiratory', 'central_nervous_system', 'skeletal', 'skin', 'vascular']
    },
    'active': {
        'question': 'Is this an active device (requires electrical/other power)?',
        'type': 'boolean',
        'help': 'True if device requires electrical power or other energy source to function'
    },
    'delivers_medicinal_substance': {
        'question': 'Does the device deliver a medicinal substance?',
        'type': 'boolean',
        'help': 'True if device administers drugs or biological substances'
    },
    'delivers_energy': {
        'question': 'Does the device deliver energy to the patient?',
        'type': 'boolean',
        'help': 'E.g., electrical stimulation, radiation, heat, ultrasound'
    },
    'monitors_vital_parameter': {
        'question': 'Does the device monitor vital physiological parameters?',
        'type': 'boolean',
        'help': 'E.g., heart rate, blood pressure, oxygen saturation, respiratory rate'
    },
    'diagnostic_role': {
        'question': 'What is the device\'s diagnostic role?',
        'type': 'select',
        'options': ['none', 'assists', 'independent'],
        'help': 'None (no diagnosis), Assists (supports clinician), Independent (makes diagnosis)'
    },
    'life_supporting': {
        'question': 'Is the device intended to support or sustain life?',
        'type': 'boolean',
        'help': 'True only if device failure would immediately threaten life'
    }
}
