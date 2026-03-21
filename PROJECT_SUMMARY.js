const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType, PageBreak } = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: "1f4788" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "1f4788" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 160, after: 160 }, outlineLevel: 2 } },
    ]
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: 1, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: 0, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      // Title
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Medical Device Classification System")]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Project Delivery Documentation",
          italics: true,
          size: 24
        })]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      // Executive Summary
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Executive Summary")]
      }),
      
      new Paragraph({
        children: [new TextRun("This document provides comprehensive documentation for the Medical Device Classification System - a deterministic, training-based solution for classifying medical devices according to MDR 2017 and CDSCO guidelines.")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Key Features:",
          bold: true
        })]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("100% deterministic classification using pattern matching and rule evaluation")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Trained on 11 comprehensive real-world examples covering Classes A through D")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Zero dependency on LLM for core extraction and classification logic")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("CDSCO database search before rule application")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Complete 7-step workflow from upload to PDF report generation")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Professional PDF reports with full justification and rule traces")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      // System Architecture
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("System Architecture")]
      }),
      
      new Paragraph({
        children: [new TextRun("The system follows a strict 7-step workflow designed to ensure complete, accurate classification while maintaining full transparency and regulatory compliance.")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("Workflow Steps")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Upload/Paste Intended Use: ",
          bold: true
        }), new TextRun("User provides input via text paste, PDF upload, or training example selection")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Extract & Normalize: ",
          bold: true
        }), new TextRun("Pattern-matching engine extracts structured fields using training data")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Completeness Check: ",
          bold: true
        }), new TextRun("Deterministic validation ensures all classification-critical fields are present")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Confirm Intended Use: ",
          bold: true
        }), new TextRun("User reviews and confirms the generated formal intended use statement")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Database Search: ",
          bold: true
        }), new TextRun("System searches CDSCO reference database for existing similar devices")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Classification: ",
          bold: true
        }), new TextRun("If no database match, MDR 2017 rule engine evaluates D→C→B→A")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Download Report: ",
          bold: true
        }), new TextRun("Professional PDF report with classification, justification, and full details")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      // Core Components
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Core Components")]
      }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("1. Extraction Engine (extraction_engine.py)")]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Purpose: ",
          bold: true
        }), new TextRun("Extract and normalize intended use fields using pattern matching learned from training examples.")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Key Methods:",
          bold: true
        })]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("extract(text): Main extraction using regex and keyword patterns")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("check_completeness(extracted): Validates all required fields present")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("create_canonical_object(extracted): Formats into standard classification object")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("generate_intended_use(canonical): Produces formal intended use statement")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("2. Rule Engine (rule_engine.py)")]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Purpose: ",
          bold: true
        }), new TextRun("Apply MDR 2017 classification rules deterministically. Evaluates highest risk first (D→C→B→A) and stops at first match.")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Classification Rules:",
          bold: true
        })]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [1400, 4000, 3960],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 1400, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Class", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Key Triggers", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 3960, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Example", bold: true })] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 1400, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "D", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Implantable active CNS/cardiac device, Life-supporting")] })]
              }),
              new TableCell({
                borders, width: { size: 3960, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Deep brain stimulator")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 1400, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "C", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Long-term surgically invasive, Active drug delivery, Vital monitoring in critical care")] })]
              }),
              new TableCell({
                borders, width: { size: 3960, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Infusion pump, Orthopedic implant, NICU monitor")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 1400, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "B", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Active non-invasive monitoring/diagnostic")] })]
              }),
              new TableCell({
                borders, width: { size: 3960, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Wearable cardiac monitor")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 1400, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "A", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Non-invasive passive, transient contact")] })]
              }),
              new TableCell({
                borders, width: { size: 3960, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Adhesive wound dressing")] })]
              })
            ]
          })
        ]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("3. Database Search (database_search.py)")]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Purpose: ",
          bold: true
        }), new TextRun("Search CDSCO reference database before applying rules. Uses multi-factor similarity scoring.")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Scoring Factors:",
          bold: true
        })]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Keyword Similarity (40%): Overlap between input and database keywords")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Text Similarity (30%): Sequence matching of intended use statements")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Category Similarity (30%): Comparison of classification characteristics")]
      }),
      
      new Paragraph({ children: [new PageBreak()] }),
      
      // Training Data
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Training Data")]
      }),
      
      new Paragraph({
        children: [new TextRun("The system is trained on 11 comprehensive examples that cover the full range of device classes and types:")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [3500, 4000, 1860],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3500, type: WidthType.DXA },
                shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Device Name", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Type", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 1860, type: WidthType.DXA },
                shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Class", bold: true })] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3500, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("CardioBand")] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Wearable cardiac monitor")] })]
              }),
              new TableCell({
                borders, width: { size: 1860, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("B")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3500, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("PainRelief Patch")] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Transdermal drug delivery")] })]
              }),
              new TableCell({
                borders, width: { size: 1860, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("A")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3500, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("OrthoFix Bone Screw")] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Orthopedic bone fixation implant")] })]
              }),
              new TableCell({
                borders, width: { size: 1860, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("C")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3500, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("NeuroPulse DBS System")] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Implantable deep brain stimulator")] })]
              }),
              new TableCell({
                borders, width: { size: 1860, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("D")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3500, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("7 additional examples")] })]
              }),
              new TableCell({
                borders, width: { size: 4000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Monitors, software, surgical devices")] })]
              }),
              new TableCell({
                borders, width: { size: 1860, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("A-C")] })]
              })
            ]
          })
        ]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      // File Structure
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Project File Structure")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [3000, 6360],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3000, type: WidthType.DXA },
                shading: { fill: "F5F5F5", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "File", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 6360, type: WidthType.DXA },
                shading: { fill: "F5F5F5", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Description", bold: true })] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "app.py", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 6360, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Main Streamlit UI application - 7-step workflow")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "extraction_engine.py", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 6360, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Pattern-based field extraction from training data")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "rule_engine.py", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 6360, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("MDR 2017 deterministic classification rules")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "database_search.py", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 6360, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("CDSCO reference database search engine")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "training_data.py", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 6360, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("11 training examples with canonical objects")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "pdf_extractor.py", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 6360, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("PDF text extraction (digital + OCR support)")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "pdf_generator.py", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 6360, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Professional PDF report generation")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, width: { size: 3000, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "requirements.txt", bold: true })] })]
              }),
              new TableCell({
                borders, width: { size: 6360, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Python package dependencies")] })]
              })
            ]
          })
        ]
      }),
      
      new Paragraph({ children: [new PageBreak()] }),
      
      // Installation & Usage
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Installation & Usage")]
      }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("Quick Start")]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "For macOS/Linux:",
          bold: true
        })]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "./run.sh",
          font: "Courier New"
        })]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun({
          text: "For Windows:",
          bold: true
        })]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "run.bat",
          font: "Courier New"
        })]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun("The launcher scripts will automatically create a virtual environment, install dependencies, and start the application.")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("Manual Installation")]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "1. Install dependencies:",
          bold: true
        })]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "pip install -r requirements.txt",
          font: "Courier New"
        })]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun({
          text: "2. Run application:",
          bold: true
        })]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "streamlit run app.py",
          font: "Courier New"
        })]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun("The application will open in your default browser at http://localhost:8501")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      // Key Design Decisions
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Key Design Decisions")]
      }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("1. Zero LLM Dependency for Core Logic")]
      }),
      
      new Paragraph({
        children: [new TextRun("All extraction and classification is performed using deterministic algorithms. Pattern matching is learned from training examples, not generated by LLM. This ensures:")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Consistent, reproducible results")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Full transparency and auditability")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Regulatory compliance and explainability")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("No risk of hallucination or inconsistency")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("2. Training-Based Pattern Learning")]
      }),
      
      new Paragraph({
        children: [new TextRun("The system builds extraction patterns from 11 comprehensive training examples. Each example includes:")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Raw input text (as users would provide)")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Complete canonical classification object")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Expected classification result")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Formal intended use statement")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("3. Database-First Approach")]
      }),
      
      new Paragraph({
        children: [new TextRun("The system always attempts to find existing CDSCO database matches before applying rules. This:")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Leverages regulatory precedent")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Reduces processing time")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Provides additional validation")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Identifies similar approved devices")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("4. Explicit Uncertainty Handling")]
      }),
      
      new Paragraph({
        children: [new TextRun("The rule engine makes up to 2 classification attempts. If still uncertain, it explicitly declares 'UNCERTAIN' rather than forcing a classification. This ensures:")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("No incorrect classifications")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Clear indication when manual review is needed")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Borderline cases properly flagged")]
      }),
      
      new Paragraph({ children: [new PageBreak()] }),
      
      // Regulatory Compliance
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Regulatory Compliance")]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "MDR 2017 Alignment:",
          bold: true
        })]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Classification rules directly implement MDR 2017 First Schedule")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("D→C→B→A evaluation order follows regulatory guidance")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("All rule triggers are based on regulation text")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun({
          text: "CDSCO Guidelines:",
          bold: true
        })]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Licensing authority assignment follows CDSCO rules")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Class A/B → State Authority")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Class C/D → Central Authority (CDSCO)")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Auditability:",
          bold: true
        })]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Complete rule trace in every classification")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Canonical object shows all decision inputs")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("PDF reports include full justification")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("No black-box LLM decisions")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      // Future Enhancements
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Future Enhancements")]
      }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("Recommended Additions")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Live CDSCO Database Integration: ",
          bold: true
        }), new TextRun("Replace static reference database with live API integration")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Advanced OCR: ",
          bold: true
        }), new TextRun("Implement full pdf2image + Tesseract pipeline for scanned PDFs")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Multi-Language Support: ",
          bold: true
        }), new TextRun("Add support for regional languages beyond English")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Batch Processing: ",
          bold: true
        }), new TextRun("Enable classification of multiple devices simultaneously")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "API Endpoint: ",
          bold: true
        }), new TextRun("Create REST API for integration with other systems")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Admin Dashboard: ",
          bold: true
        }), new TextRun("Add interface for managing training examples and rules")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({
          text: "Version Control: ",
          bold: true
        }), new TextRun("Track classification history and rule changes over time")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      // Important Disclaimers
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Important Disclaimers")]
      }),
      
      new Paragraph({
        children: [new TextRun({
          text: "⚠ Regulatory Review Required",
          bold: true,
          size: 28
        })]
      }),
      
      new Paragraph({
        children: [new TextRun("This system is a decision support tool and does NOT replace qualified regulatory professionals. All classifications must be reviewed and validated by regulatory experts before submission to licensing authorities.")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Scope of Use:",
          bold: true
        })]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Intended for preliminary classification guidance")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Supports regulatory strategy development")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Facilitates internal device categorization")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("NOT a substitute for official regulatory determination")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        children: [new TextRun({
          text: "Accuracy Considerations:",
          bold: true
        })]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Novel devices may not match training patterns")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Borderline cases require expert judgment")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Regulatory interpretations may vary")]
      }),
      
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("System declares 'UNCERTAIN' when appropriate")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      new Paragraph({ children: [new TextRun("")] }),
      
      // Contact & Support
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Contact & Support")]
      }),
      
      new Paragraph({
        children: [new TextRun("For questions, issues, or enhancement requests:")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Review the README.md for detailed documentation")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Check QUICKSTART.md for common issues and solutions")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Examine training examples for similar device types")]
      }),
      
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Review rule traces to understand classification logic")]
      }),
      
      new Paragraph({ children: [new TextRun("")] }),
      new Paragraph({ children: [new TextRun("")] }),
      
      // Footer
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({
          text: "Medical Device Classification System v1.0",
          italics: true,
          size: 20,
          color: "666666"
        })]
      }),
      
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({
          text: "Based on MDR 2017 and CDSCO Medical Device Rules",
          italics: true,
          size: 20,
          color: "666666"
        })]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('Project_Summary.docx', buffer);
  console.log('Project summary document created successfully');
});
