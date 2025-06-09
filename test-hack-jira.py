from Jira import Jira
from validation import perform_validation, determine_status
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
        #my_jira.update_jira_status(JIRA_KEY, status)

    except Exception as e:
        print("Authentication failed or connection error occured.")
    
if __name__ == "__main__":
    main()
