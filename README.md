# Talk With Me

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Installation and Setup](#installation-and-setup)
  - [Prerequisites](#prerequisites)
  - [Steps to Set Up](#steps-to-set-up)
- [How to Use the App](#how-to-use-the-app)
- [Features](#features)
- [Demo](#demo)
- [Future Plans](#future-plans)
- [Contributors](#contributors)

## Overview
**Talk With Me** is a web-based application that provides users with a platform to share their stories, experiences, and feelings anonymously. It is designed to be a space for people to express themselves freely and find comfort through storytelling.

## Technologies Used
- **Flask**: Web framework for backend logic.
- **SQLAlchemy**: ORM for handling database operations.
- **SQLite**: Database used to store user information and stories.
- **Bootstrap 5.3**: For responsive and modern UI/UX design.

## Installation and Setup

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- pip (Python package manager)
- virtualenv (optional, but recommended for creating isolated environments)

### Steps to Set Up
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/vapeasnl/talk-with-me.git
   cd talk-with-me
   ```

2. **Create a Virtual Environment (Optional):**
   ```bash
   python3 -m venv venv
   ```

3. **Install Dependencies:**
   Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   Start the development server using Flask:
   ```bash
   flask run
   ```

   This will start the server, and you can view the application by visiting [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

5. **Set Up the Demo Database (Optional):**
    Run the following command to populate the SQLite database for a demo:
   ```bash
   sqlite3 instance/hate.db < scriptdemo.sql
   ```



## How to Use the App
1. **Register/Login:**
   - New users can register by providing an email and password.
   - Existing users can log in to access their accounts.

2. **Share Your Story:**
   - Once logged in, users can submit their own stories anonymously by clicking on “Add a Story.”

3. **Browse Stories:**
   - You can view the most recent stories, top-rated stories, or explore random entries.

4. **Search:**
   - Users can search for specific stories using keywords.

5. **Logout:**
   - You can log out by clicking on the “Log out” button in the navigation bar.

## Features
- **Anonymous Story Sharing**: Users can share their stories without revealing their identity.
- **Story Browsing**: Browse through stories from other users, categorized by newest, top-rated, or random.
- **Responsive Design**: The UI is designed to work across various devices using Bootstrap 5.3.

---

## Demo

[https://www.youtube.com/watch?v=C1nDL7GRhUY](https://www.youtube.com/watch?v=C1nDL7GRhUY)

## Future Plans
- **Moderation:** Tools to moderate and filter inappropriate content.

## Contributors
- **Salim Abdessamad**
- **Ahmed Sahbeddine**

