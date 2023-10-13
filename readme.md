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

## Latex package
Download udline.sty from [here](http://minamo.my.coocan.jp/tex/udline.html) to generate LaTeX source with underline.
