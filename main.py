import requests
from bs4 import BeautifulSoup
import numpy as np
from logreg import LogisticRegression

nums = ((1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
        (19, 19),
        (20, 20),
        (21, 21),
        (22, 22),
        (23, 23),
        (24, 24),
        (31, 31),
        (34, 34),
        (38, 38),
        (41, 41),
        (42, 42),
        (43, 43),
        (45, 45),
        (47, 47),
        (48, 48),
        (51, 51),
        (18, 54),
        (77, 77),
        (78, 78),
        (99, 99))
yrs = tuple(yr for yr in range(2022, 2024))
types = {"Daytona": "ss",
        "Talladega": "ss",
        "Atlanta": "ss",
        "Sonoma": "rc",
        "Watkins Glen": "rc",
        "Charlotte Roval": "rc",
        "COTA": "rc",
        "Road America": "rc",
        "Indy Road Course": "rc",
        "Chicago Street": "rc",
        "Richmond": "s",
        "Phoenix": "s",
        "Martinsville": "s",
        "Charlotte": "s",
        "Texas": "s",
        "Kansas": "s",
        "Dover": "s",
        "Bristol": "s",
        "New Hampshire": "s",
        "Pocono": "s",
        "Las Vegas": "s",
        "Michigan": "s",
        "Atlanta": "s",
        "Darlington": "s",
        "California (Auto Club)": "s",
        "Homestead": "s",
        "Indianapolis": "s",
        "Nashville": "s",
        "Bristol Dirt": "s",
        "Gateway (WWT)": "s"}

testing = {}

# Initialize a 2D list to store the table data
training = []

for numset in nums:

    finishes = []
    ssfins = []
    rcfins = []
    sfins = []

    for ind in range(len(yrs)):
        num = numset[ind]
        yr = yrs[ind]
        url = "https://www.driveraverages.com/nascar/numberyear.php?carno_id=" + str(num) + "&yr_id=" + str(yr)

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")
            
        # Find the table containing the data
        table = soup.find("table")

        # Loop through each row in the table
        rownum = 0
        for row in table.find_all("tr"):
            if rownum < 5:
                rownum += 1
            else:
                cells = row.find_all(["th", "td"])
                index = cells[3].get_text(strip=True)
                if not index == "":
                    track = cells[5].get_text(strip=True)
                    type = types[track]

                    races = len(finishes)
                    finish = int(cells[6].get_text(strip=True))

                    if ind == len(yrs) - 1:
                        q1 = np.percentile(finishes, 25)
                        q2 = np.median(finishes)
                        q3 = np.percentile(finishes, 75)
                        start = int(cells[7].get_text(strip=True))
                        if type == "ss":
                            tq1 = np.percentile(ssfins, 25)
                            tq2 = np.median(ssfins)
                            tq3 = np.percentile(ssfins, 75)
                        if type == "rc":
                            tq1 = np.percentile(rcfins, 25)
                            tq2 = np.median(rcfins)
                            tq3 = np.percentile(rcfins, 75)
                        if type == "s":
                            tq1 = np.percentile(sfins, 25)
                            tq2 = np.median(sfins)
                            tq3 = np.percentile(sfins, 75)
                        training.append([start, q1, q2, q3, tq1, tq2, tq3, finish])


                    finishes.append(finish)
                    if type == "ss":
                        ssfins.append(finish)
                    if type == "rc":
                        rcfins.append(finish)
                    if type == "s":
                        sfins.append(finish)

                    if ind == len(yrs) - 1:
                        if num not in testing:
                            testing[num] = [None for i in range(12)]
                        driverfile = testing[num]
                        driverfile[0] = np.percentile(finishes, 25)
                        driverfile[1] = np.median(finishes)
                        driverfile[2] = np.percentile(finishes, 75)
                        driverfile[3] = np.percentile(ssfins, 25)
                        driverfile[4] = np.median(ssfins)
                        driverfile[5] = np.percentile(ssfins, 75)
                        driverfile[6] = np.percentile(rcfins, 25)
                        driverfile[7] = np.median(rcfins)
                        driverfile[8] = np.percentile(rcfins, 75)
                        driverfile[9] = np.percentile(sfins, 25)
                        driverfile[10] = np.median(sfins)
                        driverfile[11] = np.percentile(sfins, 75)
                        

# Splitting data into inputs and results
inputs = np.array(training)[:, :-1]
results = np.array(training)[:, -1]

while True:
    print("Driver Number:", end=" ")
    qnum = int(input())

    print("Starting Position:", end=" ")
    qstart = int(input())

    print("Track:", end=" ")
    track = input()
    qtype = types[track]

    driverfile = testing[qnum]

    q1 = driverfile[0]
    q2 = driverfile[1]
    q3 = driverfile[2]
    if qtype == "ss":
        tq1 = driverfile[3]
        tq2 = driverfile[4]
        tq3 = driverfile[5]
    if qtype == "rc":
        tq1 = driverfile[6]
        tq2 = driverfile[7]
        tq3 = driverfile[8]
    if qtype == "s":
        tq1 = driverfile[9]
        tq2 = driverfile[10]
        tq3 = driverfile[11]


    # New point to classify
    new_point = np.array([[qstart, q1, q2, q3, tq1, tq2, tq3]])

    for thr in range(1, 37):
        outputs = []
        for result in results:
            if result > thr:
                outputs.append(0)
            else:
                outputs.append(1)


        # Creating and training the Logistic Regression model
        model = LogisticRegression()
        model.fit(inputs, outputs)

        # Predicting the probability of each class for the new point
        prediction = model.predict(new_point)


        print("Probability of top " + str(thr) + ": " + str(np.round(prediction[0]*100, 2)) + "%")