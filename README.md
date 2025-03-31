# Flask JSON File Processor

This project is a **Flask-based backend** that processes uploaded JSON files via an API, merges the data, and returns structured insights. The backend is deployed on **Render** using **Gunicorn** for production readiness.

---

## 🚀 Features

- Upload and process two JSON files (locations & metadata) via API.
- Count valid data points per type (e.g., restaurants, hotels, cafes, museums, parks).
- Calculate the **average rating** per type.
- Identify the **most reviewed location**.
- Detect locations with **incomplete data** (bonus feature).
- Simple frontend for file uploads.

---

## 🛠 Tech Stack

- **Backend:** Flask, Gunicorn, Flask-CORS
- **Frontend:** HTML, JavaScript, Fetch API
- **Deployment:** Render

---

## 📂 Project Structure

```
📁 project-directory/
│── app.py                 # Flask backend (main file)
│── requirements.txt        # Python dependencies
│
│────── index.html          # Simple frontend for uploads
│── static/
│   └── script.js           # Frontend logic
│── README.md               # Project documentation
```

---

## 🔧 Setup & Installation

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Flask Server**

```bash
python app.py
```

Your Flask app will be running on `http://127.0.0.1:5000/`.

---

## 🔄 API Endpoints

### **Upload JSON Files & Process Data**

#### **Endpoint:** `POST /process-data`

#### **Request:**

Send two JSON files (`locations.json` and `metadata.json`) via **multipart/form-data**.

```bash
curl -X POST http://127.0.0.1:5000/process-data \
  -F "locations=@locations.json" \
  -F "metadata=@metadata.json"
```

#### **Response Example:**

```json
{
  "valid_points_per_type": { "restaurant": 5, "hotel": 3 },
  "average_rating_per_type": { "restaurant": 4.2, "hotel": 3.8 },
  "most_reviewed_location": { "id": 10, "name": "Best Cafe", "reviews": 250 },
  "incomplete_data": [15, 20]
}
```

---

## 🌐 Frontend Usage

Open `index.html` in a browser and upload JSON files. The response will be displayed beautifully.

---

## 🚀 Deploying on Render

### **1️⃣ Install Gunicorn**

```bash
pip install gunicorn
```

### **2️⃣ Create ****`requirements.txt`**

```bash
pip freeze > requirements.txt
```

### **3️⃣ Push to GitHub**

```bash
git add .
git commit -m "Configured Render Deployment"
git push origin main
```

### **4️⃣ Deploy on Render**

- Go to [Render](https://render.com/)
- Create a new **Web Service**
- Connect your GitHub repo
- Set the **Start Command:**

```bash
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

- Deploy & get your live URL

---

## 🛠 Troubleshooting

### **Fix CORS Issues**

If CORS errors occur in the frontend, install Flask-CORS:

```bash
pip install flask-cors
```

And modify **`app.py`**:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Enable CORS
```

---

Input file eg. 
##location.json
![image](https://github.com/user-attachments/assets/5732b14f-8de0-434b-ae1a-d9504b97ce7e)

metadata.json

![image](https://github.com/user-attachments/assets/a88c9e43-bd6c-4cb4-8b0b-1626ab304bdc)

















