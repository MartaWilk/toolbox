import os, shutil
from datetime import date

def main():
    home = os.environ['HOME']
    master_file_1 = 'file1_master.csv'
    master_file_2 = 'file2_master.csv'
    
    file1_identifier = 'file1'
    file2_identifier = 'file2'

    master_path = f'{home}/path'
    downloads_path = f'{home}/path2'
    archve_path = f'{home}path3'

    archive(archive_path, master_path, master_file_1, master_file_2)
    copy_new(master_path, master_file_1, master_file_2, downloads_path, file1_identifier, file2_identifier)
    pass

def archive(archive_path, master_path, master_file_1, master_file_2):
    file1_master_path = f'{master_path}/{master_file_1}'
    file2_master_path = f'{master_path}/{master_file_2}'
    date_today = date.today()
    file_1_new_name = f'file_1-{date_today}.csv'
    file_2_new_name = f'file_2-{date_today}.csv'
    file_1_renamed_path = f'{master_path}/{file_1_new_name}'
    file_2_renamed_path = f'{master_path}/{file_2_new_name}'
    try:
        os.rename(file1_master_path, file_1_renamed_path)
        os.rename(file2_master_path, file_2_renamed_path)
        shutil.move(file_1_renamed_path, archive_path)
        shutil.move(file_2_renamed_path, archive_path)
    except FileNotFoundError:
        pass

def copy_new(master_path, master_file_1, master_file_2, downloads_path, file1_identifier, file2_identifier):
    file_1_master_path = f'{master_path}/{master_file_1}'
    file_2_master_path = f'{master_path}/{master_file_2}'
    date_today = date.today()
    
    file_1_new_name = f'file_1-{date_today}.csv'
    file_2_new_name = f'file_2-{date_today}.csv'
    
    file_1_renamed_path = f'{downloads_path}/{file_1_new_name}'
    file_2_renamed_path = f'{downloads_path}/{file_2_new_name}'

    try:    
        files = os.listdir(downloads_path)
        files = [f for f in files if os.path.isfile(downloads_path+'/'+f)] #Filtering only the files.
        csv_files = filter_files(files, '.csv', downloads_path)
        file_1_csvs = filter_files(csv_files, file1_identifier)
        file_2_csvs = filter_files(csv_files, file2_identifier)
        newest_file1 = max(file_1_csvs, key=lambda x: os.path.getctime(x))
        newest_file2 = max(file_2_csvs, key=lambda x: os.path.getctime(x))
        os.rename(newest_file_1, file_1_renamed_path)
        os.rename(newest_file_2, file_2_renamed_path)
        shutil.move(file_1_renamed_path, master_path)
        shutil.move(file_2_renamed_path, master_path)
    except FileExistsError:
        pass

def filter_files(files, filter, path=None):
    result = []
    for file in files:
        if filter in file:
            if path != None:
                result.append(f"{path}/{file}")
            else:
                result.append(f"{file}")
    return result

if __name__ == "__main__":
    main()
