import csv
import os
import edgedb

def get_or_create_author(client, author_name):
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
            name := <str>$name
        }
        '''
        client.query(insert_author_query, name=author_name)
        created_author = client.query(author_query, name=author_name)
        return created_author[0].id

def main():
    
    client = edgedb.create_client()
    
    con = client._iter_coroutine(client._impl.acquire())
    #print(con._params.__dict__)
    print('----------------------------------------')
    print(os.getenv('EDGEDB_INSTANCE'))

    cd = os.getcwd()
    filepath = os.path.join(cd, 'data', 'citations.csv')

    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Remove square brackets and properly split authors
                author_names = row['authors'].strip("[]").split(',')
                author_names = [name.strip() for name in author_names]  # Ensure names are trimmed
                
                author_ids = []
                for author_name in author_names:
                    author_id = get_or_create_author(client, author_name)
                    author_ids.append(author_id)

                try:
                    query = '''
                    INSERT Work {
                        pmid := <float64>$pmid,
                        journal := <str>$journal,
                        doi := <str>$doi,
                        title := <str>$title,
                        abstract := <str>$abstract,
                        url := <str>$url,
                        authors := (SELECT Author FILTER .id IN array_unpack(<array<uuid>>$author_ids)),
                        cited_by_accounts_count := <str>$cited_by_accounts_count,
                        cited_by_posts_count := <str>$cited_by_posts_count,
                        cited_by_tweeters_count := <str>$cited_by_tweeters_count,
                        cited_by_patents_count := <str>$cited_by_patents_count,
                    }
                    '''
                    client.query(query, 
                        pmid=float(row['pmid']), 
                        journal=row['journal'], 
                        doi=row['doi'], 
                        title=row['title'], 
                        url=row['url'], 
                        cited_by_accounts_count=row['cited_by_accounts_count'], 
                        cited_by_posts_count=row['cited_by_posts_count'], 
                        cited_by_tweeters_count=row['cited_by_tweeters_count'], 
                        cited_by_patents_count=row['cited_by_patents_count'], 
                        abstract=row['abstract'], 
                        author_ids=author_ids
                    )
                    #print(f"Inserted Work with pmid: {row['pmid']}")
                    
                except ValueError as ve:
                    print('----------------------------------------')
                    print(f"ValueError for row: {row} | Error: {ve}")
                except Exception as e:
                    print(f"Error for row: {row} | Error: {e}")

    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    print('done :)')
