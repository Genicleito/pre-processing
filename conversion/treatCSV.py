# Developed by: Genicleito Gonçalves

# Function to handle CSV files by removing characters such as quotation marks, backslash, comma, semicolon.
def treatCSV(source, target, sep):
    import os
    """Function to handle CSV files by removing characters such as quotation marks, backslash, comma and semicolon.
    
    Parameters:
    source: path to source file
    target: path to target file
    sep: separator of the csv file
    
    Example: treatCSV('/home/user/source_file.csv', '/home/user/output_file.csv', sep = ",")
    """
    sep_aux = "_separator_aux_"
    target_aux = target + ".part"

    # List of sed commands used to treat the dataset
    seds = [
        "sed -r 's/\\\"\\" + sep + "\\\"/" + sep_aux + "/g' " + source + " > " + target,      # replaces the separator with the auxiliary separator
        
        # Using the '+' character in regex has the function of obtaining one or more backslashes
        "sed -r 's/\\\\+\\" + sep_aux + "/" + sep_aux + "/g' " + target + " > " + target_aux,     # remove backslashes before auxiliary separator
        "sed -r 's/\\\\+\\\"//g' " + target_aux + " > " + target,                   # remove quotes with backslash

        "sed -r 's/^\\\"|\"$/_control_quotes_/g' " + target + " > " + target_aux,    # save the quotation marks that mark the beginning and end of the record
        "sed -r 's/\\\"//g' " + target_aux + " > " + target,                  # remove quotes without backslashes
        
        "sed -r 's/\\" + sep_aux + "/\\\"\\,\\\"/g' " + target + " > " + target_aux,    # set the comma separator and restore quotation marks between fields
        "sed -r 's/_control_quotes_/\\\"/g' " + target_aux + " > " + target      # restore quotation marks at beginning and end of record
    ]

    # Apply the sed commands to the dataset
    for sed in seds:
        print("Appling [" + sed + "]")
        if(os.system(sed) != 0):
            print("==> [ERROR]")
            # Remove files created in proccess
            os.system("rm -rf " + target + "*")
            return
    # Remove the auxiliar file
    os.system("rm -rf " + target_aux)
    print("SUCESS")