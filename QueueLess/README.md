# QueueLess

QueueLess is a Django-based queue management system designed to reduce waiting time and provide a simple digital token management experience.

## Features

### Customer
- User registration and login
- View available services
- Generate queue tokens
- View token status
- See people ahead in the queue
- Estimated waiting time
- View token history

### Staff
- Staff dashboard
- View assigned counters
- Call the next customer
- Serve tokens
- Complete tokens
- Skip tokens
- View current queue

### Admin
- Admin dashboard
- View service statistics
- View counter statistics
- Monitor token activity
- Add services
- Edit services
- Enable/disable services
- Add counters
- Edit counters
- Enable/disable counters
- Assign staff to counters

## Technology Stack

- Python
- Django 6.1
- SQLite
- HTML
- CSS
- JavaScript
- Django ORM

## Project Structure

```text
QueueLess/
│
├── accounts/
├── dashboard/
├── queue_system/
├── queueless/
├── static/
├── templates/
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore