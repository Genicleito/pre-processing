sed -r 's/\;//g' /tmp/teste.csv > /tmp/out_.csv # apaga todos os ; presentes na base
sed -r 's/\"\,\"/;/g' /tmp/out_.csv > /tmp/out.csv # substitui o separador por ;

sed -r 's/\\+\;/;/g' /tmp/out.csv > /tmp/out_.csv # remove escapes de separador
sed -r 's/\\+\"//g' /tmp/out_.csv > /tmp/out.csv # remove aspas escapadas

sed -r 's/^\"|"$/_cidacs_control_quotes_/g' /tmp/out.csv > /tmp/out_.csv # guarda as aspas dos campos
sed -r 's/\"|\,//g' /tmp/out_.csv > /tmp/out.csv # remove aspas não escapadas e vírgulas no meio dos campos

sed -r 's/\;/\"\,\"/g' /tmp/out.csv > /tmp/out_.csv # volta o separador para , e resgata as aspas do final de cada campo
sed -r 's/_cidacs_control_quotes_/\"/g' /tmp/out_.csv > /tmp/out.csv # resgata as aspas do início e final das linhas