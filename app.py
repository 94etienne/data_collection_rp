from flask import Flask, render_template_string, request, jsonify, send_file, redirect, url_for
import json
import csv
import os
from datetime import datetime
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'fhhfgjgjfjdhfjjdfn@@rfhfhjgjgjg'  # Change this to a secure secret key

# Create data directory if it doesn't exist
DATA_DIR = 'student_data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# File paths
JSON_FILE = os.path.join(DATA_DIR, 'rp_student_data.json')
CSV_FILE = os.path.join(DATA_DIR, 'rp_student_data.csv')

def load_data():
    """Load existing data from JSON file"""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_data(data):
    """Save data to JSON file"""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_to_csv(data):
    """Save data to CSV file"""
    if not data:
        return
    
    # Get all unique subjects from all records
    all_subjects = set()
    for record in data:
        if 'marks' in record:
            all_subjects.update(record['marks'].keys())
    
    all_subjects = sorted(list(all_subjects))
    
    # Define CSV headers
    headers = [
        'ID', 'Timestamp', 'Examination Board', 'Year Completed HS', 
        'RP Admission Year', 'Combination', 'Department', 'Course', 'Year of Study'
    ]
    
    # Add subject headers
    for subject in all_subjects:
        headers.append(f'Mark_{subject.replace(",", "_").replace(" ", "_")}')
    
    # Write CSV file
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for record in data:
            row = [
                record.get('id', ''),
                record.get('timestamp', ''),
                record.get('examinationBoard', ''),
                record.get('yearCompleted', ''),
                record.get('rpAdmissionYear', ''),
                record.get('combination', ''),
                record.get('department', ''),
                record.get('course', ''),
                record.get('yearStudy', '')
            ]
            
            # Add marks for each subject
            marks = record.get('marks', {})
            for subject in all_subjects:
                row.append(marks.get(subject, ''))
            
            writer.writerow(row)

