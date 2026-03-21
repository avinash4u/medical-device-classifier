# Medical Device Classification System

A deterministic, rule-based classification system for medical devices based on MDR 2017 and CDSCO guidelines. This system uses **trained pattern matching** from examples, not LLM inference, to ensure consistent and regulatory-compliant classifications.

## Features

✅ **Training-Based Extraction**: Learns from 11 comprehensive examples  
✅ **Deterministic Rule Engine**: MDR 2017 compliant classification rules  
✅ **CDSCO Database Search**: Matches against reference database before rule application  
✅ **Completeness Checking**: Ensures all classification-critical fields are captured  
✅ **PDF Report Generation**: Professional classification reports with justification  
✅ **Zero LLM Dependency**: All core logic is deterministic pattern matching and rules  

## System Architecture

```
┌─────────────────────┐
│  Upload/Paste IU    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Extract & Normalize │ ◄── Uses Training Examples
│  (Pattern Matching) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Completeness Check  │ ◄── Deterministic Logic
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Confirm IU         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ CDSCO DB Search     │ ◄── Keyword + Similarity Matching
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │   Match?    │
    └──┬───────┬──┘
       │Yes    │No
       │       │
       ▼       ▼
   Use DB  ┌─────────────────────┐
   Class   │  Rule Engine        │ ◄── MDR 2017 Rules (D→C→B→A)
           │  (2 attempts max)   │
           └──────────┬──────────┘
                      │
                      ▼
              ┌───────────────┐
              │ Classification │
              │   + Report    │
              └───────────────┘
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone or download this directory**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **For OCR support (optional)**:
```bash
# On Ubuntu/Debian
sudo apt-get install tesseract-ocr

# On macOS
brew install tesseract

# On Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Step-by-Step Workflow

#### Step 1: Upload/Paste Intended Use
- **Paste Text**: Directly paste the intended use statement
- **Upload PDF**: Upload a PDF document (supports OCR for scanned PDFs)
- **Load Example**: Select from 11 training examples to test the system

#### Step 2: Extract & Normalize
- System automatically extracts fields using pattern matching
- All fields are editable if corrections needed
- No LLM involved - pure pattern recognition from training data

#### Step 3: Completeness Check
- System validates all required fields are present
- Asks **only** for missing classification-critical information
- Questions are deterministic based on field requirements

#### Step 4: Confirm Intended Use
- Review the generated formal intended use statement
- Edit if needed
- Canonical classification object is created

#### Step 5: Database Search
- System searches CDSCO reference database
- Uses keyword matching + semantic similarity
- Returns 0-5 matches with confidence scores
- You can accept a match or proceed to rule engine

#### Step 6: Classification (if needed)
- Rule engine applies MDR 2017 rules deterministically
- Evaluates D → C → B → A (highest risk first)
- Makes 2 attempts before declaring "UNCERTAIN"
- Provides full rule trace and justification

#### Step 7: Download Results
- View complete classification report
- Download PDF with all details
- Includes canonical object, intended use, classification, and justification

## Training Examples

The system is trained on 11 comprehensive examples covering:

1. **CardioBand** - Wearable cardiac monitor (Class B)
2. **PainRelief Patch** - Transdermal drug delivery (Class A)
3. **OrthoFix Bone Screw** - Orthopedic implant (Class C)
4. **NeuroScan AI** - Brain imaging analysis software (Class C)
5. **NeoBreath** - Neonatal respiratory monitor (Class C)
6. **MediFlow Pro** - Infusion pump (Class C)
7. **DermalCare** - Adhesive wound dressing (Class A)
8. **NeuroPulse DBS** - Deep brain stimulator (Class D)
9. **SpineRestore** - Kyphoplasty system (Class C)
10. **CardioRisk AI** - ECG analysis software (Class C)
11. **NeoWave BCG** - Neonatal BCG monitor (Class C)

### Adding New Training Examples

Edit `training_data.py` and add to the `TRAINING_EXAMPLES` dictionary:

```python
"Your Device Name": {
    "raw_input": "The intended use text...",
    "canonical_object": {
        "device_name": "...",
        # ... all fields
    },
    "expected_class": "C",
    "intended_use": "The formal statement..."
}
```

## File Structure

