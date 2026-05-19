from typing import List
from models import Zone
from pydantic import ValidationError
import pprint

class NegativeError(Exception):
    pass

class MapParser():
    def __init__(self, map_path):
        self.map_path = map_path
        self.map = self.read_lines(self.map_path)
        self.zones = {}
        self.nb_drones = 0
        self.start_hub : Zone = None
        self.end_hub : Zone = None
        self.connections : List = []
        self.invalid_format = "Invalid zone format. (eg: hub: zone 3 0 [color=orange max_drones=1])"


    @staticmethod
    def empty(line: str) -> bool:
        return line.strip().startswith('#') or not line.strip()


    @staticmethod
    def read_lines(map_path: str) -> List[str]:
        map = ''
        with open(map_path, 'r') as f:
            map = f.read()
        return [line.strip() for line in map.split('\n') if not MapParser.empty(line)]


    def parse_map(self) -> bool:
        if not self.map:
            raise ValueError('The map file is empty.')
        for index, line in enumerate(self.map):
            '''
            Handling the nb_drones case:
            Requirements:
                - Number of drones should be a positive integer.
                - The line indicating number of drones should be on top of the file.
                - There should be only one line for the number of drones
            '''
            
            if all(not line.startswith(prefix) for prefix in ['start_hub'
                                                              ,'end_hub'
                                                              ,'hub'
                                                              ,'nb_drones'
                                                              ,'connection']):
                raise ValueError(f'Error in line {index} : "{line}",'
                                 ' the line does not indicate any valid zone')
            if not index and not line.startswith('nb_drones'):
                raise ValueError('The very first line should ' \
                'indicate the number of drones.')

            # Handling the case of the number of drones
            if line.startswith('nb_drones'):
                if index:
                    raise ValueError('You can only set the number of drones once.')
                elif not index:
                    if len(line.split(':')) != 2:
                        raise ValueError('The line indicating number'
                        'of drones is not of the correct format'
                        ' (eg: "nb_drones: 2")')
                    try:
                        self.nb_drones = int(line.split(':')[1])
                        if self.nb_drones <= 0:
                            raise NegativeError('The number of drones should be positive.')
                    except NegativeError as e:
                        raise e
                    except ValueError:
                        raise ValueError('The number of drones should be an integer.')

            # Handling the case of zones
            elif line.startswith(('start_hub', 'hub', 'end_hub')):

                hub_line = (line.split(':', 1)[1]).strip().split(None, 3)

                if len(hub_line) not in (3, 4):
                    raise ValueError(f'Error in line {index}: "{" ".join(hub_line)}": {self.invalid_format} ')
                if len(hub_line) == 4 and (hub_line[-1].count('[') != 1 or
                                        hub_line[-1].count(']') != 1):
                    raise ValueError(f'Error in line {index}: "{" ".join(hub_line)}": {self.invalid_format} ')

                if len(hub_line) == 4 and (not hub_line[-1].strip().startswith('[')
                                        or hub_line[-1][-1].strip() != ']'):
                    raise ValueError(f'Error in line {index}: "{" ".join(hub_line)}": {self.invalid_format} ')
                metadata = {}
                if len (hub_line) == 4:
                    token = hub_line[3].strip('[]').replace('=', ' = ').split()
                    if len(token) % 3:
                        raise ValueError(f"Unsupported format: (eg: color = gray)")
                    for idx, part in enumerate(token):
                        if not idx % 3 and part not in ('max_drones', 'zone', 'color'):
                            raise ValueError(f"Parsing error in Metadata (Unexpected key): {part}")
                        if not (idx - 1) % 3 and not part == '=':
                            raise ValueError(f"Unsupported format: (eg: color = gray)")
                        if not (idx - 2) % 3:
                            if not metadata.get(token[idx - 2]):
                                metadata[token[idx - 2]] = token[idx]
                            else:
                                raise ValueError(f"Duplicated keys are not allowed ({token[idx - 2]})")
                
                if hub_line[0] in self.zones:
                        raise ValueError(f"Error in line {index}, "
                                            f'multiple zones with the name "{hub_line[0]}".')
                if line.startswith('start_hub'):
                    if not self.start_hub:
                        if not line.split(":")[0].strip() == 'start_hub':
                            raise ValueError(f'Error in line {index} : "{line}",'
                                 ' the line does not indicate any valid zone')
                        zone_coordinates = (hub_line[1], hub_line[2])
                        self.start_hub = Zone(name=hub_line[0], coordinates=zone_coordinates,
                                              **metadata, role='start_hub')
                        self.zones[hub_line[0]] = self.start_hub
                    else:
                        raise ValueError(f"Error in line {index}: You can only set the starting zone once.")

                elif line.startswith('end_hub'):
                    if not self.end_hub:
                        if not line.split(":")[0].strip() == 'end_hub':
                            raise ValueError(f'Error in line {index} : "{line}",'
                                 ' the line does not indicate any valid zone')
                        zone_coordinates = (hub_line[1], hub_line[2])
                        self.end_hub = Zone(name=hub_line[0], coordinates=zone_coordinates,
                                            **metadata, role='end_hub')
                        self.zones[hub_line[0]] = self.end_hub
                    else:
                        raise ValueError(f"Error in line {index}: You can only set the goal zone once.")

                elif line.startswith('hub'):
                    if not line.split(":")[0].strip() == 'hub':
                            raise ValueError(f'Error in line {index} : "{line}",'
                                 ' the line does not indicate any valid zone')
                    zone_coordinates = (hub_line[1], hub_line[2])
                    zone = Zone(name=hub_line[0], coordinates=zone_coordinates,
                                **metadata, role='hub')
                    self.zones[hub_line[0]] = zone

            # Handling the case of connections
            elif line.startswith('connection'):
                #connection: gate_hell1-gate_hell2 [max_link_capacity=1]
                connection_line = line.strip().split(':')
                if connection_line[0].strip() != "connection":
                        raise ValueError(f'Error in line {index} : "{line}",'
                                ' the line does not indicate any valid zone')
                print("".join(connection_line[1]).strip().split())
                connection_data = (
                                "".join(
                                    str(connection_line[1])
                                    .strip()
                                    .split(None, 1)
                                )
                                .replace("-", " - ")
                                .replace("[", " [ ")
                                .replace("]", " ] ")
                                .replace("=", " = ")
                            )
                print(connection_data)
                if line.count("-") != 1:
                    raise ValueError(f"The connection line ({connection_data[0]}) is " 
                                      "malformed (eg: <zone01>-<zone02>)")
                for idx in range(len(connection_data.split())):
                    part = connection_data.split()[idx]
                    if not idx:
                        if not part in self.zones:
                            raise ValueError(f"Error on line {index + 1}: connection"
                            f" references unknown zone '{part}'")
                    if idx == 1 and part != "-":
                        raise ValueError(f"Error on line {index + 1}."
                        " (eg: connection: <zone01>-<zone02>)")

        #validating the existence of the starting and goal zones
        if not self.start_hub and not self.end_hub:
            raise ValueError(f"Error in line {index}: Map has no Starting zone and no Goal zone .")
        elif not self.start_hub:
            raise ValueError(f"Error in line {index}: Map has no Starting zone.")
        elif not self.end_hub:
            raise ValueError(f"Error in line {index}: Map has no Goal zone.")


