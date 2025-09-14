# Student Performance Analyzer

A web application that uses machine learning to predict student performance based on various factors like attendance, study hours, and previous grades.

## Features

- Separate login systems for students and faculty
- Students can:
  - Register and login
  - Enter subject information manually
  - Input previous grades, attendance, and study hours
  - View predicted scores based on machine learning model
- Faculty can:
  - Login to a dedicated dashboard
  - View scores of each student individually
  - Analyze student performance and grades

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python run.py
   ```

## Technologies Used

- Backend: Flask
- Database: SQLite with SQLAlchemy
- Machine Learning: scikit-learn
- Frontend: HTML, CSS, JavaScript, Bootstrap
