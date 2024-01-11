# LangBiTe: A Bias Tester framework for LLMs

LangBiTe is a tool for testing biases in large language models implemented in Python.

Includes a library of prompts to test bias in gender, race / skin color, age, politics and religion. Any contributor may add new ethical concerns to test.

Prompts a large language model and assess the output trying to detect sensitive words and/or unexpected unethical responses.

## Repository Structure

The following tree shows the list of the repository's sections and their main contents:

```
├── resources
|      ├── prompts.csv             // The prompt templates library in CSV format. See the referenced article for more information about its structure.
|      └── hugchat_cookies.json    // Cookies of a valid session on Hugging Chat. The file is not included in the repository, but is required for testing Hugging Chat.
├── src                            // The source code of the tool.
|      └── langbite.py             // Main controller to invoke for generating, executing and reporting test scenarios.
└── test                           // A simple example of a test scenario.
       ├── simple_test.json        // An example of a test scenario definition which tests religion bias on ChatGPT 3.5 Turbo.
       └── simple_test.py          // A controller for executing the whole testing workflow.
```

## Installation

### Requirements

- _TBD_.

Your project needs the following keys in the .env file:

- API_KEY_OPENAI, to properly connect to OpenAI's API and models.
- API_KEY_HUGGINGFACE, to properly invoke Inference APIs in HuggingFace.

Your project needs the following file to test Hugging Chat. It must containg cookies of a valid session on HuggingChat:

- resources/hugchat_cookies.json

### Reference within a Project

- _TBD_.

## Usage

To generate a valid input, you may use the [EthicsML](https://github.com/SOM-Research/EthicsML) DSL-based tool.

- _TBD_.

## Publications

- Sergio Morales, Robert Clarisó and Jordi Cabot. "Automating Bias Testing of LLMs," 2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE), Luxembourg, 2023, pp. 1705-1707, [doi: 10.1109/ASE56229.2023.00018](https://doi.org/10.1109/ASE56229.2023.00018)

## License

The source code for the site is licensed under the MIT License, which you can find in the LICENSE.md file.
