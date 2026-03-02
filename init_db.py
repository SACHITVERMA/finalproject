import os
from dotenv import load_dotenv
import mysql.connector
# import mysql
load_dotenv()

def update_database_safely():
    try:
        # db = mysql.connector.connect(
        #     host=os.getenv("DB_HOST"),
        #     user=os.getenv("DB_USER"),
        #     password=os.getenv("DB_PASSWORD")
        # )
         # init_db.py mein is tarah change karein
        db = mysql.connector.connect(
              host=os.getenv("DB_HOST"),
              user=os.getenv("DB_USER"),
              password=os.getenv("DB_PASSWORD"),
              port=os.getenv("DB_PORT"),
              database="defaultdb", # Aiven ka default db name
              ssl_ca="ca.pem",      # Jo file aapne download kari
              ssl_verify_cert=True
        )

        cursor = db.cursor(buffered=True) 

        # 2. Database create 
        cursor.execute("CREATE DATABASE IF NOT EXISTS college_db")
        cursor.execute("USE college_db")

        # 3. Tables Creation (IF NOT EXISTS ensures no data loss)
        
        # Users Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) PRIMARY KEY, 
            password VARCHAR(255) NOT NULL, 
            name VARCHAR(255) NOT NULL, 
            dob VARCHAR(50), 
            gender VARCHAR(20), 
            roll VARCHAR(50), 
            course VARCHAR(100), 
            phone VARCHAR(20),
            attendance VARCHAR(50) DEFAULT '0',       
            internal_grade VARCHAR(20) DEFAULT 'N/A'             
        )''')

        # Results Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255),
            subject VARCHAR(255) NOT NULL,
            marks INT NOT NULL,
            total_marks INT DEFAULT 100,
            semester VARCHAR(50),
            FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
        )''')

        # ID Card Applications Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS id_applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            gender VARCHAR(20),
            father_name VARCHAR(255),
            mother_name VARCHAR(255),
            roll_no VARCHAR(50) NOT NULL,
            department VARCHAR(100),
            academic_year VARCHAR(50),
            phone VARCHAR(20),
            photo_path VARCHAR(255),
            signature_path VARCHAR(255),
            marksheet_path VARCHAR(255),
            status VARCHAR(20) DEFAULT 'Pending',
            unique_id VARCHAR(50) DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
        )''')

        # College Information Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS college_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(100), 
            content LONGTEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        # Timetable Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS timetable (
            id INT AUTO_INCREMENT PRIMARY KEY,
            course VARCHAR(50), 
            year_sem VARCHAR(50), 
            time_slot VARCHAR(100), 
            subject VARCHAR(255), 
            room_no VARCHAR(100)
        )''')

        # Chat History Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            user_email VARCHAR(255), 
            user_query TEXT, 
            bot_response TEXT, 
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        # Import History Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS import_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            file_name VARCHAR(255) NOT NULL,
            total_records INT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            admin_email VARCHAR(255) DEFAULT 'admin@coe.control'
        )''')


# Study Material Table (Notes Hub ke liye)
        cursor.execute('''CREATE TABLE IF NOT EXISTS study_notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            subject VARCHAR(100) NOT NULL,
            title VARCHAR(255) NOT NULL,
            file_path VARCHAR(255) NOT NULL,
            uploaded_by VARCHAR(100) DEFAULT 'Admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
      
# Community Chat Table (For WhatsApp Style Chat)
        cursor.execute('''CREATE TABLE IF NOT EXISTS community_chats (
          id INT AUTO_INCREMENT PRIMARY KEY,
           user_email VARCHAR(255),
           user_name VARCHAR(255),
            message TEXT NOT NULL,
           timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
         )''')

        # --- DYNAMIC DATA INSERTION (Sari Information) ---
        college_data = [
            ('Institutional Name', 'Centre of Excellence, Government College Sanjauli, Shimla.'),
            ('Address', 'Sanjauli, Shimla, Himachal Pradesh, PIN - 171006.'),
            ('Contact Details', 'Phone: 0177-2640332 | Email: principalsanjauli@gmail.com.'),
            ('Official Website', 'www.gcsanjauli.edu.in.'),
            ('NAAC Accreditation', 'The college is accredited with an A+ Grade by NAAC (2023 Cycle).'),
            ('History', 'Established in 1869 as a school and converted into a degree college in 1969.'),
            ('Academic Programs', 'Offers Undergraduate courses in Arts (BA), Science (BSc), Commerce (BCom), Computer Applications (BCA), and Vocational studies (B.Voc).'),
            ('Campus Facilities', 'Equipped with a digitized library, modern science labs, IT labs, a multipurpose hall, and sports facilities.'),
            ('Student Strength', 'Over 3000+ students are currently enrolled across various disciplines.'),
            ('Scholarships', 'Provides various state and central government scholarships including Post-Matric and Merit-based schemes.'),
            ('Faculty', 'Staffed by over 50+ highly qualified professors and academic experts.'),
            ('Vision', 'To provide quality education that empowers students with knowledge and character.'),
            ('Mission', 'To foster an environment of learning and innovation that prepares students for global challenges.'),
            ('Location Info', 'Situated approximately 12 KM from the ISBT Shimla and easily accessible via local transport.')
        ]

        print("\n--- Synchronizing College Knowledge Base ---")
        for category, content in college_data:
            # to ensure that data in tabel
            cursor.execute("SELECT id FROM college_info WHERE category = %s", (category,))
            if cursor.fetchone():
                print(f"⚠️  Already Exists: '{category}'")
            else:
                # create new row if not exsist
                cursor.execute("INSERT INTO college_info (category, content) VALUES (%s, %s)", (category, content))
                print(f"✅  Newly Added: '{category}'")

        db.commit()
        db.close()
        print("\n🚀 Database Setup and Sync Completed Successfully!")

    except Exception as e:
        print(f"❌ Error during database setup: {e}")

if __name__ == "__main__":
    update_database_safely()