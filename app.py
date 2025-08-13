import streamlit as st
import pandas as pd
import base64
from fpdf import FPDF
import io

# --- Front-end Settings ---
st.set_page_config(
    page_title="Indie Dietyy",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme and background setup with Glassmorphism and Hover effects
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

/* Apply Poppins font and a light text color to the entire app */
html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif;
    color: #f0f2f6;
}

/* Set a blurred background image for the entire app */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1542838132-ff264e12e128?q=80&w=1740&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Add a semi-transparent overlay to ensure text is readable */
.stApp::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(5px); /* Apply blur to the overlay */
    z-index: -1; /* Place behind the content */
}

/* General selector for main content area to apply glassmorphism */
.main > div {
    background: rgba(46, 48, 50, 0.6); /* Slightly darker transparent background */
    backdrop-filter: blur(10px); /* Glassmorphism effect */
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.stSidebar {
    background: rgba(26, 28, 30, 0.6); /* Semi-transparent sidebar */
    backdrop-filter: blur(10px); /* Glassmorphism effect */
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    color: #f0f2f6;
}

h1, h2, h3, h4, h5, h6 {
    color: #f0f2f6;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
    font-weight: 600;
}

.stTextInput > div > div > input, .stSelectbox > div > div > div {
    background-color: rgba(51, 51, 51, 0.7); /* Lighter dark with transparency */
    color: #f0f2f6;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 10px 15px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    transition: all 0.3s ease-in-out;
}

.stTextInput > div > div > input:focus, .stSelectbox > div > div > div:focus-within {
    border-color: #2e8b57;
    box-shadow: 0 0 0 0.2rem rgba(46, 139, 87, 0.25);
}

.stButton > button {
    background-color: #2e8b57;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease-in-out;
}

.stButton > button:hover {
    background-color: #3cb371; /* Slightly lighter green on hover */
    transform: scale(1.02); /* Added a subtle scale effect */
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.4);
}

.stTable, .stDataFrame {
    background: rgba(51, 51, 51, 0.7); /* Table background with transparency */
    border-radius: 10px;
    overflow: hidden; /* Ensures borders/shadows apply correctly */
    box-shadow: 0 6px 12px rgba(0,0,0,0.5); /* Increased shadow for highlight */
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.stTable thead tr th, .stDataFrame thead tr th {
    background-color: #2e8b57;
    color: white;
    font-weight: 600;
    padding: 12px 15px;
}

.stTable tbody tr td, .stDataFrame tbody tr td {
    background-color: rgba(60, 60, 60, 0.7);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: 10px 15px;
    color: #f0f2f6;
}

.stTable tbody tr:hover td, .stDataFrame tbody tr:hover td {
    background-color: rgba(70, 70, 70, 0.8);
}

/* Custom CSS for download links */
.download-link a {
    display: inline-block;
    background-color: #4682b4; /* SteelBlue */
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease-in-out;
    margin-right: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.download-link a:hover {
    background-color: #5b9bd5; /* Lighter SteelBlue */
    transform: translateY(-3px) scale(1.05); /* Enhanced hover effect */
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5);
}

.stMarkdown h3 {
    border-bottom: 2px solid #2e8b57;
    padding-bottom: 5px;
    margin-top: 30px;
}

.day-plan-container {
    background: rgba(51, 51, 51, 0.7); /* Slightly darker transparent background for each day */
    backdrop-filter: blur(8px);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.15);
    transition: all 0.3s ease-in-out;
}

