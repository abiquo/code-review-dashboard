Code review dashboard
=====================

A dashboard to see the status of all opened pull requests.

* **Cold** pull requests are the ones where no one has given a +1.
* **Hot!** ones are those that are waiting for the last +1 to be merged.
* **Burning** pull requests are those that are ready to be merged.

Requirements
------------

The dashboard uses [Flask](http://flask.pocoo.org/docs/) and [Requests](http://python-requests.org).
You can install them using [Pip](http://www.pip-installer.org) as follows:

    pip install Flask requests

If you don't have *pip* installed, you can install it following the instructions found in the site. It can
be installed in a virtualenv or in the core system. Here is how you can install it in your system. Installing
it into a virtualenv should be the same, once it has been activated:

    # Install setuptools
    wget https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg#md5=fe1f997bc722265116870bc7919059ea
    sudo sh sh setuptools-0.6c9-py2.4.egg

    # Install pip
    curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    sudo python get-pip.py

Running
-------

Once you have installed the requirements you can run the dashboard as follows:

    python application.py

Deploying to Heroku
-------------------

The application can also be deployed to Heroku. To deploy it you just have to create the application
and deploy it as follows:

    # Create and configure the Heroku application
    heroku create <application name>

    # Deploy the application
    git push heroku master

