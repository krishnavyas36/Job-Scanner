import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load Excel Data
file_path = r"C:\Users\dkris\Downloads\Automate.xlsx"
df = pd.read_excel(file_path)

# Set Edge options to disable GPU & WebRTC
edge_options = Options()
edge_options.add_argument("--disable-webrtc")
edge_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
edge_options.add_argument("--disable-software-rasterizer")  # Force software rendering

# Set up Microsoft Edge WebDriver
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

# Open the website
driver.get("https://notifyai.tech/monitors")

# Wait until login is completed
time.sleep(60)

# Loop through Excel rows
for index, row in df.iterrows():
    try:
        ### 1️⃣ Click "Create" button before each row ###
        create_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Create')]")
        create_button.click()
        time.sleep(2)  # Wait for dropdown

        ### 2️⃣ Click "Monitor URL" before filling data ###
        monitor_url_option = driver.find_element(By.XPATH, "//div[contains(text(), 'Monitor URL')]")
        monitor_url_option.click()
        time.sleep(3)  # Wait for form to load

        ### 3️⃣ Fill in the form ###
        # Find and fill the URL input field
        url_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter company career page URL to monitor']")
        url_field.clear()
        url_field.send_keys(row["link"])

        # Find the Keywords input field
        keyword_field = driver.find_element(By.XPATH, "//input[@placeholder='Type and press Enter']")

        # Loop through each keyword column and enter individually
        keyword_columns = ["keyword1", "Unnamed: 3", "Unnamed: 4", "Unnamed: 5", "Unnamed: 6"]
        for col in keyword_columns:
            if pd.notna(row[col]):  # Check if the column has a value
                keyword_field.send_keys(row[col])
                keyword_field.send_keys(Keys.RETURN)  # Press Enter after each keyword
                time.sleep(1)  # Pause to allow UI update

        ### 4️⃣ Click "Create Monitor" button ###
        create_monitor_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Create Monitor')]")
        create_monitor_button.click()

        time.sleep(3)  # Wait before processing the next row

    except Exception as e:
        print(f"Error on row {index}: {e}")

# Close the browser after all rows are processed
driver.quit()
