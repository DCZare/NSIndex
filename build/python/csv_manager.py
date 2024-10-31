import csv
import os
import edgedb

def get_or_create_author(client, author_name, author_data):
    author_query = '''
    SELECT Author { id }
    FILTER .name = <str>$name
    LIMIT 1
    '''
    existing_author = client.query(author_query, name=author_name)

    if existing_author:
        return existing_author[0].id
    else:
        insert_author_query = '''
        INSERT Author {
            name := <str>$name,
            First := <str>$first,
            Last := <str>$last,
            Lifespan := <str>$lifespan,
            Gender := <str>$gender,
            Ethnicity := <str>$ethnicity,
            Graduation_Year := <str>$graduation_year,
            Residency := <str>$residency,
            Chair_Chief := <str>$chair_chief,
            Program_Director := <str>$program_director,
            Positions_Held := <str>$positions_held
        }
        '''
        client.query(insert_author_query, **author_data)
        created_author = client.query(author_query, name=author_name)
        return created_author[0].id

def main():
    client = edgedb.create_client()
    filepath = os.path.join(os.getcwd(), 'data', 'citations.csv')

    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                author_names = row['authors'].strip("[]").split(',')
                author_ids = []
                for name in author_names:
                    author_data = {
                        "name": name,
                        "first": row['First'],
                        "last": row['Last'],
                        "lifespan": row['Lifespan'],
                        "gender": row['Gender'],
                        "ethnicity": row['Ethnicity'],
                        "graduation_year": row['Graduation Year'],
                        "residency": row['Residency'],
                        "chair_chief": row['Chair/Chief'],
                        "program_director": row['Program Director'],
                        "positions_held": row['Positions Held']
                    }
                    author_id = get_or_create_author(client, name, author_data)
                    author_ids.append(author_id)

                work_data = {
                    "pmid": float(row['pmid']),
                    "journal": row['journal'],
                    "doi": row['doi'],
                    "title": row['title'],
                    "work_publication_date": row['work_publication_date'],
                    "abstract": row['abstract'],
                    "url": row['url'],
                    "cited_by_accounts_count": row['cited_by_accounts_count'],
                    "cited_by_posts_count": row['cited_by_posts_count'],
                    "cited_by_tweeters_count": row['cited_by_tweeters_count'],
                    "cited_by_patents_count": row['cited_by_patents_count'],
                    "work_title": row['work_title'],
                    "work_display_name": row['work_display_name'],
                    "work_publication_year": row['work_publication_year'],
                    "author_position": row['author_position'],
                    "institution_name": row['institution_name'],
                    "institution_id": row['institution_id'],
                    "institution_country_code": row['institution_country_code'],
                    "work_id": row['work_id'],
                    "author_ids": author_ids
                }

                try:
                    query = '''
                    INSERT Work {
                        pmid := <float64>$pmid,
                        journal := <str>$journal,
                        doi := <str>$doi,
                        title := <str>$title,
                        work_publication_date := <str>$work_publication_date,
                        abstract := <str>$abstract,
                        url := <str>$url,
                        cited_by_accounts_count := <str>$cited_by_accounts_count,
                        cited_by_posts_count := <str>$cited_by_posts_count,
                        cited_by_tweeters_count := <str>$cited_by_tweeters_count,
                        cited_by_patents_count := <str>$cited_by_patents_count,
                        work_title := <str>$work_title,
                        work_display_name := <str>$work_display_name,
                        work_publication_year := <str>$work_publication_year,
                        author_position := <str>$author_position,
                        institution_name := <str>$institution_name,
                        institution_id := <str>$institution_id,
                        institution_country_code := <str>$institution_country_code,
                        work_id := <str>$work_id,
                        authors := (SELECT Author FILTER .id IN array_unpack(<array<uuid>>$author_ids))
                    }
                    '''
                    client.query(query, **work_data)
                except Exception as e:
                    print(f"Error inserting row: {row} | Error: {e}")

    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    print('done :)')
