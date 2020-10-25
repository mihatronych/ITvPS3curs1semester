import csv

def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter='#')
    data = ["id#url#date#header#content"]
    data_splitted = []
    for line in reader:
        string = "{}#{}#{}#{}#{}".format(line["id"], line["url"], line["category"], line["name"], line["description"])
        data.append(string)
        data_splitted.append(str.split(string, "#"))
    return data_splitted

def csv_dict_writer(path, fieldnames, data):
    """
    Writes a CSV file using DictWriter
    """
    with open(path, "w", encoding='utf8', newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter='#', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
