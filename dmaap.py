from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import re
import json
import sys

posted_event_from_prh = b'Empty'
# received_event_to_get_method = b"""{'event': {
#         'notificationFields': {
#             'changeIdentifier': 'PM_MEAS_FILES',
#             'changeType': 'FileReady',
#             'notificationFieldsVersion': 1,
#             'arrayOfNamedHashMap': [
#                 {
#                     'name': 'fileFromFtps.tar.gz',
#                     'hashMap': {
#                         'location': 'ftpes://myuser:mypass@172.17.0.2:21/fileFromFtps.tar.gz',
#                         'compression': 'gzip',
#                         'fileFormatType': 'org.3GPP.32.435#measCollec',
#                         'fileFormatVersion': 'V10'
#                     }
#                 },
#                 {
#                     'name': 'fileFromSftp.tar.gz',
#                     'hashMap': {
#                         'location': 'sftp://foo:pass@172.17.0.3:22/fileFromSftp.tar.gz',
#                         'compression': 'gzip',
#                         'fileFormatType': 'org.3GPP.32.435#measCollec',
#                         'fileFormatVersion': 'V10'
#                     }
#                 }
#             ]
#         }
#     }
#     }"""
received_event_to_get_method = b"""
["{
  'event': {
    'commonEventHeader': {
      'startEpochMicrosec': 8745745764578,
      'eventId': 'FileReady_1797490e-10ae-4d48-9ea7-3d7d790b25e1',
      'timeZoneOffset': 'UTC+05.30',
      'internalHeaderFields': {
        'collectorTimeStamp': 'Tue, 09 18 2018 10:56:52 UTC'
      },
      'priority': 'Normal',
      'version': '4.0.1',
      'reportingEntityName': 'otenb5309',
      'sequence': 0,
      'domain': 'notification',
      'lastEpochMicrosec': 8745745764578,
      'eventName': 'Noti_RnNode-Ericsson_FileReady',
      'vesEventListenerVersion': '7.0.1',
      'sourceName': 'oteNB5309'
    },
    'notificationFields': {
      'notificationFieldsVersion': '2.0',
      'changeType': 'FileReady',
      'changeIdentifier': 'PM_MEAS_FILES',
      'arrayOfNamedHashMap': [
        {
          'name': 'fileFromSftp.tar.gz',
          'hashMap': {
            'fileFormatType': 'org.3GPP.32.435#measCollec',
            'location': 'sftp://foo:pass@localhost:22/fileFromSftp.tar.gz',
            'fileFormatVersion': 'V10',
            'compression': 'gzip'
          }
        }
      ]
    }
  }
}"]
"""
received_event_to_get_method = b"""
["{\"event\":{\"commonEventHeader\":{\"startEpochMicrosec\":8745745764578,\"eventId\":\"FileReady_1797490e-10ae-4d48-9ea7-3d7d790b25e1\",\"timeZoneOffset\":\"UTC+05.30\",\"internalHeaderFields\":{\"collectorTimeStamp\":\"Wed, 09 19 2018 11:39:30 UTC\"},\"priority\":\"Normal\",\"version\":\"4.0.1\",\"reportingEntityName\":\"otenb5309\",\"sequence\":0,\"domain\":\"notification\",\"lastEpochMicrosec\":8745745764578,\"eventName\":\"Noti_RnNode-Ericsson_FileReady\",\"vesEventListenerVersion\":\"7.0.1\",\"sourceName\":\"oteNB5309\"},\"notificationFields\":{\"notificationFieldsVersion\":\"2.0\",\"changeType\":\"FileReady\",\"changeIdentifier\":\"PM_MEAS_FILES\",\"arrayOfNamedHashMap\":[{\"name\":\"fileFromSftp.tar.gz\",\"hashMap\":{\"location\":\"sftp://foo:pass@localhost:22/fileFromSftp.tar.gz\",\"fileFormatType\":\"org.3GPP.32.435#measCollec\",\"fileFormatVersion\":\"V10\",\"compression\":\"gzip\"}}]}}}"]
"""
received_event_to_get_method = b"""
["{\\"event\\":{\\"commonEventHeader\\":{\\"startEpochMicrosec\\":8745745764578,\\"eventId\\":\\"FileReady_1797490e-10ae-4d48-9ea7-3d7d790b25e1\\",\\"timeZoneOffset\\":\\"UTC+05.30\\",\\"internalHeaderFields\\":{\\"collectorTimeStamp\\":\\"Tue, 09 18 2018 10:56:52 UTC\\"},\\"priority\\":\\"Normal\\",\\"version\\":\\"4.0.1\\",\\"reportingEntityName\\":\\"otenb5309\\",\\"sequence\\":0,\\"domain\\":\\"notification\\",\\"lastEpochMicrosec\\":8745745764578,\\"eventName\\":\\"Noti_RnNode-Ericsson_FileReady\\",\\"vesEventListenerVersion\\":\\"7.0.1\\",\\"sourceName\\":\\"oteNB5309\\"},\\"notificationFields\\":{\\"notificationFieldsVersion\\":\\"2.0\\",\\"changeType\\":\\"FileReady\\",\\"changeIdentifier\\":\\"PM_MEAS_FILES\\",\\"arrayOfNamedHashMap\\":[{\\"name\\":\\"fileFromSftp.tar.gz\\",\\"hashMap\\":{\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"location\\":\\"sftp://foo:pass@172.17.0.3:22/fileFromSftp.tar.gz\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}}]}}}"]
"""
received_event_to_get_method = b"""
["{\\"event\\":{\\"commonEventHeader\\":{\\"startEpochMicrosec\\":0000000000000,\\"eventId\\":\\"FileReady_1797490e-10ae-4d48-9ea7-3d7d790b25e1\\",\\"timeZoneOffset\\":\\"UTC+05.30\\",\\"internalHeaderFields\\":{\\"collectorTimeStamp\\":\\"Wed, 09 19 2018 11:39:30 UTC\\"},\\"priority\\":\\"Normal\\",\\"version\\":\\"4.0.1\\",\\"reportingEntityName\\":\\"otenb5309\\",\\"sequence\\":0,\\"domain\\":\\"notification\\",\\"lastEpochMicrosec\\":8745745764578,\\"eventName\\":\\"Noti_RnNode-Ericsson_FileReady\\",\\"vesEventListenerVersion\\":\\"7.0.1\\",\\"sourceName\\":\\"oteNB5309\\"},\\"notificationFields\\":{\\"notificationFieldsVersion\\":\\"2.0\\",\\"changeType\\":\\"FileReady\\",\\"changeIdentifier\\":\\"PM_MEAS_FILES\\",\\"arrayOfNamedHashMap\\":[{\\"name\\":\\"fileFromSftp.tar.gz\\",\\"hashMap\\":{\\"location\\":\\"sftp://foo:pass@localhost:22/upload/fileFromSftp.tar.gz\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}}]}}}"]
"""
# ##ftpes
# received_event_to_get_method = b"""
# ["{\\"event\\":{\\"commonEventHeader\\":{\\"startEpochMicrosec\\":0000000000000,\\"eventId\\":\\"FileReady_1797490e-10ae-4d48-9ea7-3d7d790b25e1\\",\\"timeZoneOffset\\":\\"UTC+05.30\\",\\"internalHeaderFields\\":{\\"collectorTimeStamp\\":\\"Wed, 09 19 2018 11:39:30 UTC\\"},\\"priority\\":\\"Normal\\",\\"version\\":\\"4.0.1\\",\\"reportingEntityName\\":\\"otenb5309\\",\\"sequence\\":0,\\"domain\\":\\"notification\\",\\"lastEpochMicrosec\\":8745745764578,\\"eventName\\":\\"Noti_RnNode-Ericsson_FileReady\\",\\"vesEventListenerVersion\\":\\"7.0.1\\",\\"sourceName\\":\\"oteNB5309\\"},\\"notificationFields\\":{\\"notificationFieldsVersion\\":\\"2.0\\",\\"changeType\\":\\"FileReady\\",\\"changeIdentifier\\":\\"PM_MEAS_FILES\\",\\"arrayOfNamedHashMap\\":[{\\"name\\":\\"demo.tar.gz\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.tar.gz\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"fileFromSftp.tar.gz\\",\\"hashMap\\":{\\"location\\":\\"sftp://foo:pass@localhost:22/upload/fileFromSftp.tar.gz\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}}]}}}"]
# """
#ftpes- big file
# received_event_to_get_method = b"""
# ["{\\"event\\":{\\"commonEventHeader\\":{\\"startEpochMicrosec\\":0000000000000,\\"eventId\\":\\"FileReady_1797490e-10ae-4d48-9ea7-3d7d790b25e1\\",\\"timeZoneOffset\\":\\"UTC+05.30\\",\\"internalHeaderFields\\":{\\"collectorTimeStamp\\":\\"Wed, 09 19 2018 11:39:30 UTC\\"},\\"priority\\":\\"Normal\\",\\"version\\":\\"4.0.1\\",\\"reportingEntityName\\":\\"otenb5309\\",\\"sequence\\":0,\\"domain\\":\\"notification\\",\\"lastEpochMicrosec\\":8745745764578,\\"eventName\\":\\"Noti_RnNode-Ericsson_FileReady\\",\\"vesEventListenerVersion\\":\\"7.0.1\\",\\"sourceName\\":\\"oteNB5309\\"},\\"notificationFields\\":{\\"notificationFieldsVersion\\":\\"2.0\\",\\"changeType\\":\\"FileReady\\",\\"changeIdentifier\\":\\"PM_MEAS_FILES\\",\\"arrayOfNamedHashMap\\":[{\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"demo.zip\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/demo.zip\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
# {\\"name\\":\\"fileFromSftp.tar.gz\\",\\"hashMap\\":{\\"location\\":\\"sftp://foo:pass@localhost:22/upload/fileFromSftp.tar.gz\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}}]}}}"]
# """
#received_event_to_get_method = b"""
#["{\\"event\\":{\\"commonEventHeader\\":{\\"startEpochMicrosec\\":0000000000000,\\"eventId\\":\\"FileReady_1797490e-10ae-4d48-9ea7-3d7d790b25e1\\",\\"timeZoneOffset\\":\\"UTC+05.30\\",\\"internalHeaderFields\\":{\\"collectorTimeStamp\\":\\"Wed, 09 19 2018 11:39:30 #UTC\\"},\\"priority\\":\\"Normal\\",\\"version\\":\\"4.0.1\\",\\"reportingEntityName\\":\\"otenb5309\\",\\"sequence\\":0,\\"domain\\":\\"notification\\",\\"lastEpochMicrosec\\":8745745764578,\\"eventName\\":\\"Noti_RnNode-Ericsson_FileReady\\",\\"vesEventListenerVersion\\":\\"7.0.1\\",\\"sourceName\\":\\"oteNB5309\\"},\\"notificationFields\\":{\\"notificationFieldsVersion\\":\\"2.0\\",\\"changeType\\":\\"FileReadyFake\\",\\"changeIdentifier\\":\\"PM_MEAS_FILES_FAKE\\",\\"arrayOfNamedHashMap\\":#[{\\"name\\":\\"fileFromFtpes.tar.gz\\",\\"hashMap\\":{\\"location\\":\\"ftpes://myuser:mypass@localhost:21/fileFromFtpes.tar.gz\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}},
#{\\"name\\":\\"fileFromSftp.tar.gz\\",\\"hashMap\\":{\\"location\\":\\"sftp://foo:pass@localhost:22/upload/fileFromSftp.tar.gz\\",\\"fileFormatType\\":\\"org.3GPP.32.435#measCollec\\",\\"fileFormatVersion\\":\\"V10\\",\\"compression\\":\\"gzip\\"}}]}}}"]
#"""
class DMaaPHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        if re.search('/set_get_event', self.path):
            global received_event_to_get_method
            content_length = int(self.headers['Content-Length'])
            received_event_to_get_method = self.rfile.read(content_length)
            _header_200_and_json(self)

        return

    def do_POST(self):
        if re.search('/events/unauthenticated.FILE_READY', self.path):
            global posted_event_from_prh
            content_length = int(self.headers['Content-Length'])
            posted_event_from_prh = self.rfile.read(content_length)
            _header_200_and_json(self)

        return

    def do_GET(self):
        if re.search('/events/unauthenticated.VES_NOTIFICATION_OUTPUT/OpenDcae-c12/C12', self.path):
            _header_200_and_json(self)
            #self.wfile.write(json.dumps({'event':{'notificationFields': {'changeIdentifier': 'PM_MEAS_FILES','changeType': 'FileReady','notificationFieldsVersion': 1.0,'arrayOfAdditionalFields': [{'location': 'ftpes://myuser:mypass@localhost:21/fileFromFtps.tar.gz','compression': 'gzip','fileFormatType': 'org.3GPP.32.435#measCollec','fileFormatVersion': 'V10'},{'location': 'sftp://foo:pass@localhost:22/fileFromSftp.tar.gz','compression': 'gzip','fileFormatType': 'org.3GPP.32.435#measCollec','fileFormatVersion': 'V10'}]}}}))
            self.wfile.write(received_event_to_get_method)
            print(received_event_to_get_method)
        elif re.search('/events/pnfReady', self.path):
            _header_200_and_json(self)
            #self.wfile.write(posted_event_from_prh)
            self.wfile.write(received_event_to_get_method)
        return


def _header_200_and_json(self):
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()


def _main_(handler_class=DMaaPHandler, server_class=HTTPServer, protocol="HTTP/1.0"):

    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 2222

    server_address = ('', port)

    handler_class.protocol_version = protocol
    httpd = server_class(server_address, handler_class)

    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()


if __name__ == '__main__':
    _main_()
