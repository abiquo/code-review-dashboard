Code review dashboard
=====================

A dashboard to see the status of all opened pull requests.

Requirements
------------

The dashboard requires a few dependencies to be installed. To make the process easier, it is
recommended to install them as follows:

    # Install setuptools
    wget https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg#md5=fe1f997bc722265116870bc7919059ea
    sudo sh sh setuptools-0.6c9-py2.4.egg

    # Install pip
    curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    sudo python get-pip.py

    # Install the dependencies
    sudo pip install Flask


Before using it, you will need to create a [Github Api Token](https://github.com/blog/1509-personal-api-tokens)
and configure it in the `ABQ_REVIEW_TOKEN` environment variable.

Once you have the token configured you can run the dashboard as follows:

    python application.py
