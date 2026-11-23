# Tax-Engine/main.py
import os
import sys
from backend.parser import parse_tax_intake
from backend.engine import evaluate_tax_engine
from backend.html_generator import generate_html_report

def run_pipeline():
    # Define default input/output paths relative to project root
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "data", "TAX_INTAKE_MASTER.xlsx")
    output_dir = os.path.join(base_dir, "output")
    
    print("=" * 50)
    print("🚀 Initializing Tax-Engine Compliance Pipeline...")
    print("=" * 50)
