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

     deps_html = ""
    for d in dependent_audits:
        ctc_badge = "<span class='badge ctc'>CTC Eligible ($2,000)</span>" if d['ctc_eligible'] else "<span class='badge odc'>Fails CTC -> ODC Eligible ($500)</span>"
        deps_html += f"""
        <tr>
            <td><strong>{d['name']}</strong></td>
            <td>{ctc_badge}</td>
        </tr>
        """
    if not dependent_audits:
        deps_html = "<tr><td colspan='2' class='none-text'>No dependents listed.</td></tr>"

    entities_html = ""
    for e in entity_audits:
        checks_list = "".join([f"<li>{chk}</li>" for chk in e['checks']])
        if not checks_list:
            checks_list = "<li>No compliance flags triggered. All clear.</li>"
        
        entities_html += f"""
        <div class="entity-block">
            <h3>🏢 {e['entity_name']} <span class='tag'>Type: {e['entity_type']}</span></h3>
            <ul>{checks_list}</ul>
        </div>
        """
    if not entity_audits:
        entities_html = "<p class='none-text'>No business entities reported.</p>"

    # Complete HTML Document Template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Tax Review Chart - {client_name}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.5; color: #333; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #f8f9fa; }}
        header {{ background: #1e293b; color: #fff; padding: 24px; border-radius: 8px; margin-bottom: 24px; }}
        header h1 {{ margin: 0 0 8px 0; font-size: 24px; }}
        header p {{ margin: 0; color: #94a3b8; font-size: 14px; }}
        h2 {{ border-bottom: 2px solid #cbd5e1; padding-bottom: 6px; margin-top: 32px; color: #1e293b; font-size: 18px; }}
        .card {{ background: #fff; border: 1px solid #e2e8f0; padding: 16px; border-radius: 6px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .alert-card {{ border-left: 4px solid #ef4444; }}
        .credit-card {{ border-left: 4px solid #3b82f6; }}
        .entity-block {{ background: #fff; border: 1px solid #e2e8f0; padding: 16px; border-radius: 6px; margin-bottom: 12px; }}
        table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 6px; overflow: hidden; border: 1px solid #e2e8f0; }}
        th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid #f1f5f9; }}
        th {{ background: #f8fafc; font-weight: 600; color: #475569; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }}
        .badge.ctc {{ background: #dcfce7; color: #166534; }}
        .badge.odc {{ background: #fef9c3; color: #854d0e; }}
        .tag {{ float: right; font-size: 13px; background: #e2e8f0; padding: 2px 8px; border-radius: 4px; color: #475569; }}
        .none-text {{ color: #94a3b8; font-style: italic; }}
    </style>
</head>
<body>
    <header>
        <h1>Tax Review Chart: {client_name}</h1>
        <p>Tax Year: {tax_year} | Filing Status: {filing_status}</p>
    </header>

    <h2>Active Credits & Incentives</h2>
    {credits_html}

    <h2>Compliance & Risk Alerts</h2>
    {alerts_html}

    <h2>Dependent Qualification Audit</h2>
    <table>
        <tr>
            <th>Dependent Name</th>
            <th>Qualification Status</th>
        </tr>
        {deps_html}
    </table>

    <h2>Entity-Level Compliance</h2>
    {entities_html}

</body>
</html>
"""

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Successfully generated HTML Review Chart at: {output_filepath}")
