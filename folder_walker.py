import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import win32api
import win32security
import getpass
import matplotlib.font_manager as fm


def get_file_owner(file_path):
    # try:
        sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner()
        owner_name, _, _ = win32security.LookupAccountSid(None, owner_sid)
        return owner_name
    # except Exception:
    #     return 'Unknown'


def process_files(folder_path, csv_file_path):
    current_username = getpass.getuser()

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Path', 'Size', 'Creator', 'Created', 'Modified', 'Year', 'Month', 'Filename', 'Folder']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header only if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        for root, dirs, files in os.walk(folder_path):
            # Skip specific folders
            if 'linz' in dirs:
                dirs.remove('linz')
            if 'svetlana' in dirs:
                dirs.remove('svetlana')
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Get file information
                file_stat = os.stat(file_path)
                file_size = file_stat.st_size
                file_creator = get_file_owner(file_path)
                file_created = file_stat.st_ctime
                file_created = datetime.datetime.fromtimestamp(file_created)
                file_modified = file_stat.st_mtime
                file_modified = datetime.datetime.fromtimestamp(file_modified)
                year = file_created.year
                month = file_created.month
                
                # Write file data to the CSV file (append mode)
                writer.writerow({
                    'Name': file,
                    'Path': file_path,
                    'Size': file_size,
                    'Creator': file_creator,
                    'Created': file_created,
                    'Modified': file_modified,
                    'Year': year,
                    'Month': month,
                    'Filename': os.path.basename(file_path),
                    'Folder': os.path.basename(os.path.dirname(file_path))
                })

# Call the function to process files
folder_path = r'Y:\ndha\pre-deposit_prod\LD_working'  # Replace with the actual folder path
csv_file_path = r'C:\Users\Korotesv\folder_walker_viz9.csv'  # Replace with the desired CSV file path
process_files(folder_path, csv_file_path)
