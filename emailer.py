import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from validation import ValidationStatus

# Generates and sends an HTML email with formatted validation status results. 
# Creates an HTML table of all validation results. 
# Color-codes different statuses for visual clarity. 
# Sends email to the whole team. 
# Handles sending errors gracefully
def send_validation_report_email(fix_version_name, results, cards, validation_results=None):
    """Generate and send validation report email"""
    # Create message
    msg = MIMEMultipart()
    msg['Subject'] = f"Stratus Validation Report: {fix_version_name} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    msg['From'] = "junsoeng.lee@jpmchase.com"
    msg['To'] = "junsoeng.lee@jpmchase.com"
    # "Stratus_PROD_Validations@restricted.chase.com"
    
    # Create HTML content
    html = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 20px; }}
          h1 {{ color: #0052CC; }}
          .summary-table {{width: 30%; margin: 0 auto }}
          table {{ border-collapse: collapse; width: 100%; }}
          th, td {{ border: 1px solid #ddd; padding: 6px; text-align: left; }}
          th {{ background-color: #f2f2f2; }}
          .success {{ color: green; }}
          .failed {{ color: red; }}
          .partial {{ color: orange; }}
          .pending {{ color: gray; }}
        </style>
      </head>
      <body>
        <h1>Validation Report: {fix_version_name}</h1>
        <h2>Summary</h2>
        <table class = "summary-table">
          <tr>
            <th>Status</th>
            <th>Count</th>
          </tr>
          <tr>
            <td>Not Started</td>
            <td>{results['Not Started']}</td>
          </tr>
          <tr>
            <td>Deferred</td>
            <td>{results['Deferred']}</td>
          </tr>
          <tr>
            <td>In Progress</td>
            <td>{results['In Progress']}</td>
          </tr>
          <tr>
            <td>Pending First Occurrence</td>
            <td>{results['Pending First Occurrence']}</td>
          </tr>
          <tr>
            <td>Partially Validated</td>
            <td>{results['Partially Validated']}</td>
          </tr>
          <tr>
            <td>Validation Failed</td>
            <td>{results['Failed']}</td>
          </tr>
          <tr>
            <td>Done</td>
            <td>{results['Done']}</td>
          </tr>
        </table>
        
        <h2>Details</h2>
        <table>
          <tr>
            <th>Jira Key</th>
            <th>Summary</th>
            <th>Status</th>
            <th>Validation Status</th>
            <th>Validation Details</th>
          </tr>
    """
    
    # Add card details with validation results
    for card in cards:
        status_color = ""
        if card['status'] == 'Done':
            status_color = "success"
        elif card['status'] == 'Failed':
            status_color = "failed"
        
        # Find validation results for this card if available
        validation_info = ""
        validation_status = ""
        if validation_results and card['key'] in validation_results:
            card_validation = validation_results[card['key']]
            validation_status = card_validation['status'].value
            validation_info = "<br>".join([
                f"SQL: {result['sql']}<br>Result: {'✅' if result['passed'] else '❌'}"
                for result in card_validation['results']
            ])
        
        html += f"""
          <tr>
            <td><a href=https://jiradc-cib-cluster02.prod.aws.jpmchase.net/browse/{card['key']}">{card['key']}</a></td>
            <td>{card['summary']}</td>
            <td class="{status_color}">{card['status']}</td>
            <td class="{status_color}">{validation_status}</td>
            <td>{validation_info}</td>
          </tr>
        """
    
    html += """
        </table>
      </body>
    </html>
    """
    
    # Attach HTML content
    msg.attach(MIMEText(html, 'html'))
    
    # Send email using JP Morgan's mail relay
    try:
        # JPM internal mail settings
        SMTP_SERVER = 'mailhost.jpmchase.net'
        SMTP_PORT = 25

        print(f"Connecting to JPM Mail Relay: {SMTP_SERVER}:{SMTP_PORT}")
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        smtp.ehlo()
        smtp.starttls()

        print(f"Sending email from {msg['From']} to {msg['To']}...")
        smtp.send_message(msg)
        smtp.quit()
        print("✅ Email sent successfully!")
        return True
    
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
    
def save_email_to_file(fix_version_name, results, cards):
    """Save the email content to an HTML file instead of sending via SMTP"""
    # Create the same HTML content as your email function
    html = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 20px; }}
          h1 {{ color: #0052CC; }}
          table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
          th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
          th {{ background-color: #f2f2f2; }}
        </style>
      </head>
      <body>
        <h1>Validation Report: {fix_version_name}</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <h2>Summary</h2>
        <table>
          <tr>
            <th>Status</th>
            <th>Count</th>
          </tr>
          <tr>
            <td>Not Started</td>
            <td>{results['Not Started']}</td>
          </tr>
          <tr>
            <td>Deferred</td>
            <td>{results['Deferred']}</td>
          </tr>
          <tr>
            <td>In Progress</td>
            <td>{results['In Progress']}</td>
          </tr>
          <tr>
            <td>Pending First Occurrence</td>
            <td>{results['Pending First Occurrence']}</td>
          </tr>
          <tr>
            <td>Partially Validated</td>
            <td>{results['Partially Validated']}</td>
          </tr>
          <tr>
            <td>Failed</td>
            <td>{results['Failed']}</td>
          </tr>
          <tr>
            <td>Done</td>
            <td>{results['Done']}</td>
          </tr>
        </table>
        
        <h2>Details</h2>
        <table>
          <tr>
            <th>Jira Key</th>
            <th>Summary</th>
            <th>Status</th>
          </tr>
    """
    
    # Add card details with status color-coding
    for card in cards:
        status_color = ""
        if card['status'] == 'Done':
            status_color = "color: green;"
        elif card['status'] == 'Failed':
            status_color = "color: red;"
        
        html += f"""
          <tr>
            <td><a href="https://jiradc-cib-cluster02.prod.aws.jpmchase.net/browse/{card['key']}">{card['key']}</a></td>
            <td>{card['summary']}</td>
            <td style="{status_color}">{card['status']}</td>
          </tr>
        """
    
    html += """
        </table>
        <p>This report was generated for viewing offline.</p>
      </body>
    </html>
    """
    
    # Create a reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    
    # Create a filename based on the fix version and timestamp
    filename = f"reports/validation_report_{fix_version_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    
    # Write the HTML to a file
    with open(filename, "w") as f:
        f.write(html)
    
    # Get the absolute path for display
    abs_path = os.path.abspath(filename)
    print(f"✅ Validation report saved to: {abs_path}")
    
    return True

def test_email_functionality():
    """Test both email sending and file generation"""
    # Create mock data
    mock_fix_version = f"TEST-VERSION-{datetime.now().strftime('%Y%m%d-%H%M')}"
    mock_results = {
        'Not Started': 10, 'Deferred': 2, 'In Progress': 5,
        'Pending First Occurrence': 3, 'Partially Validated': 4,
        'Failed': 2, 'Done': 15
    }
    mock_cards = [
        {'key': 'TEST-101', 'summary': 'Test successful card', 'status': 'Done'},
        {'key': 'TEST-102', 'summary': 'Test failed card', 'status': 'Failed'},
        {'key': 'TEST-103', 'summary': 'Test pending card', 'status': 'Pending First Occurrence'},
        {'key': 'TEST-104', 'summary': 'Test partial card', 'status': 'Partially Validated'},
        {'key': 'TEST-105', 'summary': 'Test in progress card', 'status': 'In Progress'}
    ]
    
    # Try email first
    print("\nTesting email sending...")
    email_success = send_validation_report_email(mock_fix_version, mock_results, mock_cards)
    
    # Try file backup regardless
    print("\nTesting file generation...")
    file_success = save_email_to_file(mock_fix_version, mock_results, mock_cards)
    
    print("\nTest Results:")
    print(f"Email sending: {'✅ Success' if email_success else '❌ Failed'}")
    print(f"File generation: {'✅ Success' if file_success else '❌ Failed'}")
    
    return email_success or file_success

if __name__ == "__main__":
    test_email_functionality()
