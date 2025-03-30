from crew import leadgen_crew

# Start the AI workflow
if __name__ == "__main__":
    print("🚀 Running Sifiso Inc. LeadGen AI...")
    
    # Get industry input from the user
    industry = input("🔍 Enter the industry for lead generation: ").strip()

    # Ensure input is not empty
    if not industry:
        print("⚠️ Industry cannot be empty. Please enter a valid industry.")
        exit(1)

    print(f"\n📢 Searching for leads in: {industry}...\n")

    try:
        # Run CrewAI workflow
        result = leadgen_crew.kickoff(inputs={"industry": industry})
        
        # Print formatted output
        print("\n✅ Lead Generation Complete! Here are the results:\n")
        print(result)

    except Exception as e:
        print("\n❌ An error occurred while running the AI workflow.")
        print(f"Error: {e}")
