.. image:: https://travis-ci.org/brennv/palette.svg?branch=master
    :target: https://travis-ci.org/brennv/palette


===============================
palette
===============================

A palette flask app for templating.

Preview the app on Heroku_.

Features:

- user login and authentication
- mobile friendly
- customizable styling


Quickstart
----------

Run the following commands to bootstrap your environment ::

    git clone https://github.com/brennv/palette
    cd palette
    source env.sh
    flask run

You will see a pretty welcome screen.

To update and populate the database run ::

    flask db migrate
    flask db upgrade
    flask data


Deployment
----------

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``, so that ``ProdConfig`` is used. Also
change the secrets in ``keys.sh``.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
-------------

To run all tests, run ::

    flask test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.


Powermode
----------

To hot reload tests and migrations run ::

    flask powermode


Origins
----------

cookiecutter-flask_


.. _Heroku: https://calm-brushlands-54236.herokuapp.com/
.. _cookiecutter-flask: https://github.com/sloria/cookiecutter-flask
