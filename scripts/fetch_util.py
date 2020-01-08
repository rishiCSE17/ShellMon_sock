import psutil as ps
import os
import time as t
import fetch_net_info as nif
import json


def get_cpu_util(interval=None):
    dict_cpu={}
    dict_cpu['util_per_core']= ps.cpu_percent(interval=interval, percpu=True)
    dict_cpu['count_phy']=ps.cpu_count(logical=False)
    dict_cpu['count_vir']=ps.cpu_count()
    dict_cpu['mean_freq']=sum([x[0] for x in ps.cpu_freq(percpu=True)])/4
    x = ps.getloadavg()
    dict_cpu['mean_load']=round((15*x[0]+5*x[1]+x[2])/21,4)

    return dict_cpu

def get_mem_util(mypass):
    dict_mem={}
    mem_details=ps.virtual_memory()
    dict_mem['vol']=round(mem_details[0] / pow(2,30), 3) # rotal memory in GB
    dict_mem['util']=mem_details[2] /100 #utilization in [0,1] range
    try:
        dict_mem['freq']=[int(i) for i in
                            os.popen(f"echo {mypass} | "
                                     f"sudo -S dmidecode -t memory | "
                                     f"grep 'Clock Speed' | "
                                     f"cut -d ':' -f2")
                               .read().split(' ')
                          if i.isdigit()]
        dict_mem['freq']=round(sum(dict_mem['freq'])/len(dict_mem['freq']),3)
    except:
        dict_mem['freq']=1366
    return dict_mem

def get_net_util(loop, plot, iface, is_wl, interval, window):

    dict_net=nif.main(loop, plot, iface, is_wl, interval, window)
    return dict_net

def send_data(datagram):
    print(json.dumps(datagram))



def main_loop(loop=True, delay=0, cpu_interval=None, my_pass='', intf='eth0',is_wl=False):
    # distionary to send data to the server
    datagram={}
    while(True):
        ## execution block
        datagram['cpu'] = get_cpu_util(cpu_interval)
        datagram['mem'] = get_mem_util(mypass=my_pass)
        datagram['net'] = get_net_util(loop=False,
                           plot=False,
                           iface=intf,
                           is_wl=is_wl,
                           interval=1,
                           window=60)

        '''
        *** Datagram ***
        {
            cpu : { count_phy : val,
                    count_vir : val,
                    mean_frq  : val,
                    mean_load : val
                  },
            mem : { vol     : val,
                    util    : val,
                    freq    : val  
                  },
            net : { Ingress_util : val,
                    Egress_util  : val,
                    speed        : val
                  }
        }                 
        '''

        ##test block
        #send_data(datagram)

        ## breaking loop
        if not loop:
            return datagram

        ## delay block
        t.sleep(delay)

def main_fetch_util(loop, delay, cpu_interval, my_pass, intf, is_wl):
    return main_loop(loop, delay, cpu_interval, my_pass, intf, is_wl)


#main_fetch_util()