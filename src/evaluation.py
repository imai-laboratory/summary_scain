import os
import datetime
import csv
import tiktoken
import logging
import evaluator

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt = '%m/%d/%Y %H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

class Params:
    GPT_MODEL_COMPLETION = "gpt-3.5-turbo"
    #GPT_MODEL_COMPLETION = "text-davinci-003"
    GPT_MODEL_EMBEDDING = "text-embedding-ada-002"
    DIALOGUE_PATH = "./dat/"
    DIALOGUE_FILENAME = "PP"
    SPEAKERS = ["A: ", "B: "]
    DIALOGUE_START = 97
    DIALOGUE_END = 100
    MAX_TOKENS = 200
    TEMPERATURE = 0
    STOP_WORDS = "\n"
    USE_DUMMY = 0
    RESULTS_PATH = "./results/"

if __name__ == "__main__":
    params = Params()

    # Encoder
    encoding = tiktoken.encoding_for_model(params.GPT_MODEL_COMPLETION)

    # Get list of dialogues
    file_list = os.listdir(params.DIALOGUE_PATH)
    file_list = [f for f in file_list if f.startswith(params.DIALOGUE_FILENAME)]
    file_list = file_list[params.DIALOGUE_START:params.DIALOGUE_END]
    #logger.debug(file_list)

    # Loop
    n_tokens = []
    results = []
    for filename in file_list:
        logger.info("------ dialogue: {}".format(filename))
        with open(params.DIALOGUE_PATH + filename) as f:
            dialogue = [s.rstrip() for s in f.readlines()]

        ev = evaluator.Evaluator(params, encoding, dialogue, filename)
        n_token = ev.evaluate()
        logger.info("------ number of tokens: {}".format(n_token))
        n_tokens.append(n_token)
        results.extend(ev.results)
        
        # Save results for each dialogue
        dt_now = datetime.datetime.now()
        results_filename = params.RESULTS_PATH + dt_now.strftime("%Y%m%d_%H%M%S") + ".csv"
        with open(results_filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(ev.results)

    logger.info("------ number of total tokens: {}".format(sum(n_tokens)))

    # dt_now = datetime.datetime.now()
    # results_filename = params.RESULTS_PATH + dt_now.strftime("%Y%m%d_%H%M%S") + ".csv"
    # with open(results_filename, "w") as f:
    #     writer = csv.writer(f)
    #     writer.writerows(results)
