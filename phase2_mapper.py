import csv
import os
import glob # To easily find the latest completed assessment file

# --- Helper function (can copy from phase1_assessor or define here) ---
def load_csv_data(filepath):
    """Loads CSV data using DictReader."""
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            data = list(reader) # Read all rows into a list
        print(f"Successfully loaded {len(data)} rows from {filepath}")
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred loading {filepath}: {e}")
        return None

# --- Core Logic for Phase 2 ---
def analyze_framework_impact(template_questions, assessment_results):
    """Analyzes assessment results and maps risky answers to framework controls."""
    if not template_questions or not assessment_results:
        print("Missing template or assessment results for analysis.")
        return None

    # Create a dictionary for quick lookup of question details from template
    question_lookup = {q['QuestionID']: q for q in template_questions}

    # Dictionary to store findings aggregated by framework control
    # Structure: { 'FRAMEWORK:CONTROL_ID': [ {'QuestionID': '...', 'AnswerGiven': '...', 'RiskPoints': '...'}, ... ], ... }
    framework_findings = {}

    print("\n--- Analyzing Assessment Results for Framework Impact ---")

    for result in assessment_results:
        q_id = result.get('QuestionID')
        answer = result.get('AnswerGiven')
        answer_type = result.get('AnswerType', '').lower()
        # Ensure RiskWeight is an integer for comparison logic below
        try:
             risk_weight = int(result.get('RiskWeight', 0))
        except ValueError:
             risk_weight = 0 # Default if invalid

        # Re-calculate the simple risk points for this answer (needs to match Phase 1 logic)
        points_earned = 0
        if answer_type == 'yes_no':
            if answer == 'no':
                points_earned = risk_weight
        elif answer_type == 'score_1_5':
             try:
                 score = int(answer)
                 points_earned = (5 - score) * risk_weight
             except ValueError:
                 pass # Already warned in Phase 1, skip scoring

        # Define what constitutes a "risky" answer that warrants mapping
        # This is subjective; adjust based on your simple scoring threshold
        # Example: Any question that added points based on the Phase 1 scoring
        is_risky_answer = points_earned > 0 # Or perhaps points_earned >= a certain threshold (e.g., 3 or 4)

        if is_risky_answer and q_id in question_lookup:
            template_info = question_lookup[q_id]
            relevant_controls_str = template_info.get('RelevantFrameworkControl', '').strip()

            if relevant_controls_str:
                # Split multiple controls if separated by semicolon
                relevant_controls = [c.strip() for c in relevant_controls_str.split(';') if c.strip()]

                finding_details = {
                    'QuestionID': q_id,
                    'QuestionText': template_info.get('QuestionText'), # Get full text from template
                    'AnswerGiven': answer,
                    'RiskPoints': points_earned,
                    'RiskArea': template_info.get('RiskArea'), # Get area from template
                }

                for control in relevant_controls:
                    if control not in framework_findings:
                        framework_findings[control] = []
                    framework_findings[control].append(finding_details)
                    print(f"  - Mapped risky answer from {q_id} to {control}")

    print(f"\nAnalysis completed. Found potential impacts on {len(framework_findings)} framework control(s).")
    return framework_findings

def generate_framework_report(vendor_name, framework_findings):
    """Generates a report detailing framework controls impacted by vendor assessment findings."""
    report_filename = f"framework_compliance_report_{vendor_name.replace(' ', '_').lower()}.md"

    with open(report_filename, mode='w', encoding='utf-8') as outfile:
        outfile.write(f"# Framework Compliance Impact Report for Vendor: {vendor_name}\n\n")
        outfile.write(f"**Date of Analysis:** {os.path.basename(__file__)} (Simulated)\n")
        # Determine which framework was used based on the findings keys (basic)
        frameworks_found = sorted(list(set([c.split(':')[0] for c in framework_findings.keys() if ':' in c])))
        outfile.write(f"**Potentially Impacted Frameworks:** {', '.join(frameworks_found) or 'N/A'}\n\n")

        if not framework_findings:
            outfile.write("No potential framework control impacts were identified based on the vendor's assessment responses.\n")
        else:
            outfile.write("## Potential Framework Control Impacts\n\n")
            outfile.write("The following controls may be impacted by the vendor's security posture based on their assessment responses. This indicates areas of potential risk or where compensating controls may be needed internally.\n\n")

            # Sort controls alphabetically for consistency
            sorted_controls = sorted(framework_findings.keys())

            for control in sorted_controls:
                findings = framework_findings[control]
                outfile.write(f"### {control}\n\n")
                outfile.write("Relevant findings from the vendor assessment:\n\n")

                for finding in findings:
                    outfile.write(f"- **Question:** {finding.get('QuestionID', 'N/A')}: {finding.get('QuestionText', 'N/A')}\n")
                    outfile.write(f"  - **Vendor Answer:** {finding.get('AnswerGiven', 'N/A')}\n")
                    if finding.get('RiskPoints', 0) > 0: # Only show points if they contributed
                         outfile.write(f"  - **Risk Points Added:** {finding.get('RiskPoints', 0)}\n")
                    outfile.write(f"  - **Risk Area:** {finding.get('RiskArea', 'N/A')}\n")
                    outfile.write("\n") # Blank line after each finding

        outfile.write("\n---\n")
        outfile.write("This is a simulated analysis generated by a GRC Automation Toolkit project. The mapping and risk identification are based on simplified criteria.")

    print(f"Framework impact report saved to {report_filename}")
    return report_filename

if __name__ == "__main__":
    # Find the latest completed assessment data file
    # Assumes filename format: completed_assessment_[vendor_name].csv
    # You might need to adjust this if you change the filename format
    list_of_files = glob.glob('completed_assessment_*.csv')
    if not list_of_files:
        print("Error: No completed assessment data files found ('completed_assessment_*.csv'). Run Phase 1 first.")
    else:
        latest_file = max(list_of_files, key=os.path.getctime)
        print(f"Using latest assessment data file: {latest_file}")

        # Extract vendor name from the filename (basic parsing)
        vendor_name = os.path.basename(latest_file).replace('completed_assessment_', '').replace('.csv', '').replace('_', ' ').title()
        print(f"Assessing framework impact for vendor: {vendor_name}")


        template_questions = load_csv_data("vendor_questionnaire_template.csv") # Load the updated template
        assessment_results = load_csv_data(latest_file) # Load the completed assessment data

        if template_questions and assessment_results:
            framework_findings = analyze_framework_impact(template_questions, assessment_results)
            if framework_findings is not None: # analyze_framework_impact returns {} if no findings, or None on error
               report_file = generate_framework_report(vendor_name, framework_findings)
               if report_file: print(f"\nPhase 2 completed. Report: {report_file}")
            else:
                print("\nPhase 2 analysis failed.")
        else:
            print("Could not load required data files for Phase 2. Exiting.")