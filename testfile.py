import requests
from bs4 import BeautifulSoup

# URL of the webpage containing the table

num = 1
yr = 2023

url = "https://www.driveraverages.com/nascar/numberyear.php?carno_id=" + str(num) + "&yr_id=2023"

# Send an HTTP GET request to the URL
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
    
# Find the table containing the data
table = soup.find("table")

# Initialize a 2D list to store the table data
finishes = []

# Loop through each row in the table
for row in table.find_all("tr"):
    if len(row) >= 6:
        cell = row.find_all(["th", "td"])[6]
        finishes.append(cell.get_text(strip=True))

# Print the 2D list
print(finishes)