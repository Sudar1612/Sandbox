from anyio import Path
from dotenv import load_dotenv
load_dotenv() 


from landingai_ade import LandingAIADE
from agno.agent import Agent
from agno.models.azure import AzureOpenAI
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from pathlib import Path
import json

class AttendanceSheetPydanticModel(BaseModel):
    """Training record for a single trainee"""
    type_of_training: str = ""
    date_of_training: str = ""
    module_name: str = ""
    aircraft_type: str = ""
    name: List[str] = []
    sap_id: List[str] = []


def extract_data_from_pdf(pdf_path):
    """OCR + Agent extraction - returns dict or None"""
    try:
        # Parse document
        response = LandingAIADE().parse(document_url=pdf_path)
        extracted_text = response.markdown
        azure_model = AzureOpenAI(
            id="gpt-4o",  # Your Azure deployment name
            api_key="",
            azure_endpoint="https://example.openai.azure.com/",
            api_version=""
        )
                
        agent = Agent(
    model=azure_model,
    name="MyAgent",
    description="A helpful AI assistant",
    output_schema=AttendanceSheetPydanticModel,
    instructions=[
        """
        You are an expert aviation data extraction agent. Extract training data for ALL trainees.

        Extract:
        - type_of_training: Type of Training from checkbox (single value)
        - date_of_training: Last training date in DD-MM-YYYY format (single value)
        - module_name: Module name from module code (single value)
        - aircraft_type: Aircraft type from module code (single value)
        - name: List of all trainee names in order
        - sap_id: List of all eight digit SAP IDs in same order as names

        Return in this JSON structure:
        {
            "type_of_training": "",
            "date_of_training": "",
            "module_name": "",
            "aircraft_type": "",
            "name": ["name1", "name2"],
            "sap_id": ["12345678", "87654321"]
        }
        
        Do not skip any trainees. Extract only visible data, use empty strings/arrays for missing fields.
        Maintain the same order for names and sap_ids.
        
        Never return any explanations, only return the JSON NO PREAMBLE
        """],
            markdown=True
        )
        response = agent.run(extracted_text)
              
        return response.content
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_folder_to_excel(folder_path, output_excel):
    """Process all PDFs and save to Excel"""
    
   
    folder = Path(folder_path)
    pdf_files = list(folder.glob("*.pdf"))
    
    all_sheets = {}
    
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        
        data = extract_data_from_pdf(str(pdf_file))
        
        if data:
            columns = {
            "Type of Training": [data.type_of_training],
            "Date of Training": [data.date_of_training],
            "Module Name": [data.module_name],
            "Aircraft Type": [data.aircraft_type],
            "Name": data.name,
            "SAP ID": data.sap_id
        }

            # Find the max length among all list-like columns
            max_len = max(len(v) if isinstance(v, list) else 1 for v in columns.values())

            # Pad all columns to max_len
            for key, value in columns.items():
                if isinstance(value, list):
                    if len(value) < max_len:
                        columns[key] = value + [""] * (max_len - len(value))
                else:
                    # scalar value, repeat to fill
                    columns[key] = [value] * max_len

            # Create DataFrame
            df = pd.DataFrame(columns)
            sheet_name = pdf_file.stem[:31]
            all_sheets[sheet_name] = df
    
    # Save to Excel
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        for sheet_name, df in all_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Saved {len(all_sheets)} sheets to {output_excel}")


# Main
if __name__ == "__main__":
    process_folder_to_excel("RESULT SHEET", "test.xlsx")