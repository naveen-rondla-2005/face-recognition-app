import cv2
import face_recognition
import os
import time
from database import add_member, get_all_members
import streamlit as st

def capture_images(name, age, gender):
    cap = cv2.VideoCapture(0)
    img_dir = "data"
    
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_path = os.path.join(img_dir, f"{name}.mp4")
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (frame_width, frame_height))

    stframe = st.empty() 
    
    start_time = time.time()
    record_duration = 5
    face_captured = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)

        if not face_captured:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            if face_locations:
                
                largest_face_location = max(face_locations, key=lambda loc: (loc[2] - loc[0]) * (loc[1] - loc[3]))
                face_encodings = face_recognition.face_encodings(rgb_frame, [largest_face_location])
                if face_encodings:
                    add_member(name, age, gender, face_encodings[0])
                    img_path = os.path.join(img_dir, f"{name}.jpg")
                    cv2.imwrite(img_path, frame)
                    face_captured = True
        
        
        display_frame = frame.copy()
        time_left = max(0, int(record_duration - (time.time() - start_time)))
        cv2.putText(display_frame, f"Recording Video: {time_left}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if face_captured:
             cv2.putText(display_frame, "Face Encoding Saved!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        stframe.image(cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB), caption='Capturing Video...', use_column_width=True)
        
        if time.time() - start_time > record_duration:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return 1 if face_captured else 0

def verify_member_live():
    members = get_all_members()
    if not members:
        return

    known_encodings = [member["face_encoding"] for member in members.values()]
    member_names = list(members.keys())

    
    tp = 0
    fp = 0
    fn = 0
    tn = 0

    cap = cv2.VideoCapture(0)

    
    stframe = st.empty()
    metrics_placeholder = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        detected_names = []
        if face_locations:
            # Find the largest face
            largest_face_location = max(face_locations, key=lambda loc: (loc[2] - loc[0]) * (loc[1] - loc[3]))
            face_encodings = face_recognition.face_encodings(rgb_frame, [largest_face_location])

            for i, face_encoding in enumerate(face_encodings):
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                top, right, bottom, left = largest_face_location

                if True in matches:
                    match_index = matches.index(True)
                    name = member_names[match_index]
                    detected_names.append(name)
                    member_data = members[name]

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    info_text = f"{name}, {member_data['age']}"
                    cv2.putText(frame, info_text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    
                    tp += 1
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                    
                    fp += 1

        
        fn += max(0, len(member_names) - len(detected_names))

        
        tn = 0

        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        accuracy = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0
        f1score = 2 * (precision * accuracy) / (precision + accuracy) if (precision + accuracy) > 0 else 0

        
        metrics_placeholder.markdown(f"""
        **Precision:** {precision:.2f}  
        **Accuracy:** {accuracy:.2f}  
        **F1 Score:** {f1score:.2f}
        """)

        
        stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption='Verifying Member...', use_column_width=True)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def predict_age_live():
    stframe = st.empty()
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        if face_locations:
            age_gender_preds = face_recognition.face_encodings(rgb_frame, face_locations)
            for i, face_encoding in enumerate(age_gender_preds):
                age = "Unknown"
                gender = "Unknown"
                top, right, bottom, left = face_locations[i]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, f"Age: {age}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(frame, f"Gender: {gender}", (left, top - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption='Predicting Age...', use_column_width=True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()