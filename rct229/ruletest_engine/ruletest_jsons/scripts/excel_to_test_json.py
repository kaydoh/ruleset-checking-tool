import json
import math
import os
import copy

import pandas as pd

from rct229.ruletest_engine.ruletest_jsons.scripts.json_generation_utilities import *

# ---------------------------------------USER INPUTS---------------------------------------

spreadsheet_name = "transformer_tests_draft.xlsx"
json_name = "transformer_tests.json"
sheet_name = "TCDs"

# --------------------------------------SCRIPT STARTS--------------------------------------

file_dir = os.path.dirname(__file__)

# Define test spreadsheet path
spreadsheet_dir = "ruletest_spreadsheets"
spreadsheet_path = os.path.join(file_dir, "..", spreadsheet_dir, spreadsheet_name)

# Define output json file path
json_file_path = os.path.join(file_dir, "..", json_name)

# Pull out TCDs from spreadsheet
master_df = pd.read_excel(spreadsheet_path, sheet_name=sheet_name)

# Get headers to begin separating dictionary 'keys' from 'values'
headers = master_df.columns

# Initialize the key headers
keys = []

# If header has substring 'key', consider it a key
for header in headers:
    if "key" in header:
        keys.append(header)

# Copy columns from the spreadsheet that correspond to keys
keys_df = master_df[keys].copy()

# Get value columns (i.e. not key columns) from spreadsheet
rules_df = master_df.drop(keys, axis=1)

# Initiailize dictionary for JSON
json_dict = {}

# Strings used by triplets
triplet_strs = ["user", "proposed", "baseline"]


# Iterate column by column through values_df
for (rule_name, columnData) in rules_df.iteritems():

    # List of this rule's column data
    rule_value_list = columnData.values

    # If rule doesnt exist in dictionary
    if rule_name not in json_dict:

        # Initialize a potential json template used to build any of the RMR triplets
        rmr_template_dict = {}

        # Iterate through both keys and rule values
        for row_i in range(rule_value_list.size):

            # row_value is the value set to the JSON path generated by the key list
            row_value = rule_value_list[row_i]

            # Skip empty rows
            if not isinstance(row_value, str):
                if math.isnan(row_value):
                    continue

            # Initialize this row's list of keys (e.g. ['rule-15-1a', 'rmr_transformations', 'user', 'transformer'])
            key_list = [rule_name]

            for key in keys:
                key_value = keys_df[key][row_i]
                if isinstance(key_value, str):

                    # If the key includes a JSON_PATH, parse for the short hand enumeration name and adjust the key list
                    if "JSON_PATH" in key_value:
                        # Inject elements to key_list based on shorthand JSON_PATH enumeration
                        # (e.g., JSON_PATH:spaces = ["buildings","building_segments","thermal_blocks","zones","spaces"])
                        inject_json_path_from_enumeration(key_list, key_value)

                    else:
                        key_list.append(key_value)

            # If the final key is DICT_LIST, add the row key:value_list pair to list of dictionaries at this value
            if key_list[-1] == "DICT_LIST":

                add_to_dictionary_list(json_dict, key_list, row_value)
            else:

                # If this is a template definition, store the template for the RMR transformations
                if "rmr_template" in key_list:

                    set_nested_dict(rmr_template_dict, key_list, row_value)

                else:

                    # Set nested dictionary
                    set_nested_dict(json_dict, key_list, row_value)


        # Once all dictionaries are set, check if any of the RMR triplets utilize json templates
        if rmr_template_dict:

            # If no transformations are defined, set an empty dictionary
            if "rmr_transformations" not in json_dict[rule_name]:
                json_dict[rule_name]["rmr_transformations"] = {}

            # Read in transformations dictionary. This will perturb a template or fully define an RMR (if no template defined)
            rmr_transformations_dict = json_dict[rule_name]["rmr_transformations"]

            # Cycle through user, proposed, and baseline RMRs. Merge the template and their transformations
            for rmr_string in triplet_strs:

                # If this RMR utilizes the RMR template, merge its RMR transformations into the template and set
                # the RMR dictionary.
                if rmr_string in rmr_template_dict[rule_name]["rmr_template"]:

                    # If this RMR has no perturbations, set the RMR value equal to the template
                    if rmr_string not in rmr_transformations_dict:
                        rmr_transformations_dict[rmr_string] =  copy.deepcopy(rmr_template_dict[rule_name]["rmr_template"]["json_template"])

                    # If perturbations to the template exist, merge the transformations with the template
                    else:
                        rmr_transformations_dict[rmr_string] = merge_nested_dictionary(copy.deepcopy(rmr_template_dict[rule_name]["rmr_template"]["json_template"]), rmr_transformations_dict[rmr_string])


# Dump JSON to string for writing
json_string = json.dumps(json_dict, indent=4)

# Write JSON string to file
with open(json_file_path, "w") as json_file:
    json_file.write(json_string)
    print("JSON complete and written to file: " + json_name)
