from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

# Setup Selenium WebDriver (Make sure to download the correct ChromeDriver)
driver = webdriver.Chrome()

# Define search parameters
job_title = "Data Analyst"
location = "USA"

# Format the Indeed search URL
search_url = f"https://www.indeed.com/jobs?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}"
driver.get(search_url)
time.sleep(3)  # Allow page to load

job_list = []  # Store job details

# Loop through multiple pages (limit to 5 pages for now)
for page in range(1, 6):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jobs = soup.find_all('div', class_='job_seen_beacon')
    
    for job in jobs:
        try:
            title = job.find('h2', class_='jobTitle').text.strip()
            company = job.find('span', class_='companyName').text.strip()
            location = job.find('div', class_='companyLocation').text.strip()
            salary = job.find('div', class_='salary-snippet-container')
            salary = salary.text.strip() if salary else "Not Provided"
            link = "https://www.indeed.com" + job.find('a', class_='jcs-JobTitle')['href']
            
            job_list.append({
                'Title': title,
                'Company': company,
                'Location': location,
                'Salary': salary,
                'Link': link
            })
        except Exception as e:
            print("Skipping a job due to error:", e)
    
    # Move to the next page
    try:
        next_button = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
        next_button.click()
        time.sleep(3)  # Allow time for the next page to load
    except:
        print("No more pages.")
        break

# Close the browser
driver.quit()

# Save results to CSV
jobs_df = pd.DataFrame(job_list)
jobs_df.to_csv('indeed_data_analyst_jobs.csv', index=False)
print("Scraping complete! Data saved to indeed_data_analyst_jobs.csv")
