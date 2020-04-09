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
    
    sep_aux = "_separator_aux_"
    target_aux = target + ".part"

    # List of sed commands used to treat the dataset
    seds = [
        "sed -r 's/\\\"\\" + sep + "\\\"/" + sep_aux + "/g' " + source,      # replaces the separator with the auxiliary separator
        
        # Using the '+' character in regex has the function of obtaining one or more backslashes
        "sed -r 's/\\\\+\\" + sep_aux + "/" + sep_aux + "/g'",     # remove backslashes before auxiliary separator
        "sed -r 's/\\\\+\\\"//g'",                   # remove quotes with backslash

        "sed -r 's/^\\\"|\"$/_control_quotes_/g'",    # save the quotation marks that mark the beginning and end of the record
        "sed -r 's/\\\"//g'",                  # remove quotes without backslashes
        
        "sed -r 's/\\" + sep_aux + "/\\\"\\,\\\"/g'",    # set the comma separator and restore quotation marks between fields
        "sed -r 's/_control_quotes_/\\\"/g' > " + target      # restore quotation marks at beginning and end of record
    ]
    re_sed_commands = " | ".join(seds)

    # Apply the sed commands
    if(os.system(re_sed_commands) != 0):
        return False
    return True