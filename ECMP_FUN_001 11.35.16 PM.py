#!/usr/bin/env python2.5
"""
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

DESCRIPTION: To verify that SSX summarizes the routes when summary-address is enabled.
TEST PLAN: RIP Summarization Test Plans
TEST CASES: ECMP_FUN_001

HOW TO RUN: python2.5 ECMP_FUN_001.py
AUTHOR: jameer@stoke.com
REIEWER: kra@stoke.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from CISCO import *
from Linux import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from vlan import *
from misc import *
from helpers import is_healthy
import re

#Import Config and topo file
from config import *
from topo import *

class test_ECMP_FUN_001(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx1 = SSX(ssx1["ip_addr"])
        self.ssx2 = SSX(ssx2["ip_addr"])
	self.cisco = CISCO(cisco["ip_addr"])
	self.linux = Linux(linux['ip_addr'])
        self.ssx1.telnet()
        self.ssx2.telnet()
	self.linux.telnet()
	self.cisco.console(cisco["ip_addr"])
	
        # Clear the SSX config
        self.ssx1.clear_config()
        self.ssx2.clear_config()

        # wait for card to come up
        self.ssx1.wait4cards()
        self.ssx1.clear_health_stats()
        self.ssx2.wait4cards()
        self.ssx2.clear_health_stats()
	
    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx1.close()
        self.ssx2.close()
	self.linux.close()

    def test_ECMP_FUN_001(self):

        self.myLog.output("==================Starting The Test====================")
	
	
        # Push SSX config
	self.ssx1.config_from_string(ecmp_var['ECMP_FUN_001_SSX1'])
	self.ssx2.config_from_string(ecmp_var['ECMP_FUN_001_SSX2'])
	self.myLog.info("Configured the OSPF, BGP in the SSX\nConfiguring in the Cisco")
	
	
	self.cisco.clear_interface_config(intf=p_ssx1_cisco[1])
	self.cisco.clear_interface_config(intf=p_cisco_ssx2[0])
	self.myLog.info("Adding required vlans to database")
	self.cisco.cmd("vlan database")
	self.cisco.cmd("vlan %s"%ecmp_var['ospf_vlan1'])
	self.cisco.cmd("vlan %s"%ecmp_var['ospf_vlan2'])
	self.cisco.cmd("vlan %s"%ecmp_var['ospf_vlan3'])
	self.cisco.cmd("vlan %s"%ecmp_var['ospf_vlan4'])
	self.cisco.cmd("vlan %s"%ecmp_var['ospf_vlan5'])
	self.cisco.cmd("vlan %s"%ecmp_var['bgp_vlan1'])
	self.cisco.cmd("vlan %s"%ecmp_var['bgp_vlan1'])
	self.cisco.cmd("vlan 700")
	self.cisco.cmd("vlan 800")
	self.cisco.cmd("exit")
	self.cisco.cmd("conf t")
	self.cisco.cmd("no interface vlan %s"%ecmp_var['ospf_vlan1'])
	self.cisco.cmd("no interface vlan %s"%ecmp_var['ospf_vlan2'])
	self.cisco.cmd("no interface vlan %s"%ecmp_var['ospf_vlan3'])
	self.cisco.cmd("no interface vlan %s"%ecmp_var['ospf_vlan4'])
	self.cisco.cmd("no interface vlan %s"%ecmp_var['ospf_vlan5'])
	self.cisco.cmd("no interface vlan %s"%ecmp_var['bgp_vlan1'])
	self.cisco.cmd("no interface vlan %s"%ecmp_var['bgp_vlan2'])
	self.cisco.cmd("no interface vlan 700")
	self.cisco.cmd("no interface vlan 800")
	self.cisco.cmd("interface vlan %s"%ecmp_var['ospf_vlan1'])
	self.cisco.cmd("no ip address")
	self.cisco.cmd("no shutdown")
	self.cisco.cmd("ip address %s"%ecmp_var['cisco_ospf_intf1_ip/mask'])
	self.cisco.cmd("exit")
	self.cisco.cmd("interface vlan %s"%ecmp_var['ospf_vlan2'])
	self.cisco.cmd("no ip address")
	self.cisco.cmd("no shutdown")
	self.cisco.cmd("ip address %s"%ecmp_var['cisco_ospf_intf2_ip/mask'])
	self.cisco.cmd("exit")
	self.cisco.cmd("interface vlan %s"%ecmp_var['ospf_vlan3'])
	self.cisco.cmd("no ip address")
	self.cisco.cmd("no shutdown")
	self.cisco.cmd("ip address %s"%ecmp_var['cisco_ospf_intf3_ip/mask'])
	self.cisco.cmd("exit")
	self.cisco.cmd("interface vlan %s"%ecmp_var['ospf_vlan4'])
	self.cisco.cmd("no shutdown")
	self.cisco.cmd("no ip address")
	self.cisco.cmd("ip address %s"%ecmp_var['cisco_ospf_intf4_ip/mask'])
	self.cisco.cmd("exit")
        self.cisco.cmd("interface vlan %s"%ecmp_var['ospf_vlan5'])
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("no ip address")
        self.cisco.cmd("ip address %s"%ecmp_var['cisco_ssx2_ospf_intf1_ip/mask'])
	self.cisco.cmd("ip ospf mtu-ignore")
        self.cisco.cmd("exit")
	self.cisco.cmd("interface vlan %s"%ecmp_var['bgp_vlan1'])
	self.cisco.cmd("no ip address")
	self.cisco.cmd("no shutdown")
	self.cisco.cmd("ip address %s"%ecmp_var['bgp_intf_cisco_ssx1_ip/mask'])
	self.cisco.cmd("exit")
        self.cisco.cmd("interface vlan %s"%ecmp_var['bgp_vlan2'])
        self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("ip address %s"%ecmp_var['bgp_intf_cisco_ssx2_ip/mask'])
	self.cisco.cmd("exit")
	self.cisco.cmd("interface giga %s"%p_ssx1_cisco[1])
	self.cisco.cmd("switchport")
	self.cisco.cmd("switchport access vlan %s"%ecmp_var['ospf_vlan1'])
	self.cisco.cmd("switchport trunk encapsulation dot1q")
	self.cisco.cmd("switchport trunk allowed vlan %s-%s"%(ecmp_var['ospf_vlan1'],ecmp_var['ospf_vlan4']))
	self.cisco.cmd("switchport mode trunk")
	self.cisco.cmd("no ip address")
	self.cisco.cmd("exit")
	self.cisco.cmd("interface giga %s"%p_cisco_ssx2[0])
	self.cisco.cmd("switchport")
	self.cisco.cmd("switchport access vlan %s"%ecmp_var['bgp_vlan2'])
        self.cisco.cmd("switchport trunk encapsulation dot1q")
	self.cisco.cmd("switchport trunk allowed vlan %s-800"%ecmp_var['bgp_vlan2'])
	self.cisco.cmd("switchport mode trunk")
	self.cisco.cmd("no ip address")
        self.cisco.cmd("exit")
	self.cisco.cmd("no router ospf 123")
	self.cisco.cmd("router ospf 123")
	self.cisco.cmd("router-id 56.1.2.2")
	self.cisco.cmd("log-adjacency-changes")
	self.cisco.cmd("redistribute connected subnets")
	self.cisco.cmd("redistribute static subnets")
	self.cisco.cmd("network %s area 0"%ecmp_var['ospf_route1'])
	self.cisco.cmd("network %s area 0"%ecmp_var['ospf_route2'])
	self.cisco.cmd("network %s area 0"%ecmp_var['ospf_route3'])
	self.cisco.cmd("network %s area 0"%ecmp_var['ospf_route4'])
	self.cisco.cmd("exit")
	self.cisco.cmd("no router ospf 111")
	self.cisco.cmd("router ospf 111")
	self.cisco.cmd("router-id 11.11.11.11")
	self.cisco.cmd("log-adjacency-changes")
	self.cisco.cmd("redistribute connected subnets")
	self.cisco.cmd("redistribute static subnets")
	self.cisco.cmd("network %s area 0"%ecmp_var['ospf_route5'])
	self.cisco.cmd("end")
	
	time.sleep(60)
	
	#Moving to context
	self.ssx1.cmd("context %s"%ecmp_var['context_name1'])

	#Verify the all ospf's are up with the neighbor
	self.myLog.info("Verifying the ospf states at router - %s"%ecmp_var['context_name1'])
	ospf_op1 = self.ssx1.cmd('show ip ospf neighbor | grep "%s"'%ecmp_var['cisco_ospf_intf4_ip'])
        if not "Full" in ospf_op1:
		self.fail("OSPF Router is not established with the adjacent interface %s"%ecmp_var['cisco_ospf_intf4_ip'])
	ospf_op1 = self.ssx1.cmd('show ip ospf neighbor | grep "%s"'%ecmp_var['cisco_ospf_intf3_ip'])
        if not "Full" in ospf_op1:
		self.fail("OSPF Router is not established with the adjacent interface %s"%ecmp_var['cisco_ospf_intf3_ip'])
	ospf_op1 = self.ssx1.cmd('show ip ospf neighbor | grep "%s"'%ecmp_var['cisco_ospf_intf2_ip'])
        if not "Full" in ospf_op1:
		self.fail("OSPF Router is not established with the adjacent interface %s"%ecmp_var['cisco_ospf_intf2_ip'])
	ospf_op1 = self.ssx1.cmd('show ip ospf neighbor | grep "%s"'%ecmp_var['ospf_intf1_ip'])
        if not "Full" in ospf_op1:
		self.fail("OSPF Router is not established with the adjacent interface %s"%ecmp_var['cisco_ospf_intf1_ip'])
	self.myLog.output("OSPF Adjacency withh all the 4 L3 interfaces are fine")

	#Verifying the OSPF state at other router
	self.myLog.info("Verifying the OSPF state at other router")
	self.ssx2.cmd("context %s"%ecmp_var['context_name2'])
	ospf_op1 = self.ssx1.cmd("show ip ospf neighbor")
	if not "Full" in ospf_op1:
                self.fail("OSPF Router is not established with the adjacent interface")
	
	self.ssx1.cmd("context %s"%ecmp_var['context_name1'])
	self.ssx2.cmd("context %s"%ecmp_var['context_name2'])

	#Verify the MAX ECMP should be 4
	self.myLog.info("Verify the MAX ECMP should be 4")
	self.myLog.info("output of 'show ip ospf': %s"%self.ssx1.cmd("show ip ospf "))
	ecmp_op = self.ssx1.cmd("show ip ospf | grep -i ecmp")
	op = re.search("\s+Maximum\s+paths\s+\(ECMP\)\s+(\d+)",ecmp_op)
	op = op.group(1)
	if int(op) != 4:
		self.fail("ECMP path is not 4")
	self.myLog.output("Maximum Paths are: %s"%op)

	#Verifying that routes are distributed evenly among all next 4 hops
	self.myLog.info("Verifying that routes are distributed evenly among all next 4 hops")
	route_op = self.ssx1.cmd("show ip route ospf")
	self.myLog.info("output of 'show ip route ospf': %s"%route_op)
	self.failIf(int(len(route_op.split("*>")[-1].splitlines())) != 4 , "routes are not distributed evenly among all next 4 hops")
	self.failIf(int(len(route_op.split("*>")[-1].splitlines())) != 4 , "routes are not distributed evenly among all next 4 hops")

	#Verifying the External BGP
	self.ssx2.cmd("context %s"%ecmp_var['context_name3'])
	op = self.ssx2.cmd("show ip bgp neighbors")
	op = re.search("\s+Connections\s+established\s+(\d+)",op)
	op = op.group(1)
	if int(op) != 1:
		self.fail("External BGP connection not established with the neighbor")

        # Checking SSX Health
        hs1 = self.ssx1.get_health_stats()
        self.failUnless(is_healthy( hs1), "Platform is not healthy at SSX1")
        hs2 = self.ssx2.get_health_stats()
        self.failUnless(is_healthy( hs2), "Platform is not healthy at SSX2")


if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("ECMP_FUN_001.log", debug=True,console=True)
	op = vgroup_new(vgroup_ssx1_lin)
	print op
	op = vgroup_new(vgroup_rtrB_rtrC)
	print op
        suite = test_suite()
        suite.addTest(test_ECMP_FUN_001)
        test_runner(stream=sys.stdout).run(suite)
