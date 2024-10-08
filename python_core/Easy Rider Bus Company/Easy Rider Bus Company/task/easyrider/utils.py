from datetime import datetime
import re
import json
from collections import defaultdict
from pprint import pprint


def match_regex(template: re.Pattern[str], given_str: str) -> bool:
    match = re.search(template, given_str)
    if match:
        return True
    return False


class Validator:
    STOP_NAME_REGEX = re.compile(r"[A-Z].* \b(?:Road|Avenue|Boulevard|Street)\b$", flags=re.ASCII)
    STOP_TYPE_REGEX = re.compile(r"^[SOF]{1}$", flags=re.ASCII)
    A_TIME_REGEX = re.compile(r"^([0-1]{1}[0-9]|2[0-3]):[0-5][0-9]$", flags=re.ASCII)

    def __init__(self, json_data: str):
        self.raw_json = json_data
        self.json: list = json.loads(self.raw_json)
        (self.bus_ids,
         self.stop_ids,
         self.stop_names,
         self.next_stops,
         self.stop_types,
         self.a_times) = self.extract_fields()
        self.start_stops, self.finish_stops, self.transfer_stops = set(), set(), set()

        self.errors = defaultdict(lambda: defaultdict(int))

    def extract_fields(self):
        return (
            [(idx, val["bus_id"]) for idx, val in enumerate(self.json)],
            [(idx, val["stop_id"]) for idx, val in enumerate(self.json)],
            [(idx, val["stop_name"]) for idx, val in enumerate(self.json)],
            [(idx, val["next_stop"]) for idx, val in enumerate(self.json)],
            [(idx, val["stop_type"]) for idx, val in enumerate(self.json)],
            [(idx, val["a_time"]) for idx, val in enumerate(self.json)]
        )

    def validate_fields(self):
        self.bus_id_validator()
        self.stop_id_validator()
        self.stop_name_validator()
        self.next_stop_validator()
        self.stop_type_validator()
        self.a_time_validator()

    def check_a_time(self):
        bus_stop_time_data = defaultdict(list)
        for i in self.json:
            bus_stop_time_data[i["bus_id"]].append((i["stop_name"], i["next_stop"], i["a_time"]))
        bus_stop_time_data_sorted = {k: v for k, v in sorted(bus_stop_time_data.items(), key=lambda v: v[1][1])}
        wrong_a_times = defaultdict(tuple)
        for k, v in bus_stop_time_data_sorted.items():
            if result_tuple := Validator.cumulative_diff_times(sequence=v):
                wrong_a_times[k] = result_tuple
        if wrong_a_times:
            print("Arrival time test:")
            for k, v in wrong_a_times.items():
                print(f"""bus_id line {k}: wrong time on station {v[0]}""")

        else:
            print("""
Arrival time test:
OK""")

    @classmethod
    def cumulative_diff_times(cls, sequence: list[tuple[str, str, str]]) -> tuple:
        sequence_datetime = [(j[0], j[1], datetime.strptime(j[2], "%H:%M")) for j in sequence]
        for idx, val in enumerate(sequence_datetime[:-1]):
            if sequence_datetime[idx + 1][2] <= val[2]:
                sequence_datetime[idx + 1] = (sequence_datetime[idx + 1][0], sequence_datetime[idx + 1][1],
                                              sequence_datetime[idx + 1][2].strftime("%H:%M"))
                return sequence_datetime[idx + 1]

    def determine_bus_stops(self, report_stops_data: bool = False):
        bus_stop_data = defaultdict(list)
        all_stops = defaultdict(int)
        for i in self.json:
            bus_stop_data[i["bus_id"]].append((i["stop_type"], i["stop_name"]))
            all_stops[i["stop_name"]] = 0
        for k, v in bus_stop_data.items():
            if any([i not in [i[0] for i in v] for i in ["S", "F"]]):
                print(f"There is no start or end stop for the line: {k}.")
                return

        for v in bus_stop_data.values():
            for i in v:
                if i[0] == "S":
                    self.start_stops.add(i[1])
                elif i[0] == "F":
                    self.finish_stops.add(i[1])

        stops_for_bus = {k: set([i[1] for i in v]) for k, v in bus_stop_data.items()}
        for k1 in all_stops:
            for v in stops_for_bus.values():
                if k1 in v:
                    all_stops[k1] += 1

        self.transfer_stops = {k for k, v in all_stops.items() if v >= 2}

        if report_stops_data:
            print(f"""
Start stops: {len(self.start_stops)} {sorted(self.start_stops)}
Transfer stops: {len(self.transfer_stops)} {sorted(self.transfer_stops)}
Finish stops: {len(self.finish_stops)} {sorted(self.finish_stops)}""")

    def check_on_demand_stops(self):
        start_transfer_finish_stops = self.start_stops.union(self.transfer_stops, self.finish_stops)
        on_demand_stops = []
        for i in self.json:
            if i["stop_name"] in start_transfer_finish_stops and i["stop_type"] == "O":
                on_demand_stops.append(i["stop_name"])

        if on_demand_stops:
            print(f"""
On demand stops test:
Wrong stop type: {sorted(on_demand_stops)}""")

        elif not on_demand_stops:
            print("""
On demand stops test:
OK""")

    def report_errors(self, format_errors=False):
        total_type_errors = sum([v["type"] for v in self.errors.values()])
        total_required_errors = sum([v["required"] for v in self.errors.values()])
        total_format_errors = sum([v["format"] for v in self.errors.values()])

        field_errors = defaultdict(int)

        for k, v in self.errors.items():
            field_errors[k] = sum([v["type"], v["required"]])

        if format_errors:
            print(f"""
Format validation: {total_format_errors} errors
stop_name: {self.errors["stop_name"]["format"]}
stop_type: {self.errors["stop_type"]["format"]}
a_time: {self.errors["a_time"]["format"]}""")

        else:
            print(f"""
Type and required field validation: {total_type_errors + total_required_errors} errors
bus_id: {field_errors["bus_id"]}
stop_id: {field_errors["stop_id"]}
stop_name: {field_errors["stop_name"]}
next_stop: {field_errors["next_stop"]}
stop_type: {field_errors["stop_type"]}
a_time: {field_errors["a_time"]}""")

    def report_bus_data(self):
        bus_data = defaultdict(list)
        for i in self.json:
            bus_data[i["bus_id"]].append(i["stop_id"])
        print("Line names and number of stops:")
        for k, v in bus_data.items():
            print(f"bus_id: {k}, stops: {len(v)}")

    # field/db column validators
    def bus_id_validator(self):
        # integer
        for val in self.bus_ids:
            if val[1] and not isinstance(val[1], int):
                self.errors["bus_id"]["type"] += 1

            if val[1] == "":
                self.errors["bus_id"]["required"] += 1

    def stop_id_validator(self):
        # integer
        for val in self.stop_ids:
            if val[1] and not isinstance(val[1], int):
                self.errors["stop_id"]["type"] += 1

            if val[1] == "":
                self.errors["stop_id"]["required"] += 1

    def stop_name_validator(self):
        # string
        for val in self.stop_names:
            # field errors
            if val[1] and not isinstance(val[1], str):
                self.errors["stop_name"]["type"] += 1

            if val[1] == "":
                self.errors["stop_name"]["required"] += 1

            # format errors
            stop_name_match = match_regex(template=Validator.STOP_NAME_REGEX, given_str=val[1])
            if not stop_name_match:
                self.errors["stop_name"]["format"] += 1

    def next_stop_validator(self):
        # integer
        for val in self.next_stops:
            if val[1] and not isinstance(val[1], int):
                self.errors["next_stop"]["type"] += 1

            if val[1] == "":
                self.errors["next_stop"]["required"] += 1

    def stop_type_validator(self):
        # char (string of len 1)
        for val in self.stop_types:
            if val[1]:
                # field type errors
                if (not isinstance(val[1], str)) or (isinstance(val[1], str) and len(val[1]) != 1):
                    self.errors["stop_type"]["type"] += 1

                # format errors
                stop_type_match = match_regex(template=Validator.STOP_TYPE_REGEX, given_str=val[1])
                if not stop_type_match:
                    self.errors["stop_type"]["format"] += 1

    def a_time_validator(self):
        # string
        for val in self.a_times:
            if val[1] and not isinstance(val[1], str):
                self.errors["a_time"]["type"] += 1

            if val[1] == "":
                self.errors["a_time"]["required"] += 1

            # format errors
            a_time_match = match_regex(template=Validator.A_TIME_REGEX, given_str=val[1])
            if not a_time_match:
                self.errors["a_time"]["format"] += 1


if __name__ == '__main__':
    pass
