# Crawler Yahoo

This crawler was built with the objective of getting the Stocks from a specific region. The website used is https://finance.yahoo.com/screener/new'

The input parameter has to be the name of the country you want to obtain the stocks from. If the country is not found on the website, the script returns with the message "Region does not exist, please verify".

If the region is found on the website, the stocks are saved on a file with the name stocks_{region}.csv