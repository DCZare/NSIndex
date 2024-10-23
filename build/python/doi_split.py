def split():
    import csv

    input_csv_file_path = 'outputs/single_works.csv'

    output_csv_file_path = 'outputs/doi_split_works.csv'

    with open(input_csv_file_path, 'r', newline='') as infile:
        reader = csv.DictReader(infile)
        
        fieldnames = reader.fieldnames + ['DOI_origin', 'work_doi']  
        rows = []

        for row in reader:
            full_doi = row['work_doi']          
            doi_origin = ''
            work_doi = ''
            
            if full_doi.startswith('https://doi.org/'):
                doi_origin = 'https://doi.org/'  
                work_doi = full_doi[len('https://doi.org/'):]  
            
            row['DOI_origin'] = doi_origin
            row['work_doi'] = work_doi
            
            rows.append(row)  

    with open(output_csv_file_path, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"DOIs have been split into two columns and written to {output_csv_file_path}.")
