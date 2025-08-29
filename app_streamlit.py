import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Data structures
rtb_combinations = {
    'ACCOUNTING': ['Principles of Auditing and Ethics in Accounting','Monitoring Inventory System and Costing',
                   'Principle of Economics','Financial Accounting','Taxation','Credit Management and Creditors Account',
                   'Mathematics II', 'Practical ACC'],
    'LSV': ['Road Alignment and Setting out', 'Fundamental Surveying Computations', 
            'Practical LSV', 'Surveying Measurement Adjustment', 
            'Mathematics I', 'Performing Cadastral Measurement',
            'Performing Setting out of Structures', 'Arc GIS software in land management and mapping',
            'Operating Surveying Instruments'],
    'CET': ['Construction Materials', 'Structural Analysis', 'Geotechnical Engineering',
            'Construction Project Management', 'Building Services', 'Construction Drawing',
            'Surveying for Construction', 'Construction Technology'],
    'EET': ['Electrical Circuits', 'Electronics', 'Power Systems',
            'Control Systems', 'Renewable Energy Systems', 'Electrical Machines',
            'Electrical Installation', 'Industrial Automation'],
    'MET': ['Engineering Mechanics', 'Thermodynamics', 'Fluid Mechanics',
            'Machine Design', 'Manufacturing Processes', 'Automation and Control',
            'Mechatronics', 'Industrial Maintenance'],
    'CP': ['Methods of irrigation and extension technics', 'Nursery establishment and industrial crops growing', 
           'seed multiplication, Mushrooms and Ornamental crops', 'Soil conservation', 'Introduction to Chemistry', 
           'Practical CRP', 'Food crops growing and post harvest handling', 'plant biology, pests and diseases control'],
    'SoD': ['Algorithm and Programming', 'Website Development', 'System Analysis and Design', 
            'Web Application and Development', 'Database Design and Development', 'Practical SOD'], 
    'AH': ['Surgery and veterinary interventions', 'Animal Diseases prevention and control', 
           'Anatomy, physiology and artificial insemination', 'Animal feeds production and feeding', 
           'Animal products control, extension and veterinary ethics', 'Micro-organism identification and infection diseases control', 
           'Organic and inorganic chemistry', 'Ruminants Farming', 'Non-ruminant farming and companion animals', 
           'Fish Farming and Beekeeping', 'Entrepreneurship and Business organization', 'English Communication Skills', 'Practical ANH'],
    'MAS': ['Masonry basic drawing', 'Practical MAS', 'Mathematics I', 'English', 'Entrepreneurship', 
            'Construction Technology', 'Cost Estimation, Schedule and Site records', 'Elevation and scaffolding Operations', 
            'Tiles Works, Openings and Wall Plastering'],
    'WOT': ['Technical drawing, CAD, and Wooden Art style Creation', 'Wood properties and Timber Drying', 
            'Woodworking Machines Operation and Workshop Management', 'Wooden Furniture Production', 
            'Wooden Structures Construction', 'Engineered Boards and Beams Production'],
    'FOR': ['Tree Nursery Management', 'Forest Establishment and Protection', 'Forest Management Plan Implementation', 
            'Forest Exploitation', 'Forest Landscape Restoration'],
    'TOR': ['Coordinating Tour and Travel bookings', 'Coordinating tourism events', 'Community Based Tourism and Heritage Maintenance', 
            'Providing guidance on Destination', 'Tour guiding and tour packages management', 
            'Francaise Professionel pour le Tourisme', 'Kutumia Kiswahili'],
    'FOH': ['Providing Excellent customer Services', 'Housekeeping Operations', 'Front Office Operations', 
            'Performing Laundry Services', 'Handle Hotel Guest and Luggage at Airport', 
            'Professional English for Front Office', 'Francaise Professional pour l\'accueil et L\'hebergement', 'Kutumia Kiswahili'],
    'MMP': ['Graphic Design', 'Photography, lighting, and images Editing', 'Sound Production', 
            'Video Production', '2D Animation Production', 'Immersive technologies and 3D Modelling'],
    'SPE': ['Cyber Security', 'Data Structure and Algorithms', 'Restful Service and Web/Web3 Application Development', 
            'Intelligent Robotics and Embedded Systems', 'Advanced Java Programming with OOP', 
            'Software Testing and Deployment(DevOps)', 'Cross-Platform Mobile Development', 'Software Engineering'],
    'IND': ['Soft Furnishing and Furniture design', 'Interior decoration, wall and floor finishing', 
            'Residential kitchen, bathroom, and partitions design', 'Cost estimation and interior drawing', 
            'Exhibition stand, ceiling, doors and windows design'],
    'MPA': ['Creativity, Innovation, and music Performance', 'Mastering Traditional and Modern Music Performance', 
            'Music theory, Arrangement and Song composition', 'Instrumental and Vocal Mastery in Music Performance', 
            'Music business and industry Management'],
    'NIT': ['LAN and Zero Client Installation', 'Network and Fiber Optic Installation', 'Network and Systems security', 
            'Network system Automation with Machine Learning', 'IoT Systems Development and Installation', 'Cloud computing'],
    'PLT': ['Plumbing drawing and planning', 'Water supply and drainage system installation', 
            'Plumbing system installation', 'Water treatment system installation', 'Water piping system'],
    'ETL': ['Embedded systems and artificial intelligence integration', 'Electronic devices repair and maintenance', 
            'Audiovisual and broadcasting system installation', 'Telecommunication and security systems installation', 
            'Power conversion, electronic control and HVAC system installation']
}

