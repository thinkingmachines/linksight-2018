from __future__ import print_function

import zmq
import json
import time

# Constants
REQUEST_TIMEOUT = 500
SERVER_ENDPOINT = "ipc:///tmp/ipchello"

# One-time
context = zmq.Context(1)
poll = zmq.Poller()


def create_client():
    client = context.socket(zmq.REQ)
    client.connect(SERVER_ENDPOINT)
    poll.register(client, zmq.POLLIN)
    return client


def destroy_client(client):
    client.setsockopt(zmq.LINGER, 0)
    client.close()
    poll.unregister(client)


def send_message(msg_object, client, error_on_fail=True, destroy_client_on_fail=True):
    message = json.dumps(msg_object)
    client.send(message.encode())
    socks = dict(poll.poll(REQUEST_TIMEOUT))
    if socks.get(client) == zmq.POLLIN:  # Polling done, received
        response = client.recv_json()
        print("Received response "+str(response))
        return response
    else:  # Polling timeout
        if destroy_client_on_fail:
            destroy_client(client)
        if error_on_fail:
            raise ValueError("Cannot contact server")
        return None


def wait_for_job(client):
    while True:
        response = send_message({"type": "get_job_result", "id": "1"}, client)
        status = response.get("status", None)
        if status == "in_progress":
            time.sleep(0.1)
            continue
        if status == "done":
            return response
        raise ValueError("Unknown status: " + status)


def main():
    client = create_client()

    response = send_message({"type": "submit_job", "id": "1"}, client)
    if not response.get("status", None) != 'accepted':
        raise ValueError("Request not accepted")

    job_result = wait_for_job(client)

    context.term()
    # TODO: transform job result into output
    return job_result


if __name__ == "__main__":
    print(main())
