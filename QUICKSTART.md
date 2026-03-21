# Quick Start Guide

## Installation (One-Time Setup)

### For macOS/Linux:
```bash
# Navigate to the project directory
cd medical_device_classifier

# Run the launcher (will install dependencies automatically)
./run.sh
```

### For Windows:
```cmd
# Navigate to the project directory
cd medical_device_classifier

# Run the launcher (will install dependencies automatically)
run.bat
```

### Manual Setup:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## First Time Use

1. **The application will open in your browser** at `http://localhost:8501`

2. **Try an example first**:
   - In the right sidebar, select "CardioBand Wearable Monitor"
   - Click "Use This Example"
   - Follow through all steps to see the complete workflow

3. **Test with your own device**:
   - Paste your intended use text
   - OR upload a PDF
   - Follow the 7-step workflow

## Understanding the Output

### Canonical Classification Object
This is the structured representation of your device with all classification-critical fields:
- `invasiveness`: How the device contacts the body
- `implantable`: Whether it remains in the body >30 days
- `duration`: Transient, short-term, or long-term use
- `active`: Requires electrical power
- `body_system`: Primary system interacted with
- `delivers_medicinal_substance`: Administers drugs
- `delivers_energy`: Delivers electrical/thermal/other energy
- `monitors_vital_parameter`: Tracks vital signs
- `diagnostic_role`: Assists or independently diagnoses
- `life_supporting`: Failure would threaten life

### Classification Result
- **Class A**: Low risk, State Authority
- **Class B**: Medium risk, State Authority
- **Class C**: High risk, Central Authority (CDSCO)
- **Class D**: Very high risk, Central Authority (CDSCO)
- **UNCERTAIN**: Requires manual review

### Justification
Every classification includes:
- Rule triggered (e.g., "C1: Long-term Surgically Invasive Implantable")
- Explanation of why this rule matched
- Full rule trace showing all rules evaluated

## Common Use Cases

### Case 1: Simple Non-Invasive Device
Example: Adhesive wound dressing
- Expected Class: A
- Database likely has match
- Fast classification

### Case 2: Active Monitoring Device
Example: Cardiac monitor
- Expected Class: B or C (depends on population/environment)
- Rule engine will evaluate based on vital parameter monitoring
- Population matters (neonatal → higher class)

### Case 3: Implantable Active Device
Example: Neurostimulator
- Expected Class: D (CNS involvement)
- Rule D1 or D2 will trigger
- Central Authority required

### Case 4: Software/SaMD
Example: Diagnostic AI
- Expected Class: B or C (depends on diagnostic role)
- Influence on treatment decisions drives classification
- CNS/cardiovascular involvement increases risk

## Tips for Best Results

1. **Be Specific in Intended Use**:
   - Include population (adults, neonates, etc.)
   - Specify environment (hospital, home, NICU)
   - Describe contact type (skin, implanted, vascular)
   - State duration clearly

2. **Review Extracted Fields**:
   - All fields are editable in Step 2
   - Correct any misclassifications
   - Pay special attention to classification-critical fields

3. **Answer Clarifications Accurately**:
   - These questions drive classification
   - If uncertain, choose most conservative (higher risk) option
   - Duration: <60min = transient, <30 days = short-term, >30 days = long-term

4. **Understand Database vs Rules**:
   - Database match = faster, already approved similar device
   - Rule engine = deterministic, transparent logic
   - Both are valid; database is preferred when confident

5. **Use Training Examples**:
   - 11 examples cover most device types
   - Study how similar devices are classified
   - Use examples to understand field mappings

## Troubleshooting

### "No fields extracted"
- Your intended use might not match training patterns
- Manually enter fields in Step 2
- Ensure text includes key phrases like "intended for", "device", etc.

### "Classification uncertain"
- Device might be borderline between classes
- Review canonical object for completeness
- Check if similar devices exist in training examples
- Manual regulatory review recommended

### "Database returned 0 matches"
- This is normal for novel devices
- System will proceed to rule engine
- Rule-based classification is equally valid

### Fields keep showing as missing
- Ensure you're filling ALL required fields
- For boolean fields, select "Yes" or "No" explicitly
- For dropdowns, select from provided options
- Don't leave fields as "unknown"

## Next Steps After Classification

1. **Review the PDF Report**:
   - Contains all technical details
   - Includes justification and rule trace
   - Use for regulatory submission preparation

2. **Validate with Experts**:
   - This tool is decision support, not final authority
   - Have regulatory professionals review
   - Consider hiring CDSCO consultants for submissions

3. **Prepare Additional Documentation**:
   - Technical files
   - Clinical evaluation reports
   - Risk analysis
   - Quality management system documentation

4. **Submit to Appropriate Authority**:
   - Class A/B: State Licensing Authority
   - Class C/D: Central Licensing Authority (CDSCO)

## Support

For questions or issues:
1. Review the training examples for similar devices
2. Check the README.md for detailed documentation
3. Examine the rule trace to understand classification logic
4. Ensure all canonical object fields are correctly filled

## Important Reminder

⚠️ **This system provides decision support only. All classifications must be validated by qualified regulatory professionals before submission to licensing authorities.**
