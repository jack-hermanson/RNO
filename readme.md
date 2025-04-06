# RNO Web Application

This is a Flask web application designed to facilitate
basic operations of a Denver Registered Neighborhood
Organization (RNO).

## Local Environment Setup

To get this up and running in a local development environment,
follow the steps below.

### Clone the Repository

I recommend using **GitHub Desktop** to manage git.
Clone this repository using GitHub Desktop to any
directory you choose.
I use a Mac, and the operating system has a special
`~/Developer` location that displays a little hammer
in the finder window, so I clone repos to that folder.

### Create the Virtual Environment

These instructions assume a Unix-like OS or shell.
Linux or Mac should work without modifications, but
Windows is a little different. If you're using Windows,
you might want to install **GitBash** or use the 
Windows Subsystem for Linux.

1. `cd` into the root of the project you just cloned.
If you `ls`, you should see this `readme.md` and know
you're in the right place.
2. Execute `python3 -m venv venv`.
3. Execute `source venv/bin/activate`.
4. Execute `python --version` and you should see 
`Python 3.13.1` or something similar.
5. Ensure that your shell now has `(venv)` or some
indication that you are working from the virtual environment.

### Install Server Dependencies

There is a `requirements.txt` file that lists the pip libraries
this application needs and what version of each to use. 
You will need to install the libraries listed in that file
into the virtual environment you just created.

1. Make sure your shell has `(venv)` or some virtual environment
indicator.
2. Execute `pip install -r requirements.txt`.

### Create a `.env` File

Each environment where this application runs relies on `.env`
files to set environment variables.
This file is not committed to source control because it may contain
a secret key, API keys, database passwords, etc.
Create your own by copying the example.

1. First, generate a key for this environment by running the following command:
```shell
node -e "console.log(require('crypto').randomBytes(48).toString('hex'))"
```

This will generate an unfathomably large, random hexadecimal number.
Copy the output to your clipboard. Mine was:

`dc06c03e68865d67c0a3a4a5c05eb287396bd02bc1fc644a35a87ff38e7478189951fac601af47bc0ccb59e6d40376e1`

2. Execute `cp .env.example .env`. Then edit that file to be something like this:

```dotenv
FLASK_APP=application
ENVIRONMENT=development
FLASK_DEBUG=1
TEMPLATES_AUTO_RELOAD=1
SECRET_KEY=dc06c03e68865d67c0a3a4a5c05eb287396bd02bc1fc644a35a87ff38e7478189951fac601af47bc0ccb59e6d40376e1
PORT=5030
LOG_LEVEL=DEBUG
RNO_NAME='Alamo Placita'
SQLALCHEMY_ECHO=0
```

### Database

Set up a local SQLite database. There are migrations that spell
out the structure of the database. 

Execute `python -m flask db upgrade`. A database should be created.

### Install Client Dependencies

Client dependencies are just JavaScript and CSS libraries
from npm. They are used in the end user's browser, not on our server.

1. Execute `cd application/web/static` to `cd` into the static directory.
2. Execute `ls` and make sure you see a package.json file.
3. Execute `npm --version` and make sure you get a response like 
`10.8.1`. If you do not have node/npm, install it using **Volta**.
4. Execute `npm install` or, if you want to be fancy, `npm i` works too.
5. `cd` back out to the project's root directory: `cd ../../../`.


### Run the Application

I recommend using an IDE like PyCharm so you can do debugging,
but the essential command for running the application is 
`python run.py`.

1. Execute `python run.py` if you haven't yet.
2. Go to the specified port in your browser.
3. Create an account for yourself with an easy password like "test".
4. Log in using that account and make sure that worked.

### Make Yourself a Super Admin

1. Execute `sqlite3 instance/site.db`. A SQL console will appear.
2. Execute `UPDATE account SET clearance = 5;`
3. Refresh the page and you should see more menus now.

