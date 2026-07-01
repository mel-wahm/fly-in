from typing import Dict, List, Tuple, cast
from models import Zone, Connection

red_color = '\033[91m'
bold_font = '\033[1m'
end_color = '\033[0m'


class NegativeError(Exception):
    pass


class MapParser():
    def __init__(self, map_path: str) -> None:
        self.map_path = map_path
        self.map = self.read_lines(self.map_path)
        self.zones: Dict[str, Zone] = {}
        self.nb_drones = 0
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None
        self.connections: List = []
        self.invalid_format = (
            "Invalid zone format. "
            "(eg: hub: zone 3 0 [color=orange max_drones=1])"
        )

    @staticmethod
    def empty(line: str) -> bool:
        return line.strip().startswith('#') or not line.strip()

    @staticmethod
    def read_lines(map_path: str) -> List[str]:
        map = ''
        with open(map_path, 'r') as f:
            map = f.read()
        return [line.strip() for line in map.split('\n')]

    def parse_map(self) -> bool:
        if not self.map:
            raise ValueError('The map file is empty.')
        valid_lines = 0
        for index, line in enumerate(self.map):
            '''
            Handling the nb_drones case:
            Requirements:
                - Number of drones should be a positive integer.
                - The line indicating number of drones should be on top
                  of the file.
                - There should be only one line for the number of drones
            '''
            if MapParser.empty(line):
                continue
            line = line.split('#')[0].strip()
            if all(not line.startswith(prefix) for prefix in [
                    'start_hub', 'end_hub', 'hub', 'nb_drones',
                    'connection']):
                raise ValueError(
                    f"Error in line {index + 1}: unknown directive "
                    f"'{line.split(':')[0].strip()}'. Expected one of: "
                    "nb_drones, start_hub, end_hub, hub, connection.")
            if not index and not line.startswith('nb_drones'):
                raise ValueError(
                    f'Error in line {index + 1}: The very first line '
                    'should indicate the number of drones.')

            # Handling the case of the number of drones
            if line.startswith('nb_drones'):
                if valid_lines:
                    if self.nb_drones == 0:
                        raise ValueError(
                            f'Error in line {index + 1}: The first line '
                            'should indicate the number of drones.')
                    else:
                        raise ValueError(
                            f'Error in line {index + 1}: You can only set '
                            'the number of drones once.')
                else:
                    if len(line.split(':')) != 2:
                        raise ValueError(
                            f'Error in line {index + 1}: The line '
                            'indicating number'
                            'of drones is not of the correct format'
                            ' (eg: "nb_drones: 2")')
                    try:
                        self.nb_drones = int(line.split(':')[1])
                        if self.nb_drones <= 0:
                            raise NegativeError(
                                f'Error in line {index + 1}: The number '
                                'of drones should be positive.')
                    except NegativeError as e:
                        raise e
                    except ValueError:
                        raise ValueError(
                            f'Error in line {index + 1}: The number of '
                            'drones should be an integer.')

            # Handling the case of zones
            elif line.startswith(('start_hub', 'hub', 'end_hub')):

                hub_line = (line.split(':', 1)[1]).strip().split(None, 3)
                if line.split(":")[0].strip() not in (
                        'start_hub', 'hub', 'end_hub'):
                    raise ValueError(
                        f"Error in line {index + 1}: unknown directive "
                        f"'{line.split(':')[0].strip()}'. Expected one "
                        "of: nb_drones, start_hub, end_hub, hub, "
                        "connection.")

                if len(hub_line) not in (3, 4):
                    raise ValueError(
                        f'Error in line {index + 1}: '
                        f'"{" ".join(hub_line)}": {self.invalid_format} ')
                if len(hub_line) == 4 and (
                        hub_line[-1].count('[') != 1
                        or hub_line[-1].count(']') != 1):
                    raise ValueError(
                        f'Error in line {index + 1}: '
                        f'"{" ".join(hub_line)}": {self.invalid_format} ')
                if len(hub_line) == 4 and (
                        not hub_line[-1].strip().startswith('[')
                        or hub_line[-1][-1].strip() != ']'):
                    raise ValueError(
                        f'Error in line {index + 1}: '
                        f'"{" ".join(hub_line)}": {self.invalid_format} ')
                metadata: Dict[str, str] = {}
                if len(hub_line) == 4:
                    token = hub_line[3].strip('[]').replace(
                        '=', ' = ').split()
                    if not token:
                        raise ValueError(
                            f"Error in line {index + 1}: Unsupported "
                            f"metadata format {token}."
                            " (eg: [color=yellow])")
                    if len(token) % 3:
                        raise ValueError(
                            f"Error in line {index + 1}: Unsupported "
                            "metadata format: (eg: color = gray)")
                    for idx, part in enumerate(token):
                        if not idx % 3 and part not in (
                                'max_drones', 'zone', 'color'):
                            raise ValueError(
                                f"Error in line {index + 1}: Parsing "
                                f"error in Metadata (Unexpected key): "
                                f"{part}")
                        if not (idx - 1) % 3 and not part == '=':
                            raise ValueError(
                                f"Error in line {index + 1}: Unsupported "
                                "format: (eg: color = gray)")
                        if not (idx - 2) % 3:
                            if not metadata.get(token[idx - 2]):
                                metadata[token[idx - 2]] = token[idx].lower()

                            else:
                                raise ValueError(
                                    f"Error in line {index + 1}: "
                                    "Duplicated keys are not allowed "
                                    f"({token[idx - 2]})")

                if hub_line[0] in self.zones:
                    raise ValueError(
                        f"Error in line {index + 1}: multiple zones "
                        f'with the name "{hub_line[0]}".')

                zone_coordinates = (hub_line[1], hub_line[2])
                try:
                    x, y = list(map(int, zone_coordinates))
                except ValueError:

                    raise ValueError(
                        f"Error in line {index + 1}: The coordinates of "
                        "the zone can be only integers")
                if any((x, y) == self.zones[zone].coordinates
                       for zone in self.zones):
                    raise ValueError(
                        f"Error in line {index + 1}: Two zones share "
                        f"the same coordinates {(x, y)}")

                if line.startswith('start_hub'):
                    if not self.start_hub:
                        self.start_hub = Zone(
                            name=hub_line[0],
                            coordinates=cast(Tuple[int, int],
                                             zone_coordinates),
                            **metadata,  # type: ignore[arg-type]
                            role='start_hub')  # type: ignore[arg-type]
                        self.zones[hub_line[0]] = self.start_hub
                    else:
                        raise ValueError(
                            f"Error in line {index + 1}: You can only "
                            "set the starting zone once.")

                elif line.startswith('end_hub'):
                    if not self.end_hub:
                        self.end_hub = Zone(
                            name=hub_line[0],
                            coordinates=cast(Tuple[int, int],
                                             zone_coordinates),
                            **metadata,  # type: ignore[arg-type]
                            role='end_hub')  # type: ignore[arg-type]
                        if 'max_drones' in metadata:
                            if int(metadata['max_drones']) < self.nb_drones:
                                print(
                                    f"{red_color}{bold_font}Warning: Not "
                                    "enough drones for the end hub. "
                                    f"Defaulting to {self.nb_drones}"
                                    f"{end_color}")
                                self.end_hub.max_drones = self.nb_drones
                        else:
                            self.end_hub.max_drones = self.nb_drones
                        self.zones[hub_line[0]] = self.end_hub
                    else:
                        raise ValueError(
                            f"Error in line {index + 1}: You can only "
                            "set the goal zone once.")

                elif line.startswith('hub'):
                    zone = Zone(
                        name=hub_line[0],
                        coordinates=cast(Tuple[int, int], zone_coordinates),
                        **metadata,  # type: ignore[arg-type]
                        role='hub')  # type: ignore[arg-type]
                    self.zones[hub_line[0]] = zone

            # Handling the case of connections
            elif line.startswith('connection'):
                connection_line = line.strip().split(':')
                if connection_line[0].strip() != "connection":
                    raise ValueError(
                        f'Error in line {index + 1}: "{line}",'
                        ' the line does not indicate any valid zone')

                connection_data = (
                    " ".join(
                        str(connection_line[1])
                        .strip()
                        .split(None, 3)
                    )
                    .replace("-", " - ", 1)
                )
                connection_data = connection_data.split(
                    # type: ignore[assignment]
                    None, 3)
                if len(connection_data) < 3:
                    raise ValueError(
                        f"Error in line {index + 1}: The connection "
                        f"line ({' '.join(connection_data)}) is "
                        "malformed (eg: <zone1>-<zone2>)")
                z1 = None
                z2 = None
                mx = None
                for idx in range(len(connection_data)):
                    part = connection_data[idx]
                    if not idx:
                        if part not in self.zones:
                            raise ValueError(
                                f"Error in line {index + 1}: connection"
                                f" references unknown zone '{part}'")
                        z1 = part
                    if idx == 1 and part != "-":
                        raise ValueError(
                            f"Error in line {index + 1}:"
                            " (eg: connection: <zone1>-<zone2>)")
                    if idx == 2:
                        if part not in self.zones:
                            raise ValueError(
                                f"Error in line {index + 1}: connection"
                                f" references unknown zone '{part}'")
                        z2 = part
                    if idx == 3:
                        if part[0] != '[' or part[-1] != ']' \
                                or part.count(']') != 1 \
                                or part.count('[') != 1:
                            raise ValueError(
                                f"Error in line {index + 1}: Unsupported "
                                f"metadata format {part}."
                                " (eg: [max_link_capacity=1])")
                        s_part = part.strip('[]').replace(
                            '=', ' = ').split(None, 2)
                        if len(s_part) != 3 \
                                or s_part[0] != 'max_link_capacity' \
                                or s_part[1] != "=":
                            raise ValueError(
                                f"Error in line {index + 1}: Unsupported "
                                f"metadata format {part}."
                                " (eg: [max_link_capacity=1])")
                        mx = s_part[2]
                if any((conn.connection == (z1, z2) or
                        conn.connection == (z2, z1))
                       for conn in self.connections):
                    raise ValueError(
                        f"Error in line {index + 1}: Duplicated "
                        f"connections ({z1}-{z2})")
                else:
                    kwargs: dict = {"connection": (z1, z2)}
                    if mx:
                        kwargs["max_link_capacity"] = mx
                        self.connections.append(Connection(**kwargs))
                    else:
                        self.connections.append(
                            Connection(
                                connection=(z1, z2)))  # type: ignore[arg-type]
            valid_lines += 1

        # validating the existence of the starting and goal zones
        if not self.start_hub and not self.end_hub:
            raise ValueError(
                "Error: Map has no Starting zone and no Goal zone .")
        elif not self.start_hub:
            raise ValueError("Error: Map has no Starting zone.")
        elif not self.end_hub:
            raise ValueError("Error: Map has no Goal zone.")
        return True
