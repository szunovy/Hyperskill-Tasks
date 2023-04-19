import json
import re
import itertools
import nltk
# my_input = [
#     {"bus_id" : 128, "stop_id" : 1, "stop_name" : "Fifth Avenue", "next_stop" : 4, "stop_type" : "S", "a_time" : "08:12"},
#     {"bus_id" : 128, "stop_id" : 4, "stop_name" : "abbey Road", "next_stop" : 5, "stop_type" : "FF", "a_time" : "08:19"},
#     {"bus_id" : 128, "stop_id" : 5, "stop_name" : "Santa Monica Boulevard", "next_stop" : 8, "stop_type" : "O", "a_time" : "two"},
#     {"bus_id" : 128, "stop_id" : 8, "stop_name" : "Elm Street Str.", "next_stop" : 11, "stop_type" : "", "a_time" : "08:37"},
#     {"bus_id" : 128, "stop_id" : 11, "stop_name" : "Beale Street", "next_stop" : 12, "stop_type" : "", "a_time" : "39:20"},
#     {"bus_id" : 128, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 14, "stop_type" : "", "a_time" : "09:95"},
#     {"bus_id" : 128, "stop_id" : 14, "stop_name" : "Bourbon street", "next_stop" : 19, "stop_type" : "O", "a_time" : "09:59"},
#     {"bus_id" : 128, "stop_id" : 19, "stop_name" : "Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "10:12"},
#     {"bus_id" : 256, "stop_id" : 2, "stop_name" : "Pilotow Street", "next_stop" : 3, "stop_type" : "S", "a_time" : "08.13"},
#     {"bus_id" : 256, "stop_id" : 3, "stop_name" : "Startowa Street", "next_stop" : 8, "stop_type" : "d", "a_time" : "08:16"},
#     {"bus_id" : 256, "stop_id" : 8, "stop_name" : "Elm", "next_stop" : 10, "stop_type" : "", "a_time" : "08:29"},
#     {"bus_id" : 256, "stop_id" : 10, "stop_name" : "Lombard Street", "next_stop" : 12, "stop_type" : "", "a_time" : "08;44"},
#     {"bus_id" : 256, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 13, "stop_type" : "O", "a_time" : "08:46"},
#     {"bus_id" : 256, "stop_id" : 13, "stop_name" : "Orchard Road", "next_stop" : 16, "stop_type" : "", "a_time" : "09:13"},
#     {"bus_id" : 256, "stop_id" : 16, "stop_name" : "Sunset Boullevard", "next_stop" : 17, "stop_type" : "O", "a_time" : "09:26"},
#     {"bus_id" : 256, "stop_id" : 17, "stop_name" : "Khao San Road", "next_stop" : 20, "stop_type" : "o", "a_time" : "10:25"},
#     {"bus_id" : 256, "stop_id" : 20, "stop_name" : "Michigan Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "11:26"},
#     {"bus_id" : 512, "stop_id" : 6, "stop_name" : "Arlington Road", "next_stop" : 7, "stop_type" : "s", "a_time" : "11:06"},
#     {"bus_id" : 512, "stop_id" : 7, "stop_name" : "Parizska St.", "next_stop" : 8, "stop_type" : "", "a_time" : "11:15"},
#     {"bus_id" : 512, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : 9, "stop_type" : "", "a_time" : "11:76"},
#     {"bus_id" : 512, "stop_id" : 9, "stop_name" : "Niebajka Av.", "next_stop" : 15, "stop_type" : "", "a_time" : "12:20"},
#     {"bus_id" : 512, "stop_id" : 15, "stop_name" : "Jakis Street", "next_stop" : 16, "stop_type" : "", "a_time" : "12:44"},
#     {"bus_id" : 512, "stop_id" : 16, "stop_name" : "Sunset Boulevard", "next_stop" : 18, "stop_type" : "", "a_time" : "13:01"},
#     {"bus_id" : 512, "stop_id" : 18, "stop_name" : "Jakas Avenue", "next_stop" : 19, "stop_type" : "", "a_time" : "14:00"},
#     {"bus_id" : 1024, "stop_id" : 21, "stop_name" : "Karlikowska Avenue", "next_stop" : 12, "stop_type" : "S", "a_time" : "13:01"},
#     {"bus_id" : 1024, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "14:00:00"},
#     {"bus_id" : 1024, "stop_id" : 19, "stop_name" : "Prospekt Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "14:11"}
# ]
#
# stop_names_list = [record["a_time"] for record in my_input]
# print("\n".join(stop_names_list))
# print()

