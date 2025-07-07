from ultralytics import YOLO
import cv2


model=YOLO("yolo11n.pt")

#getting the classes of the cars , trucks , motorcycles etc ...
classes_ids=[1,2,3,5,7]

def detect_cars(frame):

    

    #adding the models to the frame
    results=model(frame)
    car_boxes=[]

    for box in results[0].boxes:
            
            #getting the names of the classes and id's in YOLO for every object  
            class_id=int(box.cls)
            class_name=results[0].names[class_id]
            confidence=float(box.conf)


            if (class_id in classes_ids and confidence>=0.3):

                #getting the position of the id's i want and drawing rectangle with label
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                car_boxes.append((x1, y1, x2, y2 ,class_name))
            

    #returning the location of the vehicles             
    return  car_boxes      
    

    
    