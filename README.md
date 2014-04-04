#CheGuevaraTools

### Scraper 
A multithreaded scraper with support for HTTP proxies and custom headers. 

1. Download and install dependencies ```pip install -r requirements.txt``` or
   Install as library ```pip install git+https://github.com/mmenchu/CheGuevaraTools.git```

2. Download HydeMyAss Proxy Zip files to a tmp folder
```python proxy_zip_downloader.py gmail_usrname gmail_pass path_tmp_fldr```

3. Run the example. This will curl ~900 URLS using around 300 proxies.
```python example.py```

### Notes

* Eventhough a custom scraper can be passed to ThreadedServiceFetcherManager it's 
  probably best to just return the html without parsing it and scrape off the data
  in a different script using multiple processes. 
 
* Run ```ulimit -n 1024```

Miguel Menchu
mmenchu@gmail.com