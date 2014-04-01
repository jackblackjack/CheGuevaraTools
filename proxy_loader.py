"""
Extracts all proxies from the zip files in path_to_zips and returns them in a list

   ProxyLoader.get_proxies('path_to_zips')

"""
import zipfile

class ProxyLoader:

    @staticmethod
    def get_proxies(path_to_zips):
        proxies = set()
        zip_files = filter(lambda zfile: zfile.endswith('zip'),\
                               os.listdir(path_to_zips))
        for zip_file in zip_files:
            zfile = zipfile.ZipFile(path_to_zips + zip_file)
            proxies_list = zfile.read('full_list_nopl/_reliable_list.txt')
            for proxy in proxies_list.replace('\r','').split('\n'):
                proxies.add(proxy)
            
        return list(proxies)

if __name__ == '__main__':
    ProxyLoader.get_proxies('')
    
