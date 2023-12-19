import requests
import math
from bs4 import BeautifulSoup
import numpy as np

nums = ((2022, '2', '2'),
        (2022, '3', '3'),
        (2022, '4', '4'),
        (2022, '5', '5'),
        (2022, '6', '6'),
        (2022, '7', '7'),
        (2022, '8', '8'),
        (2022, '9', '9'),
        (2022, '10', '10'),
        (2022, '11', '11'),
        (2022, '12', '12'),
        (2022, '14', '14'),
        (2022, '15', '15'),
        (2022, '17', '17'),
        (2022, '18', '18'),
        (2022, '19', '19'),
        (2022, '20', '20'),
        (2022, '21', '21'),
        (2022, '22', '22'),
        (2022, '23', '23'),
        (2022, '24', '24'),
        (2022, '34', '34'),
        (2022, '38', '38'),
        (2022, '41', '41'),
        (2022, '43', '43'),
        (2022, '47', '47'),
        (2022, '48', '48'),
        (2022, '51', '51'),
        (2022, '77', '77'),
        (2022, '78', '78'),
        (2022, '99', '99'),
        (2023, '1', '1'),
        (2023, '2', '2'),
        (2023, '3', '3'),
        (2023, '4', '4'),
        (2023, '5', '5'),
        (2023, '6', '6'),
        (2023, '7', '7'),
        (2023, '8', '8'),
        (2023, '9', '9'),
        (2023, '10', '10'),
        (2023, '11', '11'),
        (2023, '12', '12'),
        (2023, '14', '14'),
        (2023, '15', '15'),
        (2023, '16', '16'),
        (2023, '17', '17'),
        (2023, '19', '19'),
        (2023, '20', '20'),
        (2023, '21', '21'),
        (2023, '22', '22'),
        (2023, '23', '23'),
        (2023, '24', '24'),
        (2023, '31', '31'),
        (2023, '34', '34'),
        (2023, '38', '38'),
        (2023, '41', '41'),
        (2023, '42', '42'),
        (2023, '43', '43'),
        (2023, '45', '45'),
        (2023, '47', '47'),
        (2023, '48', '48'),
        (2023, '51', '51'),
        (2023, '18', '54'),
        (2023, '77', '77'),
        (2023, '78', '78'),
        (2023, '99', '99'))
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
        "Daytona Road Course": "rc",
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
        "Gateway (WWT)": "s",
        "Kentucky": "s"}

training = []

testing = {}

for numset in nums:

    finishes = []
    ssfins = []
    rcfins = []
    sfins = []

    for ind in (1, 2):
        num = numset[ind]
        yr = numset[0] + ind - 2
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
                week = cells[3].get_text(strip=True)
                if not week == "":
                    week = int(week)
                    uweek = math.ceil(week/6)
                    regweek = math.ceil(week/1.5)

                    track = cells[5].get_text(strip=True)
                    type = types[track]

                    races = len(finishes)
                    finish = int(cells[6].get_text(strip=True))

                    if ind == 2:

                        last = np.percentile(finishes[:-week], 25)
                        cur = np.percentile(finishes[-week:], 25)
                        ovrq = round(cur * week/36 + last * (36-week)/36, 2)

                        last = np.median(finishes[:-week])
                        cur = np.median(finishes[-week:])
                        ovrm = round(cur * week/36 + last * (36-week)/36, 2)

                        if type == "ss":
                            last = np.percentile(ssfins[:-uweek], 25)
                            cur = np.percentile(ssfins[-uweek:], 25)
                            tq = round(cur * week/36 + last * (36-week)/36, 2)

                            last = np.median(ssfins[:-uweek])
                            cur = np.median(ssfins[-uweek:])
                            tm = round(cur * week/36 + last * (36-week)/36, 2)

                            ss = 1
                        elif type == "rc":
                            last = np.percentile(rcfins[:-uweek], 25)
                            cur = np.percentile(rcfins[-uweek:], 25)
                            tq = round(cur * week/36 + last * (36-week)/36, 2)

                            last = np.median(rcfins[:-uweek])
                            cur = np.median(rcfins[-uweek:])
                            tm = round(cur * week/36 + last * (36-week)/36, 2)

                            ss = 0
                        else:
                            last = np.percentile(sfins[:-regweek], 25)
                            cur = np.percentile(sfins[-regweek:], 25)
                            tq = round(cur * week/36 + last * (36-week)/36, 2)

                            last = np.median(sfins[:-regweek])
                            cur = np.median(sfins[-regweek:])
                            tm = round(cur * week/36 + last * (36-week)/36, 2)

                            ss = 0
                        training.append([num, yr, week, track, ovrq, ovrm, tq, tm, ss, 36, finish])

                    finishes.append(finish)
                    if type == "ss":
                        ssfins.append(finish)
                    elif type == "rc":
                        rcfins.append(finish)
                    else:
                        sfins.append(finish)

                    if yr == 2023:
                        if num not in testing:
                            testing[num] = [None for i in range(8)]
                        driverfile = testing[num]

                        last = np.percentile(finishes[:-week], 25)
                        cur = np.percentile(finishes[-week:], 25)
                        driverfile[0] = cur * week/36 + last * (36-week)/36

                        last = np.median(finishes[:-week])
                        cur = np.median(finishes[-week:])
                        driverfile[1] = cur * week/36 + last * (36-week)/36

                        last = np.percentile(ssfins[:-uweek], 25)
                        cur = np.percentile(ssfins[-uweek:], 25)
                        driverfile[2] = cur * week/36 + last * (36-week)/36

                        last = np.median(ssfins[:-uweek])
                        cur = np.median(ssfins[-uweek:])
                        driverfile[3] = cur * week/36 + last * (36-week)/36

                        last = np.percentile(rcfins[:-uweek], 25)
                        cur = np.percentile(rcfins[-uweek:], 25)
                        driverfile[4] = cur * week/36 + last * (36-week)/36

                        last = np.median(rcfins[:-uweek])
                        cur = np.median(rcfins[-uweek:])
                        driverfile[5] = cur * week/36 + last * (36-week)/36

                        last = np.percentile(sfins[:-regweek], 25)
                        cur = np.percentile(sfins[-regweek:], 25)
                        driverfile[6] = cur * week/36 + last * (36-week)/36

                        last = np.median(sfins[:-regweek])
                        cur = np.median(sfins[-regweek:])
                        driverfile[7] = cur * week/36 + last * (36-week)/36

# Write the data to the text file
with open('training.txt', 'w') as file:
    for innerlist in training:
        # Join the elements in the inner list with commas and write to the file
        line = ', '.join(map(str, innerlist)) + '\n'
        file.write(line)

# Write the data to the text file
with open('testing.txt', 'w') as file:
    for key, value in testing.items():
        # Write key and values to the file in the desired format
        line = f"{key}: {', '.join(map(str, value))}\n"
        file.write(line)