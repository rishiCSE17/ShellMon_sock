import matplotlib.pyplot as plt
import time as t
from drawnow import *
import psutil as ps
import os


y_snd = []
y_rcv = []
y_spd = []
t_stamps = []
iface_name = ''


def plot_me():
    global x
    t_stamps.append(t.time())
    plt.title(f'Monitoring : {iface_name}')
    plt.plot(t_stamps, y_snd, label=f'Eggress Util : {y_snd[-1]} %')
    plt.plot(t_stamps, y_rcv, label=f'Ingress Util : {y_rcv[-1]} %')
    plt.plot(t_stamps, y_spd, label=f'Iface Speed  : {y_spd[-1]} Mbps')
    plt.grid()
    plt.legend()


def main_loop(loop, plot, iface, is_wl, interval, window):
    global iface_name
    while (True):
        iface_name = iface
        x = ps.net_io_counters(pernic=True)[iface]
        t.sleep(interval)
        y = ps.net_io_counters(pernic=True)[iface]

        if not is_wl:  # if Wired
            speed = ps.net_io_counters(pernic=True)[iface][2]


        else:  # if wireless
            speed = float(os.popen(f"x=`iwconfig {iface} | \
                                 grep 'Bit Rate' | \
                                 cut -d '=' -f2` ; \
                                 echo $x | \
                                 cut -d ' ' -f1"
                                   ).readline().split('\n')[0])

            freq = float(os.popen("x=`iwconfig wlp3s0 | \
                                 grep Frequency | \
                                 cut -d : -f3` ; \
                                 echo $x | \
                                 cut -d ' ' -f1"
                                  ).readline().split('\n')[0])

            tx_pwr = float(os.popen(f"x=`iwconfig {iface} | \
                                 grep 'Tx-Power' | \
                                 cut -d '=' -f3` ; \
                                 echo $x | \
                                 cut -d ' ' -f1"
                                    ).readline().split('\n')[0])

            sig_lvl = float(os.popen(f"x=`iwconfig {iface} | \
                                 grep 'Signal level' | \
                                 cut -d '=' -f3` ; \
                                 echo $x | \
                                 cut -d ' ' -f1"
                                     ).readline().split('\n')[0])

            q_link = round(eval(os.popen(f"x=`iwconfig {iface} | \
                                 grep 'Link Quality' | \
                                 cut -d '=' -f2` ; \
                                 echo $x | \
                                 cut -d ' ' -f1"
                                         ).readline().split('\n')[0]), 3)
        # Egress Utilization %
        y_snd.append(
            round(
                ((y[0] - x[0]) * 8 * 100) / (interval * speed * pow(2, 20)), 3
            )
        )

        # Ingress Utilisation %
        y_rcv.append(
            round(
                ((y[1] - x[1]) * 8 * 100) / (interval * speed * pow(2, 20)), 3
            )
        )

        # interface speed
        y_spd.append(speed)

        ######### Prepering return dict
        ret = {}

        ret['Ingress_util'] = y_rcv[-1]
        ret['Egress_util'] = y_snd[-1]
        ret['Speed'] = speed

        if is_wl:
            ret['Freq'] = freq
            ret['x_pwr'] = tx_pwr
            ret['sig_lvl'] = sig_lvl
            ret['q_link'] = q_link

        ##### For Unit Testing
        #print(ret)

        if len(y_snd) == (window - 1):  # maintaining window size
            y_snd.pop(0)
            y_rcv.pop(0)
            t_stamps.pop(0)
            y_spd.pop(0)

        if loop == False:  # preventing to reienter loop
            return ret

        if loop == True and plot == True:  # Preventing to plot if not looping
            drawnow(plot_me)

    return 0

def main(loop, plot, iface, is_wl, interval, window):
    '''
    !! DO NOT DELETE !!

    iface='wlp3s0' #interface name
    interval=1     #sampling interval
    window=60      #in sec
    is_wl=True     #if interface is a wireless one
    '''
    return main_loop(loop, plot, iface, is_wl, interval, window)


#main(loop=True, plot=True, iface='wlp3s0', is_wl=True, interval=1, window=60)  # loop=False to give 1 output
