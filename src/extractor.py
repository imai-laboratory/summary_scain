import os
import datetime
import json
import ast
import re
from time import sleep
from unittest import result
import openai
import logging
import prompts
import utils

openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = ""

# logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
#                     datefmt = '%m/%d/%Y %H:%M:%S',
#                     level = logging.DEBUG)
# logger = logging.getLogger(__name__)

class Extractor():
    def __init__(self, params, encoding, dialogue, dialogue_id):
        self.params = params
        self.encoding = encoding
        self.dialogue = dialogue
        self.dialogue_id = dialogue_id
        self.results = []
        self.n_total_token = 0
        return
    
    def openai_api_completion(self, prompt):
        params = self.params
        if params.GPT_MODEL_COMPLETION == "gpt-3.5-turbo":
            completion = openai.ChatCompletion.create(
                model=params.GPT_MODEL_COMPLETION,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=params.MAX_TOKENS,
                temperature=params.TEMPERATURE,
                stop=params.STOP_WORDS
            )
        elif params.GPT_MODEL_COMPLETION == "text-davinci-003":
            completion = openai.Completion.create(
                model=params.GPT_MODEL_COMPLETION,
                prompt=prompt,
                max_tokens=params.MAX_TOKENS,
                temperature=params.TEMPERATURE,
                #stop=params.STOP_WORDS
            )
        else:
            #logger.error("GPT model name is inappropriate")
            exit()

        # Save log
        # dt_now = datetime.datetime.now()
        # log_filename = "./log/" + dt_now.strftime("%Y%m%d_%H%M%S") + ".txt"
        # dict_log = {"prompt": prompt}
        # dict_log.update(completion)
        # json_log = json.dumps(dict_log, indent=4, ensure_ascii=False)
        # with open(log_filename, "w") as f:
        #     f.write(json_log)

        return completion

class SCAINExtractor(Extractor):
    def extract(self):
        for idx, sentence in enumerate(self.dialogue):
            if idx <= 2:
                continue

            full_dialogue = self.dialogue[:idx+1]
            #logger.debug("------ full dialogue: ")
            #logger.debug(full_dialogue)
            omitted_dialogue = self.dialogue[:idx-2] + self.dialogue[idx:idx+1]
            #logger.debug("------ ommited dialogue: ")
            #logger.debug(omitted_dialogue)
            core_sentence = sentence
            for speaker in self.params.SPEAKERS:
                core_sentence = core_sentence.removeprefix(speaker)
            #logger.debug("------ core sentence: ")
            #logger.debug(core_sentence)

            full_summary = self.rephrasing(full_dialogue, core_sentence)
            #logger.debug("------ full summary: ")
            #logger.debug(full_summary)
            omitted_summary = self.rephrasing(omitted_dialogue, core_sentence)
            #logger.debug("------ omitted summary: ")
            #logger.debug(omitted_summary)

            similarity = self.calc_similarity(full_summary, omitted_summary)
            result = [self.dialogue_id, idx, full_summary, omitted_summary, similarity]
            self.results.append(result)

        return self.n_total_token
    
    def rephrasing(self, dialogue, sentence):
        params = self.params

        if params.GPT_MODEL_COMPLETION == "gpt-3.5-turbo":
            #prompt = prompts.rephrase_chat_ja(dialogue, sentence)
            prompt = prompts.rephrase_chat_en(dialogue, sentence)
        elif params.GPT_MODEL_COMPLETION == "text-davinci-003":
            prompt = prompts.summary_comp_ja(dialogue, sentence)
        else:
            logger.error("GPT model name is inappropriate")
            exit()

        if params.USE_DUMMY == 1:
            response = utils.dummy_completion(prompt, encoding=self.encoding)
        else:
            response = self.openai_api_completion(prompt)

        total_tokens = response.get("usage").get("total_tokens")
        self.n_total_token += total_tokens

        if params.GPT_MODEL_COMPLETION == "gpt-3.5-turbo":
            rephrased_statement = response.get("choices")[0].get("message").get("content")
        elif params.GPT_MODEL_COMPLETION == "text-davinci-003":
            rephrased_statement = response.get("choices")[0].get("text")
        else:
            logger.error("GPT model name is inappropriate")
            exit()

        return rephrased_statement
    
    def calc_similarity(self, sentence1, sentence2):
        params = self.params

        if params.USE_DUMMY == 1:
            similarity = 1
        else:
            embedding1 = openai.Embedding.create(
                input=sentence1,
                model=params.GPT_MODEL_EMBEDDING
            )["data"][0]["embedding"]
            embedding2 = openai.Embedding.create(
                input=sentence2,
                model=params.GPT_MODEL_EMBEDDING
            )["data"][0]["embedding"]
            similarity = utils.cosine_similarity(embedding1, embedding2)
        
        return similarity
    
class ImportantExtractor(Extractor):
    def evaluate(self):
        important_sentences = self.detect_important_sentences(self.dialogue)
        result = [self.dialogue_id] + important_sentences # [self.dialogue_id, important_sentence_id[1], important_sentence_id[2]]
        self.results.append(result)
        return self.n_total_token
    
    def detect_important_sentences(self, dialogue):
        params = self.params
        prompt = prompts.important_chat_ja(dialogue)

        if params.USE_DUMMY == 1:
            response = utils.dummy_completion(prompt, encoding=self.encoding)
        else:
            response = self.openai_api_completion(prompt)

        total_tokens = response.get("usage").get("total_tokens")
        self.n_total_token += total_tokens
        important_sentences_str = response.get("choices")[0].get("message").get("content")
        important_sentences_list = list(ast.literal_eval(important_sentences_str))
        return important_sentences_list

class InterpretationExtractor(Extractor):
    def interpretation(self, n, A_condition, B_condition):
        params = self.params
        interpretationsA=[]
        interpretationsB=[]
        values=[]
        for i in range(1, n+1):
            if (i % 2 == 1):
                promptA = prompts.interpretation_A_A(self.dialogue, i, A_condition, B_condition)
                promptB = prompts.interpretation_A_B(self.dialogue, i, A_condition, B_condition)
            else:
                promptA = prompts.interpretation_B_A(self.dialogue, i, A_condition, B_condition)
                promptB = prompts.interpretation_B_B(self.dialogue, i, A_condition, B_condition)

            if params.USE_DUMMY == 1:
                responseA = utils.dummy_completion(promptA, encoding=self.encoding)
                responseB = utils.dummy_completion(promptB, encoding=self.encoding)
            else:
                responseA = self.openai_api_completion(promptA)
                responseB = self.openai_api_completion(promptB)

            interpretationA = responseA.get("choices")[0].get("text")
            interpretationB = responseB.get("choices")[0].get("text")
            similarity = self.calc_similarity(interpretationA, interpretationB)
            #result = [self.dialogue_id, i, "Aの解釈", interpretationA, "Bの解釈", interpretationB, similarity]
            interpretationsA.append(interpretationA)
            interpretationsB.append(interpretationB)
            values.append(round(similarity*100, 2))

        return [interpretationsA, interpretationsB, values]
    def calc_similarity(self, sentence1, sentence2):
        params = self.params

        if params.USE_DUMMY == 1:
            similarity = 1
        else:
            embedding1 = openai.Embedding.create(
                input=sentence1,
                model=params.GPT_MODEL_EMBEDDING
            )["data"][0]["embedding"]
            embedding2 = openai.Embedding.create(
                input=sentence2,
                model=params.GPT_MODEL_EMBEDDING
            )["data"][0]["embedding"]
            similarity = utils.cosine_similarity(embedding1, embedding2)
        
        return similarity