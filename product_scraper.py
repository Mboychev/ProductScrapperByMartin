import requests
import openpyxl
import pandas as pd

from bs4 import BeautifulSoup

urls = ['https://www.ivar-group.com/en/International/products/Manifolds-8524/Stainless-steel-manifolds-8646/CI-592-KC-1-1-4--54062',
       'https://www.ivar-group.com/en/International/products/Manifolds-8524/Brass-rod-manifolds-8648/KC-02-AS-1--9681',
        'https://www.ivar-group.com/en/International/products/Manifolds-8524/Brass-rod-manifolds-8648/CS-501-N-9547']
data = []

for url in urls:
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")

    # Find all tables in the page
    tables = soup.find_all("table")

    # Get the table having class="table"
    table = soup.find("table", attrs={"class": "fl-table"})

    # Get the title of the product
    title = [ttl.text.strip() for ttl in soup.find_all('title')]

    # Get all the rows of the table
    table_rows = table.find_all('tr')

    # Get the column headers
    headers = [th.text.strip() for th in table_rows[0].find_all('th')]
    if "Color" in headers:
        headers.remove("Color")

    # Get all the rows of the table excluding the first one
    rows = table_rows[1:]

    # Store the data
    data.append(title)
    data.append(headers)
    for row in rows:
        data.append([td.text.strip() for td in row.find_all('td')])
    data.append([])

    # Remove empty elements
for product in data:

    while "" in product:
        product.remove("")

    # Print the data
df = pd.DataFrame(data)
df.to_excel('test.xlsx', sheet_name='new_sheet')

