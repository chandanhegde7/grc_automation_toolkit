# GRC Automation Toolkit: Vendor Risk & Framework Mapping

This project is a Python-based toolkit designed to automate key GRC processes, specifically focusing on vendor risk assessment and linking findings to industry security frameworks.

## Phase 1: Vendor Risk Assessment Helper

This phase implements a command-line tool that simulates conducting a security and privacy assessment for a third-party vendor using a structured questionnaire. It collects responses, performs a basic risk calculation, and generates initial reports.

### How it Works:

1.  Reads a questionnaire template defined in `vendor_questionnaire_template.csv`.
2.  Prompts the user (acting as the assessor or vendor) to provide answers for each question via the command line.
3.  Validates input based on the defined answer type (`yes_no`, `score_1_5`, `text`).
4.  Calculates a simple numeric risk score based on 'risky' answers (e.g., 'no' to a 'yes_no' question, low score on a 'score_1_5' question) and pre-defined risk weights.
5.  Generates two output files:
    *   A human-readable Markdown report (`assessment_report_*.md`) summarizing the vendor, total risk score, and detailed answers grouped by risk area.
    *   A machine-readable CSV file (`completed_assessment_*.csv`) containing the raw assessment data (questions, answers, weights) for further processing (used in Phase 2).

### Questionnaire Template (`vendor_questionnaire_template.csv`):

The questionnaire is defined in a CSV file with the following columns:
*   `QuestionID`: Unique identifier for the question.
*   `QuestionText`: The full text of the question.
*   `AnswerType`: Expected input format (`yes_no`, `score_1_5`, `text`).
*   `RiskWeight`: Numeric weight (1-5) indicating the severity if the vendor has a weak control or 'risky' answer.
*   `RiskArea`: Category of the question (e.g., Data Security, Access Control).
*   `RelevantFrameworkControl`: (Initially empty in Phase 1, used in Phase 2 for mapping framework controls impacted by this question).

### Simple Scoring Logic:

The tool calculates a total risk score by accumulating "risk points".
*   `yes_no`: A 'no' answer adds `RiskWeight` points. A 'yes' answer adds 0 points.
*   `score_1_5`: An answer `A` adds `(5 - A) * RiskWeight` points. (Lower scores add more points).
*   `text`: Does not add points in this simple model but is captured for review.
A higher total score indicates higher potential risk based on the vendor's responses.

### How to Run Phase 1:

1.  Ensure Python is installed and the virtual environment is activated.
2.  Install required libraries: `pip install -r requirements.txt` (Make sure you've run `pip freeze > requirements.txt` if you installed `pandas` and `openpyxl`).
3.  Run the script from your terminal:
    ```bash
    python phase1_assessor.py
    ```
4.  Follow the prompts to enter the vendor name and provide answers for each question.

### What This Phase Demonstrates (GRC Skills):

*   Understanding of the vendor risk assessment process and structure.
*   Ability to design structured questionnaires for data collection.
*   Implementation of a basic risk scoring methodology.
*   Generating structured reports from collected data.
*   Handling and saving GRC-related data (raw assessment results).
*   Basic Python scripting and automation skills.