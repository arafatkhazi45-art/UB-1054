# UB-1054
CivicTrack is a citizen issue reporting and transparency portal that enables residents to report civic problems like potholes, garbage, streetlight failures, water leaks, and traffic issues. All reports are tracked in real time on a live map and dashboard until resolved.
Download the CivicTrack project folder and extract it if it is in ZIP format. Open the extracted folder in VS Code or any code editor.

The project structure should look like this:

civictrack/
│
├── app.py
├── database.db (auto-created on first run)
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── report.html
│ ├── dashboard.html
│ ├── map.html
│ └── admin.html
└── README.md

🧱 (Optional) Create a Virtual Environment

Open a terminal inside the project folder and run:

python -m venv venv

Activate it:

On Windows:
venv\Scripts\activate

On Mac/Linux:
source venv/bin/activate

📦 Install Required Package

Install Flask using:

pip install flask

No other Python packages are required. Bootstrap and Leaflet are loaded using CDN links.

▶️ Run the Application

Inside the project folder, run:

python app.py

🌐 Open in Browser

After running the app, open your browser and go to:

http://127.0.0.1:5000/

🔐 Admin Login (For Demo)

Username: admin
Password: 1234

🛠 Technologies Used

Python (Flask)
SQLite Database
Bootstrap 5
Leaflet.js
OpenStreetMap

📌 Notes

The SQLite database initializes automatically on the first run.
No API key is required.
The project runs completely on a local server.