# my_input = [
#     {
#         "bus_id": 128,
#         "stop_id": 1,
#         "stop_name": "Prospekt Avenue",
#         "next_stop": 3,
#         "stop_type": "S",
#         "a_time": 8.12
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 3,
#         "stop_name": "",
#         "next_stop": 5,
#         "stop_type": "",
#         "a_time": "08:19"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 5,
#         "stop_name": "Fifth Avenue",
#         "next_stop": 7,
#         "stop_type": "O",
#         "a_time": "08:25"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": "7",
#         "stop_name": "Sesame Street",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "08:37"
#     },
#     {
#         "bus_id": "",
#         "stop_id": 2,
#         "stop_name": "Pilotow Street",
#         "next_stop": 3,
#         "stop_type": "S",
#         "a_time": ""
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 3,
#         "stop_name": "Elm Street",
#         "next_stop": 6,
#         "stop_type": "",
#         "a_time": "09:45"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 6,
#         "stop_name": "Sunset Boulevard",
#         "next_stop": 7,
#         "stop_type": "",
#         "a_time": "09:59"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 7,
#         "stop_name": "Sesame Street",
#         "next_stop": "0",
#         "stop_type": "F",
#         "a_time": "10:12"
#     },
#     {
#         "bus_id": 512,
#         "stop_id": 4,
#         "stop_name": "Bourbon Street",
#         "next_stop": 6,
#         "stop_type": "S",
#         "a_time": "08:13"
#     },
#     {
#         "bus_id": "512",
#         "stop_id": 6,
#         "stop_name": "Sunset Boulevard",
#         "next_stop": 0,
#         "stop_type": 5,
#         "a_time": "08:16"
#     }
# ]

