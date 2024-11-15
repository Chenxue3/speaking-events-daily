import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Function to fetch the webpage content with Selenium
def fetch_event_page_with_selenium():
    # Configure Selenium Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize WebDriver without specifying the path
    driver = webdriver.Chrome(options=chrome_options)
    
    # Open the target webpage
    url = "https://auckland.campuslabs.com/engage/organization/tetumuherenga/events"
    driver.get(url)

    # Debugging: Print page content after loading
    print("Page content after loading:")
    print(driver.page_source[:1000])  # Print first 1000 characters to check content

    # Wait until event containers are loaded
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[style='box-sizing: border-box; padding: 10px; width: 50%; height: auto;']"))
        )
    except Exception as e:
        print("Error waiting for page to load:", e)
        driver.quit()
        return None
    
    # Retrieve page HTML content
    page_content = driver.page_source
    driver.quit()
    
    return page_content

# Function to parse and extract event details from page content
def parse_speaking_group_events(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    speaking_group_events = []  # List to store matched events
    
    # Find all outer <div> containers for events
    event_containers = soup.select("div[style='box-sizing: border-box; padding: 10px; width: 50%; height: auto;']")
    
    for container in event_containers:
        # Extract the event link from the parent container's <a> tag
        link_tag = container.find("a", href=True)
        if link_tag:
            relative_link = link_tag["href"]
            event_link = f"https://auckland.campuslabs.com{relative_link}"
        else:
            event_link = "No link available"

        # Locate the inner container with event details
        event_div = container.select_one("div.MuiCard-root")
        if not event_div:
            continue

        # Find event name in <h3> tag
        title_tag = event_div.find("h3")
        if title_tag:
            event_name = title_tag.get_text(strip=True)
            
            # Only process events containing "Speaking group" in the name
            if "Speaking group" not in event_name:
                continue
        else:
            continue  # Skip if there's no event name

        # Extract time and location from consecutive <div> tags
        details_divs = event_div.select("div[style*='padding: 0.5rem'] > div")
        
        if len(details_divs) >= 2:
            event_time = details_divs[0].get_text(strip=True)
            event_location = details_divs[1].get_text(strip=True)
        else:
            event_time = "No time specified"
            event_location = "No location specified"
        
        # Append extracted event details to the list
        speaking_group_events.append({
            "name": event_name,
            "time": event_time,
            "location": event_location,
            "link": event_link
        })
    
    return speaking_group_events

# Function to send email with event details
def send_email(events):
    # Get email credentials from environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    # Set up email message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily Event Update: Speaking Group Events"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Build HTML content
    html_content = """
    <html>
    <body>
        <h2>Speaking Group Events</h2>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>Event Name</th>
                <th>Event Time</th>
                <th>Event Location</th>
                <th>Event Link</th>
            </tr>
    """
    for event in events:
        html_content += f"""
            <tr>
                <td>{event['name']}</td>
                <td>{event['time']}</td>
                <td>{event['location']}</td>
                <td><a href="{event['link']}">Link</a></td>
            </tr>
        """
    html_content += """
        </table>
    </body>
    </html>
    """
    # Attach HTML content to email
    part = MIMEText(html_content, "html")
    message.attach(part)

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# Main function to fetch, parse, and send email if there are events
page_content = fetch_event_page_with_selenium()
if page_content:
    speaking_group_events = parse_speaking_group_events(page_content)

    # Send email if there are matched events
    if speaking_group_events:
        send_email(speaking_group_events)
    else:
        print("No matching events found. Email not sent.")
else:
    print("Failed to fetch page content.")
