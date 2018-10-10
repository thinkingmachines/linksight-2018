import json
import time

import zmq
import pandas as pd

from testing.base_matcher import BaseMatcher

REQUEST_TIMEOUT = 500
SERVER_ENDPOINT = "ipc:///tmp/ipchello"
RESPONSE_POLLING_SEC = 0.05
STAGING_CSV = "/tmp/matcher{}.csv"


# noinspection PyCompatibility
class IMatchMatcher(BaseMatcher):

    def __init__(self, dataset_file, columns):
        super().__init__(dataset_file, columns)
        if type(dataset_file) == str:
            self.dataset_path = dataset_file
        else:
            self.dataset_path = dataset_file.name
        self.context = zmq.Context(1)
        self.poll = zmq.Poller()
        self.id = "id://{}:{}".format(self.dataset_path, int(time.time() * 1e6))
        self.client = None

    def _create_client(self):
        if self.client is not None:
            self._destroy_client()
        self.client = self.context.socket(zmq.REQ)
        self.client.connect(SERVER_ENDPOINT)
        self.poll.register(self.client, zmq.POLLIN)

    def _destroy_client(self):
        self.client.setsockopt(zmq.LINGER, 0)
        self.client.close()
        self.poll.unregister(self.client)
        self.client = None

    def _send_message(self, msg_object):
        # Send message
        message = json.dumps(msg_object)
        self.client.send(message.encode())

        # Poll for response
        socks = dict(self.poll.poll(REQUEST_TIMEOUT))
        if socks.get(self.client) == zmq.POLLIN:  # Response received
            response = self.client.recv_json()
            return response
        else:  # Polling timed out
            self._destroy_client()
            raise ValueError("Cannot contact server")

    def _wait_for_job(self):
        while True:
            response = self._send_message({"type": "get_job_result", "id": self.id})
            status = response["status"]
            if status == "in_progress":
                time.sleep(RESPONSE_POLLING_SEC)
                continue
            if status == "done":
                return response
            if status == "failed":
                raise ValueError(response["content"])
            raise ValueError("Unknown status: " + status)

    def _create_job_request(self):
        return {
            "type": "submit_job",
            "id": self.id,
            "csvPath": self.dataset_path,
            "columns": self.columns,
        }

    @property
    def get_matches(self):
        self._create_client()

        # Submit job
        response = self._send_message(self._create_job_request())
        if not response["status"] != 'accepted':
            raise ValueError("Job request not accepted by server")

        # Wait for result
        job_result = self._wait_for_job()
        print(job_result)

        # Cleanup
        self._destroy_client()

        # Process result
        out_path = job_result["content"]
        df = pd.read_csv(out_path, keep_default_na=False)
        for row in df.itertuples(index=False):
            yield row._asdict()
