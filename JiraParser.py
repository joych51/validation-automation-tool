##########################################################################################
# Program Name:	jiraParser.py
# Description:	Utilities which can be used to extract info needed by
#		application for parsing queries/macros etc
#
#
##########################################################################################

import json
import re 
class JiraParser(object):
	def __init__(self, keys=[]):
		self.version = 1.0
		self.query_keys = keys 	
	
	def get_jira_queries(self, js_jira):
		"""Returns the value contained after traversing the keys passed from the calling program. Once field is retrieved Queries are parsed out"""

		# Get the field from Jira
		tmp_dict = js_jira
		for key in self.query_keys:		
			tmp_dict = tmp_dict[key]				
		
		# Strip out line feeds and tabs
		tmp_dict = tmp_dict.replace('\r', ' ').replace('\n', ' ')
		tmp_dict = tmp_dict.replace('{code}','')
		tmp_dict = tmp_dict.replace('{code:java}','')
		tmp_dict = tmp_dict.replace('{code:sql}','')		
		tmp_dict = re.sub(r'[^\x00-\x7F]+', '', tmp_dict)

		# split out the | into separate fields
		query_list = tmp_dict.split("|")
		extract_next = False
		res_queries = []
		query_cnt = 1
		for item in query_list:
			if item.strip() == "SQL":
				extract_next = True
				continue
			if extract_next:
				res_queries.append(item.strip())
				extract_next = False
				query_cnt = query_cnt + 1

		return(res_queries) 
	def get_jira_expected_results(self, js_jira):
		"""Returns the expected results from the Jira card."""

		# Get the field from Jira
		tmp_dict = js_jira
		for key in self.query_keys:		
			tmp_dict = tmp_dict[key]				

		# Strip tabs/line feeds/unicode
		tmp_dict = tmp_dict.replace('\r', ' ').replace('\n', 'EOLEOL')
		tmp_dict = tmp_dict.replace('{code}','')
		tmp_dict = tmp_dict.replace('{code:java}','')
		tmp_dict = tmp_dict.replace('{code:sql}','')		
		tmp_dict = re.sub(r'[^\x00-\x7F]+', '', tmp_dict)

		# split out the | into separate fields
		expected_results_list = tmp_dict.split("|")

		# Determine how many columns are in the expected results
		# This loop will break once we read the header of the Validation Result table
		start_idx = 0				# This will be used to split the remaining results to parse
		cnt = 0 					# Count the columns
		test_number_column = 0		# This is column with the test number
		expected_column = 0			# This is the column with the expected result
		total_columns = 0			# Total # of columns in the expected results table
		find_eol= False			    # After find the ending column, looking for the EOL
		remaining_results = []
		
		for result in expected_results_list:
			start_idx = start_idx + 1

			# Once Validation Number (from Section 4) is found we start counting the columns			
			if "Validation Number" in result.strip() and "(from Section 4)" in result.strip():				
				cnt = 1
				test_number_column = cnt
				continue 			

			# If count is set to 1 we have seen the first column of the table				
			if cnt > 0:				
				# IT appears there are '' fields between columns, we will not count these as they are not present
				# in the data
				if result.strip() != "":
					cnt = cnt + 1
				# This is the column we will get the expected result from 
				if "Expected Validation Result" in result.strip():
					expected_column = cnt
				# This is the end of the column headers, once found look for the EOL
				if "Completed When" in result.strip():
					find_eol = True
					continue
			if find_eol and "EOLEOL" in result.strip():
				break 
		# remaining results are broken to another list
		remaining_results = expected_results_list[start_idx:]
		# Total Cnt is total number of columns		
		total_columns = cnt  
		# Loop through the table and get the expected results 
		cnt = 0
		expected_results = []		
		# Loop through the remaining results, and pull out the result # and expected result
		for result in remaining_results:
			# Stop when hit Section 6
			if "Section 6" in result.strip():
				break
			cnt = cnt + 1
			if cnt == expected_column:
				expected_results.append(result.strip())
				continue
			if cnt >= total_columns:
				if "EOLEOL" in result.strip():
					cnt = 0					
		return(expected_results)

	# get_jira_results 