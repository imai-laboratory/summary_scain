import os
import requests
import pandas as pd

def save_dialogue(id, dialogue):
    filename = "./dat/" + id + ".txt"
    with open(filename, "w") as f:
        f.write("\n".join(dialogue))
    return

if __name__ == "__main__":
    # Download and extract JPersonaChat
    URL_JPersonaChat = "https://www.dropbox.com/s/sda9wzexh7ntlij/japanese_persona_chat.xlsx?dl=1"
    PATH_JPersonaChat = "./dat/japanese_persona_chat.xlsx"
    TXT_JPersonaChat = "./dat/PP1.txt"

    if not os.path.isfile(PATH_JPersonaChat):
        print("Download JPersonaChat")
        response = requests.get(URL_JPersonaChat)
        open(PATH_JPersonaChat, "wb").write(response.content)
    
    if os.path.isfile(PATH_JPersonaChat) and not os.path.isfile(TXT_JPersonaChat):
        print("Extract JPersonaChat")
        df = pd.read_excel(PATH_JPersonaChat, sheet_name="対話")
        last_persona_id = ""
        dialogue = []
        for row in df.itertuples(name=None):
            persona_id = row[2]
            speaker = row[3]
            utterance = row[4]
            if persona_id == last_persona_id:
                dialogue.append(speaker + ": " + utterance)
            else:
                save_dialogue(last_persona_id, dialogue)
                last_persona_id = persona_id
                dialogue = [speaker + ": " + utterance]

        save_dialogue(last_persona_id, dialogue)
    
    exit()