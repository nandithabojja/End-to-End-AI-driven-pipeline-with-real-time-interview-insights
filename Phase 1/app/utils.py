from pathlib import Path
from PyPDF2 import PdfReader
import csv
from fpdf import FPDF
from pathlib import Path
import zipfile
import json

def create_pdf(candidate_name, score, strengths, weaknesses, analysis, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add candidate details to the PDF
    # pdf.cell(200, 10, txt=f"Analysis Report for {candidate_name}", ln=True, align="C")
    # pdf.ln(10)
    # pdf.cell(200, 10, txt=f"Score: {score}", ln=True)
    # pdf.ln(10)
    # pdf.cell(200, 10, txt=f"Strengths: {strengths}", ln=True)
    # pdf.ln(10)
    # pdf.cell(200, 10, txt=f"Weaknesses: {weaknesses}", ln=True)
    # pdf.ln(10)
    pdf.multi_cell(200, 10, txt=f"Analysis: {analysis}")
    
    # Save the PDF
    pdf.output(str(pdf_path))

def process_pdfs(pdf_path: Path) -> str:
    """Extract text from a PDF file."""
    pdf_reader = PdfReader(str(pdf_path))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def create_report(results, output_dir):
    reports = []  # To store individual report file paths
    summary_csv_path = output_dir / "summary.csv"
    
    # Prepare the summary CSV
    with open(summary_csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write header
        csv_writer.writerow(["Candidate Name", "Score", "Strengths", "Weaknesses", "Analysis PDF"])
        
        for result in results:
            candidate_name = result.get("candidate_name", "Unknown_Candidate")
            score = result.get("score", 0)
            strengths = result.get("strengths", "Not Provided")
            weaknesses = result.get("weaknesses", "Not Provided")
            analysis = result.get("analysis", "Not Provided")
            
            # Create PDF Analysis
            pdf_path = output_dir / f"{candidate_name}_analysis.pdf"
            create_pdf(candidate_name, score, strengths, weaknesses, analysis, pdf_path)
            reports.append(pdf_path)
            
            # Write candidate data to CSV
            csv_writer.writerow([candidate_name, score, strengths, weaknesses, str(pdf_path)])
    
    # Add files to ZIP
    zip_path = output_dir / "reports.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        # Add the summary CSV
        zipf.write(summary_csv_path, arcname=summary_csv_path.name)
        # Add all PDFs
        for report in reports:
            zipf.write(report, arcname=report.name)
    
    return zip_path
