from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

def fetch_event_page_with_selenium():
    # 配置 Selenium 的 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无界面模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 设置 ChromeDriver 路径
    service = Service('/opt/homebrew/bin/chromedriver')  # 使用指定的 chromedriver 路径
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 打开页面
    url = "https://auckland.campuslabs.com/engage/organization/tetumuherenga/events"
    driver.get(url)
    
    # 使用 WebDriverWait 等待页面上活动容器加载完成
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[style='box-sizing: border-box; padding: 10px; width: 50%; height: auto;']"))
        )
    except Exception as e:
        print("Error waiting for page to load:", e)
        driver.quit()
        return None
    
    # 获取页面 HTML 内容
    page_content = driver.page_source
    driver.quit()
    
    return page_content

def parse_speaking_group_events(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # 存储所有匹配的活动信息
    speaking_group_events = []
    
    # 查找所有包含活动的外层 <div> 容器
    event_containers = soup.select("div[style='box-sizing: border-box; padding: 10px; width: 50%; height: auto;']")
    
    for container in event_containers:
        # 从父级容器查找活动链接
        link_tag = container.find("a", href=True)
        if link_tag:
            relative_link = link_tag["href"]
            event_link = f"https://auckland.campuslabs.com{relative_link}"
        else:
            event_link = "No link available"

        # 在子容器中查找包含活动详细信息的div
        event_div = container.select_one("div.MuiCard-root")
        if not event_div:
            continue

        # 查找活动名称在 <h3> 标签中的情况
        title_tag = event_div.find("h3")
        if title_tag:
            event_name = title_tag.get_text(strip=True)
            
            # 仅处理名称包含 "Speaking group" 的活动
            if "Speaking group" not in event_name:
                continue
        else:
            continue  # 跳过没有名称的活动

        # 查找时间和地点的两个连续的 <div> 标签
        details_divs = event_div.select("div[style*='padding: 0.5rem'] > div")
        
        if len(details_divs) >= 2:
            event_time = details_divs[0].get_text(strip=True)
            event_location = details_divs[1].get_text(strip=True)
        else:
            event_time = "No time specified"
            event_location = "No location specified"
        
        # 添加符合条件的活动信息到列表
        speaking_group_events.append({
            "name": event_name,
            "time": event_time,
            "location": event_location,
            "link": event_link
        })
    
    return speaking_group_events



import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(events):
    sender_email = "zoeachen1122@gmail.com"  # 发件人邮箱
    receiver_email = "xueshanchen1122@gmail.com"  # 收件人邮箱
    password = "mnfcmaebkuwtonyz"  # 发件人邮箱密码（建议使用应用密码）

    # 设置邮件内容
    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily Event Update: Speaking Group Events"
    message["From"] = sender_email
    message["To"] = receiver_email

    # 构建HTML内容
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
    # 添加HTML内容到邮件
    part = MIMEText(html_content, "html")
    message.attach(part)

    # 发送邮件
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# 主函数：从Selenium获取内容并解析
page_content = fetch_event_page_with_selenium()
if page_content:
    speaking_group_events = parse_speaking_group_events(page_content)

    # 如果有活动信息则发送邮件
    if speaking_group_events:
        send_email(speaking_group_events)
    else:
        print("No matching events found. Email not sent.")
else:
    print("Failed to fetch page content.")

