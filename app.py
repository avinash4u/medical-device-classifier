"""
Medical Device Classification System
Based on MDR 2017 and CDSCO Guidelines
"""

import streamlit as st
import json
from typing import Dict, List, Optional, Tuple
from extraction_engine import ExtractionEngine
from rule_engine import RuleEngine
from database_search import DatabaseSearch
from training_data import TRAINING_EXAMPLES
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="Medical Device Classifier",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None
if 'canonical_object' not in st.session_state:
    st.session_state.canonical_object = None
if 'intended_use' not in st.session_state:
    st.session_state.intended_use = ""
if 'db_matches' not in st.session_state:
    st.session_state.db_matches = []
if 'classification_result' not in st.session_state:
    st.session_state.classification_result = None

# Initialize engines
@st.cache_resource
def load_engines():
    extraction_engine = ExtractionEngine(TRAINING_EXAMPLES)
    rule_engine = RuleEngine()
    db_search = DatabaseSearch()
    return extraction_engine, rule_engine, db_search

extraction_engine, rule_engine, db_search = load_engines()


def main():
    st.title("🏥 Medical Device Classification System")
    st.markdown("### MDR 2017 & CDSCO Compliant")
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Process Flow")
        steps = [
            "1. Upload/Paste Intended Use",
            "2. Extract & Normalize",
            "3. Completeness Check",
            "4. Confirm Intended Use",
            "5. Database Search",
            "6. Classification",
            "7. Download Results"
        ]
        for i, step_name in enumerate(steps, 1):
            if i == st.session_state.step:
                st.markdown(f"**→ {step_name}**")
            elif i < st.session_state.step:
                st.markdown(f"✓ {step_name}")
            else:
                st.markdown(f"  {step_name}")
    
    # Main content area
    if st.session_state.step == 1:
        step_1_upload()
    elif st.session_state.step == 2:
        step_2_extract()
    elif st.session_state.step == 3:
        step_3_completeness()
    elif st.session_state.step == 4:
        step_4_confirm()
    elif st.session_state.step == 5:
        step_5_database()
    elif st.session_state.step == 6:
        step_6_classify()
    elif st.session_state.step == 7:
        step_7_download()


def step_1_upload():
    """Step 1: Upload or paste intended use document"""
    st.header("Step 1: Upload Intended Use Document")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Input Options")
        
        tab1, tab2 = st.tabs(["📝 Paste Text", "📄 Upload PDF"])
        
        with tab1:
            text_input = st.text_area(
                "Paste the Intended Use text here:",
                height=400,
                help="Copy and paste the intended use statement from your document"
            )
            
            if st.button("Process Text", type="primary", use_container_width=True):
                if text_input.strip():
                    st.session_state.raw_input = text_input
                    st.session_state.input_type = "text"
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("Please enter some text")
        
        with tab2:
            uploaded_file = st.file_uploader(
                "Upload PDF file",
                type=['pdf'],
                help="Upload a PDF containing the intended use statement"
            )
            
            if uploaded_file and st.button("Process PDF", type="primary", use_container_width=True):
                # Extract text from PDF
                from pdf_extractor import extract_text_from_pdf
                extracted_text = extract_text_from_pdf(uploaded_file)
                
                if extracted_text:
                    st.session_state.raw_input = extracted_text
                    st.session_state.input_type = "pdf"
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("Could not extract text from PDF")
    
    with col2:
        st.subheader("Example Training Cases")
        example_names = list(TRAINING_EXAMPLES.keys())
        selected_example = st.selectbox(
            "Load a training example:",
            ["-- Select --"] + example_names
        )
        
        if selected_example != "-- Select --":
            example = TRAINING_EXAMPLES[selected_example]
            st.text_area(
                "Example Input:",
                value=example['raw_input'],
                height=300,
                disabled=True
            )
            
            if st.button("Use This Example", use_container_width=True):
                st.session_state.raw_input = example['raw_input']
                st.session_state.input_type = "example"
                st.session_state.example_name = selected_example
                st.session_state.step = 2
                st.rerun()


