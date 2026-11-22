# Tax-Engine/backend/html_generator.py

def generate_html_report(evaluated_data, output_filepath="tax_review_chart.html"):
    client_name = evaluated_data.get("client_name", "Client")
    tax_year = evaluated_data.get("tax_year", "2026")
    filing_status = evaluated_data.get("filing_status", "N/A")

    active_credits = evaluated_data.get("active_credits", [])
    compliance_alerts = evaluated_data.get("compliance_alerts", [])
    dependent_audits = evaluated_data.get("dependent_audits", [])
    entity_audits = evaluated_data.get("entity_audits", [])

    # Build HTML Content Blocks
    credits_html = ""
    for c in active_credits:
        credits_html += f"""
        <div class="card credit-card">
            <h4>{c['credit']}</h4>
            <p><strong>Action Required:</strong> {c['action']}</p>
        </div>
        """
    if not active_credits:
        credits_html = "<p class='none-text'>No active credits triggered.</p>"

    alerts_html = ""
    for a in compliance_alerts:
        alerts_html += f"""
        <div class="card alert-card">
            <h4>⚠️ {a['category']}</h4>
            <p><strong>Action Required:</strong> {a['action']}</p>
        </div>
        """
    if not compliance_alerts:
        alerts_html = "<p class='none-text'>No high-priority compliance alerts.</p>"
