import os

cwd = os.getcwd()

dir_path = r"..\\coastal_csvs\\"

res = []

for file_path in os.listdir(dir_path):
    # check if current file_path is a file
    if os.path.isfile(os.path.join(dir_path, file_path)):
        # add filename to list
        res.append(file_path)
print(res)