import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading  ## Import threading

def start_search():
    exam_topic = combobox_exam_topic.get()
    start_range = entry_start_range.get()
    end_range = entry_end_range.get()

    if not exam_topic or not start_range or not end_range:
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    try:
        start_range = int(start_range)
        end_range = int(end_range)
    except ValueError:
        messagebox.showerror("Error", "Start and End ranges must be numbers.")
        return

    # Run the search in a separate thread
    threading.Thread(target=run_search, args=(exam_topic, start_range, end_range)).start()

def run_search(exam_topic, start_range, end_range):
    # Optional: Set up Chrome options
    chrome_options = Options()
    # Remove headless mode if you want to see the UI
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        for i in range(start_range, end_range + 1):
            search_query = f"{exam_topic} question {i}"
            
            # Open Google
            driver.get("https://www.google.com")
            
            # Find the search box and enter the query
            search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
            search_box.clear()
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for the search results to load and find the first search result
            first_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
            link = first_result.find_element(By.XPATH, '..').get_attribute('href')
            
            # Open the first search result in a new tab
            driver.execute_script("window.open(arguments[0]);", link)
            
            # Go back to Google to perform the next search in the original tab
            driver.get("https://www.google.com")

        # Switch to the first tab to keep it as the main tab
        driver.switch_to.window(driver.window_handles[0])

        # Print a message and wait for 1 hour to keep the pages open
        print("All pages opened. Keeping the pages open for 1 hour...")
        time.sleep(3600)  # Wait for 1 hour (3600 seconds)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Keep the browser open manually or close it if needed
        # Uncomment the following line if you want to close the browser automatically after 1 hour
        # driver.quit()
        pass  # Do nothing, keep the browser open

# List of exam topics
exam_topics = [
    "Exam Associate Cloud Engineer topic 1",
    "Exam AWS Certified SysOps Administrator - Associate topic 1",
    "Exam AWS Certified Solutions Architect - Professional SAP-C02 topic 1",
    "Exam AWS Certified Solutions Architect - Professional topic 1",
    "Exam AWS Certified Solutions Architect - Associate SAA-C03 topic 1",
    "Exam AWS Certified Security - Specialty SCS-C02 topic 1",
    "Exam AWS Certified Security - Specialty topic 1",
    "Exam AWS Certified Machine Learning - Specialty topic 1",
    "Exam AWS Certified DevOps Engineer - Professional DOP-C02 topic 1",
    "Exam AWS Certified Developer - Associate DVA-C02 topic 1",
    "Exam AWS Certified Data Engineer - Associate DEA-C01 topic 1",
    "Exam AWS Certified Cloud Practitioner topic 1",
    "Exam AWS Certified Advanced Networking - Specialty ANS-C01 topic 1",
    "Exam Associate Cloud Engineer topic 1",
    "Exam Cloud Digital Leader topic 1",
    "Exam Professional Cloud Architect topic 1",
    "Exam Professional Cloud Database Engineer topic 1",
    "Exam Professional Cloud Developer topic 1",
    "Exam Professional Cloud DevOps Engineer topic 1",
    "Exam Professional Cloud Network Engineer topic 1",
    "Exam Professional Cloud Security Engineer topic 1",
    "Exam Professional Data Engineer topic 1",
    "Exam Professional Google Workspace Administrator topic 1",
    "Exam Professional Machine Learning Engineer topic 1",
    "Exam 2V0-21.23 topic 1",
    "Exam 2V0-41.23 topic 1",
    "Exam CCSP topic 1",
    "Exam CISSP topic 1",
    "Exam SSCP topic 1"
]

# Create the main application window
root = tk.Tk()
root.title("Nasser Exam Topics")  # Set the window title
root.geometry("600x300")  # Set the initial size of the window to be larger

# Create and place labels and entry fields with increased padding
tk.Label(root, text="Exam Topic:").grid(row=0, column=0, padx=10, pady=10, sticky='w')

# Create a combobox for selecting or adding exam topics
combobox_exam_topic = ttk.Combobox(root, values=exam_topics, width=50)
combobox_exam_topic.grid(row=0, column=1, padx=10, pady=10)
combobox_exam_topic.set(exam_topics[0])  # Set default value

tk.Label(root, text="Start Range:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
entry_start_range = tk.Entry(root, width=10)
entry_start_range.grid(row=1, column=1, padx=10, pady=10, sticky='w')

tk.Label(root, text="End Range:").grid(row=2, column=0, padx=10, pady=10, sticky='w')
entry_end_range = tk.Entry(root, width=10)
entry_end_range.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# Create and place the start button with increased padding
start_button = tk.Button(root, text="Start Search", command=start_search)
start_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

# Start the Tkinter event loop
root.mainloop()
