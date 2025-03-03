from pathlib import Path
from PyPDF2 import PdfReader
from fpdf import FPDF
import zipfile

def create_pdf(candidate_name, analysis, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add analysis to the PDF
    pdf.multi_cell(200, 10, txt=f"Analysis Report for {candidate_name}\n\n{analysis}")
    
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
    
    # Generate PDFs
    for result in results:
        candidate_name = result.get("candidate_name", "Unknown_Candidate")
        file_name = result.get("file_name", "unknown")  # Original file name without extension
        analysis = result.get("analysis", "Not Provided")
        
        # Create PDF Analysis with the original file name
        pdf_path = output_dir / f"{file_name}_analysis.pdf"
        create_pdf(candidate_name, analysis, pdf_path)
        reports.append(pdf_path)
    
    # Add files to ZIP
    zip_path = output_dir / "reports.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for report in reports:
            zipf.write(report, arcname=report.name)
    
    return zip_path
