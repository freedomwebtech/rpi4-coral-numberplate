import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import google.generativeai as genai

# Initialize Firebase
cred = credentials.Certificate("rpi4-numberplate-coral-firebase-adminsdk-fbsvc-ced41e38fd.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rpi4-numberplate-coral-default-rtdb.firebaseio.com/'
})

# Initialize Google Generative AI
genai.configure(api_key="AIzaSyDZd4KxvJ3e3yhBJvIfeCIM7FtRXokwm6s")  # Add your actual API key here
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to read data from Firebase and convert to DataFrame
def read_data_to_dataframe():
    ref = db.reference('number_plates')  # Reference the 'number_plates' node
    data = ref.get()  # Retrieve all data under this node

    if data:
        print("Data retrieved from Firebase:")
        
        # Create a list to hold the rows of data
        records = []
        
        # Loop through the data to extract date, number_plate, and time
        for key, value in data.items():
            record = {
                "Date": value.get("date", ""),  # Extract the date
                "Number Plate": value.get("number_plate", ""),  # Extract the number plate
                "Time": value.get("time", "")  # Extract the time
            }
            records.append(record)  # Add the record to the list

        # Convert the list of records to a Pandas DataFrame
        df = pd.DataFrame(records)
        
        # Print the DataFrame to verify
        print("Data successfully converted to DataFrame:")
        print(df)
        
        return df
    else:
        print("No data found in Firebase.")
        return pd.DataFrame()  # Return an empty DataFrame if no data found

# Function to interact with the agent and query data
def ask_agent(query, df):
    # Define the context based on the data in the DataFrame
    context = f"Here is the data available:\n{df.to_string(index=False)}\nNow, answer the following query: {query}"
    
    # Use the model to generate a response
    response = model.generate_content(context)
    
    # Print the generated response from the agent
    return response.text

# Main function to execute
def main():
    df = read_data_to_dataframe()
    if not df.empty:
        # Ask the agent a query related to the data
        while True:
            query = input("Ask a query related to the number plate data (e.g., 'What is the number plate at 09:38:30?'): ")
            if query.lower() == 'exit':
                print("Exiting the query system.")
                break
            answer = ask_agent(query, df)
            print("Agent's response:", answer)
    else:
        print("No data to process.")

if __name__ == "__main__":
    main()
