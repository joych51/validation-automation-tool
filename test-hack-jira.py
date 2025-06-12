from Jira import Jira
from validation import perform_validation, determine_status
from emailer import send_validation_report_email
import getpass
from collections import Counter

JIRA_KEY = "CMSSTRATUS2-89285"
def count_statuses(json_data):
    """Count the number of cards for each status"""
    status_counts = Counter()

    for card_data in json_data.values():
        status = card_data.get('status', 'Unknown')
        status_counts[status] += 1
    return status_counts

def main():
    sid = input("Enter your Jira sid: ")
    passwd = getpass.getpass("Enter Jira Password: ")
    jira_url = "https://jiradc-cib-cluster02.prod.aws.jpmchase.net/rest/api/2/"
    my_jira = Jira(jira_url, sid, passwd)
    fixVersion = "MS2025-03-11"

    try:
        print("Attempting to authenticate with Jira...")

        my_json = my_jira.create_json([fixVersion], None, None)
        print("Retrieved cards for ", fixVersion)
        status_counts = count_statuses(my_json)
        print("\nStatus counts: ")
        for status, count in status_counts.items():
            print(f"{status} : {count}")

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
        
        email_status_counts = {
            'Not Started'               : status_counts.get('Open', 0),
            'Deferred'                  : status_counts.get('On Hold', 0),
            'In Progress'               : status_counts.get('Under Refinement', 0),
            'Pending First Occurrence'  : status_counts.get('Ready', 0),
            'Partially Validated'       : status_counts.get('In Progress', 0),
            'Failed'                    : status_counts.get('Ready For Review', 0),
            'Done'                      : status_counts.get('Done', 0)
        }
        # Send email with validation results
        send_validation_report_email(
            fix_version_name=card_details['fixVersion'],
            results=email_status_counts,  # Update these counts based on your needs
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