```
medical_device_classifier/
├── app.py                      # Main Streamlit application
├── extraction_engine.py        # Pattern-based extraction from training data
├── rule_engine.py             # MDR 2017 classification rules
├── database_search.py         # CDSCO database matching
├── training_data.py           # All training examples and field definitions
├── pdf_extractor.py           # PDF text extraction (digital + OCR)
├── pdf_generator.py           # Classification report PDF generation
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Classification Rules (MDR 2017)

### Class D - Very High Risk
- Implantable active devices in CNS/cardiovascular system
- Long-term invasive CNS devices
- Active devices delivering energy/substances to CNS
- Life-supporting/sustaining devices

### Class C - High Risk
- Long-term surgically invasive implantables
- Active devices delivering medicinal substances
- Vital parameter monitors in critical care (e.g., NICU)
- Software assisting diagnosis of serious conditions
- Short-term surgically invasive devices

### Class B - Medium Risk
- Short/medium-term surgically invasive devices
- Active diagnostic/monitoring devices (non-invasive)
- Invasive devices via body orifice (short/long-term)
- Long-term skin contact active devices

### Class A - Low Risk
- Non-invasive transient contact passive devices
- Non-invasive skin contact devices
- General non-invasive passive devices

## Licensing Authority

- **Class A & B**: State Licensing Authority (CDSCO)
- **Class C & D**: Central Licensing Authority (CDSCO)

## Key Design Principles

### 1. No LLM for Core Classification
- Extraction uses **pattern matching** from training examples
- Classification uses **deterministic rules** only
- LLM is available as fallback for edge cases ONLY

### 2. Training-Based Learning
- System learns extraction patterns from 11 examples
- Keyword dictionaries built from training data
- Field inference based on observed patterns

### 3. Completeness First
- All classification-critical fields must be known
- System asks minimal clarifying questions
- Only proceeds when data is complete

### 4. Database Before Rules
- Always attempts CDSCO database match first
- Rule engine only runs if no match or match rejected
- Prevents unnecessary rule evaluation

### 5. Uncertainty Handling
- Rule engine makes 2 attempts
- If still uncertain, declares "UNCERTAIN" with explanation
- Never forces a classification

## API Integration (Future)

The current system is a web UI. To integrate into other systems:

```python
from extraction_engine import ExtractionEngine
from rule_engine import RuleEngine
from database_search import DatabaseSearch
from training_data import TRAINING_EXAMPLES

# Initialize
extractor = ExtractionEngine(TRAINING_EXAMPLES)
classifier = RuleEngine()
db = DatabaseSearch()

# Extract from text
extracted = extractor.extract(intended_use_text)

# Check completeness
missing, questions = extractor.check_completeness(extracted)

# ... handle clarifications ...

# Create canonical object
canonical = extractor.create_canonical_object(extracted)

# Search database
matches = db.search(intended_use_text, canonical)

# If no match, classify with rules
if not matches:
    result = classifier.classify(canonical)
```

## Troubleshooting

### PDF Upload Not Working
- Ensure PyPDF2 is installed: `pip install PyPDF2`
- For scanned PDFs, install tesseract-ocr
- Check that the PDF is not password-protected

### Classification Shows "UNCERTAIN"
- Review the canonical object - ensure all fields are filled
- Check if the device matches any training examples
- The device might be a genuinely borderline case requiring manual review

### Extraction Misses Fields
- The device might not match training patterns
- Manually edit extracted fields in Step 2
- Consider adding similar device to training data

## Contributing

To add new training examples:
1. Add to `training_data.py` in the `TRAINING_EXAMPLES` dictionary
2. Include all required fields in canonical object
3. Provide expected classification for validation
4. Test with the UI to ensure patterns are learned

## License

This is a reference implementation for regulatory classification.
Always verify classifications with qualified regulatory professionals.

## Support

For issues or questions:
1. Check the training examples to see if similar devices exist
2. Review the rule trace in classification results
3. Examine the canonical object to ensure all fields are correct

## Regulatory Compliance

⚠️ **Important**: This system is a decision support tool, not a replacement for regulatory expertise. All classifications should be reviewed and validated by qualified regulatory professionals before submission to licensing authorities.

## Version

Version 1.0 - Initial Release
Based on MDR 2017 and CDSCO Medical Device Rules
