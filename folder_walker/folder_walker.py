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
       # print(owner_sid)
        if not owner_sid:
            #print("Owner SID is empty.")
            return None
        owner_name, _, _ = win32security.LookupAccountSid(None, owner_sid)
        return owner_name
    except Exception as e:
        
        #print(str(e))
        #sleep(1)
        try:
            sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
            owner_sid = sd.GetSecurityDescriptorOwner()
            #print(owner_sid)
            if not owner_sid:
                #print("Owner SID is empty.")
                return None
            owner_name, _, _ = win32security.LookupAccountSid(None, owner_sid)

            return owner_name
        except Exception as e:
            #print(str(e))
            #sleep(1)
            try:
                sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                #print(owner_sid)
                if not owner_sid:
                    #print("Owner SID is empty.")
                    return None
                owner_name, _, _ = win32security.LookupAccountSid(None, owner_sid)
                return owner_name
            except Exception as e:
                #print(str(e))
                return 'Unknown'


def process_files(folder_path, csv_folder_path):
    current_username = getpass.getuser()

    data = []
    for root, dirs, files in os.walk(folder_path):
        # # Skip specific folders
        # if 'linz' in dirs:
        #     dirs.remove('linz')
        
        for file in files:
            file_path = os.path.join(root, file)
            print(file_path)
            # Get file information
            try:

                file_stat = os.stat(file_path)
                file_size = file_stat.st_size
                file_creator = get_file_owner(file_path)
                file_created = file_stat.st_ctime
                file_created = datetime.datetime.fromtimestamp(file_created)
                file_modified = file_stat.st_mtime
                file_modified = datetime.datetime.fromtimestamp(file_modified)
                year = file_created.year
                month = file_created.month
                m_year = file_modified.year
                m_month = file_modified.month
                
                data.append({
                    'Name': file,
                    'Path': file_path,
                    'Size': file_size,
                    'Creator': file_creator,
                    'Created': file_created,
                    'Year': year,
                    'Month': month,
                    'Modified': file_modified,
                    'M_Year': m_year,
                    'M_Month': m_month,
                    'Folder': os.path.basename(os.path.dirname(file_path))
                })

            except:
                print(file_path)
                with open(os.path.join(csv_folder_path, "log.txt"), 'a', encoding="utf-8") as f:
                    f.write('%s "failed"\n' % (file_path))

    df = pd.DataFrame(data)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    csv_file_path = os.path.join(csv_folder_path, f'folder_walker_result_{timestamp}.csv')
    df.to_csv(csv_file_path, index=False, encoding='utf-8')
   #     print("CSV file saved:", csv_file_path)
   # except Exception as e:
    #    print("Error saving CSV file:", e)
    return df

def main():
    try:
        parser = argparse.ArgumentParser(description='Folder Walker Script')
        parser.add_argument('folder_path', help='Path of the folder to analyze')
        parser.add_argument('csv_folder_path', default='.', help='Path to save the CSV file')
        args = parser.parse_args()

        folder_path = args.folder_path
        csv_folder_path = args.csv_folder_path

    except:
        folder_path = r"Y:\ndha\CS_legaldeposit\LD\one-time"  
        csv_folder_path = r"Z:\testing"

    returned_df = process_files(folder_path, csv_folder_path)

    return returned_df



if __name__ == "__main__":
    main()