def step_2_extract():
    """Step 2: Extract and normalize fields"""
    st.header("Step 2: Extraction & Normalization")
    
    with st.spinner("Extracting fields from input..."):
        # Extract using trained engine
        extracted = extraction_engine.extract(st.session_state.raw_input)
        st.session_state.extracted_data = extracted
    
    st.success("✓ Extraction complete")
    
    # Display extracted fields
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Extracted Fields")
        
        # Create editable form
        with st.form("extracted_fields_form"):
            st.markdown("**Required Fields**")
            
            device_name = st.text_input(
                "Device Name",
                value=extracted.get('device_name', ''),
                help="Official name of the device"
            )
            
            structure_function = st.text_area(
                "Structure & Function",
                value=extracted.get('structure_function', ''),
                height=100,
                help="Physical structure and functional mechanism"
            )
            
            medical_purpose = st.text_area(
                "Medical Purpose",
                value=extracted.get('medical_purpose', ''),
                height=100,
                help="Intended medical use"
            )
            
            population = st.text_input(
                "Intended Population",
                value=extracted.get('population', ''),
                help="Target patient population"
            )
            
            intended_user = st.text_input(
                "Intended User",
                value=extracted.get('intended_user', ''),
                help="Who operates the device"
            )
            
            use_environment = st.text_input(
                "Use Environment",
                value=extracted.get('use_environment', ''),
                help="Where the device is used"
            )
            
            st.markdown("---")
            st.markdown("**Classification-Critical Fields**")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                invasiveness = st.selectbox(
                    "Invasiveness",
                    ["", "non-invasive", "invasive_via_orifice", "surgically_invasive"],
                    index=["", "non-invasive", "invasive_via_orifice", "surgically_invasive"].index(
                        extracted.get('invasiveness', '')
                    ) if extracted.get('invasiveness', '') in ["", "non-invasive", "invasive_via_orifice", "surgically_invasive"] else 0
                )
                
                implantable = st.selectbox(
                    "Implantable",
                    ["unknown", "true", "false"],
                    index=0
                )
                
                duration = st.selectbox(
                    "Duration of Use",
                    ["", "transient", "short_term", "long_term"],
                    index=["", "transient", "short_term", "long_term"].index(
                        extracted.get('duration', '')
                    ) if extracted.get('duration', '') in ["", "transient", "short_term", "long_term"] else 0
                )
                
                active = st.selectbox(
                    "Active Device",
                    ["unknown", "true", "false"],
                    index=0
                )
            
            with col_b:
                body_system = st.text_input(
                    "Body System",
                    value=extracted.get('body_system', ''),
                    help="Primary body system interacted with"
                )
                
                delivers_substance = st.selectbox(
                    "Delivers Medicinal Substance",
                    ["unknown", "true", "false"],
                    index=0
                )
                
                delivers_energy = st.selectbox(
                    "Delivers Energy",
                    ["unknown", "true", "false"],
                    index=0
                )
                
                monitors_vital = st.selectbox(
                    "Monitors Vital Parameter",
                    ["unknown", "true", "false"],
                    index=0
                )
            
            st.markdown("---")
            
            col_c, col_d = st.columns(2)
            
            with col_c:
                diagnostic_role = st.selectbox(
                    "Diagnostic Role",
                    ["", "none", "assists", "independent"],
                    index=["", "none", "assists", "independent"].index(
                        extracted.get('diagnostic_role', '')
                    ) if extracted.get('diagnostic_role', '') in ["", "none", "assists", "independent"] else 0
                )
            
            with col_d:
                life_supporting = st.selectbox(
                    "Life Supporting/Sustaining",
                    ["unknown", "true", "false"],
                    index=0
                )
            
            submitted = st.form_submit_button("Continue to Completeness Check", type="primary", use_container_width=True)
            
            if submitted:
                # Update extracted data with form values
                st.session_state.extracted_data = {
                    'device_name': device_name,
                    'generic_category': extracted.get('generic_category', ''),
                    'structure_function': structure_function,
                    'medical_purpose': medical_purpose,
                    'population': population,
                    'intended_user': intended_user,
                    'use_environment': use_environment,
                    'invasiveness': invasiveness,
                    'implantable': implantable == 'true',
                    'duration': duration,
                    'body_system': body_system,
                    'active': active == 'true',
                    'delivers_medicinal_substance': delivers_substance == 'true',
                    'delivers_energy': delivers_energy == 'true',
                    'monitors_vital_parameter': monitors_vital == 'true',
                    'diagnostic_role': diagnostic_role,
                    'life_supporting': life_supporting == 'true'
                }
                st.session_state.step = 3
                st.rerun()
    
    with col2:
        st.subheader("Original Input")
        st.text_area(
            "Raw Input:",
            value=st.session_state.raw_input,
            height=600,
            disabled=True
        )


