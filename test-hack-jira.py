from Jira import Jira
from validation import perform_validation, determine_status
from emailer import send_validation_report_email
import getpass

JIRA_KEY = "CMSSTRATUS2-89285"

def main():
    sid = input("Enter your Jira sid: ")
    passwd = getpass.getpass("Enter Jira Password: ")
    jira_url = "https://jiradc-cib-cluster02.prod.aws.jpmchase.net/rest/api/2/"
    my_jira = Jira(jira_url, sid, passwd)
    my_json = my_jira.create_json(["MS2025-03-11"],None,None)

    print(my_json)

    try:
        print("Attempting to authenticate with Jira...")

        print("Jira Key:", JIRA_KEY)
        validations = my_jira.get_validations_for_jira(JIRA_KEY)
        print("Validations:", validations)

        validation_results = perform_validation(validations)
        print("Validation Results:", validation_results)
        
        status = determine_status(validation_results)
        print("Status:", status.value)
        
        # Get card details using get_jira_card
        jira_card = my_jira.get_jira_card(JIRA_KEY)
        if not jira_card:
            raise Exception("Failed to get Jira card details")
            
        # Extract card details from the response
        card_details = {
            'fixVersion': jira_card['fields'].get('fixVersions', [{}])[0].get('name', 'Unknown Version'),
            'summary': jira_card['fields'].get('summary', 'No Summary')
        }
        
        # Prepare validation results for email
        validation_data = {
            JIRA_KEY: {
                'status': status,
                'results': validation_results
            }
        }
        
        # Send email with validation results
        send_validation_report_email(
            fix_version_name=card_details['fixVersion'],
            results={'Not Started': 0, 'Deferred': 0, 'In Progress': 0,
                    'Pending First Occurrence': 0, 'Partially Validated': 0,
                    'Failed': 0, 'Done': 0},  # Update these counts based on your needs
            cards=[{
                'key': JIRA_KEY,
                'summary': card_details['summary'],
                'status': status.value
            }],
            validation_results=validation_data
        )

    except Exception as e:
        print("Authentication failed or connection error occurred:", str(e))
    
if __name__ == "__main__":
    main()
