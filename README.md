# Converter from dbc files to json

The python3 requirements are noted in requirements.txt 

The software is based on cantools https://github.com/eerimoq/cantools,
it converts messages from a dbc to vss file -i (input-dbc) (input2-vspec)

<!-- Run command(for normal user):
sudo pip3 install -r requirements.txt
sudo python3 dbc2vssjson_converter.py -i FILENAME.DBC -b canbus

To convert json to yaml, use command:
json2yaml <json_file> <yaml_file> -->

最新版本的mapping工具（生成覆盖vss_dbc.json的mapping_overlay.vspec）

操作步骤（分别可以输出两个mapping_overlay.vspec)，一个basic.sh的，一个full.sh的）：
Just simply to run shell script
./convert_start_basic.sh (Test basic case setups)
./convert_start_full.sh (Test full cases setups)

将生成的mapping_overlay.vspec拖动到官方dbcfeeder目录下，将初始化的vss_dbc.json规则库用mapping_overlay.vspec覆盖

1. git submodule update --init
2. vss-tools/vspec2json.py -e dbc -o dbc_overlay.vspec --no-uuid  --json-pretty ./spec/VehicleSignalSpecification.vspec vss_dbc.json

简单解释：
which will create an output with the number of messages in that dbc file/a converted mapping json file/
and the mapping.json as our final target output file

if there are new input files that need to be converted to mapping, please edit convert_start.sh by modify
the .dbc or .vspec file name. That should be easy to do.
