import pandas as pd

#csv_file = 'build/store/npidata_pfile_20050523-20240811.csv'

def thin(npi_registry_path):

    csv_file = npi_registry_path

    columns_to_keep = ['NPI', 'Provider Last Name (Legal Name)', 'Provider First Name', 'Provider First Line Business Mailing Address', 'Provider Business Mailing Address City Name']  # Replace with your desired column names

    df = pd.read_csv(csv_file, usecols=columns_to_keep)

    df.to_csv('outputs/NPI.csv', index=False)

    print('NPI Registry Preprocessed')



