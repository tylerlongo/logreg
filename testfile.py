import requests
from bs4 import BeautifulSoup
import numpy as np


# Sigmoid function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Logistic Regression implementation
class LogisticRegression:
    def __init__(self, learning_rate=0.01, num_iterations=10000):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None
        self.bias = None

    def fit(self, inputs, outputs):
        (num_samples, num_features) = inputs.shape
        self.weights = np.zeros(num_features)
        self.bias = 0

        # Gradient descent optimization
        for _ in range(self.num_iterations):
            linear_model = np.dot(inputs, self.weights) + self.bias
            predictions = sigmoid(linear_model)

            # Compute gradients
            dw = (1 / num_samples) * np.dot(inputs.T, (predictions - outputs))
            db = (1 / num_samples) * np.sum(predictions - outputs)

            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict_prob(self, inputs):
        linear_model = np.dot(inputs, self.weights) + self.bias
        prediction = sigmoid(linear_model)
        return prediction


# Initialize a 2D list to store the table data
data = []


# URL of the webpage containing the table

nums = [11, 5, 6, 31, 10, 38, 42]
yrs = [2022, 2023]
type = {"Daytona": "plate",
        "Talladega": "plate",
        "Atlanta": "plate",
        "Sonoma": "rc",
        "Watkins Glen": "rc",
        "Charlotte Roval": "rc",
        "COTA": "rc",
        "Road America": "rc",
        "Indy Road Course": "rc",
        "Chicago Street": "rc"}
plate = ["Daytona", "Talladega", "Atlanta"]
rc = ["Sonoma", "Watkins Glen", "COTA", "Road America", "Indy Road Course", "Charlotte Roval", "Chicago Street"]

for num in nums:

    finishes = []
    platefins = []
    rcfins = []
    ovalfins = []

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
                cell = row.find_all(["th", "td"])[3]
                if not cell.get_text(strip=True) == "":
                    races = len(finishes)
                    if races > 0:
                        q1 = np.percentile(finishes, 25)
                        med = np.median(finishes)
                        q3 = np.percentile(finishes, 75)
                    finish = int(row.find_all(["th", "td"])[6].get_text(strip=True))
                    finishes.append(finish)
                    if yr == 2023:
                        week = []
                        start = int(row.find_all(["th", "td"])[7].get_text(strip=True))
                        track = row.find_all(["th", "td"])[5].get_text(strip=True)
                        week.append(start)
                        week.append(q1)
                        week.append(med)
                        week.append(q3)
                        week.append(finish)
                        data.append(week)

# Splitting data into features (X) and labels (y)
inputs = np.array(data)[:, :-1]
results = np.array(data)[:, -1]
outputs = []
for result in results:
    if result > 15:
        outputs.append(0)
    else:
        outputs.append(1)


# Creating and training the Logistic Regression model
model = LogisticRegression()
model.fit(inputs, outputs)

# New point to classify
new_point = np.array([[30, 20, 25, 30]])

# Predicting the probability of each class for the new point
prediction = model.predict_prob(new_point)

print("Predicted Probabilities:", prediction)