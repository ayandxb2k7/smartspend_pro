SmartSpend Pro

SmartSpend Pro is a personal finance web application built using Flask and Scikit-Learn. The application allows users to track daily expenses, automatically categorize spending, set monthly savings goals, and view a simple prediction of future expenses using a machine learning model.

This project was developed as a portfolio project to explore backend development, database handling, and basic machine learning integration within a web application.

Project Features

User registration and secure login system Add and track daily expenses Automatic expense categorization based on keywords Monthly savings goal tracking with progress calculation Basic expense prediction using Linear Regression Export expense history as CSV Responsive user interface built with Bootstrap

Technology Stack

Backend: Python and Flask Authentication: Flask-Login Database: SQLite Machine Learning: Scikit-Learn, Pandas, NumPy Frontend: HTML and Bootstrap

Project Structure

smartspend-pro/

app.py – Main Flask application model.py – Machine learning logic and categorization requirements.txt – Project dependencies database.db – SQLite database (generated locally)

templates/ – HTML templates static/ – Static files

Installation and Setup

Clone the repository git clone https://github.com/ayandxb2k7/smartspend_pro.git

Navigate to the project folder cd smartspend-pro

Install dependencies pip install -r requirements.txt

Run the application python app.py

Open the application in your browser http://127.0.0.1:5000

How to Use

First, register a new account. Login using your credentials. Add your daily expenses with title, amount, and date. Set a monthly savings goal. View total spending and predicted next expense on the dashboard. Use the export option to download your expenses as a CSV file.

How the Prediction Works

The prediction feature uses a simple Linear Regression model. It takes previous expense data and estimates the next expected expense amount based on spending trends. The implementation demonstrates how a basic machine learning model can be integrated into a web application.

Future Improvements

Add data visualization using charts Improve categorization using NLP techniques Add multi-month analytics Deploy to a cloud platform Provide REST API support

Created By

Ayan Khan Computer Science Student BITS Pilani Dubai Campus

Email: f20250376@dubai.bits-pilani.ac.in
