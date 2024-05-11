import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkcalendar import Calendar

def create_database(cursor, db_name):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def create_table(cursor):
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS complaints (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            complaint_name VARCHAR(255),
                            complaint_address VARCHAR(255),
                            complaint_mobile VARCHAR(20),
                            identification_no VARCHAR(20),
                            complaint_type VARCHAR(255),
                            identification_type VARCHAR(50),
                            detailed_location VARCHAR(255),
                            accused_name VARCHAR(255),
                            accused_address VARCHAR(255),
                            complaint_detail TEXT,
                            location_of_incident VARCHAR(255),
                            incident_date DATE,
                            incident_time TIME,
                            submission_time DATETIME,
                            status VARCHAR(20),
                            status_response VARCHAR(255)
                        )""")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(cursor, data):
    try:
        sql = """INSERT INTO complaints 
                 (complaint_name, complaint_address, complaint_mobile, identification_no, 
                 complaint_type, identification_type, detailed_location, accused_name, 
                 accused_address, complaint_detail, location_of_incident, incident_date, 
                 incident_time, submission_time, status, status_response) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, data)
        db.commit()
        print("Data inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")

def open_calendar(event=None):
    def set_date():
        incident_date_entry.delete(0, tk.END)
        incident_date_entry.insert(0, cal.get_date())
        top.destroy()

    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, background='white', foreground='black', bordercolor='blue')
    cal.pack()
    ok_button = ttk.Button(top, text="OK", command=set_date)
    ok_button.pack()

def submit_form():
    complaint_name = complaint_name_entry.get()
    complaint_address = complaint_address_entry.get()
    complaint_mobile = complaint_mobile_entry.get()
    identification_no = identification_no_entry.get()
    complaint_type = ", ".join([type_var.get() for type_var in complaint_type_vars if type_var.get() != ""])
    identification_type = identification_type_var.get()
    detailed_location = detailed_location_entry.get()
    accused_name = accused_name_entry.get()
    accused_address = accused_address_entry.get()
    complaint_detail = complaint_detail_entry.get("1.0", tk.END).strip()
    location_of_incident = location_of_incident_entry.get()
    incident_date_str = incident_date_entry.get()
    incident_date_obj = datetime.strptime(incident_date_str, '%m/%d/%y')
    incident_date = incident_date_obj.strftime('%Y-%m-%d')
    incident_time = incident_time_spinbox.get()
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = status_var.get()
    status_response = status_response_entry.get()
    data = (complaint_name, complaint_address, complaint_mobile, identification_no, 
            complaint_type, identification_type, detailed_location, accused_name, 
            accused_address, complaint_detail, location_of_incident, incident_date, 
            incident_time, submission_time, status, status_response)
    insert_data(cursor, data)
    messagebox.showinfo("Success", "Submitted successfully")

root = tk.Tk()
root.title("Complaint Form")

frame = tk.Frame(root, padx=20, pady=20, bg='lightblue')
frame.pack(expand=True)

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5, background='blue', foreground='black')
style.configure("TLabel", font=("Arial", 12), background='lightblue', foreground='black')
style.configure("TEntry", font=("Arial", 12), padding=5)
style.configure("TCombobox", font=("Arial", 12), padding=5)
style.configure("TCheckbutton", background='lightblue', foreground='black')
style.configure("TRadiobutton", background='lightblue', foreground='black')

username = input("Enter MySQL username: ")
password = input("Enter MySQL password: ")


