[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12916926.svg)](https://doi.org/10.5281/zenodo.12916926)

# LangBiTe: A Bias Tester framework for LLMs

LangBiTe is a framework for testing biases in large language models. Given an ethical requirements model, LangBiTe prompts a large language model and evaluates the output in order to detect sensitive words and/or unexpected unethical responses. It includes a library of prompts to test sexism / misogyny, racism, xenophobia, ageism, political bias, lgtbiq+phobia and religious discrimination. Any contributor may add new ethical concerns to assess.

## Code Repository Structure

The following tree shows the list of the repository's sections and their main contents:

```
└── langbite                        // The source code of the package.
      ├── langbite.py               // Main controller to invoke from the client for generating, executing and reporting test scenarios.
      └── resources
             └── prompts_CO_RE.csv  // The prompt templates libraries in CSV format.
```

## Requirements

- python-dotenv 1.0.0
- jsonschema 4.20.0
- openai 1.11.1
- pandas 2.1.4
- replicate 0.23.1
- requests 2.31.0
- numpy 1.26.3

Your project needs the following keys in the .env file:

- API_KEY_OPENAI, to properly connect to OpenAI's API and models.
- API_KEY_HUGGINGFACE, to properly invoke Inference APIs in HuggingFace.
- API_KEY_REPLICATE, to properly connect to models hosted on Replicate.

## Installation, Usage and Extension

The following tree shows the contents of the `documentation` folder:

```
└── documentation
      ├── EXTENDING.md
      ├── USER_GUIDE.md
      └── examples
            └── input_example.json
```

Please refer to the [USER_GUIDE.md](documentation/USER_GUIDE.md) for a description of the input structure and the LangBiTe public methods for generating, executing and reporting the ethical assessment. Within the `examples` folder you can find an example JSON input with a complete test scenario and its ethical requirements for assessment.

Please refer to [EXTENDING.md](documentation/EXTENDING.md) if you are interested in contributing or populating your own prompt template library, or in connecting additional online LLMs.

## Governance and Contribution

The development and community management of this project follows the governance rules described in the [GOVERNANCE.md](GOVERNANCE.md) document.

At SOM Research Lab we are dedicated to creating and maintaining welcoming, inclusive, safe, and harassment-free development spaces. Anyone participating will be subject to and agrees to sign on to our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

This project is part of a research line of the [SOM Research Lab](https://som-research.uoc.edu/), but we are open to contributions from the community. Any comment is more than welcome! If you are interested in contributing to this project, please read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Publications

This repository is the companion to the following research paper:

> Sergio Morales, Robert Clarisó and Jordi Cabot. "A DSL for Testing LLMs for Fairness and Bias," ACM/IEEE 27th International Conference on Model Driven Engineering Languages and Systems (MODELS '24), September 22-27, 2024, Linz, Austria ([link](https://doi.org/10.1145/3640310.3674093))

Other publications:

> Sergio Morales, Robert Clarisó and Jordi Cabot. "Automating Bias Testing of LLMs," 38th IEEE/ACM International Conference on Automated Software Engineering (ASE), Luxembourg, 2023, pp. 1705-1707 ([link](https://doi.org/10.1109/ASE56229.2023.00018))

> Sergio Morales, Robert Clarisó and Jordi Cabot. "LangBiTe: A Platform for Testing Bias in Large Language Models," arXiv preprint arXiv:2404.18558 (2024) [cs.SE] ([link](https://doi.org/10.48550/arXiv.2404.18558))

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The source code for the site is licensed under the MIT License, which you can find in the LICENSE.md file.
