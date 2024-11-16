# Speaking Events Daily

This repository contains a Python-based automation script designed to scrape event details from the [University of Auckland's Engage Events page](https://auckland.campuslabs.com/engage/organization/tetumuherenga/events). The project fetches and parses event information about "Speaking Group" events, which always full, then sends a daily email notification with the details to specified recipients. The script is fully automated and configured to run twice daily using GitHub Actions.

---

## Features

- **Event Scraping with Selenium**: Uses Selenium to load dynamic content from the Engage Events page, ensuring compatibility with JavaScript-driven websites.
- **Email Notification**: Sends event details (name, time, location, and link) via email to configured recipients using Gmail's SMTP service.
- **Error Handling**: Includes robust error handling for page loading issues and missing event data.
- **Automation**: Scheduled execution using GitHub Actions at 12:00 PM and 12:00 AM New Zealand Time.
- **Environment Variable Management**: Sensitive information (e.g., email credentials) is securely stored in GitHub Secrets.

---

## Technologies Used

- **Python**: Core language for the project.
- **Selenium**: For web scraping dynamic content.
- **BeautifulSoup**: For HTML parsing and event data extraction.
- **Webdriver-Manager**: For managing ChromeDriver installations.
- **SMTP**: For sending email notifications.
- **GitHub Actions**: For automating script execution on a daily schedule.

---

## Setup

### Prerequisites
1. Install [Python 3.9+](https://www.python.org/downloads/).
2. Install [Google Chrome](https://www.google.com/chrome/) and ensure it's updated to the latest version.
3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## GitHub Secrets Configuration

This project requires sensitive information to be securely stored as GitHub Secrets. The following secrets need to be added to the repository:

1. **Navigate to Repository Settings**:
   - Go to your repository on GitHub.
   - Click on `Settings` > `Secrets and variables` > `Actions`.

2. **Add Secrets**:
   - Click `New repository secret` for each of the following keys:
     - `SENDER_EMAIL`: The email address from which notifications will be sent.
     - `EMAIL_PASSWORD`: The app password for the sender Gmail account. You can generate it [here](https://support.google.com/accounts/answer/185833?hl=en).
     - `RECEIVER_EMAIL`: The email address of the recipient who will receive the daily notifications.

3. **Example**:
   If your email is `example@gmail.com`, configure:
   - `SENDER_EMAIL`: `example@gmail.com`
   - `EMAIL_PASSWORD`: `your_generated_app_password`
   - `RECEIVER_EMAIL`: `recipient_email@gmail.com`

   These secrets will be automatically used in the GitHub Actions workflow to authenticate the email-sending process.

---

## Usage

1. **Run Locally**:
   ```bash
   python event_script.py
   ```

   Ensure ChromeDriver and the required dependencies are installed before running the script.

2. **Automated Execution**:
   The script is configured to run twice daily via GitHub Actions. You can trigger it manually or let it run on the defined schedule.

---

## GitHub Actions Configuration

The repository includes a `.github/workflows/daily_event_update.yml` file for GitHub Actions. This workflow:
- Sets up the environment (Python, Chrome, and ChromeDriver).
- Installs required Python dependencies.
- Runs the scraping and email script.
- Logs output and errors for debugging purposes.

To modify the schedule, edit the `cron` value in the workflow file. For example:
```yaml
schedule:
  - cron: '0 23 * * *' # Runs at 12:00 PM NZDT (UTC+23)
```

---

## Debugging Locally

- Use the [act](https://github.com/nektos/act) tool to test the GitHub Actions workflow locally.
- Ensure Docker is running and set up with the correct architecture (e.g., `linux/amd64` for M1/M2 chips).

---

## Troubleshooting

- **ChromeDriver Version Mismatch**: Ensure the installed ChromeDriver version matches your local Chrome version.
- **SMTP Errors**: Verify that Gmail App Passwords are configured correctly, and "Less Secure Apps" access is enabled if required.
- **Selenium WebDriver Failures**: Ensure all required dependencies (e.g., `libx11-xcb1`, `libgbm-dev`) are installed on your system.

---

## Contributions

Contributions to improve the script or enhance automation are welcome! Feel free to open issues or submit pull requests.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

