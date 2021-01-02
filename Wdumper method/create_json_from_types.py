import json

with open('types_ids.txt') as file:
	types_list = [line.rstrip() for line in file]

output_string = ''

for type in types_list:
    json_string = '{{ "type": "item", "properties": [{{"type": "entityid","rank": "non-deprecated","value": "{type_id}","property": "P31" }} ] }}'.format(type_id=type)

    json_object = json.loads(json_string)
    json_formated = json.dumps(json_object)

    output_string += json_formated + ',\n'

with open('wdumper_json.txt', 'a') as output_file:
    output_file.write(output_string)
