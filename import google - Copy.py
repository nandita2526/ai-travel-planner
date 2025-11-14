import csv
import google.generativeai as genai

genai.configure(api_key="AIzaSyB3HAIz-gBUCdtQNfYzQmF9kvhy4r4rLjo")

csv_file = "travel_knowledge.csv"

def create_csv_if_not_exists():
    try:
        open(csv_file, "r")
    except FileNotFoundError:
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["keyword", "answer"])

def add_to_csv(keyword, answer):
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([keyword.lower(), answer])

def search_csv(query):
    query = query.lower()
    results = []
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            keyword, answer = row
            if keyword in query:
                results.append(answer)
    return results

destination = input("Enter destination: ")
days = input("Number of days: ")
budget = input("Budget type (Budget / Moderate / Luxury): ")
interests = input("Your interests (e.g., beaches, food, temples): ")

prompt = f"Plan a {days}-day trip to {destination} for a traveler with a {budget.lower()} budget. Interests: {interests}. Include daily plan, food suggestions, and travel tips."

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(prompt)

travel_output = response.text

print("\n----- Your Travel Plan -----\n")
print(travel_output)

create_csv_if_not_exists()
add_to_csv(destination, travel_output)

while True:
    ask = input("\nDo you have any queries? (yes/no): ").strip().lower()

    if ask == "no":
        print("Thank you! Goodbye.")
        break

    elif ask == "yes":
        user_query = input("Enter your query: ")
        results = search_csv(user_query)

        if results:
            print("\n--- Answer from Knowledge Base (CSV) ---\n")
            for ans in results:
                print(ans)
        else:
            print("\nNo stored data found for this query.")
            print("Fetching placeholder answer...\n")

            placeholder_prompt = f"List related information for: {user_query}. Keep answer short."
            placeholder = model.generate_content(placeholder_prompt).text

            print(placeholder)
            add_to_csv(user_query, placeholder)

    else:
        print("Please type only yes or no.")
