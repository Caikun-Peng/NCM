# Flask

This is the project structure for Flask App.

## Project Structure

``` markdown
flask/
├── app.py                     # The main application file containing the Flask app and routes.
├── templates/                 # Directory containing HTML templates.
│   ├── login.html             # Template for the login page.
│   ├── home.html              # Template for the home page.
│   └── switch_pages/          # Directory containing dynamically created switch pages.
│       ├── cell-1/            # Directory for switch 1 containing its related HTML files.
│       │   ├── switch.html    # cell page for switch 1.
│       │   ├── host-1.html    # Host 1 page for switch 1.
│       │   ├── host-2.html    # Host 2 page for switch 1.
│       │   └── ...  
│       ├── cell-2/            # Directory for switch 2 containing its related HTML files.
│       │   ├── switch.html    # cell page for switch 2.
│       │   ├── host-1.html    # Host 1 page for switch 2.
│       │   ├── host-2.html    # Host 2 page for switch 2.
│       │   └── ...
│       └── ...
...
```
