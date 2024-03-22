import prompts
import pandas as pd
import openai
import os
import time

openai.api_key = os.getenv("OPENAI_API_KEY")

class Params:
    GPT_MODEL_COMPLETION = "gpt-3.5-turbo"
    CSV_PATH = "./forms/"
    SPEAKERS = ["A: ", "B: "]
    CSV_START = 0
    CSV_END = 5
    MAX_TOKENS = 256
    TEMPERATURE = 0
    STOP_WORDS = "\n"
    USE_DUMMY = 0
    OUTPUT_PATH = "./forms/"

if __name__ == "__main__":
    params = Params()

    for csv_idx in range(params.CSV_START, params.CSV_END):
        print("csv ", csv_idx)
        # Open CSV
        csv_filename = params.CSV_PATH + "assist{:03}.csv".format(csv_idx)
        assist_data = pd.read_csv(csv_filename)

        # Generate assistant message
        for dialogue_idx, row in assist_data.iterrows():
            print("dialogue ", dialogue_idx)
            system, user_ut = prompts.assist_chat_ja(row.full_dialogue)
            completion = openai.ChatCompletion.create(
                model=params.GPT_MODEL_COMPLETION,
                messages=[
                    {"role": "system", "content": system}, 
                    {"role": "user", "content": user_ut}
                ],
                max_tokens=params.MAX_TOKENS,
                temperature=params.TEMPERATURE,
                stop=params.STOP_WORDS
            )
            assistant_message = completion.get("choices")[0].get("message").get("content")

            # Add speaker
            if not assistant_message.startswith("AI: "):
                assistant_message = "AI: " + assistant_message

            assist_data.at[dialogue_idx, "assist_utterance"] = assistant_message
            time.sleep(3)

        # Save CSV
        assist_data.to_csv(csv_filename, index=False)