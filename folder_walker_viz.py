import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def analyze(folder_path, plot_folder):
    # Read all CSV files from the given folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Initialize dataframes to store the combined data
    dfs = []

    for csv_file in csv_files:
        csv_file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(csv_file_path, skip_blank_lines=True, on_bad_lines='skip')
            
   
        combined_df = df
        # Group by year and calculate the number of files and total size
        files_per_year = combined_df.groupby('Year')['Name'].count()
        size_per_year = combined_df.groupby('Year')['Size'].sum()

        # Plotting the number of files per year
        plt.figure(figsize=(10, 6))
        plt.bar(files_per_year.index, files_per_year.values)
        plt.xlabel('Year')
        plt.ylabel('Number of Files')
        plt.title('Number of Files per Year')
        plt.savefig(os.path.join(plot_folder,csv_file.rstrip(".csv")+'_files_per_year.png'))
        plt.close()

        # Plotting the total size of files per year
        plt.figure(figsize=(10, 6))
        plt.bar(size_per_year.index, size_per_year.values)
        plt.xlabel('Year')
        plt.ylabel('Total Size (bytes)')
        plt.title('Total Size of Files per Year')
        plt.savefig(os.path.join(plot_folder,csv_file.rstrip(".csv")+'_size_per_year.png'))
        plt.close()

        # Group by creator and calculate the number of files and total size
        files_per_creator = combined_df.groupby('Creator')['Name'].count()
        size_per_creator = combined_df.groupby('Creator')['Size'].sum()

        # Plotting the number of files per creator
        plt.figure(figsize=(10, 6))
        plt.bar(files_per_creator.index, files_per_creator.values)
        plt.xlabel('Creator')
        plt.ylabel('Number of Files')
        plt.title('Number of Files per Creator')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(os.path.join(plot_folder,csv_file.rstrip(".csv")+'_files_per_creator.png'))
        plt.close()

        # Plotting the total size of files per creator
        plt.figure(figsize=(10, 6))
        plt.bar(size_per_creator.index, size_per_creator.values)
        plt.xlabel('Creator')
        plt.ylabel('Total Size (bytes)')
        plt.title('Total Size of Files per Creator')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(os.path.join(plot_folder,csv_file.rstrip(".csv")+'_size_per_creator.png'))
        plt.close()

# Specify the folder path where CSV files are located
folder_path = r'Y:\ndha\pre-deposit_prod\LD_working\storage_analyzer\Storage_analyzer'
plot_folder = r"Y:\ndha\pre-deposit_prod\LD_working\storage_analyzer\Storage_analyzer\pngs"

analyze(folder_path, plot_folder)