reb_combinations = {
    'PCB': ['Physics', 'Chemistry', 'Biology', 'Entrepreneurship', 'General Studies'],
    'PCM': ['Physics', 'Chemistry', 'Mathematics', 'Entrepreneurship', 'General Studies'],
    'PEM': ['Physics', 'Economics', 'Mathematics', 'Entrepreneurship', 'General Studies'],
    'MCB': ['Mathematics', 'Chemistry', 'Biology', 'Entrepreneurship', 'General Studies'],
    'BCG': ['Biology', 'Chemistry', 'Geography', 'Entrepreneurship', 'General Studies'],
    'MPG': ['Mathematics', 'Physics', 'Geography', 'Entrepreneurship', 'General Studies'],
    'MEG': ['Mathematics', 'Economics', 'Geography', 'Entrepreneurship', 'General Studies'],
    'MPC': ['Mathematics', 'Physics', 'Computer', 'Entrepreneurship', 'General Studies'],
    'MPB': ['Mathematics', 'Physics', 'Biology', 'Entrepreneurship', 'General Studies'],
    'HEG': ['History', 'Economics', 'Geography', 'Entrepreneurship', 'General Studies'],
    'EFK': ['English', 'French', 'Kinyarwanda', 'Entrepreneurship', 'General Studies'],
    'EKK': ['English', 'Kiswahili', 'Kinyarwanda', 'Entrepreneurship', 'General Studies'],
    'LEG': ['Literature', 'Economics', 'Geography', 'Entrepreneurship', 'General Studies'],
    'MEC': ['Mathematics', 'Economics', 'Computer', 'Entrepreneurship', 'General Studies'],
    'BEG': ['Biology', 'Economics', 'Geography', 'Entrepreneurship', 'General Studies'],
    'HEL': ['History', 'Economics', 'Literature', 'Entrepreneurship', 'General Studies']
}

