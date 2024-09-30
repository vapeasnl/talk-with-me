# Talk With Me

## Overview
**Talk With Me** is a web-based application that provides users with a platform to share their stories, experiences, and feelings anonymously. It is designed to be a space for people to express themselves freely and find comfort through storytelling.

The app was inspired by a personal experience of our developer, Salim Abdessamad, who went through a difficult period of financial hardship and depression. During that time, the need to talk and share his feelings led to the idea of creating this app.

## Technologies Used
- **Flask**: Web framework for backend logic.
- **SQLAlchemy**: ORM for handling database operations.
- **SQLite**: Database used to store user information and stories.
- **Bootstrap 4**: For responsive and modern UI/UX design.
- **Jinja2**: Templating engine to render dynamic web pages.

## Installation and Setup
Follow the steps below to get the app running on your local machine.

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

2. **Create a Virtual Environment (Optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**
   Run the following command to create the SQLite database:
   ```bash
   sqlite3 hate.db
   .read scriptdemo.sql
   ```

5. **Run the Application:**
   Start the development server using Flask:
   ```bash
   export FLASK_APP=application.py
   flask run
   ```

   This will start the server, and you can view the application by visiting [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

### Running with Docker (Optional)
If you'd prefer to run the application in a Docker container:
1. Ensure Docker is installed on your machine.
2. Build the Docker image:
   ```bash
   docker build -t talk-with-me .
   ```
3. Run the Docker container:
   ```bash
   docker run -d -p 5000:5000 talk-with-me
   ```

Now you can access the app via [http://localhost:5000](http://localhost:5000).

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
- **Responsive Design**: The UI is designed to work across various devices using Bootstrap 4.

## Known Issues
- Users must be logged in to add stories.
- The app is not yet fully optimized for large-scale use.

## Future Plans
- **Commenting System**: Allow users to leave comments on stories.
- **User Profiles**: Implement basic profiles for users to keep track of their stories.
- **Improved Moderation**: Tools to moderate and filter inappropriate content.
  
## Contributing
We welcome contributions to improve **Talk With Me**. To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`) and push to the branch (`git push origin feature-name`).
4. Open a pull request, and we’ll review it.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors
- **Salim Abdessamad** - Developer
- **Ahmed Sahbeddine** - Developer

---

Thank you for using Talk With Me. If you have any questions or would like to contribute, feel free to reach out or submit a pull request!
