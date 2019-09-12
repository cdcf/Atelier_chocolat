Atelier_chocolat
==================================================

I am designing and creating this app to follow my chocolate workshop productions, which is a bean-to-bar activity.
I can log all my various raw materials, suppliers, log in a (very) simplified way my purchases and the productions I am
running, with all intermediate stages I need (roasting, crushing / winnowing, grinding / conching, analysis, packing).

The app is currently under development, so please expect issues, bug, changes and so on. I am currently focusing on 
getting an app that works the way I expect in a first place, with minimal acceptable GUI, and if I can, I will improve
it to make it more sexy.

Note that all dev is done in English (tables, classes, templates etc.) however the GUI is in French - I will implement 
I18n and L10n features at a later stage.

Requirements
------------

- Python 3.7
- virtualenv (or venv if you are using Python 3.7)
- git

Setup
-----

**Step 1**: Clone the git repository

    $ git clone https://github.com/cdcf/Atelier_chocolat.git
    $ cd Atelier-chocolat

**Step 2**: Create a virtual environment and install all required framework, extensions and libraries

For Linux, OSX or any other platform that uses *bash* as command prompt (including Cygwin on Windows):

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

If you are using Python 3.x:

    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

For Windows users working on the standard command prompt:

    > virtualenv venv
    > venv\scripts\activate
    (venv) > pip install -r requirements.txt

**Step 3**: Run the initial database migration:

    (venv) $ export FLASK_APP=Atelier_chocolat.py
    (venv) $ flask db init
    (venv) $ flask db migrate -m "initial migration"
    (venv) $ flask db upgrade
     
**Step 4**: Start the application:

    (venv) $ flask run
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

Now open your web browser and type [http://localhost:5000](http://localhost:5000) in the address bar to see the
application running.
