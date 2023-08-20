import requests
from bs4 import BeautifulSoup
import numpy as np
from logreg import LogisticRegression

# Initialize a 2D list to store the table data
data = []

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 31, 34, 38, 41, 42, 43, 45, 47, 48, 51, 77, 78, 99]
yrs = [yr for yr in range(2022, 2024)]
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


print("Driver Number:", end=" ")
qnum = int(input())

print("Starting Position:", end=" ")
qstart = int(input())

print("Track:", end=" ")
track = input()
qtype = types[track]

print("Threshold:", end=" ")
qthr = int(input())


for num in nums:

    finishes = []
    ssfins = []
    rcfins = []
    sfins = []

    for yr in yrs:
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

                    if yr == 2023:
                        q = np.percentile(finishes, 25)
                        m = np.median(finishes)
                        week = []
                        start = int(cells[7].get_text(strip=True))
                        week.append(start)
                        week.append(q)
                        week.append(m)
                        if type == "ss":
                            tq = np.percentile(ssfins, 25)
                            tm = np.median(ssfins)
                        if type == "rc":
                            tq = np.percentile(rcfins, 25)
                            tm = np.median(rcfins)
                        if type == "s":
                            tq = np.percentile(sfins, 25)
                            tm = np.median(sfins)
                        week.append(tq)
                        week.append(tm)
                        week.append(finish)
                        data.append(week)

                    finishes.append(finish)
                    if type == "ss":
                        ssfins.append(finish)
                    if type == "rc":
                        rcfins.append(finish)
                    if type == "s":
                        sfins.append(finish)
    if num == qnum:
        qq = np.percentile(finishes, 25)
        qm = np.median(finishes)
        if qtype == "ss":
            qtq = np.percentile(ssfins, 25)
            qtm = np.median(ssfins)
        if qtype == "rc":
            qtq = np.percentile(rcfins, 25)
            qtm = np.median(rcfins)
        if qtype == "s":
            qtq = np.percentile(sfins, 25)
            qtm = np.median(sfins)


# Splitting data into features (X) and labels (y)
inputs = np.array(data)[:, :-1]
results = np.array(data)[:, -1]
outputs = []
for result in results:
    if result > qthr:
        outputs.append(0)
    else:
        outputs.append(1)


# Creating and training the Logistic Regression model
model = LogisticRegression()
model.fit(inputs, outputs)


# New point to classify
new_point = np.array([[qstart, qq, qm, qtq, qtm]])

# Predicting the probability of each class for the new point
prediction = model.predict_prob(new_point)

print("Probability of top " + str(qthr) + ": " + str(np.round(prediction[0]*100, 2)) + "%")