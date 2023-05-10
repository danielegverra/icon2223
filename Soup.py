import requests
from bs4 import BeautifulSoup

# Website Url
page_name = "Colosseo"
url = f'https://it.wikipedia.org/wiki/{page_name}'

# Performing GET request to the URL
response = requests.get(url)

# Using BeatifulSoup to analyze the webpage content
soup = BeautifulSoup(response.content, "html.parser")

info_table = soup.find("table", class_="infobox")

# Looking for the row containing the desired object
superficie_row = info_table.find("th", string="Superficie").parent

# Extract the value from the row
if superficie_row is not None:
    superficie = superficie_row.find("td").get_text().strip()
else:
    print("Errore nel trovare il campo superificie")

# Print the obtained value
print(f"Superficie: {superficie}")
