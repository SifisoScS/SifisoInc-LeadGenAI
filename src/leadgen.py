import csv
import os

OUTPUT_FOLDER = "output"
CSV_FILENAME = os.path.join(OUTPUT_FOLDER, "leadgen_results.csv")

def save_leads_to_csv(leads):
    """Save leads to CSV file"""
    with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["company_name", "website", "phone", "email"])
        for lead in leads:
            writer.writerow([
                lead.get("company_name", "N/A"),
                lead.get("website", "N/A"),
                lead.get("phone", "N/A"),
                lead.get("email", "N/A"),
            ])

def read_leads_from_csv():
    """Read leads from CSV file"""
    if not os.path.exists(CSV_FILENAME):
        return []
    with open(CSV_FILENAME, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)
