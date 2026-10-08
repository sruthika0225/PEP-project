# 🔔 Task Alarm & Reminder — PEP DevOps Project

A Flask-based task reminder application with scheduled alarms, snooze, dismiss, repeating reminders and SQLite storage.

This project is also configured for **DevOps automation using Docker, Terraform, Jenkins, AWS EC2 and GitHub Container Registry (GHCR).**

## 🚀 Features

- Create, edit and delete reminders
- Schedule alarms using date and time
- Once, daily and weekday repeating reminders
- Alarm screen with sound
- Snooze for 5 minutes
- Dismiss alarms
- Complete tasks
- SQLite database
- Automated tests
- Docker containerization
- AWS infrastructure provisioning using Terraform
- Jenkins-based CI/CD automation
- Docker image publishing to GHCR

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **Containerization:** Docker
- **Infrastructure as Code:** Terraform
- **CI/CD:** Jenkins
- **Cloud:** AWS EC2
- **Container Registry:** GitHub Container Registry (GHCR)
- **Version Control:** Git & GitHub

## 📁 Project Structure

```text
PEP-project/
│
├── database/
├── models/
├── routes/
├── services/
├── static/
├── templates/
├── tests/
│
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
│
└── terraform/
    ├── provider.tf
    ├── vpc.tf
    ├── ec2.tf
    ├── variables.tf
    ├── output.tf
    └── user_data.yaml