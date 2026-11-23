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

    # Verify the master intake workbook exists before running
    if not os.path.exists(input_file):
        print(f"\n❌ ERROR: Master intake file not found at:\n   {input_file}")
        print("\nPlease ensure 'TAX_INTAKE_MASTER.xlsx' is placed inside your '/data' folder.")
        sys.exit(1)

    try:
        # Step 1: Parse Excel Workbook
        print("\n[1/3] Parsing master Excel intake workbook...")
        parsed_data = parse_tax_intake(input_file)
        client_name = parsed_data.get("client_intake", {}).get("Client_Name", "Unknown_Client")
        print(f"      ✔ Successfully ingested intake data for: {client_name}")
