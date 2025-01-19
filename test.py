import cv2
import pandas as pd
from ultralytics import YOLO
from paddleocr import PaddleOCR
from tracker import Tracker
import cvzone
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

ocr = PaddleOCR()

# Initialize Firebase
cred = credentials.Certificate("rpi4-numberplate-coral-firebase-adminsdk-fbsvc-7cdd1fda67.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rpi4-numberplate-coral-default-rtdb.firebaseio.com/'
})


model = YOLO('best_full_integer_quant_edgetpu.tflite')


cap = cv2.VideoCapture('num1.mp4')



frame_count = 0
cy1=79
offset=10
tracker=Tracker()
def perform_ocr(image_array):
    if image_array is None:
        raise ValueError("Image is None")
    
    # Perform OCR on the image array
    results = ocr.ocr(image_array, rec=True)  # rec=True enables text recognition
    detected_text = []

    # Process OCR results
    if results[0] is not None:
        for result in results[0]:
            text = result[1][0]
            detected_text.append(text)

    # Join all detected texts into a single string
    return ''.join(detected_text)

list1=[]


# Data to store
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame=cv2.resize(frame,(1020,600))
    

    frame_count += 1
    if frame_count % 2 != 0:
        continue

    results = model.predict(frame,imgsz=240)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    list=[]
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
    
       
        list.append([x1,y1,x2,y2])
    bbox_idx=tracker.update(list)
    for bbox in bbox_idx:
        x3,y3,x4,y4,id=bbox
        cx=int(x3+x4)//2
        cy=int(y3+y4)//2
        if cy1<(cy+offset) and cy1>(cy-offset):

           if list1.count(id)==0:
               list1.append(id)
               crop = frame[y3:y4, x3:x4]
               crop = cv2.resize(crop, (120, 85))
               text = perform_ocr(crop)
               print(f"Detected Number Plate: {text}")
               # Get current date and time
               current_date = datetime.now().strftime('%Y-%m-%d')
               current_time = datetime.now().strftime('%H:%M:%S:%P')

               # Data to store
               data = {
                   'number_plate': text,
                   'date': current_date,
                   'time': current_time
                  }

               # Add data to the database
               ref = db.reference('number_plates')
               new_entry = ref.push(data)  # Push creates a new unique key
#              print(f"Data added with key: {new_entry.key}")

#           cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
#        cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)

    cv2.line(frame,(1,79),(1019,79),(0,0,255),2)
    cv2.imshow("FRAME", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
