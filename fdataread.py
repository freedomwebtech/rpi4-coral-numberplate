import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("")
firebase_admin.initialize_app(cred, {
    'databaseURL': ''
})

# Function to read data from Firebase
def read_data_from_firebase():
    ref = db.reference('number_plates')  # Reference the 'number_plates' node
    data = ref.get()  # Retrieve all data under this node

    if data:
        print("Data retrieved from Firebase:")
        for key, value in data.items():
            print(f"Key: {key}, Data: {value}")
    else:
        print("No data found in Firebase.")
        
read_data_from_firebase()        
