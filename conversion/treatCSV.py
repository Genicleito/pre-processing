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
    
    seds = [
        "sed -r 's/\\\"\\" + sep + "\\\"/" + sep_aux + "/g' " + source + " > " + target,      # substitui o separador pelo separador auxiliar
        
        # Adicionada a expresão '+'' aos seds que consideram a presença de contra-barra para permitir afetar uma ou mais contra-barras
        "sed -r 's/\\\\+\\" + sep_aux + "/" + sep_aux + "/g' " + target + " > " + target_aux,     # remove contra-barras presentes antes do separador auxiliar
        "sed -r 's/\\\\+\\\"//g' " + target_aux + " > " + target,                   # remove aspas escapadas com contra-barra

        "sed -r 's/^\\\"|\"$/_control_quotes_/g' " + target + " > " + target_aux,    # guarda as aspas que delimitam todo o registro
        "sed -r 's/\\\"//g' " + target_aux + " > " + target,                  # remove aspas não escapadas
        
        "sed -r 's/\\" + sep_aux + "/\\\"\\,\\\"/g' " + target + " > " + target_aux,    # define o separador como vírgula e restaura as aspas delimitadoras dos campos
        "sed -r 's/_control_quotes_/\\\"/g' " + target_aux + " > " + target      # restaura as aspas no início e fim das linhas
    ]

    for sed in seds:
        print("Appling [" + sed + "]")
        if(os.system(sed) != 0):
            print("==> [ERROR]")
            os.system("rm -rf " + target + "*")
            return
    os.system("rm -rf " + target_aux)
    print("SUCESS")