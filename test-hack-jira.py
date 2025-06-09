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
    
    try:
        print("Attempting to authenticate with Jira...")

        print("Jira Key:", JIRA_KEY)
        validations = my_jira.get_validations_for_jira(JIRA_KEY)
        print("Validations:", validations)

        validation_results = perform_validation(validations)
        print("Validation Results:", validation_results)
        
        status = determine_status(validation_results)
        print("Status:", status.value)
        
        # Get card details
        card_details = my_jira.get_card_details(JIRA_KEY)
        
        # Prepare validation results for email
        validation_data = {
            JIRA_KEY: {
                'status': status,
                'results': validation_results
            }
        }
        
        # Send email with validation results
        email_success = send_validation_report_email(
            fix_version_name=card_details.get('fixVersion', 'Unknown Version'),
            results={'Not Started': 0, 'Deferred': 0, 'In Progress': 0,
                    'Pending First Occurrence': 0, 'Partially Validated': 0,
                    'Failed': 0, 'Done': 0},  # Update these counts based on your needs
            cards=[{
                'key': JIRA_KEY,
                'summary': card_details.get('summary', 'No Summary'),
                'status': status.value
            }],
            validation_results=validation_data
        )
        
        if email_success:
            print("✅ Email sent successfully!")
        else:
            print("❌ Failed to send email")

    except Exception as e:
        print("Authentication failed or connection error occurred:", str(e))
    
if __name__ == "__main__":
    main()