import os
import csv
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from openai import OpenAI  # Import OpenAI for GPT-powered analysis

# Load API keys
load_dotenv()
search_tool = SerperDevTool()
openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI client setup
client = OpenAI(api_key=openai_api_key)

# Define Lead Researcher
lead_researcher = Agent(
    role="Lead Research Specialist",
    goal="Find and collect detailed business information for a given industry",
    verbose=True,
    memory=True,
    backstory="A highly skilled researcher who gathers in-depth data on companies.",
    tools=[search_tool]
)

# Define Lead Qualification Agent
lead_qualifier = Agent(
    role="Lead Qualification AI",
    goal="Analyze and rank business leads based on online reputation and relevance",
    verbose=True,
    memory=True,
    backstory="An AI agent that evaluates companies using GPT and assigns an AI score.",
)

# Research Task: Collect Detailed Lead Data
find_leads_task = Task(
    description=(
        "Search for businesses in {industry} and collect their information:\n"
        "- Company Name\n"
        "- Website\n"
        "- Phone\n"
        "- Email\n"
        "- Company Description\n"
        "- Online Presence Score\n"
    ),
    expected_output="A list of 5 companies with detailed info.",
    tools=[search_tool],
    agent=lead_researcher,
)

# Lead Qualification Task: AI-Powered Scoring
def ai_lead_scoring(lead_data):
    """
    Function to analyze and score leads using GPT.
    """
    prompt = f"""
    You are an AI lead qualification expert. Analyze the following company information and rank the business lead from 0 to 100 based on:
    - Industry relevance
    - Online presence and reputation
    - Website quality
    - Social media engagement

    Here is the company data:
    {lead_data}

    Provide output in this JSON format:
    {{
        "company_name": "Company XYZ",
        "ai_score": 85,
        "reason": "Strong online presence and good customer engagement"
    }}
    """

    response = client.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=150
    )
    
    return response.choices[0].message["content"]

# Task for AI Lead Scoring
qualify_leads_task = Task(
    description=(
        "Analyze the collected leads and score them based on:\n"
        "- Industry relevance\n"
        "- Online presence\n"
        "- Website quality\n"
        "- Social media activity\n\n"
        "Provide a sorted list with scores (0-100)."
    ),
    expected_output="A ranked list of leads with AI scores.",
    agent=lead_qualifier,
)

# Create Crew
leadgen_crew = Crew(
    agents=[lead_researcher, lead_qualifier],
    tasks=[find_leads_task, qualify_leads_task],
    process=Process.sequential
)

# Run AI workflow
if __name__ == "__main__":
    industry = input("🔍 Enter the industry for lead generation: ")
    print("\n🚀 Running Sifiso Inc. LeadGen AI...\n")
    result = leadgen_crew.kickoff(inputs={"industry": industry})

    # Save results to CSV
    csv_filename = "leadgen_results.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "AI Score", "Reason for Score"])
        for lead in result:
            writer.writerow([lead["company_name"], lead["ai_score"], lead["reason"]])

    print("\n✅ AI Lead Scoring Complete! Results saved in:", csv_filename)
