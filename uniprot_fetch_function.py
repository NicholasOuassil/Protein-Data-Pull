import pandas as pd

def uniprot_data_scraping(uniprot_list, data_to_pull='standard'):
    """
        Searches the uniprot database based on the supplied list of uniprot numbers and returns a Pandas DataFrame
        with the found data. Designed to suppress errors but print that it found one.

        :param accession_number: Uniprot accession number as a string
        :type accession_number: str
        
        :param data_to_pull: Which columns should be pulled from the UniProt Database. 
        This does not guarantee the data will populate. Rather this attempts to find the above data. Choices: all, standard, or list of columns.

        :return: DataFrame 
    """
    
    # Pull in lookup codes
    query_lookup_table = pd.read_excel('query_lookup_table.xlsx', header=0)
    
    # Identify the columns that we want to search for
    if data_to_pull == 'standard': # standard columns
        data_to_pull = ['Entry', 'Protein names', 'Status', 'Protein families', 'Length',
       'Mass', 'Sequence', 'Binding site', 'Calcium binding', 'DNA binding',
       'Metal binding', 'Nucleotide binding', 'Site', 'Function [CC]',
       'Absorption', 'Active site',
       'Catalytic activity', 'Cofactor', 'EC number', 'Kinetics', 'Pathway',
       'pH dependence', 'Redox potential', 'Rhea Ids',
       'Temperature dependence', 'Interacts with', 'Subunit structure [CC]',
       'Induction', 'Tissue specificity', 'Gene ontology (biological process)',
       'Gene ontology (GO)', 'Gene ontology (molecular function)',
       'Gene ontology IDs', 'ChEBI', 'ChEBI (Catalytic activity)',
       'ChEBI (Cofactor)', 'ChEBI IDs', 'Intramembrane',
       'Subcellular location [CC]', 'Transmembrane', 'Topological domain',
       'Chain', 'Cross-link', 'Disulfide bond', 'Glycosylation',
       'Initiator methionine', 'Lipidation', 'Modified residue', 'Peptide',
       'Propeptide', 'Post-translational modification', 'Signal peptide',
       'Transit peptide', 'Beta strand', 'Helix', 'Turn', 'Coiled coil',
       'Compositional bias', 'Domain [CC]', 'Domain [FT]', 'Motif', 'Region',
       'Repeat', 'Zinc finger']
    
    elif data_to_pull == 'all': # all columns that we have keys for
        data_to_pull=query_lookup_table['Column names as displayed on website'].values
        
    elif type(data_to_pull) == list: # specific names that we can lookup
        data_to_pull = data_to_pull # do nothing
        
    else: # doesnt fit the specified values
        raise ValueError('Change data_to_pull to "any", "standard" or a list of column names')
    
    
    col_string = '' #create the search column string
    first_pass=True
    for col in data_to_pull: # connect together the columns that need to be separated by commas 
        if first_pass:
            col_string = query_lookup_table.loc[query_lookup_table['Column names as displayed on website'] == col,
                                 'Column names as displayed in URL'].values[0]
            first_pass = False
            
        else:
            try: col_string += ','+query_lookup_table.loc[query_lookup_table['Column names as displayed on website'] == col,
                                 'Column names as displayed in URL'].values[0]
                
            except: print(f"Coult not find URL Name for {col}")
    
    col_string = col_string.replace(' ', '%20') #get rid of spaces
    
    # create prefix and suffix to web address 
    query_string_suffix= "&format=tab&columns="+col_string
    query_string_prefix='https://www.uniprot.org/uniprot/?query='
    
    first_pass=True
    for uniprot in uniprot_list: #go through list of all proteins
        if first_pass: # initialize the dataframe 
            try:
                total_data = pd.read_csv(query_string_prefix+uniprot+query_string_suffix, sep='\t',  thousands=',') # get data
                
                if total_data.shape[0] > 1: # Only take correct row, sometimes UniProt sends back more than 1 response
                    total_data = total_data.loc[total_data.Entry==uniprot]
                first_pass = False # dont come back here  
                
            except: 
                print(f"Could not complete URL request for {uniprot}")
            
            
        else:
            try: 
                revolve_data = pd.read_csv(query_string_prefix+uniprot+query_string_suffix, sep='\t',  thousands=',') # get data
                
                if revolve_data.shape[0] > 1: # Only take correct row, sometimes UniProt sends back more than 1 response
                    revolve_data = revolve_data.loc[revolve_data.Entry==uniprot]
                
                total_data = total_data.append(revolve_data, ignore_index=True) 
                
            except: 
                print(f"Could not complete URL request for {uniprot}")
            
            
    
    total_data=total_data.fillna(0) # fill nans with zeros
    
    return total_data
    
    
if __name__ == "__main__": 
    test_df = uniprot_data_scraping(['P61823'],data_to_pull='standard')
    print(test_df)