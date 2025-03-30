import os
import csv
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from crewai_tools import SerperDevTool

# Load API keys
load_dotenv()
search_tool = SerperDevTool()

# Define Lead Researcher
lead_researcher = Agent(
    role="Lead Research Specialist",
    goal="Find and collect detailed business information for a given industry",
    verbose=True,
    memory=True,
    backstory="A highly skilled researcher who gathers in-depth data on companies.",
    tools=[search_tool]
)

# Define Data Cleaner Agent
data_cleaner = Agent(
    role="Lead Data Cleaner",
    goal="Filter and clean the collected business leads",
    verbose=True,
    memory=True,
    backstory="An AI agent that removes duplicates, formats data, and ensures quality.",
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
    ),
    expected_output="A list of 5 companies with detailed info.",
    tools=[search_tool],
    agent=lead_researcher,
)

# Data Cleaning Task: Remove Duplicates & Validate Data
def clean_lead_data(lead_list):
    """
    Function to filter and clean lead data.
    """
    unique_leads = {}
    for lead in lead_list:
        key = lead["company_name"].lower()  # Normalize company name
        if key not in unique_leads:
            unique_leads[key] = lead

    return list(unique_leads.values())

clean_leads_task = Task(
    description=(
        "Review and clean the collected leads:\n"
        "- Remove duplicate entries\n"
        "- Validate contact details\n"
        "- Format data properly"
    ),
    expected_output="A cleaned list of unique, valid business leads.",
    agent=data_cleaner,
)

# Create Crew
leadgen_crew = Crew(
    agents=[lead_researcher, data_cleaner],
    tasks=[find_leads_task, clean_leads_task],
    process=Process.sequential
)