def step_3_completeness():
    """Step 3: Check completeness and ask clarifying questions"""
    st.header("Step 3: Completeness Check")
    
    extracted = st.session_state.extracted_data
    
    # Check completeness
    missing_fields, questions = extraction_engine.check_completeness(extracted)
    
    if not missing_fields:
        st.success("✓ All required fields are complete!")
        
        # Generate canonical object
        canonical = extraction_engine.create_canonical_object(extracted)
        st.session_state.canonical_object = canonical
        
        # Generate intended use statement
        intended_use = extraction_engine.generate_intended_use(canonical)
        st.session_state.intended_use = intended_use
        
        st.info("Proceeding to Intended Use confirmation...")
        
        if st.button("Continue", type="primary"):
            st.session_state.step = 4
            st.rerun()
    else:
        st.warning(f"⚠ Missing {len(missing_fields)} required field(s)")
        
        st.markdown("### Please provide the following information:")
        
        with st.form("clarification_form"):
            responses = {}
            
            for field, question_data in questions.items():
                st.markdown(f"**{question_data['question']}**")
                
                if question_data['type'] == 'text':
                    responses[field] = st.text_input(
                        f"{field}",
                        key=f"q_{field}",
                        help=question_data.get('help', '')
                    )
                elif question_data['type'] == 'select':
                    responses[field] = st.selectbox(
                        f"{field}",
                        options=question_data['options'],
                        key=f"q_{field}",
                        help=question_data.get('help', '')
                    )
                elif question_data['type'] == 'boolean':
                    responses[field] = st.radio(
                        f"{field}",
                        options=["Yes", "No"],
                        key=f"q_{field}",
                        help=question_data.get('help', '')
                    ) == "Yes"
            
            submitted = st.form_submit_button("Submit Answers", type="primary", use_container_width=True)
            
            if submitted:
                # Update extracted data with responses
                for field, value in responses.items():
                    st.session_state.extracted_data[field] = value
                
                # Re-run completeness check
                st.rerun()