.day-plan-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
}
</style>
""", unsafe_allow_html=True)

st.title("🌱 Indie Dietyy")
st.markdown("Your personal guide to a healthier you. We offer customized diet plans from various Indian states to meet your specific health goals.")
st.markdown("---")

# Load the dataset
try:
    df = pd.read_csv('diet_data_expanded.csv') # Load the expanded dataset
except FileNotFoundError:
    st.error("Error: diet_data_expanded.csv not found. Please ensure the file is in the same directory.")
    st.stop()

# Function to generate PDF
def create_pdf(df_plan_data, name, diet_need):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    
    pdf.cell(200, 10, txt="Your Personalized Diet Plan", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Diet Goal: {diet_need.replace('_', ' ').title()}", ln=True, align='C')
    pdf.ln(10)

    for day_data in df_plan_data:
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(200, 10, txt=f"- {day_data['Day']} -", ln=True, align='L')
        pdf.ln(2)

        pdf.set_font("Arial", size=10)
        # Meal Plan Table
        pdf.set_font("Arial", 'B', size=10)
        pdf.cell(40, 7, "Meal Type", 1)
        pdf.cell(120, 7, "Dish", 1, ln=True)

        pdf.set_font("Arial", size=10)
        pdf.cell(40, 7, "Breakfast", 1)
        pdf.multi_cell(120, 7, day_data['Breakfast'], 1)
        
        pdf.cell(40, 7, "Lunch", 1)
        pdf.multi_cell(120, 7, day_data['Lunch'], 1)

        pdf.cell(40, 7, "Snack", 1)
        pdf.multi_cell(120, 7, day_data['Snack'], 1)

        pdf.cell(40, 7, "Dinner", 1)
        pdf.multi_cell(120, 7, day_data['Dinner'], 1)

        pdf.ln(5)
        # Instructions, Exercise, Warning
        pdf.set_font("Arial", 'B', size=11)
        pdf.cell(200, 7, txt="Instructions:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, day_data['Instructions'])
        
        pdf.ln(2)
        pdf.set_font("Arial", 'B', size=11)
        pdf.cell(200, 7, txt="Exercise:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, day_data['Exercise'])

        pdf.ln(2)
        pdf.set_font("Arial", 'B', size=11)
        pdf.cell(200, 7, txt="Important Note:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, day_data['Warning'])
        
        pdf.ln(10) # Space between days

    pdf_output = pdf.output(dest='S').encode('latin-1')
    return pdf_output


# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("👤 Your Details")
    name = st.text_input("Name", key="name_input")
    age = st.number_input("Age", min_value=1, max_value=120, step=1, key="age_input")
    weight = st.number_input("Weight (in kg)", min_value=1.0, max_value=300.0, step=0.1, key="weight_input")
    height = st.number_input("Height (in cm)", min_value=1.0, max_value=300.0, step=0.1, key="height_input")
    
    st.header("🎯 Your Goal")
    diet_need = st.selectbox(
        "Need for",
        ('weight_loss', 'bulking', 'weight_gain', 'maintaining_balanced_diet'), key="diet_need_select"
    )
    
    desired_weight = None
    if diet_need == 'weight_loss':
        desired_weight = st.number_input("Desired Weight (in kg)", min_value=1.0, max_value=300.0, step=0.1, key="desired_weight_input")

    st.header("📍 Preferences")
    country = st.selectbox("Country", ["India"], key="country_select") # Only India is supported
    states = sorted(df['state'].unique()) # Get all unique states from expanded data
    state = st.selectbox("State", states, key="state_select")
    
    st.header("🚫 Allergies")
    allergies_input = st.text_area("Allergies (comma-separated, e.g., peanuts, milk, gluten)", key="allergies_input")
    allergies_list = [item.strip().lower() for item in allergies_input.split(',')] if allergies_input else []

    submit_button = st.button("Generate Diet Plan �", key="submit_button")

# --- Main App Logic ---
if submit_button:
    # Basic validation
    if not all([name, age, weight, height, diet_need, state]):
        st.error("Please fill in all the required fields.")
    else:
        st.subheader(f"Hello, {name}! Here is your personalized diet plan for {diet_need.replace('_', ' ').title()}.")
        
        # Filter the dataset
        filtered_df = df[
            (df['state'] == state) & 
            (df['diet_need'] == diet_need)
        ].copy()

        # Filter out allergies
        if allergies_list:
            for allergen in allergies_list:
                filtered_df = filtered_df[~filtered_df['allergens'].str.contains(allergen, case=False, na=False, regex=True)]

        # Group by day and create the table
        plan_data_for_pdf = [] # To store data for PDF generation

        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days_of_week:
            daily_plan = filtered_df[filtered_df['day_of_week'] == day]
            
            if not daily_plan.empty:
                plan_row = {'Day': day}
                
                # Extract meal dishes
                for meal_type in ['breakfast', 'lunch', 'snack', 'dinner']:
                    meal_dish = daily_plan[daily_plan['meal_type'] == meal_type]['dish'].iloc[0] if not daily_plan[daily_plan['meal_type'] == meal_type].empty else "N/A"
                    plan_row[meal_type.capitalize()] = meal_dish
                
                # Extract instructions, exercise, and warning (should be same for all meals of a day)
                plan_row['Instructions'] = daily_plan['instructions'].iloc[0]
                plan_row['Exercise'] = daily_plan['exercise'].iloc[0]
                plan_row['Warning'] = daily_plan['warning'].iloc[0]
                
                plan_data_for_pdf.append(plan_row)

                # Display for each day
                st.markdown(f"""
                <div class="day-plan-container">
                    <h3>🗓️ {day}</h3>
                    <p><strong>Instructions:</strong> {plan_row['Instructions']}</p>
                    <p><strong>Exercise:</strong> {plan_row['Exercise']}</p>
                    <p><strong>Important Note:</strong> {plan_row['Warning']}</p>
                """, unsafe_allow_html=True)
                
                daily_meal_df = pd.DataFrame({
                    'Meal Type': ['Breakfast', 'Lunch', 'Snack', 'Dinner'],
                    'Dish': [plan_row['Breakfast'], plan_row['Lunch'], plan_row['Snack'], plan_row['Dinner']]
                })
                st.table(daily_meal_df)
                st.markdown("</div>", unsafe_allow_html=True) # Close day-plan-container
            
        # Display the diet plan and download options if any plan was generated
        if plan_data_for_pdf:
            st.markdown("---")
            st.markdown("#### Download your plan", unsafe_allow_html=True)
            
            # Create a DataFrame from plan_data_for_pdf for CSV export
            # This DataFrame is suitable for a single comprehensive CSV
            full_plan_df_for_csv = pd.DataFrame(plan_data_for_pdf)
            full_plan_df_for_csv_cleaned = full_plan_df_for_csv[['Day', 'Breakfast', 'Lunch', 'Snack', 'Dinner', 'Instructions', 'Exercise', 'Warning']]
            
            # CSV Download
            csv_file = full_plan_df_for_csv_cleaned.to_csv(index=False).encode('utf-8')
            b64_csv = base64.b64encode(csv_file).decode()
            csv_download_link = f'<div class="download-link"><a href="data:file/csv;base64,{b64_csv}" download="diet_plan.csv">Download as CSV</a></div>'
            st.markdown(csv_download_link, unsafe_allow_html=True)
            
            # PDF Download
            pdf_bytes = create_pdf(plan_data_for_pdf, name, diet_need)
            b64_pdf = base64.b64encode(pdf_bytes).decode('latin-1')
            pdf_download_link = f'<div class="download-link"><a href="data:application/octet-stream;base64,{b64_pdf}" download="diet_plan.pdf">Download as PDF</a></div>'
            st.markdown(pdf_download_link, unsafe_allow_html=True)
        else:
            st.warning("Sorry, no diet plan could be generated with your current selections. Try a different state or remove some allergies.")
