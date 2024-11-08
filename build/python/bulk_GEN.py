# bulk_GEN.py

import requests
import pandas as pd
import os
from tkinter import Tk, filedialog

def build():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select CSV file with names")
    if not file_path:
        print("No file selected.")
        return

    df = pd.read_csv(file_path)
    required_columns = ['First', 'Last', 'Lifespan', 'Gender', 'Ethnicity', 'Graduation Year', 'Residency', 'Chair/Chief', 'Program Director', 'Positions Held']
    if not all(col in df.columns for col in required_columns):
        print(f"CSV must contain the following columns: {', '.join(required_columns)}.")
        return

    email = "davidzar@buffalo.edu"
    works_data = []
    endpoint = 'authors'
    works_outpath = 'data/works_data.csv'
    progress_file = 'data/progress.txt'

    os.makedirs('data', exist_ok=True)
    pd.DataFrame(columns=[
        'work_title', 'work_display_name', 'work_publication_year', 'work_publication_date', 'author_id',
        'first_author', 'author_position', 'institution_id', 'institution_name', 'institution_country_code',
        'work_id', 'work_doi', 'pmid', 'First', 'Last', 'Lifespan', 'Gender', 'Ethnicity', 'Graduation Year',
        'Residency', 'Chair/Chief', 'Program Director', 'Positions Held', 'Middle', 'last_author'
    ]).to_csv(works_outpath, index=False)

    total_rows = len(df)
    start_index = 0
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            start_index = int(f.read().strip())

    for index in range(start_index, total_rows):
        row = df.iloc[index]
        first_name = row['First']
        last_name = row['Last']
        filter_str = f'display_name.search:"{first_name} {last_name}"'
        filtered_authors_url = f'https://api.openalex.org/{endpoint}?filter={filter_str}'
        if email:
            filtered_authors_url += f"&mailto={email}"

        r = requests.get(filtered_authors_url)
        authors_page = r.json()

        for author in authors_page['results']:
            author_id = author['id']
            author_name = author['display_name']
            institutions = author.get('institutions', [])
            institution_info = institutions[0] if institutions else {}
            institution_name = institution_info.get('display_name')
            institution_id = institution_info.get('id')

            works_endpoint = 'works'
            works_filter = f'authorships.author.id:"{author_id}"'
            filtered_works_url = f'https://api.openalex.org/{works_endpoint}?filter={works_filter}'
            if email:
                filtered_works_url += f"&mailto={email}"

            cursor = '*'
            select = ",".join((
                'id', 'ids', 'doi', 'title', 'display_name', 'publication_year',
                'publication_date', 'primary_location', 'open_access', 'authorships',
                'cited_by_count', 'is_retracted', 'is_paratext', 'updated_date', 'created_date'
            ))

            while cursor:
                url = f'{filtered_works_url}&select={select}&cursor={cursor}'
                page_with_results = requests.get(url).json()
                results = page_with_results.get('results', [])

                for work in results:
                    pmid = work.get('id')
                    first_author = None
                    middle_authors = []
                    last_author = None

                    for i, authorship in enumerate(work.get('authorships', [])):
                        author_data = authorship.get('author', {})
                        author_position = authorship.get('author_position')
                        institution_info = authorship.get('institutions', [{}])[0] if authorship.get('institutions') else {}

                        if i == 0:
                            first_author = author_data.get('display_name')
                        elif i == len(work['authorships']) - 1:
                            last_author = author_data.get('display_name')
                        else:
                            middle_authors.append(author_data.get('display_name'))

                    works_data.append({
                        'work_title': work.get('title'),
                        'work_display_name': work.get('display_name'),
                        'work_publication_year': work.get('publication_year'),
                        'work_publication_date': work.get('publication_date'),
                        'author_id': author_id,
                        'first_author': first_author,
                        'author_position': author_position,
                        'institution_id': institution_info.get('id'),
                        'institution_name': institution_info.get('display_name'),
                        'institution_country_code': institution_info.get('country_code'),
                        'work_id': work.get('id'),
                        'work_doi': work.get('doi'),
                        'pmid': pmid,
                        'First': first_name,
                        'Last': last_name,
                        'Lifespan': row['Lifespan'],
                        'Gender': row['Gender'],
                        'Ethnicity': row['Ethnicity'],
                        'Graduation Year': row['Graduation Year'],
                        'Residency': row['Residency'],
                        'Chair/Chief': row['Chair/Chief'],
                        'Program Director': row['Program Director'],
                        'Positions Held': row['Positions Held'],
                        'Middle': ', '.join(middle_authors),  # Ensuring 'Middle' column is populated
                        'last_author': last_author,
                    })

                cursor = page_with_results['meta'].get('next_cursor', None)

        if (index + 1) % 10 == 0:
            pd.DataFrame(works_data).to_csv(works_outpath, mode='a', header=False, index=False)
            works_data.clear()
            print(f'Saved progress at {index + 1} records.')

            with open(progress_file, 'w') as f:
                f.write(str(index + 1))

        progress = (index + 1) / total_rows * 100
        remaining = total_rows - (index + 1)
        print('-----------------------------------')
        print(f"Progress: {progress:.2f}% complete. ({index + 1}/{total_rows} done, {remaining} remaining)")
        print('-----------------------------------')

    if works_data:
        pd.DataFrame(works_data).to_csv(works_outpath, mode='a', header=False, index=False)

    with open(progress_file, 'w') as f:
        f.write(str(total_rows))

    print(f'Final save completed.')

if __name__ == "__main__":
    build()
