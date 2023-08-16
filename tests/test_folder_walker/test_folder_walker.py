import os
import tempfile
import shutil
import sys
import pandas as pd
test_dir= os.getcwd()
script_dir = os.path.dirname(test_dir) 
folder_walker = os.path.join(script_dir,"folder_walker")
sys.path.insert(0, folder_walker)
from folder_walker import process_files

def test_process_files():
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    # Create some test files in the temporary directory
    test_file_1 = os.path.join(temp_dir, 'test_file_1.txt')
    test_file_2 = os.path.join(temp_dir, 'test_file_2.txt')
    with open(test_file_1, 'w') as f:
        f.write('Test content 1')
    with open(test_file_2, 'w') as f:
        f.write('Test content 2')

    # Process the temporary directory
    csv_file_path = os.path.join(temp_dir, 'test_output.csv')
    df = process_files(temp_dir, csv_file_path)

    # Check if the CSV file was created
    assert os.path.exists(csv_file_path)
    
    # Check if the DataFrame was returned
    assert isinstance(df, pd.DataFrame)
    
    # Clean up
    shutil.rmtree(temp_dir)

if __name__ == '__main__':
    test_process_files()
