import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from tools.scraper import search_leads  # ✅ Correct if running from src/tools/scraper.py

# Load API keys
load_dotenv()
search_tool = SerperDevTool()

# Define Agents
lead_researcher = Agent(
    role="Lead Research Specialist",
    goal="Find potential business leads in a given industry",
    verbose=True,
    memory=True,
    backstory="A highly skilled researcher who specializes in finding companies that match the given criteria.",
    tools=[search_tool]
)

data_collector = Agent(
    role="Lead Data Collector",
    goal="Extract and structure lead data",
    verbose=True,
    memory=True,
    backstory="An AI agent responsible for compiling contact details into an organized lead list.",
    tools=[search_tool]
)

# Define Tasks
find_leads_task = Task(
    description="Search for businesses in {industry} using online sources and provide their website and contact details.",
    expected_output="A list of 5 companies with their website and contact details.",
    tools=[search_tool],
    agent=lead_researcher,
)

compile_leads_task = Task(
    description="Format the gathered leads into a structured list and save them to a CSV file.",
    expected_output="A structured lead list saved as a CSV file.",
    agent=data_collector,
    function=search_leads  # This is where we use our new scraper function
)

# Create Crew
leadgen_crew = Crew(
    agents=[lead_researcher, data_collector],
    tasks=[find_leads_task, compile_leads_task],
    process=Process.sequential
)
