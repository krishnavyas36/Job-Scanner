import requests
import openpyxl
from bs4 import BeautifulSoup

from serpapi import GoogleSearch
import openpyxl

SERPAPI_KEY = "61ba0b7e529437e98014f05ccbec7288fdf4a00cbe66cb4adf24984d4e668953"  # Get a free API key from https://serpapi.com/

def search_career_page(company_name):
    params = {
        "engine": "google",
        "q": f"{company_name} careers",
        "api_key": SERPAPI_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    for result in results.get("organic_results", []):
        if "careers" in result.get("link", "").lower():
            return result["link"]
    return "Not Found"

def update_excel_with_links(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    
    sheet["B1"] = "Career Page URL"
    
    for row in range(2, sheet.max_row + 1):
        company_name = sheet[f"A{row}"].value
        if company_name:
            career_link = search_career_page(company_name)
            sheet[f"B{row}"] = career_link
            print(f"{company_name}: {career_link}")
    
    wb.save(file_path)
    print("Excel file updated successfully!")

# Usage
file_path = r"C:\Users\dkris\Downloads\h1b_sponsoring_companies.xlsx"  # Change to your Excel file path
update_excel_with_links(file_path)