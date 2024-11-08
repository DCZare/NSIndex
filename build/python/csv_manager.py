import csv
import os
import edgedb

def get_or_create_author(client, author_name, author_data, author_cache):
    if author_name in author_cache:
        return author_cache[author_name]
    
    author_query = '''
    SELECT Author { id }
    FILTER .First = <str>$first AND .Last = <str>$last AND .Middle = <str>$middle AND .ORCID = <str>$orcid
    LIMIT 1
    '''
    existing_author = client.query(
        author_query,
        first=author_data['first'],
        last=author_data['last'],
        middle=author_data.get('middle', None),
        orcid=author_data.get('orcid', None)
    )

    if existing_author:
        author_id = existing_author[0].id
    else:
        insert_author_query = '''
        INSERT Author {
            First := <str>$first,
            Middle := <str>$middle,
            Last := <str>$last,
            Lifespan := <str>$lifespan,
            Gender := <str>$gender,
            Ethnicity := <str>$ethnicity,
            Graduation_Year := <str>$graduation_year,
            Residency := <str>$residency,
            Chair_Chief := <str>$chair_chief,
            Program_Director := <str>$program_director,
            Positions_Held := <str>$positions_held,
            ORCID := <str>$orcid
        }
        '''
        client.query(insert_author_query, **author_data)
        created_author = client.query(
            author_query,
            first=author_data['first'],
            last=author_data['last'],
            middle=author_data.get('middle', None),
            orcid=author_data.get('orcid', None)
        )
        author_id = created_author[0].id

    author_cache[author_name] = author_id
    return author_id

def main():
    client = edgedb.create_client()
    filepath = os.path.join(os.getcwd(), 'outputs', 'citations.csv')
    author_cache = {}

    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            total_rows = len(rows)
            
            for index, row in enumerate(rows, start=1):
                author_ids = []
                author_names = row['authors'].strip("[]").split(',')

                for name in author_names:
                    author_data = {
                        "first": row.get('First', None),
                        "middle": row.get('Middle', None),
                        "last": row.get('Last', None),
                        "lifespan": row.get('Lifespan', None),
                        "gender": row.get('Gender', None),
                        "ethnicity": row.get('Ethnicity', None),
                        "graduation_year": row.get('Graduation Year', None),
                        "residency": row.get('Residency', None),
                        "chair_chief": row.get('Chair/Chief', None),
                        "program_director": row.get('Program Director', None),
                        "positions_held": row.get('Positions Held', None),
                        "orcid": row.get('ORCID', '')  # Default to empty string if missing
                    }
                    author_id = get_or_create_author(client, name, author_data, author_cache)
                    author_ids.append(author_id)

                work_data = {
                    key: row[key] for key in [
                        'pmid', 'journal', 'doi', 'title', 'work_publication_date', 
                        'abstract', 'url', 'cited_by_accounts_count', 'cited_by_posts_count',
                        'cited_by_tweeters_count', 'cited_by_patents_count', 'work_title', 
                        'work_display_name', 'work_publication_year', 'author_position', 
                        'institution_name', 'institution_id', 'institution_country_code', 
                        'work_id'
                    ] if key in row and row[key]
                }
                work_data["author_ids"] = author_ids

                try:
                    fields = ", ".join(f"{key} := <str>${key}" for key in work_data if key != "author_ids")
                    fields += ", authors := (SELECT Author FILTER .id IN array_unpack(<array<uuid>>$author_ids))"

                    query = f'''
                    INSERT Work {{
                        {fields}
                    }}
                    '''
                    client.query(query, **work_data)
                    percent_done = (index / total_rows) * 100
                    print(f"\r{percent_done:.2f}% done", end="")
                except Exception as e:
                    print(f"\nError inserting row at index {index}: {e}")

    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    print('\ndone :)')