departments = {
    'Agriculture & Veterinary Science': [
        'Agri Mechanization Technology', 'Crop Production', 'Irrigation and Drainage Technology',
        'Food Processing', 'Horticulture Technology', 'Animal Health'
    ],
    'Engineering & Technology': [
        'Civil Engineering', 'Civil Engineering Technology', 'Construction Technology',
        'Electrical Engineering', 'Electrical Engineering Technology', 'Electrical Technology',
        'Electronics and Telecommunication Technology', 'Telecommunications Engineering',
        'Mechanical Engineering', 'Mechanical Engineering Technology', 'Manufacturing Technology',
        'Mechatronics Technology', 'Automobile Technology', 'Air conditioning and Refrigeration Technology',
        'Biomedical Equipment Technology', 'Renewable Energy Technology', 'Electrical Automation'
    ],
    'Information & Communication Technology (ICT)': [
        'Information Technology','E-Commerce'
    ],
    'Mining & Natural Resources': [
        'Mining Technology', 'Wildlife and Conservation Technology',
        'Forest Resources Management', 'Forest Engineering and Wood Technology', 
        'Nature Conservation'
    ],
    'Construction & Infrastructure': [
        'Construction Technology', 'Quantity surveying', 'Land Surveying or Geomatics',
        'Geomatics Engineering', 'Highway Engineering', 'Water and Sanitation Technology',
        'Water Engineering', 'Land surveying'
    ],
    'Creative Arts & Media': [
        'Film Making and TV Production', 'Graphic Design and Animation',
        'Creative Art'
    ],
    'Tourism & Hospitality': [
        'Tourism', 'Tourism Destination Management', 'Tours and Travel Management',
        'Hospitality Management', 'Hospitality Management with the option of Food and Beverage',
        'Hospitality Management with the option of Room Division'
    ],
    'Transport & Logistics': [
        'Transport and logistics', 'Logistics and Supply Chain Management',
        'Airline and Airport Management'
    ]
}

# Initialize session state
if 'form_step' not in st.session_state:
    st.session_state.form_step = 0
if 'current_board' not in st.session_state:
    st.session_state.current_board = None
if 'year_completed' not in st.session_state:
    st.session_state.year_completed = None
if 'selected_combination' not in st.session_state:
    st.session_state.selected_combination = None
if 'subject_marks' not in st.session_state:
    st.session_state.subject_marks = {}
if 'rp_admission_year' not in st.session_state:
    st.session_state.rp_admission_year = None
if 'department' not in st.session_state:
    st.session_state.department = None
if 'course' not in st.session_state:
    st.session_state.course = None
if 'year_study' not in st.session_state:
    st.session_state.year_study = None

# File paths
JSON_FILE = "rp_student_data.json"
CSV_FILE = "rp_student_data.csv"

# Load existing data
def load_existing_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(new_data):
    # Load existing data
    existing_data = load_existing_data()
    
    # Append new data
    updated_data = existing_data + new_data
    
    # Save to JSON
    with open(JSON_FILE, 'w') as f:
        json.dump(updated_data, f, indent=2)
    
    # Save to CSV
    if updated_data:
        df = pd.DataFrame(updated_data)
        
        # Flatten the marks column for CSV
        if not df.empty and 'marks' in df.columns:
            marks_df = pd.json_normalize(df['marks'])
            marks_df.columns = [f'mark_{col}' for col in marks_df.columns]
            df = df.drop('marks', axis=1).join(marks_df)
        
        df.to_csv(CSV_FILE, index=False)
    
    return updated_data

def reset_form():
    """Reset all form state"""
    st.session_state.form_step = 0
    st.session_state.current_board = None
    st.session_state.year_completed = None
    st.session_state.selected_combination = None
    st.session_state.subject_marks = {}
    st.session_state.rp_admission_year = None
    st.session_state.department = None
    st.session_state.course = None
    st.session_state.year_study = None

# Initialize years
current_year = datetime.now().year
high_school_years = list(range(current_year, current_year - 6, -1))
rp_admission_years = list(range(current_year, current_year - 2, -1))

# App layout
st.set_page_config(page_title="RP Student Performance Data Collection", layout="wide")

# Header
st.markdown("""
    <style>
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .step-indicator {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #667eea;
    }
    .board-option {
        padding: 20px;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .board-option.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    }
    .subject-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        height: 10px;
        margin-bottom: 20px;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header">
        <h1>RP Student Research Data Collection</h1>
        <p>Rwanda Student Performance Analysis - RTB & REB High School Scores</p>
    </div>
""", unsafe_allow_html=True)

