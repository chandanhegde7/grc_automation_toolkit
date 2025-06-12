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

## Phase 2: Framework Control Mapper

This phase extends the toolkit by processing the raw assessment data collected in Phase 1 and mapping 'risky' vendor responses to specific controls within industry security frameworks (such as ISO 27001 and NIST CSF). This analysis helps identify potential compliance gaps or increased risks to the organization based on the vendor's security posture.

### How it Works:

1.  Reads the updated `vendor_questionnaire_template.csv` which now includes mappings between questions and relevant framework controls in the `RelevantFrameworkControl` column.
2.  Loads the completed vendor assessment data from the CSV file generated in Phase 1 (`completed_assessment_*.csv`). The script is designed to automatically find the latest assessment file.
3.  Analyzes each vendor answer from the assessment data. It uses the same logic as Phase 1's scoring to determine if an answer indicates a potential risk or weakness (e.g., a 'no' to a 'yes_no' question, or a low score).
4.  For each 'risky' answer, it looks up the corresponding framework controls defined in the template CSV.
5.  Aggregates the findings, listing each impacted framework control and the specific vendor answers that flagged it as a potential concern.
6.  Generates a Markdown report (`framework_compliance_report_*.md`) detailing the identified framework controls and the associated vendor assessment findings.

### Framework Mapping Logic:

*   The script uses the `RelevantFrameworkControl` column in the template CSV to establish links between questions and specific controls (e.g., `ISO27001:A.8.2.3; NISTCSF:PR.DS-1`).
*   A 'risky' answer to a question (an answer that added points in the Phase 1 scoring logic) triggers an identification that the corresponding framework control(s) are potentially impacted by the vendor's security practices. This highlights areas where further investigation, vendor remediation, or internal compensating controls might be necessary to maintain your organization's overall compliance and risk posture relative to that framework.

### How to Run Phase 2:

1.  Ensure you have completed Phase 1 and generated a `completed_assessment_*.csv` file.
2.  Ensure the `vendor_questionnaire_template.csv` file has been updated with relevant framework control mappings in the `RelevantFrameworkControl` column.
3.  Ensure Python is installed and the virtual environment is activated.
4.  Ensure required libraries are installed (`pip install -r requirements.txt`).
5.  Run the script from your terminal:
    ```bash
    python phase2_mapper.py
    ```
6.  The script will find the latest completed assessment and generate the report.

### What This Phase Demonstrates (GRC Skills):

*   Strong understanding of industry security standards and regulatory frameworks (ISO 27001, NIST CSF, etc.) and their controls.
*   Ability to map real-world scenarios/risks (vendor posture) to specific framework requirements.
*   Conducting a form of compliance gap analysis based on external data.
*   Analyzing assessment results to identify potential impacts on organizational compliance.
*   Generating structured reports on framework compliance findings.
*   Processing and linking structured GRC data from multiple sources.
*   Further Python scripting and automation skills.

## Overall GRC Skills Demonstrated

*   **Governance:** Understanding of applying policies and standards via framework mapping.
*   **Risk Management:** Identifying, assessing (via scoring), and documenting risks (vendor-related).
*   **Compliance:** Working with industry frameworks (ISO 27001, NIST CSF), assessing against requirements, and identifying potential gaps.
*   **Third-Party Risk Management:** Designing and conducting vendor assessments.
*   **GRC Tool Simulation:** Building a basic tool demonstrates understanding of GRC data structures and process automation.
*   **Data Management:** Working with structured data (CSV) for GRC activities.
*   **Reporting & Documentation:** Generating clear, structured reports (Markdown) on assessment findings and framework impacts.
*   **Automation & Scripting:** Using Python to automate repetitive GRC tasks, improving efficiency.
*   **Problem Solving:** Designing the logic for assessment, scoring, and mapping.



## Setup and Running the Project

To run this toolkit locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/chandanhegde7/grc_automation_toolkit.git
    cd grc_automation_toolkit 
    ```
2.  **Install Python:** Download and install Python 3.x from [python.org](https://www.python.org/). Ensure it's added to your PATH.
3.  **Create and Activate Virtual Environment:**
    ```bash
    # On macOS/Linux:
    python3 -m venv venv
    source venv/bin/activate
    # On Windows:
    python -m venv venv
    .\venv\Scripts\activate
    ```
    (Remember to activate the venv in each new terminal session you use for the project).
4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run Phase 1 (Vendor Assessment):**
    ```bash
    python phase1_assessor.py
    ```
    Follow the prompts. This generates the assessment data CSV.
6.  **Run Phase 2 (Framework Mapping):**
    ```bash
    python phase2_mapper.py
    ```
    This processes the assessment data and generates the framework impact report.

## Technologies Used

*   Python 3
*   Standard Python Libraries (`csv`, `os`, `glob`)
*   `pandas` (Optional, but used in setup - useful for data handling)
*   `openpyxl` (Optional, needed for pandas to read/write `.xlsx`)
*   Markdown (for report formatting)
*   Git & GitHub (for version control and hosting)