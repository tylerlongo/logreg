Language: Python

Packages: Requests, Math, BeautifulSoup, NumPy, Matplotlib, PIL

This program is designed to predict NASCAR race results, using a logistic regression algorithm. To run the program, first execute getdata.py, which fetches data from driveraverages.com, analyzes it, and produces two txt files, training.txt and testing.txt. This takes just under two minutes on my laptop, but that may vary. The getdata program only needs to be executed once after each race (once a week from February to November), in order to load in all updated data. Next, run main.py. This program reads the txt files and trains a logistic regression model on the data, which takes about half a minute. 

Once that is complete, you'll be prompted to enter a car number in the terminal. The numbers currently in use by chartered teams are: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 31, 34, 38, 41, 42, 43, 45, 47, 48, 51, 54, 77, 99 (this list of numbers will be updated once more information becomes available about the 2024 season). Hit enter after typing in a number. Next, you will be prompted to enter a track type. The three options are S (speedway), SS (superspeedway), and RC (road course). After typing one of those three options, hit enter. 

A file named graph.png will be produced instantaneously, which visually depicts a distribution of probabilities of that driver's projected result. The numbers on the x-axis refer to finishing positions, and the numbers above the bars are probabilities. For example, if the number 50 appears above the 15 bar, then this means that the driver has a 50% chance of finishing 15th or better in the race. 

The graph also uses a viridis color gradient, where yellow/green bars indicate higher likelihoods than blue/purple bars. For example, if the 20 bar is yellow, then this driver is disproportionately likely to finish around 20th. 
