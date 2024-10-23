def altmetrics():
    import pyaltmetric
    import os
    from pyaltmetric import Altmetric
    import csv

    cwd = os.getcwd()
    print(cwd)

    i = 1
    input_csv_file_path = os.path.join(cwd, 'outputs/doi_split_works.csv')
    output_csv_file_path = os.path.join(cwd, 'outputs/citations.csv')

    dois = []
    original_rows = []

    with open(input_csv_file_path, 'r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        if 'work_doi' not in fieldnames:
            raise ValueError("The 'work_doi' column is missing from doi_split_works.csv")

        for row in reader:
            dois.append(row['work_doi'])
            original_rows.append(row)

    a = Altmetric()
    citations = []
    for doi in dois:
        citation = a.doi(doi)
        if citation is not None:
            citations.append(citation)
            print(f'{i} Found: {doi}')
        else:
            print(f"{i}: No citation data found for DOI: {doi}")
        i += 1

    all_fieldnames = set(fieldnames)
    for citation in citations:
        all_fieldnames.update(citation.keys())
    all_fieldnames = sorted(all_fieldnames)

    combined_rows = []
    for original_row in original_rows:
        doi = original_row.get('work_doi')
        citation_data = next((c for c in citations if c.get('doi') == doi), {})
        combined_row = {field: original_row.get(field, '') for field in all_fieldnames}
        combined_row.update({field: citation_data.get(field, '') for field in citation_data})
        combined_rows.append(combined_row)

    with open(output_csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_fieldnames)
        writer.writeheader()
        writer.writerows(combined_rows)

    print(f"Combined citations have been written to {output_csv_file_path} in CSV format.")