# Progress indicator
progress_steps = [
    "Select Board",
    "Year Completed", 
    "Combination", 
    "Subject Marks", 
    "RP Admission Year", 
    "Department", 
    "Course", 
    "Year of Study"
]

current_step = min(st.session_state.form_step, len(progress_steps) - 1)
progress_percentage = (current_step + 1) / len(progress_steps) * 100

st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_percentage}%"></div>
    </div>
    <div class="step-indicator">
        <strong>Step {current_step + 1} of {len(progress_steps)}: {progress_steps[current_step]}</strong>
    </div>
""", unsafe_allow_html=True)

# Step 1: Board selection
if st.session_state.form_step == 0:
    st.subheader("Select High School Examination Board")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="text-align: center; padding: 20px; border: 2px solid #e1e5e9; border-radius: 10px; margin-bottom: 10px;">
                <h3>RTB</h3>
                <p>Rwanda Training Board</p>
                <p><small>(Technical & Vocational)</small></p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Select RTB", key="rtb_btn", use_container_width=True):
            st.session_state.current_board = "RTB"
            st.session_state.form_step = 1
            st.rerun()
    
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 20px; border: 2px solid #e1e5e9; border-radius: 10px; margin-bottom: 10px;">
                <h3>REB</h3>
                <p>Rwanda Education Board</p>
                <p><small>(Academic Preparation)</small></p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Select REB", key="reb_btn", use_container_width=True):
            st.session_state.current_board = "REB"
            st.session_state.form_step = 1
            st.rerun()

# Step 2: Year Completed
elif st.session_state.form_step == 1:
    st.info(f"Selected Board: **{st.session_state.current_board}**")
    
    st.subheader("Year of Completing High School")
    year_completed = st.selectbox(
        "Select year:",
        options=[None] + high_school_years,
        format_func=lambda x: "Select year..." if x is None else str(x)
    )
    
    if year_completed:
        st.session_state.year_completed = year_completed
        if st.button("Next Step", type="primary"):
            st.session_state.form_step = 2
            st.rerun()

# Step 3: Combination Selection
elif st.session_state.form_step == 2:
    st.info(f"Board: **{st.session_state.current_board}** | Year Completed: **{st.session_state.year_completed}**")
    
    st.subheader("Select Combination")
    combinations = rtb_combinations if st.session_state.current_board == "RTB" else reb_combinations
    
    if st.session_state.current_board == "REB":
        # For REB, show subjects in combination description
        combo_options = []
        for combo, subjects in combinations.items():
            combo_options.append(f"{combo} - {', '.join(subjects)}")
        
        selected_combo_display = st.selectbox(
            "Choose a combination:",
            options=[None] + combo_options,
            format_func=lambda x: "Choose a combination..." if x is None else x
        )
        
        if selected_combo_display:
            # Extract combination code from display
            selected_combination = selected_combo_display.split(" - ")[0]
            st.session_state.selected_combination = selected_combination
            if st.button("Next Step", type="primary"):
                st.session_state.form_step = 3
                st.rerun()
    else:
        # For RTB, just show combination names
        selected_combination = st.selectbox(
            "Choose a combination:",
            options=[None] + list(combinations.keys()),
            format_func=lambda x: "Choose a combination..." if x is None else x
        )
        
        if selected_combination:
            st.session_state.selected_combination = selected_combination
            if st.button("Next Step", type="primary"):
                st.session_state.form_step = 3
                st.rerun()

# Step 4: Subject Marks
elif st.session_state.form_step == 3:
    st.info(f"Board: **{st.session_state.current_board}** | Year: **{st.session_state.year_completed}** | Combination: **{st.session_state.selected_combination}**")
    
    st.subheader("Enter Marks for Each Subject (0-100)")
    combinations = rtb_combinations if st.session_state.current_board == "RTB" else reb_combinations
    subjects = combinations[st.session_state.selected_combination]
    
    # Initialize marks if not exists
    if not st.session_state.subject_marks:
        st.session_state.subject_marks = {subject: 0 for subject in subjects}
    
    # Create input fields in columns
    cols = st.columns(2)
    all_marks_entered = True
    
    for i, subject in enumerate(subjects):
        with cols[i % 2]:
            mark = st.number_input(
                subject,
                min_value=0,
                max_value=100,
                value=st.session_state.subject_marks.get(subject, 0),
                key=f"mark_{subject}_{st.session_state.form_step}"
            )
            st.session_state.subject_marks[subject] = mark
            if mark == 0:
                all_marks_entered = False
    
    if all_marks_entered and all(mark > 0 for mark in st.session_state.subject_marks.values()):
        if st.button("Next Step", type="primary"):
            st.session_state.form_step = 4
            st.rerun()
    else:
        st.warning("Please enter marks for all subjects (must be greater than 0)")

# Step 5: RP Admission Year
elif st.session_state.form_step == 4:
    st.info(f"Board: **{st.session_state.current_board}** | Combination: **{st.session_state.selected_combination}** | Subjects completed ✓")
    
    st.subheader("Year of Admission to RP")
    rp_admission_year = st.selectbox(
        "Select year:",
        options=[None] + rp_admission_years,
        format_func=lambda x: "Select year..." if x is None else str(x)
    )
    
    if rp_admission_year:
        st.session_state.rp_admission_year = rp_admission_year
        if st.button("Next Step", type="primary"):
            st.session_state.form_step = 5
            st.rerun()

# Step 6: Department Selection
elif st.session_state.form_step == 5:
    st.info(f"Board: **{st.session_state.current_board}** | RP Admission: **{st.session_state.rp_admission_year}**")
    
    st.subheader("Select Department")
    department = st.selectbox(
        "Choose a department:",
        options=[None] + list(departments.keys()),
        format_func=lambda x: "Choose a department..." if x is None else x
    )
    
    if department:
        st.session_state.department = department
        if st.button("Next Step", type="primary"):
            st.session_state.form_step = 6
            st.rerun()

# Step 7: Course Selection
elif st.session_state.form_step == 6:
    st.info(f"Department: **{st.session_state.department}**")
    
    st.subheader("Select Course/Program")
    course = st.selectbox(
        "Choose a course:",
        options=[None] + departments[st.session_state.department],
        format_func=lambda x: "Choose a course..." if x is None else x
    )
    
    if course:
        st.session_state.course = course
        if st.button("Next Step", type="primary"):
            st.session_state.form_step = 7
            st.rerun()

# Step 8: Year of Study
elif st.session_state.form_step == 7:
    st.info(f"Department: **{st.session_state.department}** | Course: **{st.session_state.course}**")
    
    st.subheader("Current Year of Study")
    year_study = st.selectbox(
        "Select year:",
        options=[None, "Year 1", "Year 2"],
        format_func=lambda x: "Select year..." if x is None else x
    )
    
    if year_study:
        st.session_state.year_study = year_study
        
        # Show summary and submit
        st.subheader("Review Your Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Basic Information:**")
            st.write(f"- Board: {st.session_state.current_board}")
            st.write(f"- Year Completed HS: {st.session_state.year_completed}")
            st.write(f"- Combination: {st.session_state.selected_combination}")
            st.write(f"- RP Admission Year: {st.session_state.rp_admission_year}")
            st.write(f"- Year of Study: {st.session_state.year_study}")
        
        with col2:
            st.write("**Academic Information:**")
            st.write(f"- Department: {st.session_state.department}")
            st.write(f"- Course: {st.session_state.course}")
            
            st.write("**Subject Marks:**")
            for subject, mark in st.session_state.subject_marks.items():
                st.write(f"- {subject}: {mark}")
        
        if st.button("Submit Student Data", type="primary"):
            # Create data record
            form_data = {
                "id": datetime.now().timestamp(),
                "timestamp": datetime.now().isoformat(),
                "examinationBoard": st.session_state.current_board,
                "yearCompleted": st.session_state.year_completed,
                "rpAdmissionYear": st.session_state.rp_admission_year,
                "combination": st.session_state.selected_combination,
                "department": st.session_state.department,
                "course": st.session_state.course,
                "yearStudy": st.session_state.year_study,
                "marks": st.session_state.subject_marks
            }
            
            # Save data
            updated_data = save_data([form_data])
            
            # Move to success step
            st.session_state.form_step = 8
            st.rerun()

# Step 9: Success and Summary
elif st.session_state.form_step == 8:
    # Congratulations message
    st.balloons()
    
    st.markdown("""
        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; border-radius: 15px; margin-bottom: 30px;">
            <h1>🎉 Congratulations!</h1>
            <h2>Student data submitted successfully!</h2>
            <p style="font-size: 1.2em; margin-top: 20px;">
                Your data has been saved to JSON and CSV files and is now part of our research database.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Data Collection Summary
    st.subheader("📊 Data Collection Summary")
    
    # Load and display data count
    existing_data = load_existing_data()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Students Recorded", len(existing_data))
    
    # Download buttons
    st.subheader("💾 Download Data",disabled=True)
    
    download_col1, download_col2 = st.columns(2)
    
    with download_col1:
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r") as f:
                st.download_button(
                    label="📄 Download JSON",
                    data=f.read(),
                    file_name=f"rp_student_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True,
                    disabled=True  # Added this parameter to make it read-only
                )

    with download_col2:
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, "r") as f:
                st.download_button(
                    label="📊 Download CSV",
                    data=f.read(),
                    file_name=f"rp_student_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    disabled=True  # Added this parameter to make it read-only
                )
    
    # Additional options
    st.markdown("---")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("📝 Add Another Student", type="primary", use_container_width=True):
            reset_form()
            st.rerun()
    
    with action_col2:
        if st.button("👁️ View All Data", use_container_width=True, disabled=True):
            # Show data table
            st.subheader("All Recorded Data")
            df = pd.DataFrame(existing_data)
            
            # Flatten marks for display
            if not df.empty and 'marks' in df.columns:
                marks_df = pd.json_normalize(df['marks'])
                df_display = df.drop('marks', axis=1).reset_index(drop=True)
                df_display = pd.concat([df_display, marks_df], axis=1)
            else:
                df_display = df
            
            st.dataframe(df_display, use_container_width=True)

    with action_col3:
        if st.button("🗑️ Clear All Data", use_container_width=True,disabled=True):
            if st.session_state.get('confirm_delete', False):
                if os.path.exists(JSON_FILE):
                    os.remove(JSON_FILE)
                if os.path.exists(CSV_FILE):
                    os.remove(CSV_FILE)
                st.success("All data has been cleared!")
                st.session_state.confirm_delete = False
                st.rerun()
            else:
                st.session_state.confirm_delete = True
                st.warning("Click again to confirm deletion of all data")
                st.rerun()

# Navigation buttons
if st.session_state.form_step > 0 and st.session_state.form_step < 8:
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("Previous Step"):
            st.session_state.form_step -= 1
            st.rerun()
    
    with col2:
        if st.button("Reset Form"):
            reset_form()
            st.rerun()

# Show initial summary only if no form is in progress
if st.session_state.form_step == 0:
    st.markdown("---")
    st.subheader("Data Collection Overview")
    
    # Load and display data count
    existing_data = load_existing_data()
    
    if existing_data:
        st.metric("Total Students Recorded", len(existing_data))
        
        if st.button("View Existing Data",disabled=True ):
            df = pd.DataFrame(existing_data)
            
            # Flatten marks for display
            if not df.empty and 'marks' in df.columns:
                marks_df = pd.json_normalize(df['marks'])
                df_display = df.drop('marks', axis=1).reset_index(drop=True)
                df_display = pd.concat([df_display, marks_df], axis=1)
            else:
                df_display = df
            
            st.dataframe(df_display.head(5), use_container_width=True)
            st.caption("Showing first 5 records. Complete the form to access full data management.")
    else:
        st.info("No data has been collected yet. Start by selecting an examination board above.")