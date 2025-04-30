# MetamorphicAFC Project

This repository is divided into two main components.

## 1. CONCRETE

The first is [CONCRETE](https://github.com/khuangaf/CONCRETE/tree/master), a symbolic fact-checking system.

### Environment Setup

To run CONCRETE, you must create a Conda environment with Python 3.7:

```bash
conda create -n <env_name> python=3.7
conda activate concrete
```

Then, install the required dependencies:

```bash
conda install --yes --file requirements_conda.txt
```

This will set up the environment needed to run the tool via terminal.

### How to Run

To execute CONCRETE and its respective steps, please refer to the instructions in the original [CONCRETE repository](https://github.com/khuangaf/CONCRETE/tree/master).

- For Windows users, follow the adapted scripts provided in the `scripts` folder.
- For Linux users, use the commands available in the original project.

---

## 2. MetamorphicAFC

This part of the project contains a suite of metamorphic tests over the dataset, organized as follows:

### Test Modules

- `claim_tests/`: Modifies the textual claim, testing robustness against synonymous, lexical or structural changes.
- `claimant_tests/`: Alters or removes the claimant field to assess model dependency on the source of the claim.
- `context_tests/`: Edits the context evidence, simulating noisy, contradictory or incomplete scenarios.
- `date_tests/`: Modifies dates related to the claim, evidence, and review to evaluate temporal consistency.

### Utility Scripts

Available in the `scripts/` folder:

- `analyze_examples.py`: Prints example outputs from mutated inputs.
- `merge_predictions.py`: Combines predictions from different models or mutation types.
- `calculate_f1.py`: Computes F1-score based on ground truth labels.
- `generate_confusion_matrix.py`: Creates a confusion matrix comparing expected vs. predicted labels.
- `normalize_labels.py`: Standardizes labels across different outputs.
- `unify_datasets.py`: Merges different mutation datasets into a single evaluation file.

We use these scrips to clean, normalize and analize the data.

### Full Pipeline Execution (Using `__init__.py`)

To execute the entire metamorphic testing pipeline — from mutation generation to fact-checking — run the `__init__.py` module directly.

#### 1. Generate Mutated Claims from Original TSV

```bash
python -m xfact-metamorphic-tests --mode mutate --input path/to/input.tsv --output path/to/output_mutated.tsv
```

This will apply all metamorphic relations (MRs) defined in the framework and save the result to `output_mutated.tsv`.

#### 2. Run Fact-Checking on Mutated Data with a Model

```bash
python -m xfact-metamorphic-tests --mode check --input path/to/output_mutated.tsv --output path/to/predictions.json --model openai --temperature 0
```

Replace `--model` with one of the supported models:

- `openai` → GPT (via OpenAI API)
- `maritaca` → Sabiá 3.0 (via custom API)
- `gemini` → Google Gemini (via API)

You can also pass `--temperature`, `--max_tokens`, and other model-related parameters.

#### 3. Example: End-to-End

```bash
python -m xfact-metamorphic-tests --mode mutate --input data/xfact_subset.tsv --output data/xfact_mutated.tsv

python -m xfact-metamorphic-tests --mode check --input data/xfact_mutated.tsv --output results/openai_predictions.json --model openai --temperature 0.2
```

Ensure your `.env` or environment variables include the API keys required by each model.

Make sure you are in an environment where all dependencies from `requirements.txt` are installed:

```bash
pip install -r requirements.txt
```

## 3. Project Resources

- You can access our internal working files and scripts in the following Google Drive folder:  
  [Main Drive](https://drive.google.com/drive/u/0/folders/1bwaYasG16EYRr1pbCzdHp4gbMiBQXYIe)

- Experimental results are located in the "resultados" folder inside this Drive:  
  [Results Folder](https://drive.google.com/drive/u/0/folders/1smfdpAlmK6rN857mg1YuUhjWIuW9KrTr)

---

Feel free to check each subdirectory for additional usage examples, configurations, and scripts tailored for metamorphic testing over fact-checking models.
