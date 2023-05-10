pip3 install -r requirements.txt
rm -rf SDVOS_Vspec.json
rm -rf mapping_overlay.json
python3 vspec2json.py -i ./spec/SDVOS_basic.vspec
PYTHONPATH=./:./common/base:.. LD_LIBRARY_PATH=../../build/:$LD_LIBRARY_PATH python3 dbc2vssjson_converter.py -i Smart_basic.dbc -a SDVOS_Vspec.json -b canbus
json2yaml mapping_overlay.json mapping_overlay.vspec