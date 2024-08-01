import csv
import os
import shutil
import requests

temp_folder = './temp/'
phishes_file_path = f'./{temp_folder}/verified_online.csv'
list_name = 'PhishingList'

def get_phishing_list():
    url = f"http://data.phishtank.com/data/online-valid.csv"
    print(f"[*] Fetching url: {url}")
    response = requests.get(url)
     
    # Check if the response is successful
    if response.status_code == 200:
        content_type = response.headers.get('content-type')
        print(content_type)
        if (content_type =='text/csv') :
            with open(phishes_file_path, 'wt', encoding="utf-8") as csvfile:
                csvfile.write(response.text)
            print(f"[*] Successfully written csv at: {phishes_file_path}")
        else:
            print(f"[ERROR] Expected csv but got: {content_type}")
    else:
            print(f"[ERROR] Got Status Code: {response.status_code}")
            
            

if os.path.exists(temp_folder):
    print("[*] Removing temp folder")
    shutil.rmtree(temp_folder)

print("[*] Create new temp folder")
os.mkdir(temp_folder)

print("[*] Fetching List from PhishTank")
get_phishing_list()

# For simplicity I am using the local csv for now
# shutil.copyfile('./verified_online.csv', phishes_file_path)

print("[*] Reading new list")
new_links = set()
with open(phishes_file_path, 'r', encoding="utf-8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        if row[4].strip().lower() == "yes":
            stripped = row[1].replace("https://", "").replace("http://", "").rstrip("/")
            appended = f"0.0.0.0 {stripped}"
            new_links.add(appended)

print("[*] Opening old list")
with open('./phishes', 'r', encoding="utf-8") as phishes_file:
    old_links = {line.strip() for line in phishes_file}

# Update old links with new links
links = old_links | new_links

print("[*] Writing list")
with open('./phishes', 'w', encoding="utf-8") as phishes_file:
    phishes_file.write("\n".join(sorted(links)) + "\n")

print("[*] Done!")