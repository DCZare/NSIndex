import csv


def single():
    #input_csv_file_path = 'outputs/OA_data.csv'
    input_csv_file_path = 'data/works_data.csv'
    output_csv_file_path = 'outputs/single_works.csv'

    seen_titles = set()
    filtered_rows = []

    # Read the input CSV file and filter out duplicate titles
    with open(input_csv_file_path, 'r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        if 'work_title' not in fieldnames:
            raise ValueError("The 'work_title' column is missing from file_a.csv")
        
        for row in reader:
            title = row['work_title']
            if title not in seen_titles:
                seen_titles.add(title)
                filtered_rows.append(row)

    # Write the filtered data to a new CSV file
    with open(output_csv_file_path, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"Filtered data has been written to {output_csv_file_path} with duplicates removed.")

