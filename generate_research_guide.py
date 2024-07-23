import numpy as np
import os
import pandas as pd
import re

from datetime import datetime

def get_research_table(filename='./4. Research Guide.xlsx'):
    return pd.read_excel(filename)

def write_title(filename):
    date_str = datetime.strftime(datetime.now(),'%Y-%m-%d')
    with open(filename,'w') as f:
        pf = lambda x: print(x, file=f)
        pf('# Research Guide')
        pf('Sunlight Search\n')
        pf(f'{date_str}\n\n')

def write_search_table(df,filename):
    with open(filename,'a') as f:
        pf = lambda x: print(x, file=f)
        categories_list = [re.findall('^[^-].+',s) for s in df['Use This Resource To:'] if isinstance(s,str)]
        categories_unique = np.unique([c for cc in categories_list for c in cc])
        pf('## CONTENTS BY USE')
        for category in categories_unique:
            c_df = df[[category in c for c in categories_list]].sort_values('Resource')
            pf(f'### {category}\n')
            for o_idx, row in c_df.iterrows():
                pf(f"- [{row.Resource}](#{row.Resource.lower().replace(' ','-')}) (*{row.Category}*)")
            pf('\n')

def write_resource_list(df,filename):
    with open(filename,'a') as f:
        pf = lambda x: print(x, file=f)
        pf('## RESOURCES')
        for o_idx, row in df.sort_values('Resource').iterrows():        
            pf(f'### {row.Resource}\n')
            pf(f'*{row.Category}*\n')
            if isinstance(row.Link,str):
                link_list = [r for r in row.Link.split('\n') if len(r) > 0]
                pf(f"Links:\n")
                for link in link_list:
                    pf(f'- {link}')
                pf('\n')
            pf(f'Description: {row.Description}\n')
            pf(f'Uses:\n\n{row["Use This Resource To:"]}')
            pf('\n')

def convert_to_docx(filename):
    out_filename = filename.split('.')[0] + '.docx'
    os.system(f'pandoc {filename} -f markdown -o {out_filename}')

def write_report(df,filename='./research-guide.txt'):
    write_title(filename)
    write_search_table(df,filename)
    write_resource_list(df,filename)
    convert_to_docx(filename)

def main():
    research_df = get_research_table()
    write_report(research_df)

if __name__ == "__main__":
    main()
