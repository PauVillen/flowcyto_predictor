#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code to map genes to their ensembl_ID and to create cell IDs
@author: pauvillen14
"""

# Import libraries
import pandas as pd
import mygene

# Load data
df = pd.read_csv("final_db.csv", index_col=0)

# Connect to gene database
my_gene = mygene.MyGeneInfo()

# List of genes, list of cells
gene_list = df['Symbol'].unique().tolist()
cell_list = df['Cell.type'].unique()

# Match genes to their Ensembl ID
results = my_gene.querymany(gene_list, scopes='symbol', fields='ensembl.gene', species='human')

# Create dictionary to store the Symbol - Ensembl ID relation
symbol_to_ensembl = {}
for item in results:
    if 'ensembl' in item:
        # If the result is a list, take the first one
        if isinstance(item['ensembl'], list):
            symbol_to_ensembl[item['query']] = item['ensembl'][0]['gene']
        elif isinstance(item['ensembl'], dict):
            symbol_to_ensembl[item['query']] = item['ensembl']['gene']
# Manually add the Ensembl ID for the two genes which get no hit
symbol_to_ensembl['HIST1H3H'] = 'ENSG00000278828'
symbol_to_ensembl['C2ORF88'] = 'ENSG00000187699'
            
# Map the dictionary to the data frame
df['ensembl_id'] = df['Symbol'].map(symbol_to_ensembl)

# Assign IDs to cell types
cell_id_map = {name: f"CELL_{i:04d}" for i, name in enumerate(cell_list)}
df['cell_id'] = df['Cell.type'].map(cell_id_map)

# Save updated CSV
df.to_csv("final_db_ids.csv", index=False)
