Meridian Hospital — Appointments Dashboard

A single-page hospital appointment management dashboard built with HTML, CSS, and vanilla JavaScript. The application provides a browser-based interface for managing doctors, patients, and appointments, with dashboard statistics and interactive charts.

Features

Dashboard — Displays total doctors, total patients, total appointments, and today's appointments.

Upcoming Appointments — Shows the next scheduled appointments in a compact queue.

Appointment Analytics — Includes a 7-day appointment trend, appointment status breakdown, and appointments by specialization.

Doctor Management — Add and remove doctors with their specialization.

Patient Management — Add and remove patients with age, gender, and phone details.

Appointment Management — Book appointments between patients and doctors and set appointment status to Scheduled, Completed, or Cancelled.

Cascading Deletes — Removing a doctor or patient also removes their associated appointments.

Persistent Data — Uses browser localStorage so data remains available after refreshing the page.

Responsive Design — Layout adapts to smaller screens using CSS media queries.

Tech Stack

HTML5 — Page structure and application markup

CSS3 — Layout, styling, responsive design, and UI components

JavaScript — Application logic, navigation, CRUD operations, validation, and dashboard rendering

Chart.js 4.4.0 — Interactive charts and data visualization

localStorage — Client-side data persistence

Dashboard

The dashboard provides an overview of the hospital's appointment activity through:

Total doctors

Total patients

Total appointments

Today's appointments

Upcoming scheduled appointments

Appointments over the last 7 days

Appointment status distribution

Appointments grouped by doctor specialization

Data Management

The application maintains three main data collections:

Doctors
Patients
Appointments

Appointments connect a patient with a doctor using their IDs.

Data is stored in the browser using:

localStorage

The application also includes initial seed data so the dashboard contains sample doctors, patients, and appointments when opened for the first time.

Running the Project

No installation or build process is required.

1. Clone the repository

git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>

2. Open the application

Open hospital-dashboard.html directly in your browser.

Alternatively, use the Live Server extension in VS Code for local development.

Project Structure

meridian-hospital/
│
├── hospital-dashboard.html    # Complete dashboard application
└── README.md                  # Project documentation

The current implementation keeps the HTML, CSS, and JavaScript in a single HTML file for a simple zero-install setup.

Design & Architecture

The project separates its responsibilities inside the single-page application:

Data layer — DB, loadData(), and saveData() manage application data and localStorage persistence.

Rendering layer — Functions such as renderDashboard(), renderDoctors(), renderPatients(), and renderAppointments() update the interface.

Navigation — Dashboard, Appointments, Doctors, and Patients are handled as separate views within the same page.

Validation — Forms check required fields before creating records.

Relationship handling — Appointments reference doctors and patients through IDs.

Cascade behavior — Deleting a doctor or patient automatically removes related appointments.

Charts

The dashboard uses Chart.js to generate three visualizations:

Appointments, last 7 days — Line chart showing appointment volume by day.

Status breakdown — Doughnut chart showing Scheduled, Completed, and Cancelled appointments.

Appointments by specialization — Bar chart showing appointment load across medical specializations.

Sample Data

The application starts with sample records including:

Two doctors

Two patients

Two appointments

This allows the dashboard and charts to display meaningful information immediately after opening the application.

Limitations

This is a frontend-only application, so:

Data is stored only in the current browser.

Data does not synchronize between devices.

Multiple users cannot access a shared database.

Clearing browser storage removes the saved application data.

There is no authentication or role-based access control.

There is no backend server or cloud database.

Future Improvements

Possible improvements include:

Add a Python/Flask or Node.js backend.

Replace localStorage with SQLite, MySQL, or PostgreSQL.

Add user authentication and role-based access.

Add doctor availability and scheduling conflict detection.

Add appointment search and filtering.

Add patient history and medical records.

Add export functionality for reports.

Deploy the dashboard using GitHub Pages or another hosting platform.

Author

Himanshu Sharma

Computer Science & Engineering Student

Interested in AI/ML, Software Development, Web Development, and Programming.

License

This project is free to use, modify, and share.
