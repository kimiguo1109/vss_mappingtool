# importing the module
import os
import json
import yaml
import sys, getopt

# vspec文件内容转换成json格式(vspec从pyreader读取出来与yaml格式相同)
def vspec_to_json(argv):
    mode = False
    inputfilevspec = ''
    try:
        opts, args = getopt.getopt(argv,"hi:w",["ivspecfile", "mode="])
    except getopt.GetoptError:
        print ('vspec2json.py -i <inputfile>')
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print ('vspec2json.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ivspecfile"):
            inputfilevspec = arg
        elif opt in ("-w", "--writeable"):
            mode = True

    with open(inputfilevspec, 'r', encoding="utf-8") as f:
        datas = yaml.load(f,Loader=yaml.FullLoader)  # 将文件的内容转换为字典形式
    jsonDatas = json.dumps(datas, indent=5) # 将字典的内容转换为json格式的字符串
    dict = json.loads(s=jsonDatas)
    with open('SDVOS_Vspec' + '.json', 'w') as outfile:
        json.dump(dict, outfile, indent=2)
    # print(jsonDatas)

if __name__ == "__main__":
    vspec_to_json(sys.argv[1:])
