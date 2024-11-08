# Dont run me


def pipeline():
    print('------------------')
    print('Initializing Build')
    print('------------------')

    npi_registry_path = 'store/NPPES_Data_Dissemination_October_2024/npidata_pfile_20050523-20241013.csv'

    print('------------------')
    print('Loading NPI Registry')
    print('------------------')

    #from thin import thin

    #thin(npi_registry_path)
    print('NPI Thinning Skipped') #uncommented if above is commented

    print('------------------')
    print('Calling Backend')
    print('------------------')

    #from backend import build
    #from bulk_GEN import build

    #build()

    print('------------------')
    print('OpenAlex Data Compiled')
    print('------------------')


    print('------------------')
    print('Collapsing Redundancies')
    print('------------------')

    from single import single

    single()

    print('------------------')
    print('Redundancies Managed')
    print('------------------')

    
    from doi_split import split

    split()

    print('------------------')
    print('DOIs Split')
    print('------------------')

    print('------------------')
    print('Altmetrics Loading')
    print('------------------')

    from altmetrics import altmetrics

    altmetrics()

    print('------------------')
    print('Altmetrics Compiled')
    print('------------------')


    

#pipeline()

