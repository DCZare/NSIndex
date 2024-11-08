import time
import pyaltmetric
import os
from pyaltmetric import Altmetric
import csv

cwd = os.getcwd()

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
batch_size = 10  # We will save after every 10 DOIs
total_rows = len(dois)
successful_fetches = 0
failed_fetches = 0

# Retry logic for fetching citations
def fetch_citation_with_retry(doi, retries=5, delay=2):
    global successful_fetches, failed_fetches
    for attempt in range(retries):
        try:
            citation = a.doi(doi)
            if citation:
                successful_fetches += 1
                return citation
            else:
                failed_fetches += 1
                return None
        except requests.exceptions.HTTPError as e:
            print(f"Error fetching DOI {doi}: {e}")
            if e.response.status_code == 503:
                print(f"--Retrying-- 503 Service Unavailable. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"Non-retryable error for DOI {doi}. Skipping.")
                failed_fetches += 1
                break  # Don't retry on other errors
    failed_fetches += 1  # Increment failed fetch count if retries fail
    return None  # Return None if all retries fail

# Use the original fieldnames for consistency
all_fieldnames = fieldnames.copy()  # Start with the original fieldnames

# Gather all citation data and update fieldnames
for i, doi in enumerate(dois):
    citation = fetch_citation_with_retry(doi)

    # Print progress percentage
    percent_done = (i + 1) / total_rows * 100
    percent_successful = successful_fetches / (i + 1) * 100 if (i + 1) > 0 else 0
    print(f"Progress: {percent_done:.2f}% | Success Rate: {percent_successful:.2f}% | Fetching citation for DOI {i+1}/{total_rows}: {doi}")

    if citation:
        citations.append(citation)
        # Update fieldnames with new keys from the citation
        for key in citation.keys():
            if key not in all_fieldnames:
                all_fieldnames.append(key)
        print(f'Success! :) DOI: {doi}')
    else:
        print(f"Failed to fetch citation for DOI {doi}.")

    # Save every 10 DOIs
    if (i + 1) % 10 == 0:
        combined_rows = []
        for original_row in original_rows[i - 9:i + 1]:  # Get the last 10 rows
            doi = original_row.get('work_doi')
            citation_data = next((c for c in citations if c.get('doi') == doi), {})
            combined_row = {field: original_row.get(field, '') for field in all_fieldnames}
            combined_row.update({field: citation_data.get(field, '') for field in citation_data})
            combined_rows.append(combined_row)

        # Write to CSV after every 10 DOIs
        if combined_rows:
            with open(output_csv_file_path, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=all_fieldnames)
                if i == 9:  # Write header only for the first batch
                    writer.writeheader()
                writer.writerows(combined_rows)
            print(f"Progress saved at {i + 1}/{total_rows} DOIs.")
            
print(f"Final save completed. Success rate: {successful_fetches}/{total_rows} DOIs fetched successfully.")
