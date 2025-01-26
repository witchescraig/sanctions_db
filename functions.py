import pandas as pd
import pycountry
# this is needed because sometimes Entity_DesignationDate is blank, so as 'proxy' we can use Entity_Regulation_PublicationDate
def replace_blanks(row):
    if pd.isna(row['Entity_DesignationDate']) or row['Entity_DesignationDate'] == '':
        return row['Entity_Regulation_PublicationDate']
    return row['Entity_DesignationDate']

# this can be used if you wanna sort of standardize the aliases
def rimuovi_caratteri_speciali(df, nome_colonna):
    df[nome_colonna] = df[nome_colonna].apply(lambda x: re.sub(r'[^\w\s]', '', x))
    return df

# this is needed to explode the nested columns in a DataFrame
def explode_nested_col(df):
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list) or isinstance(x, dict)).any():
            df = df.explode(col).reset_index(drop=True)
            df = pd.concat([df.drop([col], axis=1), pd.json_normalize(df[col]).add_prefix(col+'_')], axis=1)
    return df
    
# this is needed to convert all iso2 codes in iso3 and standardize country data
def iso2_to_iso3(iso2):
    try:
        if pd.notna(iso2):  
            iso2 = iso2.strip()  
            return pycountry.countries.get(alpha_2=iso2).alpha_3
        return None
    except (AttributeError, LookupError):
        print(f"Invalid ISO2 code: {iso2}")
        return None

# this is needed to convert all country names in iso3 and standardize country data
def descr_to_iso3(country_name):
    try:
        if pd.notna(country_name):
            country_name = country_name.strip()
            return pycountry.countries.lookup(country_name).alpha_3
        return None
    except (AttributeError, LookupError):
        print(f"Invalid Country Name: {country_name}", end='\r')
        return country_name