# Student Home

#### Video Demo: [Watch here](https://www.youtube.com/watch?v=8J_4LqUM2UM)

#### Description:
Student Home is a **Flask-based web application** designed to help students efficiently organize and manage their academic lives. The application integrates several essential features, such as a GPA calculator, a class schedule manager, and an assignment tracker, all aimed at helping students stay organized, track their progress, and maintain focus on their academic goals. By streamlining these critical aspects of student life, **Student Home** provides users with a convenient platform to keep their academic information in one place, making it easier to stay on top of deadlines, assignments, and grades. Whether you're a high school student, a college student, or anyone pursuing an education, this app can help you optimize your academic experience.

## Features:
- **Assignment Tracker 📌**
  - Add, edit, and delete assignments with ease.
  - Track assignment due dates and progress to ensure nothing is forgotten.
  - Assignments are displayed in a simple, organized list for quick access.
  - Helps students stay on top of their workload and meet deadlines efficiently.

- **Editable Class Schedule 🗓️**
  - Students can input and manage their weekly class schedule.
  - Schedule updates are simple, ensuring that any changes to the semester’s timetable can be reflected.
  - Structured weekly view provides clarity on class timings, locations, and other important details.
  - Enhances time management by allowing students to visualize their entire academic schedule.

- **GPA Calculator 🎓**
  - Allows students to enter their grades for each class along with the type of class (AP, IB, etc.).
  - Automatically calculates the GPA based on user inputs and displays the cumulative result.
  - Supports the calculation of weighted GPA for students in advanced courses like AP and IB.
  - A useful tool for students who need to keep track of their academic performance throughout the semester.

- **User Authentication 🔐**
  - Secure login and registration system using Flask, ensuring that each user’s data is protected.
  - Each user has a private and personalized dashboard with their own assignments and schedule.
  - Passwords are securely hashed using `werkzeug.security` for safe storage.
  - Authentication ensures that no one else can view or alter a user’s personal academic data.

## Project Structure:
- `app.py`: The core file that powers the Flask application. It handles routing, user authentication, form processing, data handling with SQLAlchemy, and rendering templates.
- `templates/`: Contains HTML files for rendering the frontend pages. These templates manage the display of the GPA calculator, class schedule, assignments, and user login/registration pages.
- `static/`: Holds CSS and JavaScript files used to style the pages and enhance the client-side user experience.
- `requirements.txt`: A list of the Python dependencies required to run the app. It includes necessary libraries such as `Flask`, `Flask-SQLAlchemy`, and `Flask-Session`.
- `README.md`: This document that provides an overview of the project, its features, and instructions for setup and usage.

## Languages & Technologies Used:
- **Python**: The backend of the application is built using Python and the Flask web framework. It handles all the application logic, such as managing routes, processing user input, and interacting with the database.
- **SQLite**: The application uses SQLite as the database to store user data, assignments, class schedules, and other critical information. SQLAlchemy ORM is used for efficient database operations and management.
- **JavaScript**: Client-side scripting is used for interactive features like dynamic form validation, smooth transitions, and asynchronous updates to the UI.
- **HTML/CSS**: The frontend uses HTML for the structure and CSS for styling to create an intuitive and visually appealing user interface.
