# SCAIN extraction and analysis

## Intsallation
Install the packages via the following command: 
```shell
$ pipenv install
```

## Setup
### Download and extract dataset
Download and extract dataset via the following command: 
```shell
$ pipenv run setup
```

### Set OpenAI API key
Set your OpenAI API key as the environment variable: 
```shell
$ export OPENAI_API_KEY=<your OpenAI API key>
```

## Extraction
Extract SCAINs via the following command:
```shell
$ pipenv run extraction
```
Set values of `DIALOGUE_START` and `DIALOGUE_END` properly to avoid model overload.

## Analysis
Run `analysis_extraction.ipynb` and `analysis_survey.ipynb` to analyze the results.

### Latex package
Download udline.sty from [here](http://minamo.my.coocan.jp/tex/udline.html) to generate LaTeX source with underline.

## Dataset
You can download SCAINs dataset from [here](https://drive.google.com/drive/folders/176HNlHdMLuhIspDhOB0vd_nxCvR8jZJM?usp=sharing).

* crowd_dataset_omit
    * links
        * links of Google Forms to collect explanations of core statements
    * datasetXXX \(XXX ranges from 001 to 048\)
        * filename
            * filename of dialogue from JPersonaChat
        * turn
            * number of turns where core statement is located
        * omitted_dialogue
            * dialogue without candidate statements
        * core_sentence
            * the last statement of the omitted dialogue
        * similarity
            * similarity score between complete and omitted dialogues

* response_omitted
    * responseXX \(XX ranges from 1 to 48\)
        * A sheet contains questions and responses of the corresponding Google Form in Japanese.
        * The responses have not been cleaned.
        * The data do not include usernames of the workers.

* crowd_dataset_full
    * links
        * links of Google Forms to collect correctness ratings of explanations
    * datasetXXX \(XXX ranges from 001 to 050\)
        * filename
            * filename of dialogue from JPersonaChat
        * turn
            * number of turns where core statement is located
        * complete_dialogue
            * dialogue with all statements, including ones after core statement
        * core_sentence
            * the statement to be explained
        * similarity
            * similarity score between complete and omitted dialogues
        * nor
            * number of explantions for the core statement
        * resX \(X ranges from 0 to \[nor - 1\]\)
            * explanation of the core statement

* response_full_cleaned
    * responseX \(X ranges from 1 to 50\)
        * A sheet contains questions and responses of the corresponding Google Form in Japanese.
        * The responses has been cleaned.
            * Responses from workers who participated in the explanation task have been deleted.
            * If the same worker had responded to the same form multiple times, only the first response was adopted.
        * The data do not include usernames of the workers.