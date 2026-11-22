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
