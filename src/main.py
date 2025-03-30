import os
import csv
from crew import leadgen_crew

# Define output folder
OUTPUT_FOLDER = "output"
CSV_FILENAME = os.path.join(OUTPUT_FOLDER, "leadgen_results.csv")

# Ensure the /output/ folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Start the AI workflow
if __name__ == "__main__":
    industry = input("🔍 Enter the industry for lead generation: ")
    print("\n🚀 Running Sifiso Inc. LeadGen AI...\n")
    
    # Run the AI workflow
    result = leadgen_crew.kickoff(inputs={"industry": industry})

    # Save results to CSV
    def save_leads_to_csv(leads):
        with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "AI Score", "Reason for Score"])
            for lead in leads:
                writer.writerow([lead["company_name"], lead["ai_score"], lead["reason"]])

        print("\n✅ AI Lead Scoring Complete! Results saved in:", CSV_FILENAME)

    save_leads_to_csv(result)
