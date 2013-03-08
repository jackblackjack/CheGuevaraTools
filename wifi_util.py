import subprocess

def exec_command(str_command):
    """
    Runs a process on the command line, returns stdout
    """
    process = subprocess.Popen(str_command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return output

def is_sbucks_wifi():
    """
    Determines if we're connected to Starbucks' wifi. 
    """
    try:
        airport_out = exec_command('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I')
        return 'attwifi' in [k for k in airport_out.split('\n') if ' SSID' in k][0].split(':')[1].strip()
    except:
        return False
