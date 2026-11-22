# Tax-Engine/backend/html_generator.py

def generate_html_report(evaluated_data, output_filepath="tax_review_chart.html"):
    client_name = evaluated_data.get("client_name", "Client")
    tax_year = evaluated_data.get("tax_year", "2026")
    filing_status = evaluated_data.get("filing_status", "N/A")