my_input = [{"bus_id" : 128, "stop_id" : 1, "stop_name" : "Fifth Avenue", "next_stop" : 4, "stop_type" : "S", "a_time" : "08:12"}, {"bus_id" : 128, "stop_id" : 4, "stop_name" : "abbey Road", "next_stop" : 5, "stop_type" : "FF", "a_time" : "08:19"},  {"bus_id" : 128, "stop_id" : 5, "stop_name" : "Santa Monica Boulevard", "next_stop" : 8, "stop_type" : "O", "a_time" : "two"},  {"bus_id" : 128, "stop_id" : 8, "stop_name" : "Elm Street Str.", "next_stop" : 11, "stop_type" : "", "a_time" : "08:37"},  {"bus_id" : 128, "stop_id" : 11, "stop_name" : "Beale Street", "next_stop" : 12, "stop_type" : "", "a_time" : "39:20"},  {"bus_id" : 128, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 14, "stop_type" : "", "a_time" : "09:95"},  {"bus_id" : 128, "stop_id" : 14, "stop_name" : "Bourbon street", "next_stop" : 19, "stop_type" : "O", "a_time" : "09:59"},  {"bus_id" : 128, "stop_id" : 19, "stop_name" : "Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "10:12"},  {"bus_id" : 256, "stop_id" : 2, "stop_name" : "Pilotow Street", "next_stop" : 3, "stop_type" : "S", "a_time" : "08.13"},  {"bus_id" : 256, "stop_id" : 3, "stop_name" : "Startowa Street", "next_stop" : 8, "stop_type" : "d", "a_time" : "08:16"},  {"bus_id" : 256, "stop_id" : 8, "stop_name" : "Elm", "next_stop" : 10, "stop_type" : "", "a_time" : "08:29"},  {"bus_id" : 256, "stop_id" : 10, "stop_name" : "Lombard Street", "next_stop" : 12, "stop_type" : "", "a_time" : "08;44"},  {"bus_id" : 256, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 13, "stop_type" : "O", "a_time" : "08:46"},  {"bus_id" : 256, "stop_id" : 13, "stop_name" : "Orchard Road", "next_stop" : 16, "stop_type" : "", "a_time" : "09:13"},  {"bus_id" : 256, "stop_id" : 16, "stop_name" : "Sunset Boullevard", "next_stop" : 17, "stop_type" : "O", "a_time" : "09:26"},  {"bus_id" : 256, "stop_id" : 17, "stop_name" : "Khao San Road", "next_stop" : 20, "stop_type" : "o", "a_time" : "10:25"},  {"bus_id" : 256, "stop_id" : 20, "stop_name" : "Michigan Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "11:26"},  {"bus_id" : 512, "stop_id" : 6, "stop_name" : "Arlington Road", "next_stop" : 7, "stop_type" : "s", "a_time" : "11:06"},  {"bus_id" : 512, "stop_id" : 7, "stop_name" : "Parizska St.", "next_stop" : 8, "stop_type" : "", "a_time" : "11:15"},  {"bus_id" : 512, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : 9, "stop_type" : "", "a_time" : "11:76"},  {"bus_id" : 512, "stop_id" : 9, "stop_name" : "Niebajka Av.", "next_stop" : 15, "stop_type" : "", "a_time" : "12:20"},  {"bus_id" : 512, "stop_id" : 15, "stop_name" : "Jakis Street", "next_stop" : 16, "stop_type" : "", "a_time" : "12:44"},  {"bus_id" : 512, "stop_id" : 16, "stop_name" : "Sunset Boulevard", "next_stop" : 18, "stop_type" : "", "a_time" : "13:01"},  {"bus_id" : 512, "stop_id" : 18, "stop_name" : "Jakas Avenue", "next_stop" : 19, "stop_type" : "", "a_time" : "14:00"},  {"bus_id" : 1024, "stop_id" : 21, "stop_name" : "Karlikowska Avenue", "next_stop" : 12, "stop_type" : "S", "a_time" : "13:01"},  {"bus_id" : 1024, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "14:00:00"},  {"bus_id" : 1024, "stop_id" : 19, "stop_name" : "Prospekt Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "14:11"}]
# print('\n'.join(record['a_time'] for record in my_input))
# print('end')


# DATABASE_JSON = my_input

stop_types = ('S', 'O', 'F', '')
required_fields = ('bus_id', 'stop_id', 'stop_name', 'next_stop', 'a_time')
fields_structure_dict = {
    'bus_id': {'required': 1, 'type': 'int', 'format': ''},
    'stop_id': {'required': 1, 'type': 'int', 'format': ''},
    'stop_name': {'required': 1, 'type': 'str', 'format': '[A-Z][a-z]* (Road|Avenue|Boulevard|Street)$'},
    'next_stop': {'required': 1, 'type': 'int', 'format': ''},
    'stop_type': {'required': 0, 'type': 'char', 'format': '(^[SOF]$|^$)'},
    'a_time': {'required': 1, 'type': 'str', 'format': '^([01]\d|2[0-3]):[0-5]\d$'}
}


# check if it can be one by comprehension
for key in fields_structure_dict:
    fields_structure_dict[key].update(error = 0)


# # fields_dict['stop_type'] = {'error': 0}

# errors_amount = 0

# checks whether datatypes in the base are correct with documentation
def check_data_type():
    for record in DATABASE_JSON:
        # print(record)
        for field, value in fields_structure_dict.items():
            if value['required'] == 1 and record[field] == '':
                value['error'] += 1
                continue
            #  correct type check (first for char, then for else)
            if value['type'] == 'char':
                if isinstance(record[field], str):
                    if  len(record[field]) > 1:
                        value['error'] += 1
                        continue
                else:
                    value['error'] += 1
                    continue
            else:
                # correct type check
                if not isinstance(record[field], eval(fields_structure_dict[field]['type'])):
                    value['error'] += 1
                    continue
            #  check if stop type is in given possible values
            if field == 'stop_type' and record['stop_type'] not in (stop_types or ''):
                fields_structure_dict['stop_type']['error'] += 1
                continue

    errors_sum = 0
    errors_sum = sum([value['error'] for value in fields_structure_dict.values()])
    
    print(f'Type and required field validation: {errors_sum} errors')
    for field, value     in fields_structure_dict.items():
        print(f'{field}: {value["error"]}')

# checks if syntax of data in the base is correct with documentation
def check_syntax():

    stop_names_erors = []
    for record in DATABASE_JSON:
        # print(record['a_time'])
        # print(record)
        for field, value in fields_structure_dict.items():
            if value['format'] and type(record[field]) == str:
                if not (re.search(value['format'], record[field])):
                    # if field == 'a_time':
                    #     print(record[field])
                    #     print()
                    value['error'] += 1
    errors_sum = 0


    errors_sum = sum([value['error'] for value in fields_structure_dict.values()])

    print(f'Format validation: {errors_sum} errors')

    for field, value in fields_structure_dict.items():
        if value['format']:
            print(f"{field}: {value['error']}")


#  creates list of bus stops ids and their types for each line
# pass argument 1 to print
def get_bus_lines(print_tag = 0):
    bus_lines = {}
    #make list of every bus line in database
    for record in DATABASE_JSON:
        if record['bus_id'] not in bus_lines:
            bus_lines[record['bus_id']] = {'stops':[]}

    # print(bus_lines)
    for record in DATABASE_JSON:
        for key, values in bus_lines.items():
            if record['bus_id'] == key and record['stop_id'] not in values['stops']:
                values['stops'].append([record['stop_id'], record['stop_type'], record['stop_name']])
    # print(bus_lines)
    if print_tag == 1:
        for key, values in bus_lines.items():
            print(f'bus_id: {key}, stops: {len(values["stops"])}')
    return bus_lines

# checks amount of bus stops and
def check_bus_stops(print_tag = 0):
    # stop types: S-start, F-stop, T-transfer
    stop_type_dict = {'S':[], 'T':[],'F':[]}
    # variables for checking if every line has start and stop in db
    bus_stops_dict = get_bus_lines()
    for line_id, data in bus_stops_dict.items():
        start_counter = 0
        end_counter = 0
        for stop in data['stops']:
            if stop[1] == 'S':
                start_counter += 1
                if stop not in stop_type_dict['S']:
                    stop_type_dict['S'].append((stop[0], stop[2]))
            elif stop[1] == 'F':
                end_counter += 1
                if stop not in stop_type_dict['F']:
                    stop_type_dict['F'].append((stop[0], stop[2]))
            # elif stop[1] in  {'O', ''}:
            #     stop_type_dict['T'].append(stop)
            # print(stop)
            # print( [bus_stops_dict[k]['stops'][0, 2] for k in bus_stops_dict.keys() -{line_id}][0])
            # print(stop[0])
            #
            # if stop[0] in [bus_stops_dict[k]['stops'][0] for k in bus_stops_dict.keys() - {line_id}][0] and stop not in stop_type_dict['T']:
            #     print('tak')
            #     print(stop)
            #     stop_type_dict['T'].append(stop)
            for k in bus_stops_dict.keys() - {line_id}:
                for elems in bus_stops_dict[k]['stops']:
                    if stop[0]==elems[0] and stop[0] not in [ems[0] for ems in stop_type_dict['T']]:
                        stop_type_dict['T'].append((stop[0], stop[2]))


            # if stop not in [k[3] for k in stop_type_dict.keys() - {line_id}]
        if not start_counter == 1 or not end_counter == 1:
            print(f'There is no start or end stop for the line: {line_id}.')
            return
    # print(stop_type_dict)
    if print_tag == 1:
        print(f'Start stops: {len(stop_type_dict["S"])}', sorted([stop[1] for stop in stop_type_dict['S']]))
        print(f'Transfer stops: {len(stop_type_dict["T"])}', sorted([stop[1] for stop in stop_type_dict['T']]))
        print(f'Finish stops: {len(stop_type_dict["F"])}', sorted([stop[1] for stop in stop_type_dict['F']]))
    return stop_type_dict

def check_arrival_time():
    wrong_info = None
    bus_lines = []
    #make list of every bus line in database
    for record in DATABASE_JSON:
        if record['bus_id'] not in bus_lines:
            bus_lines.append(record['bus_id'])
    # print(bus_lines)
    for line_id in bus_lines:
        temp_line_data = [record for record in DATABASE_JSON if record['bus_id'] == line_id]
        for index, record in enumerate(temp_line_data):
            # getting starting stop and removing it from temporary list of stops for current line
            if record['stop_type'] == 'S':
                current_stop = temp_line_data.pop(index)
                break
        time_current = current_stop['a_time']

        # with each iteration record of next stop is popped from list, so loop until its not empty
        while temp_line_data:
            # print(temp_line_data)
            next_stop_index = next((index for (index, record) in enumerate(temp_line_data) if record["stop_id"] == current_stop['next_stop']), None)

            next_stop = temp_line_data.pop(next_stop_index)
            # print(next_stop['stop_id'])
            if current_stop['a_time'] > next_stop['a_time']:
                # initialize the list if it wasnt earlier for saving memory
                if wrong_info is None:
                    wrong_info = []
                # create list with wrong records info tuples [0] - line id, [1] stop name, to print later
                # and break from loop with first error found
                wrong_info.append((line_id, next_stop['stop_name']))
                break
            # stepping to next stop
            current_stop = next_stop

    # printing results
    print('Arrival time test:')
    if wrong_info is None:
        print('OK')
    else:
        # in record[0] is line id, [1] is stop name with error
        for record in wrong_info:
            print(f'bus_id line {record[0]}: wrong time on station {record[1]}')


# check whether start, final and transfer stops are not on demand
def check_stops_demand():
    wrong_stop_demand = None
    stops_STF = check_bus_stops()
    # print(stops_STF)

    stops_on_demand = [(record['stop_id'], record['stop_name']) for record in DATABASE_JSON if record['stop_type'] == 'O']
    # print(stops_on_demand)
    # for elements in itertools.chain.from_iterable(values for key, values in stops_STF.items()):
    #     print(elements)

    for stop in stops_on_demand:
        if stop in itertools.chain.from_iterable([values for key, values in stops_STF.items()]):
            # print(stop)
            if wrong_stop_demand is None:
                wrong_stop_demand = []
            wrong_stop_demand.append(stop)

    print('On demand stops test:')
    if wrong_stop_demand is None:
        print('OK')
    else:
        print(f'wrong stop type', [stop_record[1] for stop_record in sorted(wrong_stop_demand, key=lambda x: x[1])])
        # print(sorted(wrong_stop_demand))

def main():
    global DATABASE_JSON
    DATABASE_JSON = json.loads(input())


    # DATABASE_JSON = my_input
    # global bus_stops_dict
    # bus_stops_dict = get_bus_lines()
    # print('calosc')
    # print(bus_stops_dict)
    # check_bus_stops()
    # check_syntax()

    # check_arrival_time()

    check_stops_demand()


if __name__ == "__main__":
    main()