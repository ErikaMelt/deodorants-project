import re


def replace_line(pattern, replace, input_file):
    # Open the input and output files
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        # Loop through each line of the input file
        for line in f_in:
            # Apply the regex pattern to the line and replace any matches with '.00'
            modified_line = re.sub(pattern, replace, line)

            # Write the modified line to the output file
            f_out.write(modified_line)


input_file1 = 'data/VMI_Movimientos-20190716_part1.txt'
output_file = 'data/VMI_Movimientos-20190716.txt'
pattern = r'\s\.000\b'
replace = '\t0.000'

replace_line(pattern, replace, input_file1)

#%%

#%%

#%%