try:
    db = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password
    )

    cursor = db.cursor()
    conditional_creation =int(input("Is complaints_db already created : Enter 1 - Yes and 0 - No "))
    
    if(conditional_creation==0):
        create_database(cursor, "complaints_db")

    cursor.execute("USE complaints_db")

    create_table(cursor)

    complaint_name_label = ttk.Label(frame, text="Complaint Name (As per Identification Card):", background='lightblue')
    complaint_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    complaint_name_entry = ttk.Entry(frame)
    complaint_name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

    complaint_address_label = ttk.Label(frame, text="Complaint Address:", background='lightblue')
    complaint_address_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
    complaint_address_entry = ttk.Entry(frame)
    complaint_address_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    complaint_mobile_label = ttk.Label(frame, text="Complaint Mobile Number:", background='lightblue')
    complaint_mobile_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    complaint_mobile_entry = ttk.Entry(frame)
    complaint_mobile_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    identification_no_label = ttk.Label(frame, text="Identification No.:", background='lightblue')
    identification_no_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
    identification_no_entry = ttk.Entry(frame)
    identification_no_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

    detailed_location_label = ttk.Label(frame, text="Detailed Location:", background='lightblue')
    detailed_location_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
    detailed_location_entry = ttk.Entry(frame)
    detailed_location_entry.grid(row=4, column=1, sticky="w", padx=10, pady=5)

    accused_name_label = ttk.Label(frame, text="Accused Name (if known):", background='lightblue')
    accused_name_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
    accused_name_entry = ttk.Entry(frame)
    accused_name_entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)

    accused_address_label = ttk.Label(frame, text="Accused Address (if known):", background='lightblue')
    accused_address_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)    
    accused_address_entry = ttk.Entry(frame)
    accused_address_entry.grid(row=6, column=1, sticky="w", padx=10, pady=5)

    complaint_detail_label = ttk.Label(frame, text="Complaint Detail:", background='lightblue')
    complaint_detail_label.grid(row=7, column=0, sticky="w", padx=10, pady=5)
    complaint_detail_entry = tk.Text(frame, font=("Arial", 12), height=4, width=30)
    complaint_detail_entry.grid(row=7, column=1, sticky="w", padx=10, pady=5)

    complaint_label = ttk.Label(frame, text="Complaint Type:", background='lightblue')
    complaint_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)

    complaint_types = ["Type 1", "Type 2", "Type 3", "Type 4", "Type 5", "Others"]
    complaint_type_vars = []

    for i, complaint_type in enumerate(complaint_types):
        var = tk.StringVar()
        checkbox = ttk.Checkbutton(frame, text=complaint_type, variable=var, onvalue=complaint_type, offvalue="", width=15)
        checkbox.grid(row=8, column=i+1, sticky="w", padx=5, pady=5)
        complaint_type_vars.append(var)

    identification_type_label = ttk.Label(frame, text="Identification Type:", background='lightblue')
    identification_type_label.grid(row=9, column=0, sticky="w", padx=10, pady=5)

    identification_types = ["Aadhar Card", "PAN Card", "Voter Card", "Passport", "Driving License", "Mnrega Card", "Employee Card"]
    identification_type_var = tk.StringVar()
    identification_type_entry = ttk.Combobox(frame, textvariable=identification_type_var, values=identification_types, width=15, state="readonly")
    identification_type_entry.grid(row=9, column=1, sticky="w", padx=10, pady=5)
    identification_type_entry.current(0)

    incident_date_label = ttk.Label(frame, text="Date of Incident:", background='lightblue')
    incident_date_label.grid(row=10, column=0, sticky="w", padx=10, pady=5)

    incident_date_entry = ttk.Entry(frame)
    incident_date_entry.grid(row=10, column=1, sticky="w", padx=10, pady=5)
    incident_date_entry.bind("<Button-1>", lambda event: open_calendar())

    incident_time_label = ttk.Label(frame, text="Time of Incident:", background='lightblue')
    incident_time_label.grid(row=11, column=0, sticky="w", padx=10, pady=5)

    incident_time_spinbox = ttk.Spinbox(frame, from_=0, to=23, wrap=True, width=5)
    incident_time_spinbox.grid(row=11, column=1, sticky="w", padx=5, pady=5)

    location_of_incident_label = ttk.Label(frame, text="Location of Incident (PS):", background='lightblue')
    location_of_incident_label.grid(row=12, column=0, sticky="w", padx=10, pady=5)
    location_of_incident_entry = ttk.Entry(frame)
    location_of_incident_entry.grid(row=12, column=1, sticky="w", padx=10, pady=5)

    status_label = ttk.Label(frame, text="Status:", background='lightblue')
    status_label.grid(row=13, column=0, sticky="w", padx=10, pady=5)

    status_var = tk.StringVar()
    status_options = ["Active", "Resolved", "Not Related"]
    for i, option in enumerate(status_options):
        ttk.Radiobutton(frame, text=option, variable=status_var, value=option).grid(row=13, column=i+1, sticky="w", padx=5, pady=5)

    status_response_label = ttk.Label(frame, text="Status Response:", background='lightblue')
    status_response_label.grid(row=14, column=0, sticky="w", padx=10, pady=5)
    status_response_entry = ttk.Entry(frame)
    status_response_entry.grid(row=14, column=1, sticky="w", padx=10, pady=5)


    submit_button = ttk.Button(frame, text="Submit", command=submit_form)
    submit_button.grid(row=15, columnspan=2, pady=10)

    root.mainloop()

    cursor.close()
    db.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")