@app.route('/')
def index():
    """Serve the main data collection form"""
    # HTML content embedded directly - no need for external file
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RP Student Performance Data Collection</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .form-container {
            padding: 40px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
            font-size: 1rem;
        }
        
        select, input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: white;
        }
        
        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .board-selection {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .board-option {
            padding: 20px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .board-option:hover {
            border-color: #667eea;
            transform: translateY(-2px);
        }
        
        .board-option.selected {
            border-color: #667eea;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        }
        
        .board-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 5px;
        }
        
        .board-desc {
            font-size: 0.9rem;
            color: #666;
        }
        
        .subjects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }
        
        .subject-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }
        
        .subject-card label {
            font-size: 0.9rem;
            margin-bottom: 8px;
            color: #495057;
        }
        
        .submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .submit-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .hidden {
            display: none;
        }
        
        .summary {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        
        .summary h3 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .data-count {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .export-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        
        .export-btn:hover {
            background: #218838;
        }
        
        .clear-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .clear-btn:hover {
            background: #c82333;
        }

        .nav-buttons {
            margin: 20px 0;
            text-align: center;
        }

        .nav-btn {
            background: #667eea;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin: 0 10px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .nav-btn:hover {
            background: #5a6fd8;
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .form-container {
                padding: 20px;
            }
            
            .board-selection {
                grid-template-columns: 1fr;
            }
            
            .subjects-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 RP Student Research Data Collection</h1>
            <p>Rwanda Student Performance Analysis - RTB & REB High School Scores</p>
            <div class="nav-buttons">
                <a href="/view-data" class="nav-btn">📊 View All Records</a>
            </div>
        </div>
        
        <div class="form-container">
            <!-- Examination Board Selection -->
            <div class="form-group">
                <label>📚 Select High School Examination Board</label>
                <div class="board-selection">
                    <div class="board-option" onclick="selectBoard('RTB')">
                        <div class="board-title">RTB</div>
                        <div class="board-desc">Rwanda Training Board<br>(Technical & Vocational)</div>
                    </div>
                    <div class="board-option" onclick="selectBoard('REB')">
                        <div class="board-title">REB</div>
                        <div class="board-desc">Rwanda Education Board<br>(Academic Preparation)</div>
                    </div>
                </div>
            </div>
            
            <!-- Year Completed High School -->
            <div class="form-group">
                <label for="yearCompleted">📅 Year of Completing High School</label>
                <select id="yearCompleted">
                    <option value="">Select year...</option>
                </select>
            </div>
            
            <!-- Combination Selection -->
            <div class="form-group hidden" id="combinationGroup">
                <label for="combination">Select Combination</label>
                <select id="combination">
                    <option value="">Choose a combination...</option>
                </select>
            </div>
            
            <!-- Subjects and Marks -->
            <div class="form-group hidden" id="subjectsGroup">
                <label>📝 Enter Marks for Each Subject (0-100)</label>
                <div class="subjects-grid" id="subjectsContainer"></div>
            </div>
            
            <!-- Year Admitted to RP -->
            <div class="form-group hidden" id="rpAdmissionGroup">
                <label for="rpAdmissionYear">🏛️ Year of Admission to RP</label>
                <select id="rpAdmissionYear">
                    <option value="">Select year...</option>
                </select>
            </div>
            
            <!-- Department Selection -->
            <div class="form-group hidden" id="departmentGroup">
                <label for="department">🏢 Select Department</label>
                <select id="department">
                    <option value="">Choose a department...</option>
                </select>
            </div>
            
            <!-- Course Selection -->
            <div class="form-group hidden" id="courseGroup">
                <label for="course">📚 Select Course/Program</label>
                <select id="course">
                    <option value="">Choose a course...</option>
                </select>
            </div>
            
            <!-- Year of Study -->
            <div class="form-group hidden" id="yearStudyGroup">
                <label for="yearStudy">📖 Current Year of Study</label>
                <select id="yearStudy">
                    <option value="">Select year...</option>
                    <option value="Year 1">Year 1</option>
                    <option value="Year 2">Year 2</option>
                </select>
            </div>
            
            <button class="submit-btn" onclick="submitFormToServer()" id="submitBtn" disabled>
                Submit Student Data
            </button>
            
            <!-- Summary Section -->
            <div class="summary">
                <h3>📊 Data Collection Summary</h3>
                <div class="data-count" id="dataCount">0</div>
                <div>Students Recorded</div>
                <div style="margin-top: 15px;">
                    <button class="export-btn hidden" id="exportJsonBtn" onclick="downloadFile('json')">
                        Export JSON
                    </button>
                    <button class="export-btn hidden" id="exportCsvBtn" onclick="downloadFile('csv')">
                        Export CSV
                    </button>
                    <button class="clear-btn hidden" id="clearBtn" onclick="clearServerData()">
                        Clear All Data
                    </button>
                </div>
            </div>
        </div>
    </div>'''
    
    # Add complete JavaScript functionality
    javascript_code = '''
    <script>
        // Data structures
        const rtbCombinations = {
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
                    'Professional English for Front Office', 'Francaise Professional pour l\\'accueil et L\\'hebergement', 'Kutumia Kiswahili'],
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
        };

        const rebCombinations = {
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
        };

        const departments = {
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
        };

        // Form state
        let currentBoard = '';
        
        // Initialize year dropdowns
        function initializeYears() {
            const currentYear = new Date().getFullYear();
            const yearCompleted = document.getElementById('yearCompleted');
            const rpAdmissionYear = document.getElementById('rpAdmissionYear');
            
            // High school completion years (last 6 years)
            for (let i = 0; i < 6; i++) {
                const year = currentYear - i;
                const option = document.createElement('option');
                option.value = year;
                option.textContent = year;
                yearCompleted.appendChild(option);
            }
            
            // RP admission years (last 2 years)
            for (let i = 0; i < 2; i++) {
                const year = currentYear - i;
                const option = document.createElement('option');
                option.value = year;
                option.textContent = year;
                rpAdmissionYear.appendChild(option);
            }
        }
        
        // Select examination board
        function selectBoard(board) {
            currentBoard = board;
            
            // Update UI
            document.querySelectorAll('.board-option').forEach(option => {
                option.classList.remove('selected');
            });
            event.target.closest('.board-option').classList.add('selected');
            
            // Show combination selection
            const combinationGroup = document.getElementById('combinationGroup');
            const combination = document.getElementById('combination');
            
            combinationGroup.classList.remove('hidden');
            combination.innerHTML = '<option value="">Choose a combination...</option>';
            
            const combinations = board === 'RTB' ? rtbCombinations : rebCombinations;
            Object.keys(combinations).forEach(combo => {
                const option = document.createElement('option');
                option.value = combo;
                option.textContent = board === 'REB' ? 
                    combo + ' - ' + combinations[combo].join(', ') : combo;
                combination.appendChild(option);
            });
            
            // Reset dependent sections
            hideSection('subjectsGroup');
            hideSection('rpAdmissionGroup');
            hideSection('departmentGroup');
            hideSection('courseGroup');
            hideSection('yearStudyGroup');
            
            checkFormValidity();
        }
        
        // Handle combination selection
        document.getElementById('combination').addEventListener('change', function() {
            const combination = this.value;
            if (combination) {
                showSubjects(combination);
            } else {
                hideSection('subjectsGroup');
                hideSection('rpAdmissionGroup');
                hideSection('departmentGroup');
                hideSection('courseGroup');
                hideSection('yearStudyGroup');
            }
            checkFormValidity();
        });
        
        // Show subjects for marks entry
        function showSubjects(combination) {
            const subjectsGroup = document.getElementById('subjectsGroup');
            const subjectsContainer = document.getElementById('subjectsContainer');
            
            const combinations = currentBoard === 'RTB' ? rtbCombinations : rebCombinations;
            const subjects = combinations[combination];
            
            subjectsContainer.innerHTML = '';
            
            subjects.forEach(subject => {
                const subjectCard = document.createElement('div');
                subjectCard.className = 'subject-card';
                subjectCard.innerHTML = '<label>' + subject + '</label><input type="number" min="0" max="100" placeholder="Enter mark (0-100)" data-subject="' + subject + '" onchange="checkFormValidity()">';
                subjectsContainer.appendChild(subjectCard);
            });
            
            subjectsGroup.classList.remove('hidden');
            
            // Show RP admission year selection after subjects
            document.getElementById('rpAdmissionGroup').classList.remove('hidden');
        }
        
        // Handle RP admission year selection
        document.getElementById('rpAdmissionYear').addEventListener('change', function() {
            const rpYear = this.value;
            if (rpYear) {
                showDepartments();
            } else {
                hideSection('departmentGroup');
                hideSection('courseGroup');
                hideSection('yearStudyGroup');
            }
            checkFormValidity();
        });
        
        // Show departments
        function showDepartments() {
            const departmentGroup = document.getElementById('departmentGroup');
            const department = document.getElementById('department');
            
            department.innerHTML = '<option value="">Choose a department...</option>';
            Object.keys(departments).forEach(dept => {
                const option = document.createElement('option');
                option.value = dept;
                option.textContent = dept;
                department.appendChild(option);
            });
            
            departmentGroup.classList.remove('hidden');
        }
        
        // Handle department selection
        document.getElementById('department').addEventListener('change', function() {
            const department = this.value;
            if (department) {
                showCourses(department);
            } else {
                hideSection('courseGroup');
                hideSection('yearStudyGroup');
            }
            checkFormValidity();
        });
        
        // Show courses
        function showCourses(department) {
            const courseGroup = document.getElementById('courseGroup');
            const course = document.getElementById('course');
            
            course.innerHTML = '<option value="">Choose a course...</option>';
            departments[department].forEach(courseOption => {
                const option = document.createElement('option');
                option.value = courseOption;
                option.textContent = courseOption;
                course.appendChild(option);
            });
            
            courseGroup.classList.remove('hidden');
        }
        
        // Handle course selection
        document.getElementById('course').addEventListener('change', function() {
            const course = this.value;
            if (course) {
                document.getElementById('yearStudyGroup').classList.remove('hidden');
            } else {
                hideSection('yearStudyGroup');
            }
            checkFormValidity();
        });
        
        // Handle year of study selection
        document.getElementById('yearStudy').addEventListener('change', checkFormValidity);
        document.getElementById('yearCompleted').addEventListener('change', checkFormValidity);
        
        // Hide section
        function hideSection(sectionId) {
            document.getElementById(sectionId).classList.add('hidden');
        }
        
        // Check form validity
        function checkFormValidity() {
            const yearCompleted = document.getElementById('yearCompleted').value;
            const rpAdmissionYear = document.getElementById('rpAdmissionYear').value;
            const combination = document.getElementById('combination').value;
            const department = document.getElementById('department').value;
            const course = document.getElementById('course').value;
            const yearStudy = document.getElementById('yearStudy').value;
            
            // Check if all subjects have marks
            const subjectInputs = document.querySelectorAll('[data-subject]');
            const allMarksEntered = Array.from(subjectInputs).every(input => 
                input.value !== '' && input.value >= 0 && input.value <= 100
            );
            
            const isValid = currentBoard && yearCompleted && 
                           combination && allMarksEntered && rpAdmissionYear &&
                           department && course && yearStudy;
            
            document.getElementById('submitBtn').disabled = !isValid;
        }
        
        // Reset form
        function resetForm() {
            currentBoard = '';
            document.querySelectorAll('.board-option').forEach(option => {
                option.classList.remove('selected');
            });
            
            document.getElementById('yearCompleted').value = '';
            document.getElementById('rpAdmissionYear').value = '';
            document.getElementById('combination').value = '';
            document.getElementById('department').value = '';
            document.getElementById('course').value = '';
            document.getElementById('yearStudy').value = '';
            
            hideSection('combinationGroup');
            hideSection('subjectsGroup');
            hideSection('rpAdmissionGroup');
            hideSection('departmentGroup');
            hideSection('courseGroup');
            hideSection('yearStudyGroup');
            
            checkFormValidity();
        }
        
        // Flask-specific functions
        function submitFormToServer() {
            const formData = {
                id: Date.now(),
                timestamp: new Date().toISOString(),
                examinationBoard: currentBoard,
                yearCompleted: document.getElementById('yearCompleted').value,
                rpAdmissionYear: document.getElementById('rpAdmissionYear').value,
                combination: document.getElementById('combination').value,
                department: document.getElementById('department').value,
                course: document.getElementById('course').value,
                yearStudy: document.getElementById('yearStudy').value,
                marks: {}
            };
            
            // Collect marks
            const subjectInputs = document.querySelectorAll('[data-subject]');
            subjectInputs.forEach(input => {
                formData.marks[input.dataset.subject] = parseInt(input.value);
            });
            
            // Send to Flask server
            fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Student data submitted successfully and saved to server!');
                    resetForm();
                    updateServerSummary();
                } else {
                    alert('Error submitting data: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error submitting data to server');
            });
        }
        
        function downloadFile(format) {
            window.open('/download/' + format, '_blank');
        }
        
        function clearServerData() {
            if (confirm('Are you sure you want to clear all server data? This action cannot be undone.')) {
                fetch('/clear', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('All server data has been cleared!');
                        updateServerSummary();
                    } else {
                        alert('Error clearing data: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error clearing server data');
                });
            }
        }
        
        function updateServerSummary() {
            fetch('/data-count')
            .then(response => response.json())
            .then(data => {
                const dataCount = document.getElementById('dataCount');
                const exportJsonBtn = document.getElementById('exportJsonBtn');
                const exportCsvBtn = document.getElementById('exportCsvBtn');
                const clearBtn = document.getElementById('clearBtn');
                
                dataCount.textContent = data.count;
                
                if (data.count > 0) {
                    exportJsonBtn.classList.remove('hidden');
                    exportCsvBtn.classList.remove('hidden');
                    clearBtn.classList.remove('hidden');
                } else {
                    exportJsonBtn.classList.add('hidden');
                    exportCsvBtn.classList.add('hidden');
                    clearBtn.classList.add('hidden');
                }
            });
        }
        
        // Initialize the form
        document.addEventListener('DOMContentLoaded', function() {
            initializeYears();
            updateServerSummary();
            checkFormValidity();
        });
    </script>
