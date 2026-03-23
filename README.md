# Face Recognition & Age Prediction App

A modern Streamlit-based web application for real-time face recognition, member management, and age/gender prediction.

## 🚀 Features

- **👤 Add Member**: Capture live video to detect and encode faces, storing them for future recognition.
- **🔍 Check Member**: Recognize registered members in real-time with live performance metrics (Precision, Accuracy, F1 Score).
- **🎂 Age & Gender Prediction**: Estimate age and gender from a live camera feed.
- **🛡️ Data Privacy**: Local processing with a JSON-based database for secure member management.

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Computer Vision**: [OpenCV](https://opencv.org/)
- **Face Recognition**: [face-recognition](https://github.com/ageitgey/face_recognition) (dlib-based)
- **Database**: JSON (Local storage)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/naveen-rondla-2005/face-recognition-app.git
   cd face-recognition-app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📂 Project Structure

- `app.py`: Main Streamlit application entry point.
- `face_ops.py`: Core logic for face capture, encoding, and recognition.
- `database.py`: Module for managing the local JSON database.
- `haarcascade_frontalface_default.xml`: OpenCV Haar Cascade for face detection.
- `age_deploy.prototxt`: Model configuration for age/gender prediction.
- `requirements.txt`: Python dependencies.

## 🔒 Security Note
The `data/` directory (containing raw images/videos) and `database.json` are excluded from version control to prevent data leaks. Ensure you back up your local database manually if needed.

---
Developed by [Naveen Rondla](https://github.com/naveen-rondla-2005)
