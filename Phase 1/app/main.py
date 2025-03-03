from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import zipfile
from app.utils import process_pdfs, create_report
from app.together_api import analyze_pdf

app = FastAPI()

# Setup for templates and static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = Path("data/uploads")
REPORT_DIR = Path("data/reports")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/upload/")
async def upload_files(files: list[UploadFile], job_description: str = Form(...)):
    # Save files to the uploads directory
    pdf_paths = []
    for file in files:
        file_path = UPLOAD_DIR / file.filename
        pdf_paths.append(file_path)
        with open(file_path, "wb") as f:
            f.write(await file.read())
    
    # Process and analyze the PDFs
    analysis_results = []
    for pdf_path in pdf_paths:
        pdf_text = process_pdfs(pdf_path)
        result = analyze_pdf(pdf_text, job_description)
        analysis_results.append(result)
    
    # Create a final report
    zip_path = create_report(analysis_results, REPORT_DIR)
    
    return FileResponse(zip_path, media_type="application/zip", filename="resume_analysis.zip")
