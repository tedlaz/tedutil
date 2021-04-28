import os
from tedutil import acc_parse as acp


dir_path = os.path.dirname(os.path.realpath(__file__))


def test_parse():
    fil = os.path.join(dir_path, 'acc.txt')
    f2ee, chart0, ee_lines = acp.acc_parse(fil)
    print(acp.match_account('24.02.00.000', f2ee))
    print(acp.match_account('24.01.00.024', f2ee))
    # print(ee_lines)
    # print(chart0)
    print(f2ee)
