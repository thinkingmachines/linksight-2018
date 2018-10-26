import json
import logging
import pandas as pd
import time
import zmq

from testing.base_matcher import BaseMatcher

REQUEST_TIMEOUT = 2000
DEFAULT_IPC_ENDPOINT = "ipc:///volume/imatch_ipc"
RESPONSE_POLLING_SEC = 0.05


# noinspection PyCompatibility
class IMatchMatcher(BaseMatcher):

    def __init__(self, dataset_file, columns, ipc_endpoint=DEFAULT_IPC_ENDPOINT):
        super().__init__(dataset_file, columns)
        if type(dataset_file) == str:
            self.dataset_path = dataset_file
        else:
            self.dataset_path = dataset_file.name
        self.context = zmq.Context(1)
        self.poll = zmq.Poller()
        self.id = "id://{}:{}".format(self.dataset_path, int(time.time() * 1e6))
        self.client = None
        self.ipc_endpoint = ipc_endpoint
        print("Using IPC endpoint: " + self.ipc_endpoint)

    def _create_client(self):
        if self.client is not None:
            self._destroy_client()
        self.client = self.context.socket(zmq.REQ)
        self.client.connect(self.ipc_endpoint)
        self.poll.register(self.client, zmq.POLLIN)

    def _destroy_client(self):
        self.client.setsockopt(zmq.LINGER, 0)
        self.client.close()
        self.poll.unregister(self.client)
        self.client = None

    def _send_message(self, msg_object):
        # Send message
        message = json.dumps(msg_object)
        msg_object['time'] = time.time()
        self.client.send(message.encode())
        print("Sent message "+str(message.encode()))
        # Poll for response
        socks = dict(self.poll.poll(REQUEST_TIMEOUT))
        if socks.get(self.client) == zmq.POLLIN:  # Response received
            print("Got response")
            response = self.client.recv_json()
            return response
        else:  # Polling timed out
            print("Timeout!")
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
