import pandas as pd
import os

def parse_tax_intake(filepath):
    """
    Opens the master intake Excel workbook and parses Client_Intake,
    all dynamic Dependent tabs, and Entity_Info into a structured dictionary.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find intake template at: {filepath}")
        
    xls = pd.ExcelFile(filepath)
    
    parsed_package = {
        "client_intake": {},
        "dependents": [],
        "entities": []
    }
    
    # 1. Parse Client_Intake Tab
    if "Client_Intake" in xls.sheet_names:
        df_client = pd.read_excel(xls, sheet_name="Client_Intake", header=None)
        for _, row in df_client.iterrows():
            key = row[0]
            val = row[1]
            
            if pd.notna(key) and isinstance(key, str):
                if key.startswith("---") or "Comments" in key:
                    continue
                clean_key = key.strip()
                parsed_package["client_intake"][clean_key] = None if pd.isna(val) else val

    # 2. Parse Dynamic Dependent Tabs (Dependent_1, Dependent_2, etc.)
    dep_sheets = [s for s in xls.sheet_names if s.startswith("Dependent")]
    for sheet in dep_sheets:
        df_dep = pd.read_excel(xls, sheet_name=sheet, header=None)
        dep_dict = {}
        for _, row in df_dep.iterrows():
            key = row[0]
            val = row[1]
            
            if pd.notna(key) and isinstance(key, str):
                if key.startswith("---") or "Comments" in key:
                    continue
                clean_key = key.strip()
                dep_dict[clean_key] = None if pd.isna(val) else val
                
        # Only keep the dependent tab if a name or DOB is populated
        if dep_dict.get("Dependent_Name") or dep_dict.get("DOB"):
            parsed_package["dependents"].append(dep_dict)

    # 3. Parse Entity_Info Tab
    if "Entity_Info" in xls.sheet_names:
        df_ent = pd.read_excel(xls, sheet_name="Entity_Info", header=None)
        ent_dict = {}
        for _, row in df_ent.iterrows():
            key = row[0]
            val = row[1]
            
            if pd.notna(key) and isinstance(key, str):
                if key.startswith("---") or "Comments" in key:
                    continue
                clean_key = key.setItem(clean_key, val) if hasattr(ent_dict, 'setItem') else None # standard dict below
                clean_key = key.strip()
                ent_dict[clean_key] = None if pd.isna(val) else val
                
        # Only keep entity info if an Entity Name is populated
        if ent_dict.get("Entity_Name"):
            parsed_package["entities"].append(ent_dict)

    return parsed_package