</body>
</html>
    '''
    
    return html_content + javascript_code

@app.route('/submit', methods=['POST'])
def submit_data():
    """Handle form submission"""
    try:
        student_data = request.get_json()
        
        # Load existing data
        existing_data = load_data()
        
        # Add new data
        existing_data.append(student_data)
        
        # Save to JSON
        save_data(existing_data)
        
        # Save to CSV
        save_to_csv(existing_data)
        
        return jsonify({'success': True, 'message': 'Data saved successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/data-count')
def data_count():
    """Get count of stored records"""
    try:
        data = load_data()
        return jsonify({'count': len(data)})
    except Exception as e:
        return jsonify({'count': 0})

@app.route('/download/<format>')
def download_file(format):
    """Download data in specified format"""
    try:
        data = load_data()
        
        if not data:
            return "No data available for download", 404
        
        if format == 'json':
            # Create JSON file in memory
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            json_buffer = io.BytesIO(json_data.encode('utf-8'))
            json_buffer.seek(0)
            
            return send_file(
                json_buffer,
                as_attachment=True,
                download_name=f'rp_student_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
                mimetype='application/json'
            )
        
        elif format == 'csv':
            # Ensure CSV is up to date
            save_to_csv(data)
            
            return send_file(
                CSV_FILE,
                as_attachment=True,
                download_name=f'rp_student_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mimetype='text/csv'
            )
        
        else:
            return "Invalid format", 400
    
    except Exception as e:
        return f"Error downloading file: {str(e)}", 500

@app.route('/clear', methods=['POST'])
def clear_data():
    """Clear all stored data"""
    try:
        # Clear JSON file
        save_data([])
        
        # Clear CSV file
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        
        return jsonify({'success': True, 'message': 'Data cleared successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/view-data')
def view_data():
    """View all stored data in a formatted table"""
    try:
        data = load_data()
        
        if not data:
            return "<h2>No data available</h2><a href='/'>Back to Form</a>"
        
        # Create HTML table
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>RP Student Data - View All Records</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .marks { font-size: 0.9em; }
                .nav { margin: 20px 0; }
                .nav a { padding: 10px 15px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-right: 10px; }
                .nav a:hover { background: #5a6fd8; }
            </style>
        </head>
        <body>
            <div class="nav">
                <a href="/">Back to Form</a>
                <a href="/download/json">Download JSON</a>
                <a href="/download/csv">Download CSV</a>
            </div>
            <h1>RP Student Performance Data Records</h1>
            <p><strong>Total Records:</strong> ''' + str(len(data)) + '''</p>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Timestamp</th>
                        <th>Board</th>
                        <th>HS Year</th>
                        <th>RP Year</th>
                        <th>Combination</th>
                        <th>Department</th>
                        <th>Course</th>
                        <th>Year of Study</th>
                        <th>Marks</th>
                    </tr>
                </thead>
                <tbody>
        '''
        
        for record in data:
            marks_str = "<br>".join([f"{subject}: {score}" for subject, score in record.get('marks', {}).items()])
            
            html += f'''
                <tr>
                    <td>{record.get('id', '')}</td>
                    <td>{record.get('timestamp', '').split('T')[0] if record.get('timestamp') else ''}</td>
                    <td>{record.get('examinationBoard', '')}</td>
                    <td>{record.get('yearCompleted', '')}</td>
                    <td>{record.get('rpAdmissionYear', '')}</td>
                    <td>{record.get('combination', '')}</td>
                    <td>{record.get('department', '')}</td>
                    <td>{record.get('course', '')}</td>
                    <td>{record.get('yearStudy', '')}</td>
                    <td class="marks">{marks_str}</td>
                </tr>
            '''
        
        html += '''
                </tbody>
            </table>
            <div class="nav">
                <a href="/">Back to Form</a>
                <a href="/download/json">Download JSON</a>
                <a href="/download/csv">Download CSV</a>
            </div>
        </body>
        </html>
        '''
        
        return html
    
    except Exception as e:
        return f"Error viewing data: {str(e)}"

if __name__ == '__main__':
    print("Flask app starting...")
    print("Available endpoints:")
    print("- / : Main form")
    print("- /view-data : View all records")
    print("- /download/json : Download JSON")
    print("- /download/csv : Download CSV")
    print("\nAccess the application at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)