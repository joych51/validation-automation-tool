# Validation Automation Tool

## **Project Overview**
Develop an automated React-based tool to validate Jira cards by executing SQL queries specified within the cards. The tool connects to an Oracle Database (TH) to retrieve data, compare it with expected results, and update the Jira card status accordingly. The backend is implemented using Python and FastAPI.

---

## **Key Features**
1. **Jira Integration**:
   - Use Jira API to access and retrieve Jira cards.
   - Extract SQL queries from a specific section of each card.

2. **Database Connection**:
   - Connect to the Oracle Database (TH) to execute the extracted SQL queries.
   - Retrieve and compare the results with the expected table specified in the Jira card.

3. **Validation Logic**:
   - If the results match the expected table, update the Jira card status to "Complete."
   - If the results do not match, update the status to "Failed."
   - If only partial validation is possible, update the status to "Partially Validated."
   - If no data is found, update the status to "Pending First Occurrence."

4. **User Interface**:
   - Implement a GUI using React with a "Start" button to initiate the automation process.
   - Provide an input field for users to manually enter a Jira key for validation.

5. **Backend Implementation**:
   - Use Python and FastAPI to handle API requests, database connections, and validation logic.
   - Ensure secure and efficient communication between the frontend and backend.

6. **Automated Status Reporting**:
   - Every 12 hours, send an email to `IT_STRATUS_DEV@jpmchase.com` with the status of all Jira cards.
   - Include details of each card's validation status in the email.

---

## **Step-by-Step Guide**

### **Step 1: Set Up the Project Structure**
1. **Frontend (React)**:
   - Use the existing `validation-automation-tool` folder for the React frontend.
   - Ensure dependencies like `axios` are installed.

2. **Backend (Python + FastAPI)**:
   - Create a `backend` folder for the FastAPI backend.
   - Set up a Python virtual environment and install dependencies:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     pip install fastapi uvicorn python-oracledb requests
     ```

3. **Folder Structure**:
validation-automation-tool/
    frontend/               # React frontend code
    backend/                # FastAPI backend code
        app/
            main.py         # FastAPI entry point
            database.py     # Handles Oracle DB connections
            jira.py         # Jira API integration
            validation.py   # Validation logic for SQL queries
            emailer.py      # Email reporting functionality
        requirements.txt    # Python dependencies