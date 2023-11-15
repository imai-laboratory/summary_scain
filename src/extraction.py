import os
import datetime
import time
import csv
import tiktoken
import logging
import extractor

from importlib.machinery import OPTIMIZED_BYTECODE_SUFFIXES
from flask import Flask, render_template, request, flash

app = Flask(__name__)

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt = '%m/%d/%Y %H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

class Params:
    #GPT_MODEL_COMPLETION = "gpt-3.5-turbo"
    GPT_MODEL_COMPLETION = "text-davinci-003"
    GPT_MODEL_EMBEDDING = "text-embedding-ada-002"
    DIALOGUE_PATH = "./dat/"
    DIALOGUE_FILENAME = "PP"
    FILENAME = "PP1.txt"
    FILEPATH = DIALOGUE_PATH + FILENAME
    SPEAKERS = ["A: ", "B: "]
    DIALOGUE_START = 0
    DIALOGUE_END = 1
    MAX_TOKENS = 200
    TEMPERATURE = 0
    STOP_WORDS = "\n"
    USE_DUMMY = 0
    RESULTS_PATH = "./results/generations/important/"

    def setFileName(self, filename):
        type(self).FILENAME = filename
        type(self).FILEPATH = type(self).DIALOGUE_PATH + type(self).FILENAME
        print(type(self).FILENAME)
        print(type(self).FILEPATH)

def dialogue():
    params = Params()
    with open(params.FILEPATH) as f:
        dialogue = [s.rstrip() for s in f.readlines()]
    return dialogue

def generate(A_CONDITION, B_CONDITION):
    params = Params()

    # Encoder
    encoding = tiktoken.encoding_for_model(params.GPT_MODEL_COMPLETION)

    file_path = params.DIALOGUE_PATH + params.FILENAME
    with open(file_path) as f:
        dialogue = [s.rstrip() for s in f.readlines()]
    ex = extractor.InterpretationExtractor(params, encoding, dialogue(), params.FILEPATH)
    #results = ex.interpretation(sum([1 for _ in open(file_path)]), params.A_CONDITION, params.B_CONDITION)

    time.sleep(3)

    dt_now = datetime.datetime.now()
    results_filename = params.RESULTS_PATH + dt_now.strftime("%Y%m%d_%H%M%S") + ".csv"
    with open(results_filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(results)
    
    return results

if __name__ == "__main__":
    params = Params()

    # Encoder
    encoding = tiktoken.encoding_for_model(params.GPT_MODEL_COMPLETION)

    # Get list of dialogues
    file_list = os.listdir(params.DIALOGUE_PATH)
    file_list = [f for f in file_list if f.startswith(params.DIALOGUE_FILENAME)]
    file_list = file_list[params.DIALOGUE_START:params.DIALOGUE_END]
    logger.debug(file_list)

    # Loop
    n_tokens = []
    results = []
    for filename in file_list:
        logger.info("------ dialogue: {}".format(filename))
        with open(params.DIALOGUE_PATH + filename) as f:
            dialogue = [s.rstrip() for s in f.readlines()]

        ex = extractor.SCAINExtractor(params, encoding, dialogue, filename)
        #ex = extractor.ImportantExtractor(params, encoding, dialogue, filename)
        n_token = ex.extract()
        logger.info("------ number of tokens: {}".format(n_token))
        n_tokens.append(n_token)
        results.extend(ex.results)

        # Wait to avoid overloading
        time.sleep(3)
        
        # Save results for each dialogue
        dt_now = datetime.datetime.now()
        results_filename = params.RESULTS_PATH + dt_now.strftime("%Y%m%d_%H%M%S") + ".csv"
        with open(results_filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(ex.results)

    logger.info("------ number of total tokens: {}".format(sum(n_tokens)))
