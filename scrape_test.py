import requests
from bs4 import BeautifulSoup

# 1. Define URL of target page
url = "https://playbill.com/jobs?show=60"

# 2. Fetch the HTML document using GET request

try:
    response = requests.get(url)
    
    response.raise_for_status()
    
    html_content = response.text 
    print(f"successfully fetched the webpage (Status Code: {response.status_code})")
except requests.exceptions.RequestException as err:
    print(f"An error occured: {err}")
    exit()
    
# 3. Parse the HTML document using Beautiful Soup   
soup = BeautifulSoup(html_content, 'html.parser')

# 4. Grab all casting call containers
casting_calls = soup.find_all("div", class_="loadmore-item")

# 5. Go through casting calls and extract links

call_links = list()

for call in casting_calls:
    link = call.find('a')
    
    if link:
        href = link.get('href')
        if href:
            call_links.append(href)
            
# 6. write links to file
output_path = "links.txt"
with open(output_path, 'w') as file:
    file.write('\n'.join(call_links))