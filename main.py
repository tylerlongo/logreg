import numpy as np
from logreg import LogisticRegression
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from PIL import Image

training = []

# Read data from the text file and convert it to a list of lists
with open('training.txt', 'r') as file:
    lines = file.readlines()
    # Parse the lines into a list of lists
    for line in lines:
        # Split the line into individual values using comma as the separator
        values = line.strip().split(', ')[4:]
        # Convert values to integers and append them to the data list
        training.append([float(value) for value in values])

# Splitting data into inputs and results
inputs = np.array(training)[:, :-1]
results = np.array(training)[:, -1]


testing = {}

with open('testing.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        # Split the line into key and values
        key, values = line.strip().split(': ')
        # Convert values to a list of integers
        testing[key] = list(map(float, values.split(', ')))


thrs = [1, 3, 5, 10, 15, 20, 25]
weights = []
bias = []

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
        weights.append(model.weights)
        bias.append(model.bias)


while True:
    print("******************************")

    print("Driver Number:", end=" ")
    qnum = input()

    print("Track Type:", end=" ")
    qtype = input()

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
    new_point = np.array([[qq, qm, qtq, qtm, ss, 36]])

    probs = []

    for i in range(len(thrs)):
        # Predicting the probability of each class for the new point
        model.weights = weights[i]
        model.bias = bias[i]
        prediction = model.predict(new_point)
        probs.append(prediction[0])
    
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['figure.facecolor'] = 'black'
    plt.rcParams['savefig.facecolor'] = 'black'

    dlt = [probs[0]]
    for i in range(len(probs)-1):
        dlt.append((probs[i+1]-probs[i])/(thrs[i+1]-thrs[i]))

    norm = colors.Normalize(vmin=1/72, vmax=1/18)

    plt.style.use('dark_background')
    xpos = np.arange(len(thrs))
    ypos = np.array(probs)/probs[-1]
    bars = plt.bar(xpos, ypos, color=plt.cm.viridis(norm(dlt)))
    plt.xticks(xpos, thrs)


    # Annotate each bar with its scaled value
    for bar, value in zip(bars, probs):
        if value < 0.0095:
            annotation = f'{value*100:.2f}'
        elif value < 0.095:
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
