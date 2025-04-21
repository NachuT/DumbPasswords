# Dumb Passwords

Full-Stack Application that puts your password manager into a gesture based program.

## How this Works?
Uses Supabase for the server, Flask and Python for the backend, and Mediapipe with plain Html, CSS and JS for the Frontend. The Supabase right now contains all stored passwords and login credentials with the Flask API providing a connection for the frontend to use.

## How to run this?
1. Get Supabase by running SQL code in `server.sql` the SQL editor
2. Get all enviornment variables and run
   `pip3 install -r requirements.txt` and then `python3 main.py` (this should be on port 3000)
3. Run the website - I prefer `python3 -m http.server 8000`
View Demo Here: [Video](https://www.youtube.com/watch?v=TFRzPojy2UM)
