<!-- markdownlint-disable MD041-->
<!-- markdownlint-disable MD058-->
<!-- markdownlint-disable MD009-->
<!-- markdownlint-disable MD034-->
<!-- markdownlint-disable MD032-->
<!-- markdownlint-disable MD022-->
<!-- markdownlint-disable MD007-->
<!-- markdownlint-disable MD055-->
<!-- markdownlint-disable MD056-->
<!-- markdownlint-disable MD012-->


+----------------------------------------------------+
|                 pyATS components                   |
+----------------------------------------------------+
| AETest  : Python test script                        |
|                                                    |
| Testbed : Inventory YAML file                       |
|                                                    |
| Unicon  : Device connections ≈ Netmiko/Scrapli      |
|                                                    |
| Genie   : Output parser ≈ TextFSM + NTC templates   |
+----------------------------------------------------+

+----------------------------------------------------------+
|                AETest framework structure                |
+----------------------+----------------+------------------+
|     CommonSetup       |    Testcases    |   CommonCleanup  |
|-----------------------|-----------------|-----------------|
| Subsection            | Setup           | Subsection      |
| └─ Connect to devices | Test1           | └─ Unconfigure  |
|                       | Test2           | └─ ...          |
|                       | ...             |                 |
|                       | Cleanup         |                 |
|                       |                 |                 |
| Subsection            | Setup           | Subsection      |
| └─ Configure VLANs    | Test3           | └─ Collect logs |
| └─ Configure IP addr. |                 | └─ Disconnect   |
+-----------------------+-----------------+-----------------+

===> Validate testbed file which in yml
(.VpyATS) sushil@sushil:~/pyATS$ cat testbed.yml 
testbed:
  credentials:
    default:
      username: cisco
      password: cisco
devices:
  MI6-63:
    os: iosxe
    type: CE rotuer iosxe DEVNETEXPERT LAB
    connections:
      vty:
        protocol: ssh
        ip: 10.1.10.63
  CE-61:
    os: iosxe
    type: CE rotuer iosxe DEVNETEXPERT LAB
    connections:
      vty:
        protocol: ssh
        ip: 10.1.10.61

(.VpyATS) sushil@sushil:~/pyATS$ pyats validate testbed testbed.yml

===> Connection check for the devices within the testbed file
(.VpyATS) sushil@sushil:~/pyATS$ pyats validate testbed testbed.yml --connect
/home/sushil/pyATS/.VpyATS/bin/pyats:5: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pyats.cli.__main__ import main
Loading testbed file: testbed.yml
--------------------------------------------------------------------------------

Testbed Name:
    testbed

