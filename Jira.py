########################################################################################
# Program Name: Jira.py
# Description: Class for accessing information and updating information in Jira
#########################################################################################
import os
import requests
import json
import jwt 
from datetime import datetime, timezone 
from JiraParser import JiraParser

class Jira(object):
    def __init__(self,jira_url, jira_sid=None, jira_password=None, jira_resource="JPMC:URI:RS-25188-87400-JiraOauthAPI-PROD", 
                 jira_client_id="PC-31400-SID-10276-PROD",jira_domain="NAEAST", ida_url = "https://idag2.jpmorganchase.com/adfs/oauth2/token"):
        """Initialize the Jira class with necessary credentials."""

        self.jira_url = jira_url
        self.jira_sid = jira_sid
        self.jira_password = jira_password
        self.jira_resource = jira_resource
        self.jira_client_id = jira_client_id 
        self.jira_bearer_token = None 
        self.jira_domain = jira_domain
        self.ida_url = ida_url

    def getBearerToken(self):
        """Get a bearer token for Jira API using the provided credentials."""
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'password',
            'username': f"{self.jira_domain}\\{self.jira_sid}",
            'password': self.jira_password,
            'resource': self.jira_resource,
            'client_id': self.jira_client_id
        }
        response = (requests.get(self.ida_url,headers=headers,data=data))
        if response.status_code != 200:
            return 1
        else:
            data = response.json()
            token = str(data['access_token'])
            self.jira_bearer_token = token 
            return 0

    def isTokenExpired(self):
        """Check if the bearer token is expired."""
        if not self.jira_bearer_token:
            return True
        
        # Decode the JWT token to check its expiration
        try:
            decoded_token = jwt.decode(self.jira_bearer_token, options={"verify_signature": False})
            exp = decoded_token.get("exp")
            if exp:
                # Check if the current time is past the expiration time
                return datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc)
        except jwt.ExpiredSignatureError:
            return True
        except Exception as e:
            print(f"Error decoding token: {e}")
            return True
        
        return False
    
    # Given a jql query return all of the cards
    def get_release_cards(self, release_versions = []): 
    # Given a list of jira cards get all the jira_card_info - return info for each card including queries
        """Given a list of release versions, return all jira cards associated with those versions."""
        """Expect the release_version to be MSYYYY-MM-DD fomrat, e.g., MS2024-01-01"""

        cards = []
        jql = "jql=project=%22CMSSTRATUS2%22%20AND%20type%20not%20IN%20(deliverable,epic)%20AND%20Component%20IN%20componentMatch(%22Stratus%20Validations%22)%20AND%20(" 
        iter = 0
        jql=jql + f"fixVersion%20IN%20unreleasedVersions()%20OR%20fixVersion%20IS%20EMPTY)%20AND%20status%20IN(%22OPEN%22,%22ON%20HOLD%22,%22UNDER%20REFINEMENT%22,%22READY%22,%22IN%20PROGRESS%22,%22READY%20FOR%20REVIEW%22,%22DONE%22)"
        jql = jql + "%20AND%20("
        iter = 0
        for release in release_versions:
            if iter != 0:
                jql = jql + "OR%20"
            jql = jql + f"description%20~%20%22{release}%22%20"
            iter = iter + 1
        jql = jql + ")%20AND(description%20!~%20%22PRV%20Incomplete%22%20OR%20description%20!~%20%22PRV-Incomplete%22)"
        if self.isTokenExpired():
            if self.getBearerToken() != 0:
                print("Failed to get bearer token")
                return None
        headers = {
            "Authorization": f"Bearer {self.jira_bearer_token}",
            "Content-Type": "application/json"
        }
        # TODO: make this more dynamic
        jql = jql + "&maxResults=200"
        # TODO: The Jira API indicates the /search api is deprecated, however, when trying to use the /search/jql endpoint on the Chase instance it returns a 404 error
        url = f"{self.jira_url}search?{jql}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            if response_json["total"] > response_json['maxResults']:
                print(f"Warning: More than {response_json['maxResults']} results found. Only the first {response_json['maxResults']} will be returned.")
            for issue in response_json["issues"]:
                cards.append(issue["key"])
            return cards
        else:
            print(f"Error retrieving Jira card: {response.text}")
            return cards

    # Retrieves a Jira card by its key (e.g., "PROJ-123") from the Jira REST API.
    def get_jira_card(self, jira_key):
        """Retrieve a Jira card by its key."""
        if self.isTokenExpired():
            if self.getBearerToken() != 0:
                print("Failed to get bearer token")
                return None
        headers = {
            "Authorization": f"Bearer {self.jira_bearer_token}",
            "Content-Type": "application/json"
        }
        url = f"{self.jira_url}issue/{jira_key}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error retrieving Jira card: {response.text}")
            return None

    def get_jira_status(self, jira_key):
        """ Retrieve the status of a Jira card by its key."""
        jira_card = self.get_jira_card(jira_key)
        try:
            status = jira_card["fields"]["status"]["name"]
        except Exception as e:
            print(f"Error retrieving status for Jira card {jira_key}: {e}")
            return None
        return status 
    
    def get_avail_transitions(self, jira_key):
        """Retrieve available transitions for a Jira card by its key."""
        if self.isTokenExpired():
            if self.getBearerToken() != 0:
                print("Failed to get bearer token")
                return None
        headers = {
            "Authorization": f"Bearer {self.jira_bearer_token}",
            "Content-Type": "application/json"
        }
        url = f"{self.jira_url}issue/{jira_key}/transitions"
        response = requests.get(url, headers=headers)        
        if response.status_code == 200:
            try:
                transitions = response.json()["transitions"]
            except Exception as e:
                transitions=[]
        else:
            transitions = []
        return transitions
                 

    # Extracts the SQL query from a specified field in the Jira card JSON data.
    def extract_sql_query(self,jira_card):
        """Extract SQL query from the Jira card."""
        parser = JiraParser(["fields","description"])
        # Adjust field names based on your Jira structure
        queries = parser.get_jira_queries(jira_card) 
        results = parser.get_jira_expected_results(jira_card)

        return queries, results 
    
    def create_json(self,release_tags, file_name="jira_cards.json", jira_key=None):
        """ Given the release tags, get all of the cards associated with the release, then extract the queries of each card """
        dict = {}
        if jira_key is None:
            cards = self.get_release_cards(release_tags)
        else:
            cards = [jira_key]
        if not cards:
            if file_name is not None:
                json.dump(dict, fout, indent=4)            
                fout.close() 
            return dict
        for card in cards:
            jira_card = self.get_jira_card(card)
            queries, results = self.extract_sql_query(jira_card) 
            idx = 0            
            validations = []
            for query in queries:
                try:
                    result = results[idx]
                except Exception as e:
                    result = None
                validation = {
                    "sql":query,
                    "expected_results":result
                }
                validations.append(validation)
                idx = idx + 1
            issue_dict = {
                "status": jira_card["fields"]["status"]["name"],
                "fixVersions": [version["name"] for version in jira_card["fields"]["fixVersions"]],
                "validations": validations
            }
            dict[card] = issue_dict
        
        if file_name is not None:
            fout = open(file_name, "w")
            json.dump(dict, fout, indent=4)
            fout.close()
        
        return dict

    def add_jira_comment(self, jira_key, comment):
        """Add a comment to a Jira card."""
        if self.isTokenExpired():
            if self.getBearerToken() != 0:
                print("Failed to get bearer token")
                return None            
        url = f"{self.jira_url}issue/{jira_key}/comment"
        payload = {
            "body": comment
        }
        headers = {
            "Authorization": f"Bearer {self.jira_bearer_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
    
        if response.status_code in [200, 201, 204]:
            return True
        else:
            print(f"Error adding comment to Jira card: {response.text}")
            return False
        

    # Updates a Jira card's status by making a transition API call. Maps status strings to appropriate Jira transition IDs.
    def update_jira_status(self,jira_key, status):
        """Update the status of a Jira card."""
        # Map status strings to Jira transition IDs
        if self.isTokenExpired():
            if self.getBearerToken() != 0:
                print("Failed to get bearer token")
                return None
        current_status = self.get_jira_status(jira_key)
        avail_transitions = self.get_avail_transitions(jira_key)                
        if not avail_transitions:
            print(f"No available transitions for Jira card {jira_key}")
            return False
        for transition in avail_transitions:
            if transition["name"] == status:
                transition_id = transition["id"]
                break
        if not transition:
            return False         
        url = f"{self.jira_url}issue/{jira_key}/transitions"        
        payload = {
            "transition": {"id": transition_id},
            "fields":{}
        }
        headers = {
            "Authorization": f"Bearer {self.jira_bearer_token}",
            "Content-Type": "application/json"
        }        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
    
        if response.status_code in [200, 201, 204]:
            return True
        else:
            print(f"Error updating Jira status: {response.text}")
            return False
        
    def get_validations_for_jira(self, jira_key):
        response_json = self.create_json([None, None], None, jira_key)
        return response_json[jira_key]["validations"]
