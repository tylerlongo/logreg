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

print("******************************")
print("training AI algorithm", end=" ", flush=True)

for numset in nums:

    finishes = []
    ssfins = []
    rcfins = []
    sfins = []
    print(".", end=" ", flush=True)

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
                        q = np.percentile(finishes, 25)
                        m = np.median(finishes)
                        start = int(cells[7].get_text(strip=True))
                        if type == "ss":
                            tq = np.percentile(ssfins, 25)
                            tm = np.median(ssfins)
                            ss = 1
                        elif type == "rc":
                            tq = np.percentile(rcfins, 25)
                            tm = np.median(rcfins)
                            ss = 0
                        else:
                            tq = np.percentile(sfins, 25)
                            tm = np.median(sfins)
                            ss = 0
                        training.append([start, q, m, tq, tm, ss, finish])


                    finishes.append(finish)
                    if type == "ss":
                        ssfins.append(finish)
                    elif type == "rc":
                        rcfins.append(finish)
                    else:
                        sfins.append(finish)

                    if ind == len(yrs) - 1:
                        if num not in testing:
                            testing[num] = [None for i in range(8)]
                        driverfile = testing[num]
                        driverfile[0] = np.percentile(finishes, 25)
                        driverfile[1] = np.median(finishes)
                        driverfile[2] = np.percentile(ssfins, 25)
                        driverfile[3] = np.median(ssfins)
                        driverfile[4] = np.percentile(rcfins, 25)
                        driverfile[5] = np.median(rcfins)
                        driverfile[6] = np.percentile(sfins, 25)
                        driverfile[7] = np.median(sfins)

# Splitting data into inputs and results
inputs = np.array(training)[:, :-1]
results = np.array(training)[:, -1]

print("")

while True:
    print("******************************")

    print("Driver Number:", end=" ")
    qnum = int(input())

    print("Starting Position:", end=" ")
    qstart = int(input())

    print("Track:", end=" ")
    track = input()
    qtype = types[track]

    driverfile = testing[qnum]

    qq = driverfile[0]
    qm = driverfile[1]
    if qtype == "ss":
        qtq = driverfile[2]
        qtm = driverfile[3]
        ss = 1
    if qtype == "rc":
        qtq = driverfile[4]
        qtm = driverfile[5]
        ss = 0
    if qtype == "s":
        qtq = driverfile[6]
        qtm = driverfile[7]
        ss = 0


    # New point to classify
    new_point = np.array([[qstart, qq, qm, qtq, qtm, ss]])

    thrs = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 36, 37, 38, 39, 40]
    for thr in thrs:
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