import hashlib
import time
from os import path, makedirs
from shutil import copyfile, rmtree
from urllib.parse import urljoin

import pandas as pd
import requests

from linksight.api.matchers.base_matcher import BaseMatcher

REQUEST_TIMEOUT = 2000
RESPONSE_POLLING_SEC = 0.05

DEFAULT_ENDPOINT = "http://localhost:8686/"
DEFAULT_SHARED_DIR = "/imatch_vol/data/"


# noinspection PyCompatibility
class IMatchMatcher(BaseMatcher):

    def __init__(self, dataset_file, columns, endpoint=DEFAULT_ENDPOINT, shared_dir=DEFAULT_SHARED_DIR):
        super().__init__(dataset_file, columns)
        if type(dataset_file) == str:
            self.dataset_path = dataset_file
        else:
            self.dataset_path = dataset_file.name
        self.id = self._create_id()
        self.endpoint = endpoint
        self.shared_dir = path.join(shared_dir, self.id)
        self.input_path = path.join(self.shared_dir, "in.csv")
        print("Using server endpoint: {}".format(self.endpoint))

    def _create_id(self):
        s = "id://{}:{}".format(self.dataset_path, int(time.time() * 1e6))
        return hashlib.md5(s.encode("utf-8")).hexdigest()

    def _wait_for_job(self):
        while True:
            r = requests.get(self._get_url("jobresult/{}".format(self.id)))
            r.raise_for_status()
            response = r.json()
            status = response["status"]
            if status == "in_progress":
                time.sleep(RESPONSE_POLLING_SEC)
                continue
            if status == "done":
                return response
            if status == "failed":
                raise ValueError(response["content"])
            raise ValueError("Unknown status: {}".format(status))

    def _create_job_request(self):
        return {
            "type": "submit_job",
            "id": self.id,
            "csvPath": self.input_path,
            "outputDir": self.shared_dir,
            "columns": self.columns,
        }

    def _get_url(self, path):
        return urljoin(self.endpoint, path)

    def get_matches(self):
        # Check if server alive
        requests.get(self._get_url("hi")).raise_for_status()

        # Copy input CSV to shared volume
        makedirs(self.shared_dir)
        copyfile(self.dataset_path, self.input_path)

        # Submit job
        r = requests.post(self._get_url("submit"), json=self._create_job_request())
        r.raise_for_status()

        # Wait for result
        job_result = self._wait_for_job()

        # Process result
        out_path = job_result["content"]
        df = pd.read_csv(out_path, keep_default_na=False)
        for row in df.itertuples(index=False):
            yield row._asdict()

        # Cleanup
        rmtree(self.shared_dir)
