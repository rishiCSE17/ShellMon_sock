import psutil as ps
import os
import time as t
import scripts.fetch_net_info as nif

def get_cpu_util(interval=None):
    dict_cpu={}
    dict_cpu['util_per_core']= ps.cpu_percent(interval=interval, percpu=True)
    dict_cpu['count_phy']=ps.cpu_count(logical=False)
    dict_cpu['count_vir']=ps.cpu_count()
    dict_cpu['mean_freq']=sum([x[0] for x in ps.cpu_freq(percpu=True)])/4
    x = os.getloadavg()
    dict_cpu['mean_load']=round((15*x[0]+5*x[1]+x[2])/21,4)

    return dict_cpu

def get_mem_util(mypass):
    dict_mem={}
    mem_details=ps.virtual_memory()
    dict_mem['vol']=round(mem_details[0] / pow(2,30), 3) # rotal memory in GB
    dict_mem['util']=mem_details[2] /100 #utilization in [0,1] range
    dict_mem['freq']=[int(i) for i in
                        os.popen(f"echo {mypass} | "
                                 f"sudo -S dmidecode -t memory | "
                                 f"grep 'Clock Speed' | "
                                 f"cut -d ':' -f2")
                           .read().split(' ')
                      if i.isdigit()]
    dict_mem['freq']=sum(dict_mem['freq'])/len(dict_mem['freq'])
    return dict_mem

def get_net_util(loop, plot, iface, is_wl, interval, window):

    dict_net=nif.main(loop, plot, iface, is_wl, interval, window)
    return dict_net

def main_loop(delay=0, cpu_interval=None, my_pass=''):
    while(True):
        ## execution block
        print(get_cpu_util(cpu_interval))
        print(get_mem_util(mypass=my_pass))
        print(get_net_util(loop=False,
                           plot=False,
                           iface='wlp3s0',
                           is_wl=True,
                           interval=1,
                           window=60))

        ## delay block
        t.sleep(delay)

def fetch_util_main():
    main_loop(delay=2, my_pass='Nil27311072008')

fetch_util_main()