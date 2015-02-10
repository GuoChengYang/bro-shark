import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime

from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler
from watchdog.observers import Observer

from elasticsearch import Elasticsearch


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.json", "*.log"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        this_file = event.src_path.lstrip('./')
        log_type = os.path.splitext(this_file)[0]
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), this_file)
        if 'loaded_scripts' in this_file:
            return
        print "New Log Found: {}".format(this_file)
        # # the file will be processed there
        # cat = subprocess.Popen(['cat', event.src_path.lstrip('./')], stdout=subprocess.PIPE)
        # jq = subprocess.Popen('jq \'.\'',
        #                 stdin=cat.stdout,
        #                 stdout=subprocess.PIPE,)
        #                 # shell=True)
        # end_of_pipe = jq.stdout
        # print end_of_pipe
        resp = ''
        try:
            es = Elasticsearch()
            # print os.path.join(os.path.abspath(os.path.dirname(__file__)), this_file)
            with open(file_path) as json_data:
                for line in json_data:
                    # decoded_response = json_data.read().decode("UTF-8")
                    doc = json.loads(line)
                    # print "TIME:"
                    # print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(doc['ts']))
                    # doc['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S.%f', time.localtime(doc['ts']))
                    doc['timestamp'] = datetime.fromtimestamp(int(doc['ts']))
                    resp = es.index(index='bro', doc_type=log_type, body=doc, timestamp=doc['timestamp'])
            # time.sleep(1)
            os.remove(file_path)
        except Exception as e:
            print e
        if 'created' in resp:
            return resp['created']
        else:
            return False
        # subprocess.call(['cat', event.src_path], shell=True)
        # print "New bro-log: {}".format(this_file)
        # for line in end_of_pipe:
        #     print '\t', line.strip()
        # print
        # print
        # print event.src_path, event.event_type  # print now on
        # ly for degug

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # event_handler = LoggingEventHandler()
    event_handler2 = MyHandler()

    observer = Observer()
    observer.schedule(event_handler2, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
