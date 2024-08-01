import csv
import os
import shutil

temp_folder = './temp/'
list_name = 'PhishingList'

if os.path.exists(temp_folder):
    print("[*] Removing temp folder")
    shutil.rmtree(temp_folder)

print("[*] Create new temp folder")
os.mkdir(temp_folder)

print("[*] Fetching List from PhishTank")
# call PhishTank-API and put csv in the temp folder
# Remember to do Error handling

# For simplicity I am using the local csv for now
shutil.copyfile('./verified_online.csv', f'./{temp_folder}/verified_online.csv')

print("[*] Reading new list")
new_links = set()
with open(f'./{temp_folder}/verified_online.csv', 'r', encoding="utf-8") as csvfile:
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