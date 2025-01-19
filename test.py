import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("rpi4--coral-firebase-adminsdk-fbsvc-341820fd89.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rpi4--coral-default-rtdb.firebaseio.com/'
})

# Get current date and time
current_date = datetime.now().strftime('%Y-%m-%d')
current_time = datetime.now().strftime('%H:%M:%S')

# Data to store
data = {
    'number_plate': 'ABC1235',
    'date': current_date,
    'time': current_time
}

# Add data to the database
ref = db.reference('number_plates')
new_entry = ref.push(data)  # Push creates a new unique key
print(f"Data added with key: {new_entry.key}")
