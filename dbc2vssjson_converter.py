#Scripted by Kimi Guo 2022/03/14
import sys, getopt
import cantools
import json
from collections import OrderedDict

# dictionary for the messages starting with messages prepared to add new messages in that
messages_dict = {}

# the main method expect on argument which is the input-file as ".dbc", a parameter for the bus and the mode
def main(argv):
    mode = False
    inputfiledbc = ''
    inputfilevspec = ''
    try:
        opts, args = getopt.getopt(argv,"hi:a:b:w",["idbcfile=", "ivspecfile", "bus=", "mode="])
    except getopt.GetoptError:
        print ('dbc2vssjson.py -i <inputfile> -a <inputfile2> -m <writeable(true|false) -b <canbus>')
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print ('dbc2vssjson.py -i <inputfile> -a <inputfile2> -m <writeable(true|false)> -b <canbus>')
            sys.exit()
        elif opt in ("-i", "--idbcfile"):
            inputfiledbc = arg
        elif opt in ("-a", "--ivspecfile"):
            inputfilevspec = arg
        elif opt in ("-b", "--bus"):
            bus = arg
        elif opt in ("-w", "--writeable"):
            mode = True
            print (mode)
    # load the can database file in cantools to work on the db
    db = cantools.database.load_file(inputfiledbc)
    with open(inputfilevspec, 'r', encoding='UTF-8') as vspec_json_file:
        vspec_dict = json.load(vspec_json_file)
    # load the messages to iterate over them altough print number of lines as output
    messages = db.messages
    print("Number of messages " + str(len(messages)))

    # print(list(vspec_dict.keys()))
    vss_namedict = {'EtasVehicleSpeed':'Vehicle.Speed', 
        'EtasVCLEFT_mirrorTiltXPosition':'Vehicle.Body.Mirrors.Left.Tilt',
        'EtasVCLEFT_mirrorTiltYPosition':'Vehicle.Body.Mirrors.Left.Pan',
        'EtasVCRIGHT_mirrorTiltXPosition':'Vehicle.Body.Mirrors.Right.Tilt',
        'EtasVCRIGHT_mirrorTiltYPosition':'Vehicle.Body.Mirrors.Right.Pan',
        'EtasVCSeat_row1XPosition':'Vehicle.Cabin.Seat.Row1.Position',
        'EtasVCSeat_row1ZPosition':'Vehicle.Cabin.Seat.Row1.Height',
        'EtasVCFRONT_tempAmbientFiltered':'Vehicle.OBD.AmbientAirTemperature',
        'EtasSteeringAngle129':'Vehicle.Chassis.SteeringWheel.Angle'}

    for message in messages:
        signals = message.signals
        # print(signals)
        
        for signal in signals:
            if message.name in vss_namedict.keys():
                message.name = vss_namedict[signal.name]
                vss_datatype_value = vspec_dict[message.name]['datatype']
                # print(vss_datatype_value)
                vss_type_value = vspec_dict[message.name]['type']
                message_json = {"datatype" : vss_datatype_value, "type": vss_type_value}
                messages_dict[message.name] = message_json
                signal_dict = messages_dict[message.name]

            if signal.name == 'EtasVCLEFT_mirrorTiltXPosition' or signal.name == 'EtasVCLEFT_mirrorTiltYPosition' or signal.name == 'EtasVCRIGHT_mirrorTiltXPosition' or signal.name == 'EtasVCRIGHT_mirrorTiltYPosition':
                vss_math = 'floor((x*40)-100)'
                signal_json = {"signal" : signal.name, "interval_ms" : 100, "transform": {"math" : vss_math}}
                signal_dict["dbc"] = signal_json
            
            elif signal.name == 'EtasSteeringAngle129':
                vss_math = 'floor(x+0.5)'
                signal_json = {"signal" : signal.name, "interval_ms" : 100, "transform": {"math" : vss_math}}
                signal_dict["dbc"] = signal_json
                # messages_dict[message.name] = message_json

            elif signal.name == 'EtasVCSeat_row1XPosition':
                vss_min = vspec_dict[message.name]['min']
                vss_unit_value = vspec_dict[message.name]['unit']
                vss_signal_description = vspec_dict[message.name]['description']

                message_json = {"datatype" : vss_datatype_value, "type": vss_type_value, "min" : vss_min, 
                "unit" : vss_unit_value, "description" : vss_signal_description}
                messages_dict[message.name] = message_json
                signal_dict = messages_dict[message.name]

                signal_json = {"signal" : signal.name, "interval_ms" : 100}
                signal_dict["dbc"] = signal_json

            elif signal.name == 'EtasVCSeat_row1ZPosition':
                vss_min = vspec_dict[message.name]['min']
                vss_unit_value = vspec_dict[message.name]['unit']
                vss_signal_description = vspec_dict[message.name]['description']

                message_json = {"datatype" : vss_datatype_value, "type": vss_type_value, "min" : vss_min, 
                "unit" : vss_unit_value, "description" : vss_signal_description}
                messages_dict[message.name] = message_json
                signal_dict = messages_dict[message.name]

                signal_json = {"signal" : signal.name, "interval_ms" : 100}
                signal_dict["dbc"] = signal_json

            elif signal.name == 'EtasVehicleSpeed':
                signal_json = {"signal" : signal.name, "interval_ms" : 100}
                signal_dict["dbc"] = signal_json
            
            elif signal.name == 'EtasVCFRONT_tempAmbientFiltered':
                signal_json = {"signal" : signal.name, "interval_ms" : 1000}
                signal_dict["dbc"] = signal_json

            # else:
            #     message_json = {}
            #     messages_dict[message.name] = message_json

    output_all = messages_dict
    with open('mapping_overlay' + '.json', 'w') as outfile:
        json.dump(output_all, outfile, indent=2)
    print(inputfiledbc + ' has been mapped')
    print("Finished")

if __name__ == '__main__':
   main(sys.argv[1:])
