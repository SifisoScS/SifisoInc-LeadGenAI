import requests
from bs4 import BeautifulSoup
import csv
from crewai_tools import SerperDevTool

# Initialize web search tool
search_tool = SerperDevTool()

def get_extra_details(website_url):
    """Scrape additional details from company website."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(website_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Example: Extract the 'About' section (modify based on the site)
            about_section = soup.find("meta", {"name": "description"})
            return about_section["content"] if about_section else "No description available"
    except Exception as e:
        return f"Error fetching details: {str(e)}"

def save_leads_to_csv(leads):
    """Save leads to a CSV file."""
    filename = "leads.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Company", "Website", "Phone", "Email", "Address", "About"])
        for lead in leads:
            writer.writerow([lead["name"], lead["website"], lead["phone"], lead["email"], lead["address"], lead["about"]])
    print(f"✅ Leads saved to {filename}")

def search_leads(industry):
    """Search for businesses and enrich them with scraped data."""
    search_results = search_tool.run(f"Top 5 {industry} companies in South Africa with contact details")
    
    leads = []
    for result in search_results[:5]:  # Limit to top 5
        website = result.get("link", "N/A")
        about_text = get_extra_details(website)

        leads.append({
            "name": result.get("title", "N/A"),
            "website": website,
            "phone": "N/A",  # Can extract this with deeper scraping
            "email": "N/A",  # Needs extra scraping
            "address": "N/A",
            "about": about_text
        })

    save_leads_to_csv(leads)
    return leads
