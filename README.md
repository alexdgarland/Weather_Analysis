Weather Analysis
===========================

Sample ETL/ analysis application written using Python, PostgreSQL and Pentaho DI.  Very much a work in progress!

Using publically-available data from the University of Edinburgh School of Geosciences:
http://www.geos.ed.ac.uk/Weathercam/station/data.html


Installation
===========================

All code should run okay on both Windows and Linux (tested on Windows 7, Centos and Fedora).

As of my last update, the solution is not complete - but if you do want to give what there is of it a try, follow the steps below:

1)  Install Postgres (see http://www.postgresql.org/download/).  My development version is 9.3; the solution may work on earlier versions but I make no guarantees, I think there may be at least one bit of recently added syntax used (so requiring alteration for <=9.2).

2)  Set up users.
At minimum, you'll want an admin-level account to set up the database.
As this is not a production app it is possible to run ETL and application code using the admin account, but if you want to add separate, less-privileged accounts for this, it is supported by the configuration options.
Unless you want to drill into object permissions in detail, just set it so account(s) can read and write data to any table/ view and execute any function/ procedure in the database created in step 3 (you obviously may need to create it first!) but not alter the schema.

3)  Create a new database for storing and processing weather data.

4)  Run [the database set-up script](source/SQL/Postgres create weather data tables.sql) against the new database.
    
Note that at this point I'm assuming the script is run once to set up the database from scratch; if run against a populated database, tables will be dropped and recreated with resulting data loss.  I'm going to have a look at open-source options for schema control and comparison (similar to Microsoft Visual Studio Database Projects) in due course.

5)  Install Pentaho Community Edition - Data Integration ("Kettle") - http://community.pentaho.com/.

6)  Add the following settings to the Kettle config file (<user home directory>/.kettle/kettle.properties):

    WEATHERDBHOST       The name of the server the Postgres instance is running on.  Typically this will just be localhost.
    WEATHERDBNAME       The name of the Postgres database created in step 3.
    WEATHERDBPORT       The port Postgres is running on - unless you've explictly changed it, it will be the default (5432).
    WEATHERDBUSER       The name of the Postgres user account for running ETL jobs.
    WEATHERDBPASSWORD   The password for the above user account.
        
An example file is provided in this repo [here](sample_config/kettle.properties.SAMPLE).
    
7)  If you don't already have Python installed, pick the latest version of Python 2 or Python 3 from (e.g.) https://www.python.org/downloads/.

All code has been tested on Python 2.6 and at least one version of  Python 3.
For the analytical code (not written as of 02/01/2015 but planned), it's worth downloading the (free) "Anaconda" distribution from Continuum Analytics (https://store.continuum.io/cshop/anaconda/) instead of/ as well as the basic Python distro.  Note that both are running the standard "CPython" reference implementation, but Anaconda comes with a lot of additional 3rd-party libraries pre-installed plus some good GUI tools.

8) Install psycopg2 (a PostgreSQL driver module for Python).  See [here](http://initd.org/psycopg/docs/install.html) for instructions.  I found that on Windows, using easy_install (Python package manager) resulted in a version which didn't work due to DLL issues, so I would recommeng getting an .exe installer from [here](http://www.stickpeople.com/projects/python/win-psycopg/).

9)  Pick a secure directory for Python config (e.g. add new folder "Python_Config" under your user home directory).  Add a user- or machine-level environment variable called "PythonAppConfigFolder" with the value being the full path of this folder, so the Python code can find it.

10)  Create a new text file called "PostgresConnection.cfg" and add the following settings, using a layout readable by the Python ConfigParser library (see https://docs.python.org/2/library/configparser.html):

    server->
        host:           The name of the server the Postgres instance is running on.  Typically this will just be localhost.
    server->
        port:           The port Postgres is running on - unless you've explictly changed it, it will be the default (5432).
    credentials->
        user:           The name of the Postgres user account for accessing from Python scripts - may well be the same account as for running ETL jobs.
    credentials->
        password:       The password for the above user account.
    weatheranalysis->
        database_name:  The name of the Postgres database created in step 3.
 
An example file is provided in this repo [here](sample_config/PostgresConnection.cfg.SAMPLE).


    
10) ****************    FURTHER INSTRUCTIONS TO FOLLOW    ****************


