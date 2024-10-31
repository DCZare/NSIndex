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
    author_results = []
    works_data = []
    endpoint = 'authors'
    author_outpath = 'data/authors_data.csv'
    works_outpath = 'data/works_data.csv'

    os.makedirs('data', exist_ok=True)
    pd.DataFrame(columns=['author_id', 'author_name', 'orcid', 'institution_id', 'institution_name'] + required_columns[2:]).to_csv(author_outpath, index=False)
    pd.DataFrame(columns=[
        'work_title', 'work_display_name', 'work_publication_year', 'work_publication_date', 'author_id',
        'author_name', 'author_position', 'institution_id', 'institution_name', 'institution_country_code',
        'work_id', 'work_doi', 'First', 'Last', 'Lifespan', 'Gender', 'Ethnicity', 'Graduation Year',
        'Residency', 'Chair/Chief', 'Program Director', 'Positions Held'
    ]).to_csv(works_outpath, index=False)

    total_rows = len(df)

    for index, row in df.head(10000).iterrows():
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
            orcid = author.get('orcid')
            institutions = author.get('institutions', [])
            institution_info = institutions[0] if institutions else {}
            institution_name = institution_info.get('display_name')
            institution_id = institution_info.get('id')

            author_info = {
                'author_id': author_id,
                'author_name': author_name,
                'orcid': orcid,
                'institution_id': institution_id,
                'institution_name': institution_name,
            }
            for col in required_columns[2:]:
                author_info[col] = row[col]

            author_results.append(author_info)

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
                    for authorship in work.get('authorships', []):
                        author_data = authorship.get('author', {})
                        author_position = authorship.get('author_position')
                        institution_info = authorship.get('institutions', [{}])[0] if authorship.get('institutions') else {}

                        works_data.append({
                            'work_title': work.get('title'),
                            'work_display_name': work.get('display_name'),
                            'work_publication_year': work.get('publication_year'),
                            'work_publication_date': work.get('publication_date'),
                            'author_id': author_data.get('id'),
                            'author_name': author_data.get('display_name'),
                            'author_position': author_position,
                            'institution_id': institution_info.get('id'),
                            'institution_name': institution_info.get('display_name'),
                            'institution_country_code': institution_info.get('country_code'),
                            'work_id': work.get('id'),
                            'work_doi': work.get('doi'),
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
                        })

                cursor = page_with_results['meta'].get('next_cursor', None)

        if (index + 1) % 100 == 0:
            pd.DataFrame(author_results).to_csv(author_outpath, mode='a', header=False, index=False)
            pd.DataFrame(works_data).to_csv(works_outpath, mode='a', header=False, index=False)
            author_results.clear()
            works_data.clear()
            print(f'Saved progress at {index + 1} records.')

        progress = (index + 1) / total_rows * 100
        remaining = total_rows - (index + 1)
        print('-----------------------------------')
        print(f"Progress: {progress:.2f}% complete. ({index + 1}/{total_rows} done, {remaining} remaining)")
        print('-----------------------------------')

    if author_results:
        pd.DataFrame(author_results).to_csv(author_outpath, mode='a', header=False, index=False)
    if works_data:
        pd.DataFrame(works_data).to_csv(works_outpath, mode='a', header=False, index=False)
    print(f'Final save completed.')

if __name__ == "__main__":
    build()
