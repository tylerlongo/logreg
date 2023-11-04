import requests
from bs4 import BeautifulSoup
import numpy as np
from logreg import LogisticRegression
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from PIL import Image

nums = ((2021, 2, 2),
        (2021, 3, 3),
        (2021, 4, 4),
        (2021, 5, 5),
        (2021, 6, 6),
        (2021, 7, 7),
        (2021, 8, 8),
        (2021, 9, 9),
        (2021, 10, 10),
        (2021, 11, 11),
        (2021, 12, 12),
        (2021, 14, 14),
        (2021, 15, 15),
        (2021, 17, 17),
        (2021, 18, 18),
        (2021, 19, 19),
        (2021, 20, 20),
        (2021, 21, 21),
        (2021, 22, 22),
        (2021, 23, 23),
        (2021, 24, 24),
        (2021, 34, 34),
        (2021, 38, 38),
        (2021, 41, 41),
        (2021, 42, 42),
        (2021, 43, 43),
        (2021, 47, 47),
        (2021, 48, 48),
        (2021, 51, 51),
        (2021, 77, 77),
        (2021, 78, 78),
        (2021, 99, 99),
        (2022, 1, 1),
        (2022, 2, 2),
        (2022, 3, 3),
        (2022, 4, 4),
        (2022, 5, 5),
        (2022, 6, 6),
        (2022, 7, 7),
        (2022, 8, 8),
        (2022, 9, 9),
        (2022, 10, 10),
        (2022, 11, 11),
        (2022, 12, 12),
        (2022, 14, 14),
        (2022, 15, 15),
        (2022, 16, 16),
        (2022, 17, 17),
        (2022, 19, 19),
        (2022, 20, 20),
        (2022, 21, 21),
        (2022, 22, 22),
        (2022, 23, 23),
        (2022, 24, 24),
        (2022, 31, 31),
        (2022, 34, 34),
        (2022, 38, 38),
        (2022, 41, 41),
        (2022, 42, 42),
        (2022, 43, 43),
        (2022, 45, 45),
        (2022, 47, 47),
        (2022, 48, 48),
        (2022, 51, 51),
        (2022, 18, 54),
        (2022, 77, 77),
        (2022, 78, 78),
        (2022, 99, 99))
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
        "Gateway (WWT)": "s"}

testing = {}

# Initialize a 2D list to store the table data
training = []

print("******************************")
print("training", end=" ")

for numset in nums:

    finishes = []
    ssfins = []
    rcfins = []
    sfins = []
    print(".", end=" ", flush=True)

    for ind in (1, 2):
        num = numset[ind]
        yr = numset[0] + ind - 1
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

                    if ind == 2:
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

                    if yr == 2023:
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

    thrs = [1, 3, 5, 10, 15, 20, 25]

    probs = []

    for thr in thrs:
        outputs = []
        for result in results:
            if result > int(thr):
                outputs.append(0)
            else:
                outputs.append(1)


        # Creating and training the Logistic Regression model
        model = LogisticRegression()
        model.fit(inputs, outputs)

        # Predicting the probability of each class for the new point
        prediction = model.predict(new_point)
        probs.append(prediction[0])
    
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['figure.facecolor'] = 'black'
    plt.rcParams['savefig.facecolor'] = 'black'

    dlt = [probs[0]]
    for i in range(len(probs)-1):
        dlt.append((probs[i+1]-probs[i])/(thrs[i+1]-thrs[i]))

    norm = colors.Normalize(vmin=1/72, vmax=1/18)

    def format(value):
        if value < 0.01:
            return 2
        elif value < 0.1:
            return 1
        else:
            return 0


    plt.style.use('dark_background')
    xpos = np.arange(len(thrs))
    ypos = np.array(probs)/probs[-1]
    bars = plt.bar(xpos, ypos, color=plt.cm.viridis(norm(dlt)))
    plt.xticks(xpos, thrs)


    # Annotate each bar with its scaled value
    for bar, value in zip(bars, probs):
        if value < 0.01:
            annotation = f'{value*100:.2f}'
        elif value < 0.1:
            annotation = f'{value*100:.1f}'
        else:
            annotation = f'{value*100:.0f}'
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, annotation,
            ha='center', va='bottom', color='white', font="arial", size=18)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines['bottom'].set_linewidth(2)
    ax.tick_params(axis='x', width=2, length=6)
    plt.xticks(fontname='arial', fontsize=18)

    image = "graph.png"

    graphsize = 1548
    numsize = 576

    blank = Image.new("RGB", (graphsize, graphsize), (0,0,0))
    blank.save(image)

    plt.savefig(image, dpi=300, bbox_inches='tight')

    plt.clf()

    graph = Image.open(image)

    numimage = Image.open(str(qnum) + ".jpg")

    # Create a new blank image with the same dimensions as the input images
    resized = Image.new("RGB", (graphsize, graphsize), (0,0,0))

    # Paste the first image onto the new image
    resized.paste(graph, (0, 150))

    # Paste the second image on top of the first image
    resized.paste(numimage.resize((numsize, numsize)), (89, 0))

    # Save the final image
    resized.save(image)
