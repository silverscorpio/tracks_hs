import re
import json
from collections import defaultdict


def match_regex(template: re.Pattern[str], given_str: str) -> bool:
    match = re.search(template, given_str)
    if match:
        return True
    return False


class Validator:
    BUS_ID_REGEX = ""
    STOP_ID_REGEX = ""
    STOP_NAME_REGEX = re.compile(r"[A-Z]{1}. Road|Avenue|Boulevard|Street", flags=re.ASCII)
    NEXT_STOP_REGEX = ""
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

    def report_errors(self, format_errors: False):
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
