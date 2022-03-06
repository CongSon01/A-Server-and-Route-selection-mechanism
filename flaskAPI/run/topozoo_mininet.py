from zipfile import ZipFile
import xml.etree.ElementTree as ET

def convert_to_colon_separated (a):
    #a = "0000000000000001"
    for j in range(0, int(len(a) / 2)):
        if j == 0:
            continue
        a = a[0:2 * j + j - 1] + ":" + a[2 * j + j - 1:]
    # a = "00:00:00:00:00:00:00:01"
    return a

def convert_id_to_dpid (id):
    """
    param id: input switch id e.g. 1
    return : output dpid e.g. 00:00:00:00:00:00:00:01
    """
    return convert_to_colon_separated (format(id,'00000000000016x'))

def convert_id_to_mac (id):
    """
    param id: input switch id e.g. 1
    return : output dpid e.g. 00:00:00:00:00:00:00:01
    """
    return convert_to_colon_separated (format(id,'00000000000012x'))

class TopologyZooXML:
    """
    TopologyZooXML is a class for using XML files and Get topology matrix
    """
    def __init__(self,path):
        self.topology_zoo_xml_path = path
        self.root = ET.parse(path).getroot()
        self.switches = self.get_switches()
        self.edge_counter = self.get_edge_counter()
        self.edge_switches = self.get_edge_swithes()
        
    def get_switches (self):
        """
        Reads xml file and create list of all switches
        """
        switches = []
        for item in self.root.getchildren():
            for i in item.getchildren():
                if 'id' in i.keys():
                    switches.append((convert_id_to_dpid(int(i.attrib['id'])+1),int(i.attrib['id'])))
        return switches
    
   
    def get_edge_counter(self):
        """
        Reads xml file and create a dictionary of switch and count of it's connected links
        """
        edge_counter = {}  #{00:00:00:00:00:00:00:01:2,00:00:00:00:00:00:00:02:1}
       
        for sw1 in self.switches:
            edge_counter[sw1] = 0
        
        for item in self.root.getchildren():
            for i in item.getchildren():
                if 'source' in i.keys() and 'target' in  i.keys():
                    src_sw_dpid = convert_id_to_dpid(int(i.attrib['source'])+1)
                    edge_counter[(src_sw_dpid,int(i.attrib['source']))]=edge_counter[(src_sw_dpid,int(i.attrib['source']))]+1

        return edge_counter

    def get_edge_swithes(self):
        """
        Gets list of all edge switches
        """
        edge_switches = []
        for (sw,sw_id),edge_count in self.edge_counter.items():
            if edge_count is  1 or 2:
                edge_switches.append((sw,sw_id))
        return edge_switches

    def get_topology(self,number_of_hosts_to_be_added = 0 , random_hosts = False):
        """
        Gets topology in the following structrue:
        {first_switch_dpid or host_mac,second_switch_dpid,"h or s"}
        """
        final_topo = {}
        links_dup_check = {}

        for item in self.root.getchildren():
            for i in item.getchildren():
                if 'source' in i.keys() and 'target' in  i.keys():
                    src_sw_dpid = convert_id_to_dpid(int(i.attrib['source'])+1)
                    dst_sw_dpid = convert_id_to_dpid(int(i.attrib['target'])+1)

                    if (src_sw_dpid,dst_sw_dpid) not in links_dup_check and (dst_sw_dpid,src_sw_dpid) not in links_dup_check:
                        final_topo[((src_sw_dpid,int(i.attrib['source'])),(dst_sw_dpid,int(i.attrib['target'])),'s')] = 1
                        links_dup_check[(src_sw_dpid,dst_sw_dpid)] = True

        for sw in self.edge_switches:
            host_mac = sw[0][6:]
            final_topo[((host_mac,sw[1]),sw,'h')] = 1
        return final_topo