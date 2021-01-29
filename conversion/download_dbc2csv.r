# # # Linux command to download files
# # mkdir -p download_files/ && cd download_files/ && wget -vc ftp://ftp.datasus.gov.br/dissemin/publicos/SINASC/NOV/DNRES/DNBR{2014..2017}*

install.packages('read.dbc')
require('read.dbc')
require('curl')

raw_path = 'download_files/raw/'
refined_path = 'download_files/refined/'
url_ftp = 'ftp://ftp.datasus.gov.br/dissemin/publicos/SINASC/NOV/DNRES/'

list_files_from_ftp <- function(url = url_ftp) {
  # handle to list dir
  h = new_handle(dirlistonly = T)
  # create a connection with the url
  con = curl(url = url_ftp, open = 'r', handle = h)
  # get a list of the files
  files = read.table(con)[, 1]
  # build the complete URL of the files
  f = function(x) { paste(url_ftp, x, sep = '') }
  # returns a vector with the links of the listed files
  unlist(lapply(files, f))
}

extract <- function(url = url_ftp, base_name = '', write_path = raw_path, range_years = NA) {
  # Download files
  if (!dir.exists(write_path)) { dir.create(write_path, recursive = T) }
  if (!is.na(range_years)) {
    for (ano in range_years) {
      filename = paste(base_name, ano, '.dbc', sep = '')
      cat('Downloading...', filename, '\n')
      curl_download(url = paste(url, filename, sep = ''), destfile = paste(write_path, filename, sep = ''))
    }
  } else {
    bases = list_files_from_ftp(url)
    for (base in bases) {
      filename = tail(unlist(strsplit(base, '/')), n=1)
      target_file = paste(write_path, gsub('.DBC', '.dbc', filename), sep = '')
      cat('Downloading...', filename, '|', 'Saving in...', target_file, '\n')
      curl_download(url = paste(url, filename, sep = ''), destfile = target_file)
    }
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