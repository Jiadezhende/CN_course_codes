def csv_parser(file_path):
    import csv
    domains = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                domains.append(row[1])  # Assuming second column is the domain
    return domains