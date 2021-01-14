# OBS: considerar tbm casos: ", | ,"

# Developed by: Genicleito Gonçalves

# Function to handle CSV files by removing characters such as quotation marks, backslash, comma, semicolon.
def treatCSV(source, target, sep):
    """Function to handle CSV files by removing characters such as quotation marks, backslash, comma and semicolon.
    
    Parameters:
    source: path to source file
    target: path to target file
    sep: separator of the csv file
    
    Example: treatCSV('/home/user/source_file.csv', '/home/user/output_file.csv', sep = ",")
    """
    import os
    quote_ctrl = '_quote_control_'
    field_separator = '_field_separator_'
    # aux_sep = '_auxiliary_separator_'
    aux_start_sep = '_auxiliary_start_separator_'
    aux_end_sep = '_auxiliary_end_separator_'
    # target_aux = target + ".part"

    # List of sed commands used to treat the dataset
    sed_conditions = [
        f"s/[\\]*\"{sep}\"/{field_separator}/g;s/[\\]*\"{sep}/{aux_end_sep}/g;s/[\\]*{sep}\"/{aux_start_sep}/g",    # replaces the separator with the auxiliary separator
        
        # Using the '+' character in regex has the function of obtaining one or more backslashes
        # f"s/[\\]+{field_separator}/{field_separator}/g",     # remove backslashes before auxiliary separator
        # "s/[\\]+\"//g",                   # remove quotes with backslash

        f"s/^\"/{quote_ctrl}/g;s/\"$/{quote_ctrl}/g",    # save the quotation marks that mark the beginning and end of the record
        "s/[\\]*\"//g",                  # remove quotes # without backslashes
        
        f"s/{field_separator}/\",\"/g;s/{aux_start_sep}/{sep}\"/g;s/{aux_end_sep}/\"{sep}/g",    # set the comma separator and restore quotation marks between fields
        f"s/{quote_ctrl}/\"/g"      # restore quotation marks at beginning and end of record
    ]
    cmd = f'sed -r \'{";".join(sed_conditions)}\' {source} > {target}'

    # Apply the sed commands
    if(os.system(cmd) != 0):
        return False
    return True