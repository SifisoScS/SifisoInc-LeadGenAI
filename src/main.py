import os
import csv
from crew import leadgen_crew

# Define output folder
OUTPUT_FOLDER = "output"
CSV_FILENAME = os.path.join(OUTPUT_FOLDER, "leadgen_results.csv")

# Ensure the /output/ folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Custom rule-based lead scoring system
def score_lead(lead):
    score = 0

    # 1️⃣ Check if website exists
    if lead.get("website"):
        score += 30  # Website presence is a strong indicator

    # 2️⃣ Check if both email & phone are available
    if lead.get("email") and lead.get("phone"):
        score += 40  # Direct contact info is important

    # 3️⃣ Score based on company description length
    if lead.get("description"):
        length = len(lead["description"])
        if length > 100:
            score += 30  # More detailed descriptions indicate credibility
        elif length > 50:
            score += 20  # Shorter descriptions get fewer points

    return score

# Save results to CSV
def save_leads_to_csv(leads):
    with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Website", "Phone", "Email", "AI Score", "Reason for Score"])
        
        for lead in leads:
            lead["ai_score"] = score_lead(lead)
            reason = f"Scored based on website ({lead.get('website', 'No')}), contact info, and description length."
            writer.writerow([
                lead.get("company_name", "N/A"),
                lead.get("website", "N/A"),
                lead.get("phone", "N/A"),
                lead.get("email", "N/A"),
                lead["ai_score"],
                reason
            ])

    print("\n✅ Lead Scoring Complete! Results saved in:", CSV_FILENAME)

# Start the AI workflow
if __name__ == "__main__":
    industry = input("🔍 Enter the industry for lead generation: ")
    print("\n🚀 Running Sifiso Inc. LeadGen AI...\n")
    
    # Run the AI workflow
    result = leadgen_crew.kickoff(inputs={"industry": industry})

    # Save scored leads to CSV
    save_leads_to_csv(result)
