# 🏢 Office Management System  

A **Python-based Office Management System** that helps manage employees, departments, attendance, and payroll in a structured way.  
This project demonstrates **CRUD operations, database integration, and a modular Flask architecture**.

---

## ✨ Features  

👨‍💼 **Employee Management** – Add, View, Update, Delete employees  
🏢 **Department Management** – Create & assign departments  
🕒 **Attendance System** – Mark daily check-in/check-out  
💰 **Payroll Module** – Generate salary reports  
🔑 **User Authentication** – Admin & Employee login  
📊 **Reports** – Attendance, Employee List, Payroll  
🗄️ **Database Support** – MySQL / SQLite  

---

## 🛠️ Tech Stack  

- 💻 **Language**: Python 3.x  
- ⚡ **Framework**: Flask  
- 🗄️ **Database**: MySQL / SQLite  
- 🎨 **Frontend**: HTML, CSS, JavaScript (Jinja2 Templates)  
- 📚 **Libraries**: flask, sqlalchemy, werkzeug  

---

## 📂 Project Structure  

OFFICE_MANAGEMENT_SYSTEM/  
│── app.py # Main application file  
│── config.py # Configuration (DB settings, secret keys)  
│── models.py # Database models  
│── routes.py # Route definitions  
│── static/ # CSS, JS, images  
│── templates/ # HTML templates  
│── requirements.txt # Dependencies  
│── README.md # Documentation  
└── database/  
    └── office.db # SQLite database file  

---

## 🚀 How to Run  

```bash
# 1. Clone the repository  
git clone https://github.com/your-username/OFFICE_MANAGEMENT_SYSTEM.git
cd OFFICE_MANAGEMENT_SYSTEM  

# 2. Create virtual environment (optional but recommended)  
python -m venv venv  
venv\Scripts\activate   # On Windows  
source venv/bin/activate  # On Linux/Mac  

# 3. Install dependencies  
pip install -r requirements.txt  

# 4. Run the application  
python app.py  
