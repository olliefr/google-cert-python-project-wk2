#!/usr/bin/env python3

import os
import sys
import requests
from pprint import pprint

corpweb_ip = 'a.b.c.d'
local_directory = 'data/feedback'

# The programme is run with a single argument which is the IP address
# for the API endpoint. The second optional argument is the local directory
# containing the .txt files which should be processed.
if __name__ == '__main__':
  if len(sys.argv) < 2 or len(sys.argv) > 3:
    print('Error: API endpoint IP address must be provided as an argument.')
    print(f"       Local feedback directory is optional, default = '{local_directory}'.")
    print(f"Usage: {sys.argv[0]} corpweb_ip [local_directory]", file=sys.stderr)
    sys.exit(1)

  # Both corpweb_ip and local_directory are provided as arguments
  if len(sys.argv) == 3:
    corpweb_ip      = sys.argv[-2]
    local_directory = sys.argv[-1]

  # Only corpweb_ip is provided as an argument
  if len(sys.argv) == 2:
    corpweb_ip = sys.argv[-1]

  # Construct API endpoint address
  # FIXME Does the IP address need validating? This is not a public script though.
  # corpweb_ip can be an IP address or a DNS name as well though...
  api_endpoint_url = f"http://{corpweb_ip}/feedback"

  # Read the directory contents and terminate on error.
  # Print a helpful error message on failure.
  try:
    feedback_files = os.listdir(local_directory)
  except OSError as err:
    print(f"Can't read the feedback directory '{local_directory}'.", file=sys.stderr)
    print(err, file=sys.stderr)
    sys.exit(2)

  for feedback_file in feedback_files:
    # Build a dictionary with the data from the file.
    # Assume that each feedback file has the right format, each field on its own line
    feedback = {}
    try:
      with open(os.path.join(local_directory, feedback_file)) as feedback_file_content:
        for field in ['title', 'name', 'date', 'feedback']:
          feedback[field] = feedback_file_content.readline().rstrip('\n ')
          # Assumed no empty fields, print a warning otherwise
          if feedback[field] == '':
            print(f"Warning: '{field}' is empty in '{feedback_file}' file.", file=sys.stderr)
    except OSError as err:
      print(f"Can't open the feedback file '{feedback_file}'. File skipped.", file=sys.stderr)
      print(err, file=sys.stderr)
    else:
      # At this point the content of a single feedback file was read into
      # a dictionary without error.
      pprint(feedback)
      # Using 'requests' POST the feedback dictionary to the API endpoint
      # FIXME Not using the timeout parameter, so the POST request can hang indefinitely
      try:
        response = requests.post(api_endpoint_url, json = feedback)
      except RequestException as err:
        # Something catastrophic has happened to the request,
        # it probably has not even reached the API endpoint.
        print(f"Error while connecting to the REST API. File '{feedback_file}' not uploaded.", file=sys.stderr)
      else:
        if not response.ok:
          print(f"Error returned by the API endpoint while processing '{feedback_file}'.", file=sys.stderr)
          print(f"Status code: '{response.status_code}'.", file=sys.stderr)
          print(response.headers, file=sys.stderr)
          print(response.text, file=sys.stderr)
        else:
          if response.status_code != 201:
            print("Warning: success reported but with status {response.status_code} while processing '{feedback_file}'.", file=sys.stderr)
