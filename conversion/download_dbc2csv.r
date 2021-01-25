# # # Linux command to download files
# # mkdir -p download_files/ && cd download_files/ && wget -vc ftp://ftp.datasus.gov.br/dissemin/publicos/SINASC/NOV/DNRES/DNBR{2014..2017}*

install.packages('read.dbc')
require('read.dbc')
require('curl')

# Download files
dir.create('download_files/')
url = 'ftp://ftp.datasus.gov.br/dissemin/publicos/SINASC/NOV/DNRES/'
for (ano in 2014:2017) {
	filename = paste('DNBR', ano, '.dbc', sep = '')
	cat('Downloading...', filename, '\n')
	curl_download(url = paste(url, filename, sep = ''), destfile = paste('download_files/', filename, sep = ''))
}

# convert files to .csv
bases = list.files('download_files/', pattern = '.dbc')
for (base in bases) {
  filename = paste('download_files', base, sep = '/')
  cat('Converting to csv...', filename, '\n')
  write.csv(x = read.dbc(filename), file = gsub('.dbc', '.csv', filename), row.names = F, na = "")
}