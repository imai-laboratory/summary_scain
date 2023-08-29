import os
import datetime
import time
import csv
import tiktoken
import logging
import json
import extractor

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt = '%m/%d/%Y %H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

class Params:
    GPT_MODEL_COMPLETION = "gpt-3.5-turbo"
    #GPT_MODEL_COMPLETION = "text-davinci-003"
    GPT_MODEL_EMBEDDING = "text-embedding-ada-002"
    DIALOGUE_PATH = "./dat/TIAGE/"
    DIALOGUE_FILENAME = "anno_test.json"
    SPEAKERS = ["A: ", "B: "]
    DIALOGUE_START = 77
    DIALOGUE_END = 101
    MAX_TOKENS = 200
    TEMPERATURE = 0
    STOP_WORDS = "\n"
    USE_DUMMY = 0
    RESULTS_PATH = "./results/extraction/topic_shift/"

if __name__ == "__main__":
    params = Params()

    # Encoder
    encoding = tiktoken.encoding_for_model(params.GPT_MODEL_COMPLETION)

    # Load dialogue
    with open(params.DIALOGUE_PATH + params.DIALOGUE_FILENAME) as f:
        dataset = json.load(f)

    data_range = range(params.DIALOGUE_START, params.DIALOGUE_END)

    # Loop
    n_tokens = []
    results = []
    for data_idx in data_range:
        logger.info("------ dialogue: {}".format(data_idx))
        data = dataset[str(data_idx)]
        dialogue = [row[0] for row in data]

        ex = extractor.SCAINExtractor(params, encoding, dialogue, str(data_idx))
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

    # Save results at once
    # dt_now = datetime.datetime.now()
    # results_filename = params.RESULTS_PATH + dt_now.strftime("%Y%m%d_%H%M%S") + ".csv"
    # with open(results_filename, "w") as f:
    #     writer = csv.writer(f)
    #     writer.writerows(results)
