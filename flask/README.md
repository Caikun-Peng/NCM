# My Flask App

This is the project structure for My Flask App.

## Project Structure

## Description

- `app.py`: The main application file containing the Flask app and routes.
- `templates/`: Directory containing HTML templates.
  - `login.html`: Template for the login page.
  - `home.html`: Template for the home page.
  - `switch_pages/`: Directory containing dynamically created switch pages.
    - `switch1/`: Directory for switch 1 containing its related HTML files.
      - `switch.html`: Template for switch 1.
      - `host1_action.html`: Host 1 action page for switch 1.
      - `host2_action.html`: Host 2 action page for switch 1.
    - `switch2/`: Directory for switch 2 containing its related HTML files.
      - `switch.html`: Template for switch 2.
      - `host1_action.html`: Host 1 action page for switch 2.
      - `host2_action.html`: Host 2 action page for switch 2.

my_flask_app/
│
├── app.py
├── templates/
│   ├── login.html
│   ├── home.html
│   └── switch_pages/
│       ├── switch1/
│       │   ├── switch.html
│       │   ├── host1_action.html
│       │   ├── host2_action.html
│       │   └── ...
│       ├── switch2/
│       │   ├── switch.html
│       │   ├── host1_action.html
│       │   ├── host2_action.html
│       │   └── ...
│       └── ...

