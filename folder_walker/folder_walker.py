import os
import csv
import pandas as pd
import datetime
import win32api
import win32security
import getpass
import sys
import argparse
from time import sleep

def get_file_owner(file_path):
    try:
        sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner()
        owner_name, _, _ = win32security.LookupAccountSid(None, owner_sid)
        return owner_name
    except Exception:
        sleep(1)
        try:
            sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
            owner_sid = sd.GetSecurityDescriptorOwner()
            owner_name, _, _ = win32security.LookupAccountSid(None, owner_sid)
            return owner_name
        except Exception:
            sleep(1)
            try:
                sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                owner_name, _, _ = win32security.LookupAccountSid(None, owner_sid)
                return owner_name
            except Exception:
                return 'Unknown'

                
def process_files(folder_path, csv_folder_path):
    current_username = getpass.getuser()

    data = []
    for root, dirs, files in os.walk(folder_path):
        # Skip specific folders
        if 'linz' in dirs:
            dirs.remove('linz')
        
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
            
            data.append({
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

    df = pd.DataFrame(data)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    csv_file_path = os.path.join(csv_folder_path, f'folder_walker_result_{timestamp}.csv')

    try:
        df.to_csv(csv_file_path, index=False, encoding='utf-8')
        print("CSV file saved:", csv_file_path)
    except Exception as e:
        print("Error saving CSV file:", e)
    return df

def main():
    parser = argparse.ArgumentParser(description='Folder Walker Script')
    parser.add_argument('folder_path', help='Path of the folder to analyze')
    parser.add_argument('--csv', dest='csv_folder_path', default='.', help='Path to save the CSV file')
    args = parser.parse_args()

    folder_path = args.folder_path
    csv_folder_path = args.csv_folder_path

    returned_df = process_files(folder_path)

    return returned_df



if __name__ == "__main__":
    main()
