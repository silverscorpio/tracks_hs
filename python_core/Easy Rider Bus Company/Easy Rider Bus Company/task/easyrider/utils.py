import json
from collections import defaultdict


class Validator:
    BUS_ID_REGEX = ""
    STOP_ID_REGEX = ""
    STOP_NAME_REGEX = ""
    NEXT_STOP_REGEX = ""
    STOP_TYPE_REGEX = ""
    A_TIME_REGEX = ""

    def __init__(self, json_data: str):
        self.raw_json = json_data
        self.json: list = json.loads(self.raw_json)
        (self.bus_ids,
         self.stop_ids,
         self.stop_names,
         self.next_stops,
         self.stop_types,
         self.a_times) = self.extract_fields()

        self.errors = defaultdict(dict)

    def extract_fields(self):
        return (
            [(idx, val["bus_id"]) for idx, val in enumerate(self.json)],
            [(idx, val["stop_id"]) for idx, val in enumerate(self.json)],
            [(idx, val["stop_name"]) for idx, val in enumerate(self.json)],
            [(idx, val["next_stop"]) for idx, val in enumerate(self.json)],
            [(idx, val["stop_type"]) for idx, val in enumerate(self.json)],
            [(idx, val["a_time"]) for idx, val in enumerate(self.json)]
        )

    def report_errors(self):
        total_type_errors = sum([v["type"] for v in self.errors.values()])
        total_required_errors = sum([v["required"] for v in self.errors.values()])

        field_errors = defaultdict(int)
        for k, v in self.errors.items():
            field_errors[k] = sum([v["type"], v["required"]])

        print(f"""
Type and required field validation: {total_type_errors + total_required_errors} errors
bus_id: {field_errors["bus_id"]}
stop_id: {field_errors["stop_id"]}
stop_name: {field_errors["stop_name"]}
next_stop: {field_errors["next_stop"]}
stop_type: {field_errors["stop_type"]}
a_time: {field_errors["a_time"]}""")

    # field/db column validators
    def bus_id_validator(self):
        # integer
        for val in self.bus_ids:
            if not isinstance(val[1], int):
                self.errors["bus_id"]["type"] += 1

            if not val[1]:
                self.errors["bus_id"]["required"] += 1

    def stop_id_validator(self):
        # integer
        for val in self.stop_ids:
            if not isinstance(val[1], int):
                self.errors["stop_id"]["type"] += 1

            if not val[1]:
                self.errors["stop_id"]["required"] += 1

    def stop_name_validator(self):
        # string
        for val in self.stop_names:
            if not isinstance(val[1], str):
                self.errors["stop_name"]["type"] += 1

            if not val[1]:
                self.errors["stop_name"]["required"] += 1

    def next_stop_validator(self):
        # integer
        for val in self.next_stops:
            if not isinstance(val[1], int):
                self.errors["next_stop"]["type"] += 1

            if not val[1]:
                self.errors["next_stop"]["required"] += 1

    def stop_type_validator(self):
        # char (string)
        for val in self.stop_types:
            if not isinstance(val[1], str):
                self.errors["stop_type"]["type"] += 1

            if not val[1]:
                self.errors["stop_type"]["required"] += 1

    def a_time_validator(self):
        # string
        for val in self.a_times:
            if not isinstance(val[1], str):
                self.errors["a_time"]["type"] += 1

            if not val[1]:
                self.errors["a_time"]["required"] += 1
