import subprocess
import itertools
import time
import os

from time import sleep
import argparse
from random import choice
import string
import json

parser = argparse.ArgumentParser(description='script to run inference and return top 3 class predictions of models and determine if agree on top class')

parser.add_argument("-m", "--models_list", help="models for inference as strings no commma", nargs='*')
parser.add_argument("-i", "--input_file", help="input for model", nargs='*')

args = parser.parse_args()
models = args.models_list
input_file = args.input_file


def run_inference(model_name):
    print('running inference using: ', model_name, input_file)
    # generate unique inference run id and results file
    inference_id = (''.join(choice(string.digits + string.ascii_letters) for i in range(5)))
    print('unique_inference_id: ', inference_id)
    result_file_name = "result_files/result_" + f"{model_name}_{inference_id}"+".json"

    # start the torch serve with model file
    subprocess.call(f"torchserve --start --model-store model-store --models model={model_name}.mar --ncs", shell=True, stdout=subprocess.DEVNULL)
    sleep(3)
    # test in parallel to inference API
    print("running inference...")
    start_time = time.time()
    print(time.ctime())
    subprocess.run(f"bash -c 'url=\"http://127.0.0.1:8080/predictions/model/{model_name}\"; curl -X POST $url -T {input_file} >results.json'", shell=True, capture_output=True, text=True)
    total_time = int((time.time() - start_time)*1e6)

    print("total time in ms:", total_time)

    # get metrics of ts inference latency and ts query latency 
    output = subprocess.run("curl http://127.0.0.1:8082/metrics", shell=True, capture_output=True, text=True)

    inference_time=0
    query_time=0
    
    # capture inference latency and query latency from metrics
    for line in output.stdout.split('\n'):
        if line.startswith('ts_inference_latency_microseconds'):
            inference_time = line.split(' ')[1]
        if line.startswith('ts_queue_latency_microseconds'):
            query_time = line.split(' ')[1]

    # calculate the throughput
    throughput = 1000 / total_time * 1000000

    # write metrics to csv file
    f = open(f"result_files/{model_name}_{inference_id}_metrics.csv", "a")
    f.write(f"{model_name},{inference_id},{total_time},{inference_time},{query_time},{throughput}\n")
    f.close()

    # stop torchserve
    stop_result = os.system("torchserve --stop")
    print(stop_result)
    with open  ("result_files/result_" + f"{model_name}_{inference_id}"+".json") as json_file:
        data = json.load(json_file)
    return list(data.keys())[0]


   

def main():
    predictions = []
    for model_name in models:
        predictions.append(run_inference(model_name, input_file))
    print("matched predictions are: ", True if len(set(predictions)) == 1 else False)

if __name__ == "__main__":
    main()