from pydantic import BaseModel, Field
from landingai_ade import LandingAIADE
from landingai_ade.lib import pydantic_to_json_schema

from agentic_doc.parse import parse

class ScheduleEPartI(BaseModel):
    property: str = Field(description="Extract the row heading (A or B or C) if present, return as Property A, Property B, or Property C. If not present, return N/A.")
    address_line_1: str = Field(description="Extract Address Line 1 from the document for the given property.")
    address_line_2: str = Field(description="Extract Address Line 2 from the document for the given property.")
    city: str = Field(description="Extract City from the document for the given property.")
    state: str = Field(description="Extract State from the document for the given property.")
    zip_code: str = Field(description="Extract Zip Code from the document for the given property.")
    type_of_property: str = Field(description="Extract from subheading 1b Type of Property for the given property (A, B, or C).")
    fair_rental_days: str = Field(description="Extract the exact amount for Fair Rental Days. Double-check correctness.")
    personal_use_days: str = Field(description="Extract the exact amount for Personal Use Days. Double-check correctness.")
    qjv: str = Field(description="Extract the checkbox value under QJV subheading. Return 'Yes' if checked, otherwise 'No'.")
    rents_received: str = Field(description="Extract the exact amount for Rents Received. Double-check correctness.")
    royalties_received: str = Field(description="Extract the exact amount for Royalties Received. Double-check correctness.")
    advertising: str = Field(description="Extract the exact amount from row 5 Advertising. If not present, return N/A.")
    auto_and_travel: str = Field(description="Extract the exact amount from row 6 Auto and Travel. Double-check correctness.")
    cleaning_and_maintenance: str = Field(description="Extract the exact amount from row 7 Cleaning and Maintenance. Double-check correctness.")
    commissions: str = Field(description="Extract the exact amount from row 8 Commissions. Double-check correctness.")
    insurance: str = Field(description="Extract the exact amount from row 9 Insurance. Double-check correctness.")
    legal_and_other_professional_fees: str = Field(description="Extract the exact amount from row 10 Legal and Other Professional Fees. Double-check correctness.")
    management_fees: str = Field(description="Extract the exact amount from row 11 Management Fees. Double-check correctness.")
    mortgage_interest_paid_to_banks_etc: str = Field(description="Extract the exact amount from row 12 Mortgage Interest Paid To Banks Etc. Double-check correctness.")
    other_interest: str = Field(description="Extract the exact amount from row 13 Other Interest. Double-check correctness.")
    repairs: str = Field(description="Extract the exact amount from row 14 Repairs. Double-check correctness.")
    supplies: str = Field(description="Extract the exact amount from row 15 Supplies. Double-check correctness.")
    taxes: str = Field(description="Extract the exact amount from row 16 Taxes. Double-check correctness.")
    utilities: str = Field(description="Extract the exact amount from row 17 Utilities. Double-check correctness.")
    depreciation_expense_or_depletion: str = Field(description="Extract the exact amount from row 18 Depreciation Expense Or Depletion. Double-check correctness.")
    other_description: str = Field(description="Extract the text description from row 19 Other (list). Double-check correctness.")
    other_amount: str = Field(description="Extract the amount from row 19 Other (list). Double-check correctness.")
    total_expenses: str = Field(description="Extract the exact amount from row 20 Total Expenses. Add Lines 5 through 19. Double-check correctness.")
    subtract_line_20_from_line_3_and_4: str = Field(description="Extract the exact amount from row 21 Subtract Line 20 From Line 3 (Rents) And/Or 4 (Royalties). Double-check correctness.")
    deductible_rental_real_estate_loss_after: str = Field(description="Extract the exact amount from row 22 Deductible Rental Real Estate Loss After. Double-check correctness.")


#  API key
api_key = ""

# PDF file path
pdf_path = "sample.pdf"

# Initialize client
client = LandingAIADE(apikey=api_key)


schema = pydantic_to_json_schema(ScheduleEPartI)

results = parse(pdf_path, extraction_model=ScheduleEPartI)

fields = results[0].extraction
metadata = results[0].extraction_metadata
print(f"Field value: {fields.city}, confidence: {metadata.city.confidence}")
print(fields)
