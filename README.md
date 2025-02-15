# Gmail Sender Action 📩

This GitHub Action enables you to send emails via **Gmail** using **HTML templates** directly from your GitHub workflows.

![image](https://github.com/user-attachments/assets/f8bca9ac-f0d6-4872-bfee-a94b6288ed0b)

## 📌  Features
- **Send emails** to multiple recipients (up to 5)  
- **Supports custom HTML templates**  
- **Secure authentication** using Gmail App Password  
- **Rich HTML email formatting**  
- **Seamless integration** with GitHub Actions  

## 📌 **Use Cases**  
You can use this **Gmail Sender GitHub Action** for various automation scenarios, including:  

- **Automated Reports** – Send test reports, build logs, or CI/CD results via email.  
- **Release Notifications** – Notify stakeholders when a new version is released.  
- **Deployment Alerts** – Send emails upon successful deployment or failures.  
- **Issue Tracking** – Email updates when an issue is created or resolved.  
- **Scheduled Reminders** – Set up periodic emails for reminders or team updates.  
- **Security Alerts** – Notify the team about security vulnerabilities or warnings.  


---

## 📥 Required Inputs
| Input            | Description                                        | Required |
|-----------------|------------------------------------------------|----------|
| `sender_email`  | Gmail address used for sending emails           | ✅       |
| `app_password`  | Gmail App Password for authentication           | ✅       |
| `receiver_emails` | Comma-separated list of recipient emails (max 5) | ✅       |
| `template_path` | Path to the HTML template file in the repository | ✅       |
| `subject`       | Email subject line (optional)                    | ❌       |

---

## ⚙️ Setup Instructions

### 1️⃣ Generate a Gmail App Password
1. Go to **Google Account Settings**
2. Navigate to **Security > 2-Step Verification > App Passwords**
3. Generate a new App Password for **"Mail"**

### 2️⃣ Add Repository Secrets
Go to **GitHub Repo → Settings → Secrets and Variables → Actions** and add:
- **`GMAIL_SENDER`** → Your Gmail address
- **`GMAIL_APP_PASSWORD`** → Your Gmail App Password
- **`RECIPIENTS`** → Your Recipients upto 5 eg : person1@gmail.com, person2@gmail.com

### 3️⃣ Create Workflow File
Inside `.github/workflows/{your-filename}.yml`, add the following workflow:

```yaml
name: Send Email

on: [push]

jobs:
  send-email:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2
      
      - name: Send Email via Gmail
        uses: Raghul-M/gmail-sender-action@v1
        with:
          sender_email: ${{ secrets.GMAIL_SENDER }}
          app_password: ${{ secrets.GMAIL_APP_PASSWORD }}
          receiver_emails: ${{ secrets.RECIPIENTS }}
          template_path: "templates/email_template.html"
          subject: "Notification from GitHub Action"
```

---

## 📌 Important Notes
- **Maximum 5 recipients** per email.  
- **HTML template file must exist** in the repository.  
- **Requires Gmail account with 2FA enabled**.  
- **App Password must have mail permissions**.  

---

## 📖 Example Usage
### Example HTML Template (`templates/email_template.html`)
This email template is **customizable**, allowing you to design your email with images, styles, and dynamic content.

<p align="center">
  <img src="https://github.com/user-attachments/assets/e6c18387-877b-450c-8337-8bb22385156c" alt="Workflow Image">
</p>


## 🐛 Bug Reports & Feedback
Please report any issues or feature requests via the **[GitHub repository's issue tracker](https://github.com/Raghul-M/gmail-sender-action/issues)**.



## 🤝 Contributing
This project is **open-source**, and contributions are welcome! Feel free to submit **issues**, **feature requests**, or **pull requests**.

Want to discuss? Connect with me on Linkedin **[Raghul-M](https://www.linkedin.com/m-raghul/)**!