red_color = '\033[91m'
green_color = '\033[92m'
end_color = '\033[0m'
yellow_color = '\033[93m'
blue_color = '\033[94m'
light_blue_color = '\033[96m'

# maps = [
#   'maps/easy/01_linear_path.txt', 
#   'maps/easy/02_simple_fork.txt', 
#   'maps/easy/03_basic_capacity.txt', 
#   'maps/medium/01_dead_end_trap.txt', 
#   'maps/medium/02_circular_loop.txt', 
#   'maps/medium/03_priority_puzzle.txt', 
#   'maps/hard/01_maze_nightmare.txt', 
#   'maps/hard/02_capacity_hell.txt', 
#   'maps/hard/03_ultimate_challenge.txt', 
#   'maps/challenger/01_the_impossible_dream.txt'
# ]

# errr = []
# for map in maps:
#     print(f"Parsing {map}...")
#     parser = MapParser(map)
#     try:
#         parser.parse_map()
#         print(f"{green_color}Parsed successfully!{end_color}")
#         print("Start Hub: ", parser.start_hub)
#         print("End Hub: ", parser.end_hub)
#         print("Other Hubs: ", {k:v for k,v in parser.zones.items() if v.role == 'hub'})
#         print("Number of Drones: ", parser.nb_drones)
#     except ValidationError as e:
#         errr.append(map)

#         for error in e.errors():    
#             print(f"{red_color}Validation Error: {error['msg']} in field {error['loc']}{end_color}")
#     except ValueError as e:
#         errr.append(map)
#         print(f"{red_color}Error: {e}{end_color}")
#     print('-----------------------------')
# if not errr:
#     print(f"{green_color}No errors found{end_color }")
# else:
#     print(f"{red_color}Errors were found in: {errr}.{end_color}")
# print('Parsing completed.')

try:
    parser = MapParser("maps/easy/02_simple_fork.txt")
    parser.parse_map()
    for k, v in parser.zones.items():
        print(f"{light_blue_color}{k}:  {v}{end_color}")
    print(f"{green_color}Parsed successfully!{end_color}")
except ValidationError as e:
    for err in e.errors():
        print(f"{red_color}{err['loc']}: {err['msg']}")
except Exception as e:
    print(f"{red_color}Error: ", e)
