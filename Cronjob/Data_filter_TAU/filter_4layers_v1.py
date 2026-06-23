# -*- coding: utf-8 -*-
"""
Created on Thu May  8 11:19:30 2025

@author: USER

Use: python filter_4layers_v1.py <input_file> <output_file>
if calling from the same derictory where <filter_4layers_v2.py> is. if not need to give path to <filter_4layers_v2.py>

"""

import pandas as pd
import sys
import os
import time
import csv
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    if len(sys.argv) != 3:
        print("Usage: python filter_4layers_v1.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"{Fore.RED}Error: File '{input_file}' does not exist.")
        sys.exit(1)

    #base, ext = os.path.splitext(input_file)
    #output_file = f"{base}_filtered{ext}"
    
    # Remove existing output file to start fresh
    if os.path.exists(output_file):
        os.remove(output_file)

    chunk_size = 100_000  # Adjust based on memory — higher is faster if RAM allows
    total_lines = sum(1 for _ in open(input_file)) - 1  # estimate for progress
    total_chunks = total_lines // chunk_size + 1

    start_time = time.time()
    print(f"{Fore.CYAN}Processing '{input_file}' in chunks...")

    # Prepare to write filtered output with header
    header_written = False
    try:
        for chunk in tqdm(pd.read_csv(input_file,
                                      chunksize=chunk_size,
                                      delimiter=';',
                                      quoting=csv.QUOTE_MINIMAL,
                                      quotechar='"',
                                      doublequote=False,
                                      encoding='ascii',
                                      on_bad_lines='skip'),  # Skip malformed rows
                          total=total_chunks, colour='green'):
            if 'NEventsInCluster' not in chunk.columns:
                print(f"Error: 'NEventsInCluster' column not found.")
                print("Available columns:", chunk.columns.tolist())
                sys.exit(1)

            filtered = chunk[chunk['NEventsInCluster'] == 4]
            # Round floats that are actually integers
            # for col in filtered.select_dtypes(include='float').columns:
            #     if (filtered[col] % 1 == 0).all():
            #         filtered.loc[:, col] = filtered[col].astype(int)
                    
                    # Round floats that are actually integers
            for col in filtered.select_dtypes(include='float').columns:
                if (filtered[col] % 1 == 0).all():  # if all values are whole numbers
                    filtered[col] = filtered[col].astype(int)




            # Append to file, writing header only once
            #filtered.to_csv(output_file, mode='a', header=not header_written, index=False, sep=';')
            #header_written = True
            
            filtered.to_csv(output_file, mode='a',     index=False,
                            sep=';',
                            quoting=csv.QUOTE_MINIMAL,
                            quotechar='"',
                            doublequote=False,
                            lineterminator='\r\n',
                            encoding='ascii'
                            )
            

    except Exception as e:
        print(f"Failed during processing: {e}")
        sys.exit(1)

    elapsed = time.time() - start_time
    print(f"Done. {len(filtered)} events saved to '{output_file}'.")
    print(f"Elapsed time: {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()
