from scapy.all import *
from django.conf import settings
import threading
import time

from .VPNNuralNet import VPNClassifier

from siteList.models import SiteList

class CaptureThread(object):

    def __init__(self,ip):
        self.ip = ip
        self.file_name = os.path.join(settings.BASE_DIR,'firewall/VPNNuralNet/captures/capture_'+ip+'.pcap')
        self.rule_file = os.path.join(settings.BASE_DIR,'firewall/utils/rules.xml')
        self.data_file = os.path.join(settings.BASE_DIR, 'firewall/utils/flowstats/netmate.out')

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        t = AsyncSniffer(iface={"wlo1":"localhost"},filter="ip host 192.168.0.103")
        t.start()
        time.sleep(15)
        t.stop()
        wrpcap(self.file_name,t.results)
        netmate_cmd = "sudo netmate -r "+ self.rule_file + " -f "+self.file_name
        os.system(netmate_cmd)
        self.res = VPNClassifier.evalualte("/media/irondev25/e_drive/7th_sem/project/code/code/firewall/firewall/utils/flowstats/netmate.out")
        resBool = True
        if(self.res < 0.5):
            resBool = False
        else:
            resBool = True
        # siteListEntry = SiteList(self.ip,resBool)
        # siteListEntry.save()
        print(resBool)
        # os.system("cp /media/irondev25/e_drive/7th_sem/project/code/code/firewall/firewall/utils/flowstats/netmate.out /home/irondev25/netmate"+self.ip+".out")
        os.system("rm "+self.data_file)

        