Testbed Devices:
.
|-- CE-61 [iosxe/CE rotuer iosxe DEVNETEXPERT LAB]
`-- MI6-63 [iosxe/CE rotuer iosxe DEVNETEXPERT LAB]

YAML Lint Messages
------------------

Connection Check
----------------

    note that connection checks are not 100% accurate - it does not take
    into account that connection implementations may choose to interpret
    the entire connection block differently.

    For example - Unicon autouses A/B console/standby, but does not allow
    explicit connection to B.

 - MI6-63/vty               [PASSED]                                          
 - CE-61/vty                [PASSED]                                          

Warning Messages
----------------
 - Device 'CE-61' has no interface definitions
 - Device 'MI6-63' has no interface definitions

===>Python3 interactive for show commands
from rich import print as rprint
from rich.pretty import pretty_repr

rprint(pretty_repr(show_arp_cmd))
{
    'interfaces': {
        'GigabitEthernet4': {
            'ipv4': {
                'neighbors': {
                    '192.168.63.63': {
                        'ip': '192.168.63.63',
                        'link_layer_address': '5254.0056.d3a0',
                        'type': 'ARPA',
                        'origin': 'static',
                        'age': '-',
                        'protocol': 'Internet'
                    }
                }
            }
        }
    }
}

>>> route_feature = testbed.devices['CE-61'].learn('static_routing')

2025-04-27 23:57:02,139: %UNICON-INFO: +++ CE-61 with via 'vty': executing command 'show vrf detail' +++
show vrf detail
CE-61#

2025-04-27 23:57:02,425: %UNICON-INFO: +++ CE-61 with via 'vty': executing command 'show ip static route' +++
show ip static route
Codes: M - Manual static, A - AAA download, N - IP NAT, D - DHCP,
       G - GPRS, V - Crypto VPN, C - CASA, P - Channel interface processor,
       B - BootP, S - Service selection gateway
       DN - Default Network, T - Tracking object
       L - TL1, E - OER, I - iEdge
       D1 - Dot1x Vlan Network, K - MWAM Route
       PP - PPP default route, MR - MRIPv6, SS - SSLVPN
       H - IPe Host, ID - IPe Domain Broadcast
       U - User GPRS, TE - MPLS Traffic-eng, LI - LIIN
       IR - ICMP Redirect, Vx - VXLAN static route
       LT - Cellular LTE
Codes in []: A - active, N - non-active, B - BFD-tracked, D - Not Tracked, P - permanent, -T Default Track


Codes in (): UP - up, DN - Down, AD-DN - Admin-Down, DL - Deleted
Static local RIB for default 

M  192.168.89.0/24 [1/0] via 10.1.10.2 [A]
CE-61#

2025-04-27 23:57:02,738: %UNICON-INFO: +++ CE-61 with via 'vty': executing command 'show ipv6 static detail' +++
show ipv6 static detail
IPv6 Static routes Table - default
Codes: * - installed in RIB, u/m - Unicast/Multicast only
Codes for []: P - permanent I - Inactive permanent
       U - Per-user Static route
       N - ND Static route
       M - MIP Static route
       P - DHCP-PD Static route
       R - RHI Static route
       V - VxLan Static route
CE-61#
>>> rprint(pretty_repr(route_feature.info))
{
    'vrf': {
        'default': {
            'address_family': {
                'ipv4': {
                    'routes': {
                        '192.168.89.0/24': {
                            'route': '192.168.89.0/24',
                            'next_hop': {
                                'next_hop_list': {
                                    1: {
                                        'index': 1,
                                        'active': True,
                                        'next_hop': '10.1.10.2',
                                        'preference': 1
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

>>> arp_feature = testbed.devices['CE-61'].learn('arp')
>>> rprint(pretty_repr(arp_feature.info))
{
    'interfaces': {
        'GigabitEthernet4': {
            'ipv4': {
                'neighbors': {
                    '192.168.61.61': {
                        'ip': '192.168.61.61',
                        'link_layer_address': '5254.00b2.3c7d',
                        'origin': 'static'
                    },
                    '192.168.61.51': {
                        'ip': '192.168.61.51',
                        'link_layer_address': '5254.0006.2f09',
                        'origin': 'dynamic'
                    }
                }
            },
            'arp_dynamic_learning': {
                'local_proxy_enable': False,
                'proxy_enable': True
            }
        },
        'GigabitEthernet1': {
            'ipv4': {
                'neighbors': {
                    '10.1.10.98': {
                        'ip': '10.1.10.98',
                        'link_layer_address': '000c.298a.c058',
                        'origin': 'dynamic'
                    },
                    '10.1.10.61': {
                        'ip': '10.1.10.61',
                        'link_layer_address': '5254.0099.d322',
                        'origin': 'static'
                    },
                    '10.1.10.2': {
                        'ip': '10.1.10.2',
                        'link_layer_address': '0050.56f6.5161',
                        'origin': 'dynamic'
                    },
                    '10.1.10.1': {
                        'ip': '10.1.10.1',
                        'link_layer_address': '0050.56c0.0008',
                        'origin': 'dynamic'
                    }
                }
            },
            'arp_dynamic_learning': {
                'local_proxy_enable': False,
                'proxy_enable': True
            }
        },
        'Loopback10041': {
            'arp_dynamic_learning': {
                'local_proxy_enable': False,
                'proxy_enable': True
            }
        },
        'Loopback100': {
            'arp_dynamic_learning': {
                'local_proxy_enable': False,
                'proxy_enable': True
            }
        },
        'Loopback0': {
            'arp_dynamic_learning': {
                'local_proxy_enable': False,
                'proxy_enable': True
            }
        }
    },
    'statistics': {
        'incomplete_total': 0,
        'in_requests_pkts': 39,
        'entries_total': 6,
        'in_replies_pkts': 17,
        'out_requests_pkts': 1,
        'out_replies_pkts': 15,
        'in_drops': 0
    }
}

>>> route_feature = testbed.devices['CE-61'].learn('static_routing')
>>> rprint(pretty_repr(route_feature.info))
{
    'vrf': {
        'default': {
            'address_family': {
                'ipv4': {
                    'routes': {
                        '192.168.89.0/24': {
                            'route': '192.168.89.0/24',
                            'next_hop': {
                                'next_hop_list': {
                                    1: {
                                        'index': 1,
                                        'active': True,
                                        'next_hop': '10.1.10.2',
                                        'preference': 1
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

>>> show_ip_route_cmd = testbed.devices['CE-61'].parse('show ip route')
>>> rprint(pretty_repr(show_ip_route_cmd))
{
    'vrf': {
        'default': {
            'address_family': {
                'ipv4': {
                    'routes': {
                        '10.0.10.41/32': {
                            'route': '10.0.10.41/32',
                            'active': True,
                            'source_protocol_codes': 'C',
                            'source_protocol': 'connected',
                            'next_hop': {
                                'outgoing_interface': {
                                    'Loopback10041': {
                                        'outgoing_interface': 'Loopback10041'
                                    }
                                }
                            }
                        },
                        '10.1.10.0/24': {
                            'route': '10.1.10.0/24',
                            'active': True,
                            'source_protocol_codes': 'C',
                            'source_protocol': 'connected',
                            'next_hop': {
                                'outgoing_interface': {
                                    'GigabitEthernet1': {
                                        'outgoing_interface': 'GigabitEthernet1'
                                    }
                                }
                            }
                        },
                        '10.1.10.61/32': {
                            'route': '10.1.10.61/32',
                            'active': True,
                            'source_protocol_codes': 'L',
                            'source_protocol': 'local',
                            'next_hop': {
                                'outgoing_interface': {
                                    'GigabitEthernet1': {
                                        'outgoing_interface': 'GigabitEthernet1'
                                    }
                                }
                            }
                        },
                        '192.168.61.0/24': {
                            'route': '192.168.61.0/24',
                            'active': True,
                            'source_protocol_codes': 'C',
                            'source_protocol': 'connected',
                            'next_hop': {
                                'outgoing_interface': {
                                    'GigabitEthernet4': {
                                        'outgoing_interface': 'GigabitEthernet4'
                                    }
                                }
                            }
                        },
                        '192.168.61.61/32': {
                            'route': '192.168.61.61/32',
                            'active': True,
                            'source_protocol_codes': 'L',
                            'source_protocol': 'local',
                            'next_hop': {
                                'outgoing_interface': {
                                    'GigabitEthernet4': {
                                        'outgoing_interface': 'GigabitEthernet4'
                                    }
                                }
                            }
                        },
                        '192.168.62.0/24': {
                            'route': '192.168.62.0/24',
                            'active': True,
                            'metric': 2,
                            'route_preference': 110,
                            'source_protocol_codes': 'O IA',
                            'source_protocol': 'ospf',
                            'next_hop': {
                                'next_hop_list': {
                                    1: {
                                        'index': 1,
                                        'next_hop': '192.168.61.51',
                                        'updated': '01:00:06',
                                        'outgoing_interface': 'GigabitEthernet4'
                                    }
                                }
                            }
                        },
                        '192.168.89.0/24': {
                            'route': '192.168.89.0/24',
                            'active': True,
                            'metric': 0,
                            'route_preference': 1,
                            'source_protocol_codes': 'S',
                            'source_protocol': 'static',
                            'next_hop': {
                                'next_hop_list': {
                                    1: {'index': 1, 'next_hop': '10.1.10.2'}
                                }
                            }
                        },
                        '192.168.100.61/32': {
                            'route': '192.168.100.61/32',
                            'active': True,
                            'source_protocol_codes': 'C',
                            'source_protocol': 'connected',
                            'next_hop': {
                                'outgoing_interface': {
                                    'Loopback100': {
                                        'outgoing_interface': 'Loopback100'
                                    }
                                }
                            }
                        },
                        '192.168.168.61/32': {
                            'route': '192.168.168.61/32',
                            'active': True,
                            'source_protocol_codes': 'C',
                            'source_protocol': 'connected',
                            'next_hop': {
                                'outgoing_interface': {
                                    'Loopback0': {
                                        'outgoing_interface': 'Loopback0'
                                    }
                                }
                            }
                        },
                        '192.168.168.62/32': {
                            'route': '192.168.168.62/32',
                            'active': True,
                            'metric': 3,
                            'route_preference': 110,
                            'source_protocol_codes': 'O IA',
                            'source_protocol': 'ospf',
                            'next_hop': {
                                'next_hop_list': {
                                    1: {
                                        'index': 1,
                                        'next_hop': '192.168.61.51',
                                        'updated': '01:00:06',
                                        'outgoing_interface': 'GigabitEthernet4'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
