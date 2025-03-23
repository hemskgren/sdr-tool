import subprocess
import json
import sys
from pprint import pprint
from threading import Thread
import argparse

# Logger
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("logger")
# logger.info("Starting rtl433-counter")

# This method parses the input text from the subprocess to a json object
def parse(input_text):
    # print(input_text)
    try:
        return json.loads(input_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


# sending to api
# def sendToApi(text):
#     # print(text)
#     parsed_json = parse(text)
#     # result = <send_to_api(parsed_json)> # here your http.post


# count seen messages
sender_count = {}
sender_details = []
def countSeenMessages(text, details):
    if sender_count == {}:
        logger.info("Counting seen messages:")
    parsed_json = parse(text)
    
    # print(type(parsed_json['model']))
    if details == 'yes':
        pprint(parsed_json)
    else:
        # print first seen of each model and add to sender_details
        if f"{parsed_json['id']}_{parsed_json['model']}" not in sender_count:
            pprint(parsed_json)
            sender_details.append(parsed_json)
            # pprint(sender_details)

    sender_count[f"{parsed_json['id']}_{parsed_json['model']}"] = sender_count.get(f"{parsed_json['id']}_{parsed_json['model']}", 0) + 1
    # logger.info(f"Counter: {sender_count}")
    print(f"Message recived - counter: {sender_count}")


# This method creates a subprocess with subprocess.Popen and takes a List<str> as command
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def main():
    # rtl433-counter arguments parser
    parser = argparse.ArgumentParser(description='rtl433-counter settings')
    parser.add_argument('--host', type=str, help='Host of the rtl_433 device', required=False, default='127.0.0.1')
    parser.add_argument('--port', type=str, help='Port of the rtl_433 device', required=False, default='1234')
    parser.add_argument('--frequency', type=str, help='Frequency to work with', required=False, default='433.920M')
    parser.add_argument('--exec', type=str, help='rtl_433 path', required=False, default='/usr/bin/rtl_433')
    parser.add_argument('--details', type=str, help='detail log', required=False, default='yes', choices=['yes', 'no'])
    args = parser.parse_args()

    logger.info(f"Using: {args.exec} connecting Host: {args.host} Port: {args.port} for work on frequency: {args.frequency}")

    try:
        # listen thru remote rtl_433 > json return in type str
        for text in execute([f'{args.exec}', '-d', f'rtl_tcp:{args.host}:{args.port}', '-f',f'{args.frequency}', '-F', 'json', '-M', 'level' ]):
            
            # print(text, end="")
            # I'm starting a new thread to avoid data loss. So I can listen to the weather station's output and send it async to the api
            # thread = Thread(target = sendToApi, args = (text,))
            thread = Thread(target = countSeenMessages, args = (text, args.details))
            thread.start()

    except KeyboardInterrupt:
        # Print the statement for exception 
        print("Stopped by user - print collected data")
        logger.info("Collected data:")
        logger.info(sender_count)
        for sender in sender_details:
            # logger.info(sender)
            print(sender)

        # Close the program 
        sys.exit(0) 


if __name__ == "__main__":
    main()