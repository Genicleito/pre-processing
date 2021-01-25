# # # Linux command to download files
# # mkdir -p download_files/ && cd download_files/ && wget -vc ftp://ftp.datasus.gov.br/dissemin/publicos/SINASC/NOV/DNRES/DNBR{2014..2017}*

install.packages('read.dbc')
require('read.dbc')
require('curl')

raw_path = 'download_files/raw/'
refined_path = 'download_files/refined/'

extract <- function(url = 'ftp://ftp.datasus.gov.br/dissemin/publicos/SINASC/NOV/DNRES/', base_name = '', write_path = raw_path, range_years = 2000:2019) {
  # Download files
  if (!dir.exists(write_path)) { dir.create(write_path, recursive = T) }
  for (ano in range_years) {
    filename = paste(base_name, ano, '.dbc', sep = '')
    cat('Downloading...', filename, '\n')
    curl_download(url = paste(url, filename, sep = ''), destfile = paste(write_path, filename, sep = ''))
  }
}

conversion <- function(read_path = raw_path, write_path = refined_path) {
  # create dir
  if (!dir.exists(write_path)) { dir.create(write_path, recursive = T) }
  # convert files to .csv
  bases = list.files(read_path, pattern = '.dbc')
  for (base in bases) {
    filename = paste(read_path, base, sep = '')
    csvFile = gsub('.dbc', '.csv', paste(write_path, base, sep = ''))
    cat('Converting to csv...', filename, '\n')
    write.csv(x = read.dbc(filename), file = csvFile, row.names = F, na = "")
  }
}

extract(base_name = 'DNBR', range_years = 2014:2017)
conversion()