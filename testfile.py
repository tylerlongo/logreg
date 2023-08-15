import requests
from bs4 import BeautifulSoup
import numpy as np


# Sigmoid function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Logistic Regression implementation
class LogisticRegressionCustom:
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

    def predict(self, inputs):
        linear_model = np.dot(inputs, self.weights) + self.bias
        predictions = sigmoid(linear_model)
        return (predictions > 0.5).astype(int)

    def predict_prob(self, inputs):
        linear_model = np.dot(inputs, self.weights) + self.bias
        predictions = sigmoid(linear_model)
        return predictions


# Initialize a 2D list to store the table data
data = []


# URL of the webpage containing the table

nums = [11, 5, 6, 31, 10, 38, 42]
yrs = [2022, 2023]
plate = ["Daytona", "Talladega", "Atlanta"]
rc = ["Sonoma", "Watkins Glen", "COTA", "Road America", "Indy Road Course", "Charlotte Roval", "Chicago Street"]

for num in nums:

    finishes = []

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
                        if track in plate:
                            week.append(1)
                        else:
                            week.append(0)
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
logreg_model = LogisticRegressionCustom()
logreg_model.fit(inputs, outputs)

# New point to classify
new_point = np.array([[0, 5, 5, 10, 20]])

# Predicting the class of the new point
predicted_class = logreg_model.predict(new_point)

# Predicting the probability of each class for the new point
predicted_prob = logreg_model.predict_prob(new_point)

print("Predicted Class:", predicted_class)
print("Predicted Probabilities:", predicted_prob)