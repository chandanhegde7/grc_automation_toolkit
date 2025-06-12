import csv
import os

def load_questionnaire(filepath="vendor_questionnaire_template.csv"):
    """Loads the questionnaire template from a CSV file."""
    questions = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as infile:
            # Use DictReader for easy access by column name
            reader = csv.DictReader(infile)
            # Ensure required columns exist
            required_cols = ['QuestionID', 'QuestionText', 'AnswerType', 'RiskWeight', 'RiskArea']
            
            
            if not all(col in reader.fieldnames for col in required_cols):
                 raise ValueError(f"CSV is missing required columns. Make sure it has: {required_cols}")

            for row in reader:
                # Basic type conversion for RiskWeight
                try:
                    row['RiskWeight'] = int(row['RiskWeight'])
                except ValueError:
                    print(f"Warning: Invalid RiskWeight for QuestionID {row.get('QuestionID', 'N/A')}. Using 0.")
                    row['RiskWeight'] = 0 # Default to 0 if not a valid number
                questions.append(row)
        print(f"Successfully loaded {len(questions)} questions from {filepath}")
        return questions
    except FileNotFoundError:
        print(f"Error: Questionnaire template not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred loading the questionnaire: {e}")
        return None
    
def get_validated_input(question):
    """Gets validated input from the user based on the question's AnswerType."""
    prompt = f"\n{question['QuestionID']}: {question['QuestionText']} ({question['AnswerType']})\nYour answer: "
    while True:
        user_input = input(prompt).strip().lower() # Get input, strip whitespace, lowercase
        answer_type = question['AnswerType'].lower()

        if answer_type == 'yes_no':
            if user_input in ['yes', 'no', 'y', 'n']:
                # Standardize answer for consistency
                return 'yes' if user_input in ['yes', 'y'] else 'no'
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        elif answer_type == 'score_1_5':
            try:
                score = int(user_input)
                if 1 <= score <= 5:
                    return str(score) # Return as string to keep data consistent
                else:
                    print("Invalid input. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif answer_type == 'text':
            if user_input: # Allow any non-empty string
                 return user_input # Return original case for text
            else:
                print("Input cannot be empty for text questions.")
        else:
            # Should not happen if template is correct, but good fallback
            print(f"Warning: Unknown AnswerType '{question['AnswerType']}'. Accepting any text.")
            return user_input

def conduct_assessment(questions):
    """Guides the user through the questionnaire and collects answers."""
    if not questions:
        print("No questions loaded to conduct assessment.")
        return None

    vendor_name = input("Enter the name of the vendor being assessed: ").strip()
    if not vendor_name:
        print("Vendor name cannot be empty. Assessment cancelled.")
        return None

    print(f"\n--- Starting Assessment for {vendor_name} ---")

    assessment_results = []
    for question in questions:
        answer = get_validated_input(question)
        assessment_results.append({
            'QuestionID': question['QuestionID'],
            'QuestionText': question['QuestionText'],
            'AnswerType': question['AnswerType'],
            'RiskWeight': question['RiskWeight'], # Keep the weight for scoring
            'RiskArea': question['RiskArea'],
            'AnswerGiven': answer,
            # RelevantFrameworkControl will be added in Phase 2 processing
        })

    print(f"\n--- Assessment for {vendor_name} Completed ---")
    return vendor_name, assessment_results

def calculate_risk_score(assessment_results):
    """Calculates a simple total risk score based on answers and weights."""
    total_risk_points = 0
    question_scores = {} # To store points per question

    for result in assessment_results:
        question_id = result['QuestionID']
        answer = result['AnswerGiven']
        answer_type = result['AnswerType'].lower()
        risk_weight = result['RiskWeight']
        points = 0 # Points contributed by this answer

        if answer_type == 'yes_no':
            # 'no' answers add risk points based on weight
            if answer == 'no':
                points = risk_weight
            # 'yes' answers add 0 points

        elif answer_type == 'score_1_5':
             try:
                 score = int(answer)
                 # Lower scores (1, 2) add more risk points based on weight
                 # Score 1 adds (5-1)*weight = 4*weight
                 # Score 5 adds (5-5)*weight = 0*weight
                 points = (5 - score) * risk_weight
             except ValueError:
                 # Should not happen with validation, but handle defensively
                 print(f"Warning: Could not score QuestionID {question_id} with invalid answer '{answer}'.")
                 points = risk_weight # Assume highest risk if un-scorable

        # Text answers don't contribute directly to this simple numeric score
        # You could add logic here to flag text answers for review if needed

        total_risk_points += points
        question_scores[question_id] = points # Store points for this question

    return total_risk_points, question_scores

def generate_assessment_report(vendor_name, assessment_results, total_score, question_scores):
    """Generates a human-readable assessment report in Markdown format."""
    report_filename = f"assessment_report_{vendor_name.replace(' ', '_').lower()}.md"

    with open(report_filename, mode='w', encoding='utf-8') as outfile:
        outfile.write(f"# Vendor Risk Assessment Report: {vendor_name}\n\n")
        outfile.write(f"**Date of Assessment:** {os.path.basename(__file__)} (Simulated)\n") # Indicates it's from your script
        outfile.write(f"**Total Risk Score (Higher is riskier):** {total_score}\n\n") # Explain what score means

        # Basic scoring interpretation (optional)
        if total_score > 50: # Example thresholds, adjust based on your RiskWeights
            risk_level = "High"
        elif total_score > 20:
            risk_level = "Medium"
        else:
             risk_level = "Low"
        outfile.write(f"**Overall Risk Level (Based on simple scoring):** {risk_level}\n\n")


        outfile.write("## Detailed Responses\n\n")

        # Sort results by RiskArea for better readability
        sorted_results = sorted(assessment_results, key=lambda x: x.get('RiskArea', ''))

        current_risk_area = None
        for result in sorted_results:
            if result.get('RiskArea') != current_risk_area:
                current_risk_area = result.get('RiskArea', 'Uncategorized')
                outfile.write(f"### {current_risk_area}\n\n")

            question_id = result['QuestionID']
            points_earned = question_scores.get(question_id, 0)

            outfile.write(f"**{question_id}:** {result['QuestionText']}\n")
            outfile.write(f"> **Answer:** {result['AnswerGiven']}\n")
            # Only show points if they contributed
            if result['AnswerType'].lower() != 'text':
                 outfile.write(f"> **Risk Points Added:** {points_earned} (Weight: {result['RiskWeight']})\n")
            outfile.write("\n") # Add a blank line between questions

        outfile.write("\n---\n")
        outfile.write("This is a simulated assessment generated by a GRC Automation Toolkit project. The scoring is based on a simplified model.")

    print(f"Assessment report saved to {report_filename}")
    return report_filename

def save_assessment_data(vendor_name, assessment_results):
    """Saves the raw assessment results to a CSV file for further processing."""
    data_filename = f"completed_assessment_{vendor_name.replace(' ', '_').lower()}.csv"
    # Ensure the data includes RiskWeight and AnswerType for Phase 2 logic
    fieldnames = ['QuestionID', 'QuestionText', 'AnswerType', 'RiskWeight', 'RiskArea', 'AnswerGiven'] # Add more fields if needed

    try:
        with open(data_filename, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(assessment_results)
        print(f"Raw assessment data saved to {data_filename}")
        return data_filename
    except Exception as e:
        print(f"Error saving raw assessment data: {e}")
        return None
    
if __name__ == "__main__":
    # Ensure we are in the activated virtual environment (optional check)
    # import sys
    # if 'venv' not in sys.executable:
    #     print("Warning: Not running in the virtual environment. Activate it before running.")
    #     # Optionally exit: sys.exit(1)

    questionnaire = load_questionnaire()
    if questionnaire:
        vendor_name, results = conduct_assessment(questionnaire)
        if results:
            total_score, question_scores = calculate_risk_score(results)
            report_file = generate_assessment_report(vendor_name, results, total_score, question_scores)
            data_file = save_assessment_data(vendor_name, results)
            print("\nPhase 1 completed.")
            if report_file: print(f"- Report: {report_file}")
            if data_file: print(f"- Data: {data_file}")
    else:
         print("Could not load questionnaire. Exiting.")