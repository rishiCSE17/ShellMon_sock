import psutil as ps
import os
import time

def get_cpu_util(interval=None):
    dict_cpu={}
    dict_cpu['util_per_core']= ps.cpu_percent(interval=interval, percpu=True)
    dict_cpu['count_phy']=ps.cpu_count(logical=False)
    dict_cpu['count_vir']=ps.cpu_count()
    dict_cpu['mean_freq']=sum([x[0] for x in ps.cpu_freq(percpu=True)])/4
    x = os.getloadavg()
    dict_cpu['mean_load']=round((15*x[0]+5*x[1]+x[2])/21,4)

    return dict_cpu


def main_loop(delay=0):
    while(True):
        ## execution block
        print(get_cpu_util())


        ## delay block
        time.sleep(delay)

def fetch_util_main():
    main_loop(delay=2)

fetch_util_main()