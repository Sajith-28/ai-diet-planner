# 🌱 Indie Dietyy — AI-Powered Weekly Diet Planner

An AI-powered diet planning web application built with **Streamlit**.  
It generates **personalized weekly diet plans** based on user details like age, weight, height, location (Indian states), goals (weight loss, bulking, weight gain, balanced diet), and allergies.  
The app allows downloading plans as **CSV** or **PDF**.

---

## ✨ Features
- **Glassmorphism UI** with responsive design.
- Personalized **diet plans** based on:
  - State-specific cuisine
  - Fitness goals (Weight Loss, Bulking, Weight Gain, Balanced Diet)
  - Allergies filtering
- **BMI-based recommendations** (optional).
- Download **diet plan** as **CSV** or **PDF**.
- Data-driven from an expanded CSV dataset (`diet_data_expanded.csv`).

---

## 🛠️ Tech Stack
- **Frontend**: Streamlit (with custom CSS)
- **Backend**: Python (Pandas, FPDF)
- **Data**: CSV dataset of meals from various Indian states
- **Deployment**: Streamlit Cloud / Local

---

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/indie-dietyy.git
cd indie-dietyy
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Ensure dataset is present**
Place `diet_data_expanded.csv` in the project root directory.

---

## 🚀 Run the App Locally
```bash
streamlit run app.py
```
This will open the app in your browser at:  
`http://localhost:8501`

---

## 📂 Project Structure
```
.
├── app.py                     # Main Streamlit application
├── diet_data_expanded.csv     # Dataset with state-based diet plans
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 📄 Data Format (`diet_data_expanded.csv`)
| state   | diet_need   | day_of_week | meal_type | dish         | allergens | instructions  | exercise     | warning |
|---------|-------------|-------------|-----------|--------------|-----------|--------------|-------------|---------|
| Kerala  | weight_loss | Monday      | breakfast | Idli & Sambar| gluten    | Eat fresh... | Morning walk| Avoid...|

---

## 📥 Download Options
- **CSV**: Full weekly plan
- **PDF**: Structured printable diet plan

---

## 📸 Screenshots
*(Add screenshots of your app UI here)*

---

## 📜 License
This project is licensed under the **MIT License**.
