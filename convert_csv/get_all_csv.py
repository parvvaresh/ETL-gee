import os

def get_all_csv(folder_path : str) -> list:
    try:
        if not os.path.isdir(folder_path):
            print("fThe folder path '{folder_path}' does not exist.")
            return []
        
        all_files = os.listdir(folder_path)


        csv_files = [file for file in all_files if file.endswith(".csv")]
         

        csv_file_full_path = [(os.path.join(folder_path, file), file) for file in csv_files]

        return csv_file_full_path

    except Exception as e:
        print("fan error occurred :‌ {e}")
        return []


