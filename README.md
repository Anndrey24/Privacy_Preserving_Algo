# Privacy Preserving Billing and Settlements in Local Energy Markets
This code repository was created to support my 3<sup>rd</sup> Year Project / Dissertation for a BSc Computer Science degree at The University of Manchester.

## Project Description
This project aims to implement a novel privacy-preserving billing and settlements protocol, PPBSP, for use in local energy markets with imperfect bid-offer fulfillment, which only uses homomorphically encrypted versions of the users’ half-hourly consumption data using Python and the python-paillier library.   
In addition, PPBSP also supports various cost-sharing mechanisms among market participants, including two new and improved methods of proportionally redistributing the cost of maintaining the balance of the electrical grid in a fair and intuitive manner.

## Installation and Dependencies
This project requires Python and the python-paillier library. To install python-paillier, use the following command:  
```pip install phe```

## Usage
To use the PPBSP protocol, run the `main.py` script. This script will run a simulation of the local energy market billing and settlements procedure according to the parameters defined within the same file. These parameters are:  
- number of suppliers
- number of users
- number of trading slots  

The subsequent output includes a comparison of the 4 billing models' runtimes and energy supplier profits.

## Project Structure
The project has the following file structure:
- `main.py`: This is the main script that runs the PPBSP simulation.
- `TradingPlatform.py`: This file contains the TradingPlatform object, implementing 4 different billing algorithms.
- `User.py`: This file contains the implementation of the User object.
- `Supplier.py`: This file contains the implementation of the Supplier object.
- `GridOperator.py`: This file contains the implementation of the GridOperator object.
- `phe_tests.py`: This is the script used for measuring the execution time of various operations from the python-paillier library.
- `trading_sim.py`: This file illustrates the basic principle behind the settlements procedure.
- `README.md`: This is the project's README file.

## Acknowledgements
I would like to thank my supervisor, Dr. Mustafa A. Mustafa, who provided continuous counsel and guidance during the entirety of my project’s timeline, and whose consistent weekly availability meant my burning questions never went unanswered for long. I also wish to acknowledge the contributions of the python-paillier open source community.



