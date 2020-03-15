# Copyright (C) 2020 Frederick W. Nielsen
#
# This file is part of Cisco Collaboration Tool Scripts
#
# Cisco Collaboration Cloud Tools is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Cisco Collaboration Cloud Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cisco Collaboration Cloud Tools.  If not, see <http://www.gnu.org/licenses/>.

"""
Simple flask routine for collecting HTTP POST feedback from Cisco video room endpoints
"""

import json
from datetime import datetime, timezone

from flask import Flask, request

APP = Flask(__name__)

@APP.route('/send_feedback', methods=['POST'])
def feedback_handler():
    """parse received HTTP POST data and log to file"""
    client_ip = (request.remote_addr)
    content = request.get_json()

    if 'Identification' in content[next(iter(content))]:
        content['endpoint'] = content[next(iter(content))]['Identification']['SystemName']['Value']
        del content[next(iter(content))]['Identification']

    content['time'] = datetime.now(timezone.utc)

    with open(client_ip + '.json', 'a+') as output_file:
        output_file.write(json.dumps(content, indent=1, default=str))

    return 'endpoint post processed'

APP.run(host='0.0.0.0', port=44301, ssl_context="adhoc")
