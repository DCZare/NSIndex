from filter_UI import str_fill

def build():

    filter_str = str_fill()

    email = "davidzar@buffalo.edu"

    endpoint = 'works'

    filters = ",".join((
        f'{filter_str}',
    ))

    filtered_works_url = f'https://api.openalex.org/{endpoint}?filter={filters}'
    if email:
        filtered_works_url += f"&mailto={email}"
    print(f'complete URL with filters:\n{filtered_works_url}')

    import requests

    r = requests.get(filtered_works_url)
    results_page = r.json()
    print(f"retrieved {len(results_page['results'])} works")


    print(results_page['meta']['count'])
    results_page['meta']['count'] / 25

    cursor = '*'

    select = ",".join((
        'id',
        'ids',
        'doi',
        'title',
        'display_name',
        'publication_year',
        'publication_date',
        'primary_location',
        'open_access',
        'authorships',
        'cited_by_count',
        'is_retracted',
        'is_paratext',
        'updated_date',
        'created_date',
    ))

    works = []
    loop_index = 0
    while cursor:
        
        url = f'{filtered_works_url}&select={select}&cursor={cursor}'
        page_with_results = requests.get(url).json()
        
        results = page_with_results['results']
        works.extend(results)

        cursor = page_with_results['meta']['next_cursor']
        loop_index += 1
        if loop_index in [5, 10, 20, 50, 100] or loop_index % 500 == 0:
            print(f'{loop_index} api requests made so far')
    print(f'done. made {loop_index} api requests. collected {len(works)} works')

    import pandas as pd
    data = []
    for work in works:
        for authorship in work['authorships']:
            if authorship:
                author = authorship['author']
                author_id = author['id'] if author else None
                author_name = author['display_name'] if author else None
                author_position = authorship['author_position']
                for institution in authorship['institutions']:
                    if institution:
                        institution_id = institution['id']
                        institution_name = institution['display_name']
                        institution_country_code = institution['country_code']
                        data.append({
                            'work_title': work['title'],
                            'work_display_name': work['display_name'],
                            'work_publication_year': work['publication_year'],
                            'work_publication_date': work['publication_date'],
                            'author_id': author_id,
                            'author_name': author_name,
                            'author_position': author_position,
                            'institution_id': institution_id,
                            'institution_name': institution_name,
                            'institution_country_code': institution_country_code,
                            'work_id': work['id'],
                            'work_doi': work['doi'],
                        })
    df = pd.DataFrame(data)

    import os
    if not os.path.isdir('data'):
        os.mkdir('data')

    #outpath = 'outputs/build_output.csv'
    outpath = 'outputs/OA_data.csv'

    df.to_csv(outpath, index=False)

    print('Exported')

