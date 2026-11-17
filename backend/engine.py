# Tax-Engine/backend/engine.py

def evaluate_tax_engine(parsed_data):
    """
    Takes the parsed dictionary from parser.py and runs deterministic
    Boolean logic gates for individual credits and entity compliance flags.
    """
    client = parsed_data.get("client_intake", {})
    dependents = parsed_data.get("dependents", [])
    entities = parsed_data.get("entities", [])
    
    results = {
        "client_name": client.get("Client_Name", "Unknown Client"),
        "tax_year": client.get("Tax_Year", "2026"),
        "filing_status": client.get("Filing_Status", "Unspecified"),
        "active_credits": [],
        "compliance_alerts": [],
        "dependent_audits": [],
        "entity_audits": []
    }
    
    # 1. Evaluate Dependents (CTC vs. ODC Gates)
    for idx, dep in enumerate(dependents, start=1):
        dep_name = dep.get("Dependent_Name", f"Dependent {idx}")
        
        valid_ssn = dep.get("Valid_SSN") is True
        no_self_support = dep.get("Provided_Over_Half_Support") is False
        citizen_res = dep.get("Citizen_Resident") is True
        not_joint = dep.get("Dep_Filing_Joint_Return") is False
        
        ctc_qualified = False
        odc_qualified = False
        
        # Core CTC Test: Valid SSN, no self-support, citizen/resident, no joint return
        if valid_ssn and no_self_support and citizen_res and not_joint:
            ctc_qualified = True
        else:
            # Fails CTC rules (e.g. ITIN holder or older qualifying relative), falls to ODC ($500)
            odc_qualified = True
            
        results["dependent_audits"].append({
            "name": dep_name,
            "ctc_eligible": ctc_qualified,
            "odc_eligible": odc_qualified
        })
        
    # 2. Evaluate 1040 Credits & Flags based on Client Intake Gates
    if client.get("Paid_Childcare") is True and client.get("Under_Care_Limite") is True:
        results["active_credits"].append({
            "credit": "Child & Dependent Care Credit (Form 2441)",
            "action": "Verify provider EIN/SSN, name, address, and total expenses paid."
        })
        
    if client.get("Paid_Higher_ed") is True and client.get("Under_Ed_Limit") is True:
        results["active_credits"].append({
            "credit": "Education Credits - AOTC / LLC (Form 8863)",
            "action": "Review Form 1098-T box 1/2 amounts and verify 4-year limit for AOTC."
        })
        
    if client.get("Contributed_Retirement") is True and client.get("Under_Savers_Limit") is True:
        results["active_credits"].append({
            "credit": "Retirement Savings Contributions Credit (Saver's Credit / Form 8880)",
            "action": "Verify traditional/Roth IRA or employer retirement plan contribution eligibility."
        })
        
    if client.get("Crypto_Activity") is True:
        results["compliance_alerts"].append({
            "category": "Digital Assets (Crypto)",
            "action": "Verify Form 1040 digital asset question is marked YES & review Form 8949 / transaction CSVs."
        })
        
    if client.get("Foreign_Accounts") is True:
        results["compliance_alerts"].append({
            "category": "Foreign Accounts / FBAR",
            "action": "Check peak aggregate balance against $10,000 threshold for FinCEN 114 (FBAR) and Sch B Part III."
        })

    # 3. Evaluate Entity-Level Compliance Flags
    for ent in entities:
        ent_name = ent.get("Entity_Name", "Unnamed Entity")
        ent_type = ent.get("Entity_Type")
        
        entity_checks = []
        
        # S-Corp Reasonable Compensation Check
        if ent_type == "1120S" and ent.get("Officer_W2_Paid") is False and ent.get("Shareholder_Distribuations") is True:
            entity_checks.append("🚨 HIGH PRIORITY: S-Corp took distributions without officer W-2 wages. Audit reasonable compensation.")
            
        # Form 7203 Basis Check
        if ent_type in ["1120S", "1065"] and (ent.get("Shareholder_Distribuations") is True or ent.get("Shareholder_Loans_Exist") is True):
            entity_checks.append("📊 Stock/Debt Basis Tracking Required (Form 7203): Reconcile beginning basis prior to filing.")
            
        # 1099 Contractor Check
        if ent.get("Contractors_Paid_600_Plus") is True:
            entity_checks.append("📋 1099-NEC Compliance: Confirm W-9s are on file and 1099-NEC forms were transmitted.")
            
        # Fixed Assets Check
        if ent.get("Fixed_Assets_Purchased_Sold") is True:
            entity_checks.append("🏢 Fixed Assets (Form 4562): Review purchase invoices for Section 179 or Bonus Depreciation.")

        results["entity_audits"].append({
            "entity_name": ent_name,
            "entity_type": ent_type,
            "checks": entity_checks
        })

    return results