import requests
from bs4 import BeautifulSoup


# Initialize a 2D list to store the table data
finishes = []


# URL of the webpage containing the table

num = 48
yr = [2022, 2023]

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
            week = []
            cell = row.find_all(["th", "td"])[7]
            week.append(int(cell.get_text(strip=True)))
            cell = row.find_all(["th", "td"])[6]
            week.append(int(cell.get_text(strip=True)))
            finishes.append(week)

# Print the 2D list
print(finishes)