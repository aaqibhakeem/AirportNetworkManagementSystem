# AirOptima
Explore AirOptima as it reimagines air travel, blending technology with aviation to elevate the efficiency and safety of our skies. By harmonizing airspace dynamics, it brings an innovative approach to route planning, making modern aviation more sustainable and resilient.

## Features
* Seamlessly integrated operations for managing data on airports, flights, and routes.
* Advanced route optimization algorithms designed for precise and efficient flight path planning.
* Comprehensive flight tracking to monitor aircraft locations and statuses.
* Interactive visualization interface for user-friendly data presentation and system navigation.
* Robust MySQL database integration ensuring secure and scalable data storage solutions.


### Prerequisites

1. **Python** for running the project. 

2. **MySQL** to store data about flights, routes, airports and airlines.


### To run this project locally
1. Install [python](https://www.python.org/downloads/).
2. Create a local [MySQL](https://dev.mysql.com/downloads/workbench/) instance.
3. Clone this repository and install the required packages using `requirements.txt` file.

```
git clone https://github.com/aaqibhakeem/AirportNetworkManagementSystem.git
pip install -r requirements.txt
```

4. Initialize your MySQL instance and create a new database `CREATE DATABASE <database_name>`. Setup tables in the database afterward.

```
cd setup
python dbsetup.py
```

5. Change the fields in the `dbdetails.py` file.
```
    host="<hostname>",             # Replace with your MySQL host
    user="<username>",             # Replace with your MySQL user
    password="<password>",         # Replace with your MySQL password
    database="<database_name>"     # Replace with your MySQL database name
```

6. Go back to the repository directory and run `python main.py` in the terminal with the project.  


## Built With

- [MySQL](https://www.mysql.com/) - MySQL is an open-source relational database management system.
- [PySide6](https://doc.qt.io/qtforpython-6/) - The set of Python bindings for the Qt 6 application framework, enabling the creation of cross-platform GUIs.
- [NetworkX](https://networkx.org/) - The Python library designed for creating, analyzing, and visualizing complex networks.
- [Plotly](https://plotly.com/) - The graphing library for Python that enables the creation of interactive visualizations.
- [Pandas](https://pandas.pydata.org/) - The Python library for data manipulation and analysis, primarily used for structured data.
