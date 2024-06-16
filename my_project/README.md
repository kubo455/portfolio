# EXPENCE TRACKER

#### Video demo: <URL https://youtu.be/NYIu6QTEQW4>
#### Description:
I have created the expense tracker web application. This app is used for tracking user's expenses and income. First,
the user has to register and log in to the app. I used bcrypt to hash the user's password.

The app was developed using Visual Studio Code.

## Usage
On the main page, users can see where they can add their expenses and balance. They can also view charts of income and expenses,
as well as a chart displaying all expenses. Users can see their last 15 expences and keep track of all their expenses.

Users have the option to create new expense types or use the default types of expenses provided. This can be done in the settings page,
where they can add new types of expenses and change their password. They are required to use their old password in order to create a new one.

## Style
In the static folder, I have a CSS file for styling my templates and each element within them.
I used help of Chat-GPT to assist me with styling, demonstrating how to modify certain elements so I wouldn't have to search for them on my own.
My goal was to create a visually appealing and user-friendly environment. 

## Templates
The aplication is structured using HTML templates stored in the 'templates' folder:
- base : template from which all other templates inherit, ensuring a consistent look throughout the application.

- error_message: provide feedback to the user on their interactions, particularly displaying error messages when something goes wrong.

- index:  main page or home page for users is stored here. Users can track their expenses, add new expenses, add new balance, view charts,
           and see their last 15 spendings.

- login: template contains the login form where users can sign in or navigate to the register page to create an account.

- message: used to provide feedback to the user after successful actions.

- register: page is dedicated to allowing users to create an account. If they already have an account,
             they can navigate to the login page via a login URL link.

- settings: enables users to modify their account settings, including changing their password and creating new expense types.

## Main aplication and helpers.py
- app.py : here is my main application code including all functions.

- helper.py : my other functions, but only one for now, which is chart_colors. This function creates colors within a spectrum and adds them to my chart of expenses.

- table.py : this is the app I use to create tables in my database.db using SQLite. Here, I store data about users, their expenses, balance, user ID,
             passwords, and other relevant information.

## Project changes
I have to change my aplication at first because it was too complex and I want it to be simple and user friendly. I have to delete some templates, I think now my app
is better. I change it few times and rebuilt it, but now I like it,

## Dependencies
- ChartJS: popular JavaScript library for creating interactive and customizable charts and graphs on webpages. It provides a simple yet powerful API for developers to easily
           create various types of charts, including line charts, bar charts, pie charts, and more. I used it because it is beginner friendly and symple to use.

- Flask: I used flask as my primary web framework. It is symple to us, and perfromance is enought for my project.

- Sqlite: software library that provides a relational database management system. I used it because we was previously 
          using it in earlier weeks in CS50.

