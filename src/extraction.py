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
    FILENAME = "PP4.txt"
    FILEPATH = DIALOGUE_PATH + FILENAME
    SPEAKERS = ["A: ", "B: "]
    DIALOGUE_START = 0
    DIALOGUE_END = 1
    MAX_TOKENS = 200
    TEMPERATURE = 0
    STOP_WORDS = "\n"
    USE_DUMMY = 0
    RESULTS_PATH = "./results/generation/interpretation/"
    #A_CONDITION = "Bの同級生だが，まだBの性格をあまり知らない人物"
    #B_CONDITION = "普段成績が良く，謙虚な人間"
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

    # file_path = params.DIALOGUE_PATH + params.FILENAME
    # with open(file_path) as f:
    #     dialogue = [s.rstrip() for s in f.readlines()]
    ex = extractor.InterpretationExtractor(params, encoding, dialogue(), params.FILEPATH)
    #results = ex.interpretation(sum([1 for _ in open(file_path)]), params.A_CONDITION, params.B_CONDITION)
    results = ex.interpretation(sum([1 for _ in open(params.FILEPATH)]), A_CONDITION, B_CONDITION)

    #time.sleep(3)

    # dt_now = datetime.datetime.now()
    # results_filename = params.RESULTS_PATH + dt_now.strftime("%Y%m%d_%H%M%S") + ".csv"
    # with open(results_filename, "w") as f:
    #     writer = csv.writer(f)
    #     writer.writerows(results)
    
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    params = Params()
    output=""
    A_CONDITION = ""
    B_CONDITION = ""
    log = dialogue()
    resultA=""
    resultB=""
    values=[]
    for i in range(sum([1 for _ in open(params.FILEPATH)])):
        values.append("")

    if request.method == 'POST':
        if request.form['action'] == 'select':
            params.setFileName(request.form.get('conversation'))
            log = dialogue()
            values=[]
            for i in range(sum([1 for _ in open(params.FILEPATH)])):
                values.append("")
            return render_template('index.html', dialogue=zip(log, values), filename=params.FILENAME, resultA=resultA, resultB=resultB)

        elif request.form['action'] == 'generate':
            A_CONDITION = request.form.get('A_Condition')  # フォームから目標を取得
            B_CONDITION = request.form.get('B_Condition')

            if A_CONDITION and B_CONDITION:
                output = generate(A_CONDITION, B_CONDITION)
                resultA = output[0]
                resultB = output[1]
                values = output[2]
                return render_template('index.html', resultA=resultA, resultB=resultB, dialogue=zip(log, values), filename=params.FILENAME, A_CONDITION=A_CONDITION, B_CONDITION=B_CONDITION)
            else:
                return render_template('index.html', dialogue=zip(log, values), filename=params.FILENAME, resultA=resultA, resultB=resultB)
        else:
            return render_template('index.html', dialogue=zip(log, values), filename=params.FILENAME, resultA=resultA, resultB=resultB)

    if request.method == "GET":
        return render_template('index.html', dialogue=zip(log, values), filename=params.FILENAME, resultA=resultA, resultB=resultB)

if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     params = Params()

#     # Encoder
#     encoding = tiktoken.encoding_for_model(params.GPT_MODEL_COMPLETION)

#     # Get list of dialogues
#     # file_list = os.listdir(params.DIALOGUE_PATH)
#     # file_list = [f for f in file_list if f.startswith(params.DIALOGUE_FILENAME)]
#     # file_list = file_list[params.DIALOGUE_START:params.DIALOGUE_END]
#     # logger.debug(file_list)

#     # Loop
#     #n_tokens = []
#     #results = []
#     # for filename in file_list:
#     #     logger.info("------ dialogue: {}".format(filename))
#     #     with open(params.DIALOGUE_PATH + filename) as f:
#     #         dialogue = [s.rstrip() for s in f.readlines()]

#     #     ex = extractor.SCAINExtractor(params, encoding, dialogue, filename)
#     #     #ex = extractor.ImportantExtractor(params, encoding, dialogue, filename)
#     #     n_token = ex.extract()
#     #     logger.info("------ number of tokens: {}".format(n_token))
#     #     n_tokens.append(n_token)
#     #     results.extend(ex.results)

#     #     # Wait to avoid overloading
#     #     time.sleep(3)
        
#     #     # Save results for each dialogue
#     #     dt_now = datetime.datetime.now()
#     #     results_filename = params.RESULTS_PATH + dt_now.strftime("%Y%m%d_%H%M%S") + ".csv"
#     #     with open(results_filename, "w") as f:
#     #         writer = csv.writer(f)
#     #         writer.writerows(ex.results)

#     # logger.info("------ number of total tokens: {}".format(sum(n_tokens)))
#     file_path = params.DIALOGUE_PATH + params.FILENAME
#     with open(file_path) as f:
#         dialogue = [s.rstrip() for s in f.readlines()]
#     ex = extractor.InterpretationExtractor(params, encoding, dialogue, file_path)
#     results = ex.interpretation(sum([1 for _ in open(file_path)]), params.A_CONDITION, params.B_CONDITION)
#     #results.extend(results)
#     time.sleep(3)

#     dt_now = datetime.datetime.now()
#     results_filename = params.RESULTS_PATH + dt_now.strftime("%Y%m%d_%H%M%S") + ".csv"
#     with open(results_filename, "w") as f:
#         writer = csv.writer(f)
#         writer.writerows(results)
#     # Save results at once
#     # dt_now = datetime.datetime.now()
#     # results_filename = params.RESULTS_PATH + dt_now.strftime("%Y%m%d_%H%M%S") + ".csv"
#     # with open(results_filename, "w") as f:
#     #     writer = csv.writer(f)
#     #     writer.writerows(results)