def step_4_confirm():
    """Step 4: Confirm the generated intended use statement"""
    st.header("Step 4: Confirm Intended Use Statement")
    
    st.markdown("### Generated Intended Use Statement")
    
    # Display canonical object
    with st.expander("View Canonical Classification Object", expanded=False):
        st.json(st.session_state.canonical_object)
    
    # Editable intended use
    intended_use = st.text_area(
        "Intended Use Statement:",
        value=st.session_state.intended_use,
        height=400,
        help="You can edit this statement if needed"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✓ Confirm and Continue", type="primary", use_container_width=True):
            st.session_state.intended_use = intended_use
            st.session_state.step = 5
            st.rerun()
    
    with col2:
        if st.button("← Back to Edit Fields", use_container_width=True):
            st.session_state.step = 2
            st.rerun()


def step_5_database():
    """Step 5: Search CDSCO database"""
    st.header("Step 5: CDSCO Database Search")
    
    with st.spinner("Searching CDSCO database..."):
        matches = db_search.search(
            st.session_state.intended_use,
            st.session_state.canonical_object
        )
        st.session_state.db_matches = matches
    
    if matches:
        st.success(f"✓ Found {len(matches)} potential match(es)")
        
        st.markdown("### Select the best match or proceed to rule-based classification:")
        
        for i, match in enumerate(matches):
            with st.expander(f"Match {i+1}: {match['device_name']} - Class {match['class']} (Confidence: {match['confidence']:.1%})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Device Name:** {match['device_name']}")
                    st.markdown(f"**Generic Category:** {match['generic_category']}")
                    st.markdown(f"**Intended Use:**")
                    st.write(match['intended_use'])
                    st.markdown(f"**Classification:** Class {match['class']}")
                    st.markdown(f"**Authority:** {match['authority']}")
                
                with col2:
                    if st.button(f"Accept This Match", key=f"accept_{i}", type="primary", use_container_width=True):
                        st.session_state.classification_result = {
                            'source': 'database',
                            'class': match['class'],
                            'authority': match['authority'],
                            'confidence': match['confidence'],
                            'justification': f"Matched with CDSCO database entry: {match['device_name']}",
                            'matched_device': match['device_name']
                        }
                        st.session_state.step = 7
                        st.rerun()
        
        st.markdown("---")
        if st.button("None of these match - Use Rule Engine", use_container_width=True):
            st.session_state.step = 6
            st.rerun()
    
    else:
        st.info("No confident matches found in CDSCO database")
        st.markdown("Proceeding to rule-based classification...")
        
        if st.button("Continue to Rule Engine", type="primary", use_container_width=True):
            st.session_state.step = 6
            st.rerun()


def step_6_classify():
    """Step 6: Apply rule-based classification"""
    st.header("Step 6: Rule-Based Classification")
    
    with st.spinner("Applying MDR 2017 classification rules..."):
        result = rule_engine.classify(st.session_state.canonical_object)
        st.session_state.classification_result = result
    
    if result['class'] == 'UNCERTAIN':
        st.warning("⚠ Classification Uncertain")
        st.markdown(result['justification'])
        
        st.markdown("### Manual Review Required")
        st.markdown("Possible classifications based on rule evaluation:")
        for possible in result.get('possible_classes', []):
            st.markdown(f"- Class {possible['class']}: {possible['reason']}")
    else:
        st.success(f"✓ Classification Complete: Class {result['class']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Classification", f"Class {result['class']}")
            st.metric("Licensing Authority", result['authority'])
        
        with col2:
            st.metric("Confidence", f"{result['confidence']:.0%}")
            st.metric("Rule Triggered", result.get('rule_triggered', 'N/A'))
        
        st.markdown("### Justification")
        st.info(result['justification'])
        
        if 'rule_trace' in result:
            with st.expander("View Rule Evaluation Trace"):
                st.json(result['rule_trace'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Database Search", use_container_width=True):
            st.session_state.step = 5
            st.rerun()
    
    with col2:
        if st.button("Continue to Download →", type="primary", use_container_width=True):
            st.session_state.step = 7
            st.rerun()


def step_7_download():
    """Step 7: Download results"""
    st.header("Step 7: Classification Results")
    
    result = st.session_state.classification_result
    
    # Summary
    st.markdown("## Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Device Name", st.session_state.canonical_object['device_name'])
    
    with col2:
        st.metric("Classification", f"Class {result['class']}")
    
    with col3:
        st.metric("Authority", result['authority'].split('(')[0].strip())
    
    # Detailed results
    st.markdown("---")
    st.markdown("## Complete Classification Report")
    
    with st.expander("Intended Use Statement", expanded=True):
        st.write(st.session_state.intended_use)
    
    with st.expander("Canonical Classification Object", expanded=False):
        st.json(st.session_state.canonical_object)
    
    with st.expander("Classification Details", expanded=True):
        st.markdown(f"**Class:** {result['class']}")
        st.markdown(f"**Authority:** {result['authority']}")
        st.markdown(f"**Source:** {result['source']}")
        st.markdown(f"**Confidence:** {result['confidence']:.1%}")
        st.markdown(f"**Justification:**")
        st.info(result['justification'])
    
    # Generate PDF
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("📄 Generate PDF Report", type="primary", use_container_width=True):
            from pdf_generator import generate_classification_pdf
            
            pdf_bytes = generate_classification_pdf(
                st.session_state.canonical_object,
                st.session_state.intended_use,
                result
            )
            
            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_bytes,
                file_name=f"{st.session_state.canonical_object['device_name'].replace(' ', '_')}_Classification_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col2:
        if st.button("🔄 Start New Classification", use_container_width=True):
            # Reset all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    main()
