# RA Management Suit

The RA Management Suite is a comprehensive platform tailored to the unique demands of Resident Assistants and their coordinators. It seamlessly integrates essential modules such as a calendar and scheduling system to ensure there's always an RA on duty, without hampering their academic commitments. Additionally, it supports event planning and management, and boasts a logging page for vital announcements.


## Installation 

The Installation instructions are assuming you are using a terminal in a virtual environment with Python 3.11.5 and are able to use pip to install packages.  
1. To start `cd` into the directory you want the project.
2. Clone the repo: 
    ```console
    git clone https://git.cs.usask.ca/vhp437/cmpt370-project.git
    ```
3. Go into the project directory: 
    ```console
    cd ./cmpt370-project
    ```
4. Install required packages: 
    ```console
    pip install -r requirements.txt
    ```

## Running Program

After proper installation you should be able to run the project by running:   
```console
python RAManagementSuite
 ```   
The expected output should look like: 
```console
 * Serving Flask app '__init__'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
Open a browser and go to the link returned (http://127.0.0.1:5000 for the example above)  
There are some pre-made accounts for initial setup all using "password" as their password
* coordinator@test.com
* senior@test.com
* returner@test.com
* basic@test.com

