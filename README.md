# Storage_analyzer

This script is designed to traverse a specified folder directory, collect file information, and store it in a CSV file. The CSV file will have a datestamp in its name and will include details like file name, path, size, creator, creation date, modification date, year, month, filename, and parent folder. The script will also return the collected data as a pandas DataFrame.

## Usage

To use this script, follow these steps:

1. Clone the repository or download the script file.
2. Open a terminal/command prompt.
3. Navigate to the directory where the script is located.
4. Run the script with the following command:

   ```bash
   python folder_walker_script.py path_to_folder csv_folder_path
   ```
   
   Or use **run_from_github.py** sctipt exemple  - replace script url link on raw folder_walker.py link from github. Use your folder path and csv filepath. This way df will be returned.

```python
import sys
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
script_url = r"https://raw.githubusercontent.com/nlnzcollservices/Storage_analyzer/main/folder_walker/folder_walker.py?token=GHSAT0AAAAAACGJ33BR5D7LAUOC4OA3XZTOZG4OZJA"
response = requests.get(script_url, verify=False)
script_content = response.text
folder_path = r'Y:\ndha\CS_legaldeposit\LD_Proj'
csv_filepath = r"Y:\ndha\pre-deposit_prod\LD_working\storage_analyzer\Storage_analyzer"
modified_script_content = (
    script_content
    + f"\nfolder_path = r'{folder_path}'\ncsv_filepath = r'{csv_filepath}'"
)
namespace = {}
exec(modified_script_content, namespace)
process_files = namespace["process_files"]
df = process_files(folder_path, csv_filepath)
print(df)
```
