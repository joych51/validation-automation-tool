from typing import List, Dict, Any, Optional
from enum import Enum

class ValidationStatus(str, Enum):
    FAILED = "Failed"
    COMPLETE = "Complete"
    PARTIAL = "Partially Validated"
    PENDING = "Pending First Occurrence"

class ValidationType(str, Enum):
    NO_ROWS = "no rows"
    HAS_ROWS = "rows"

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def perform_validation(validations: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Validates SQL queries results against expected results.
    """
    if not isinstance(validations, list):
        raise ValidationError("Validations must be a list")

    results = []
    for validation in validations:
        # Input validation
        if not isinstance(validation, dict):
            raise ValidationError("Each validation must be a dictionary")
        if "sql" not in validation or "expected_results" not in validation:
            raise ValidationError("Validation must contain 'sql' and 'expected_results'")
        
        sql = validation["sql"]
        expected_results = validation["expected_results"]
        
        try:
            # Execute SQL (mocked for now)
            execution_result = _mock_execute_sql(sql)
            
            # Validate results
            passed, error = _validate_result(execution_result, expected_results)
            
            results.append({
                "sql": sql,
                "passed": passed,
                "error": error
            })
        except Exception as e:
            results.append({
                "sql": sql,
                "passed": False,
                "error": f"Execution error: {str(e)}"
            })
    
    return results

def determine_status(results: List[Dict[str, Any]]) -> ValidationStatus:
    """
    Determine overall validation status based on validation results.
    """
    if not results:
        raise ValidationError("No validation results provided")

    # Check for any errors first
    if any(result.get('error') is not None for result in results):
        return ValidationStatus.FAILED

    # Count passes
    total = len(results)
    passed = sum(1 for result in results if result.get('passed', False))

    if passed == total:
        return ValidationStatus.COMPLETE
    elif passed > 0:
        return ValidationStatus.PARTIAL
    else:
        return ValidationStatus.PENDING

def _mock_execute_sql(sql: str) -> Optional[List[Dict[str, Any]]]:
    """Mock function for SQL execution - to be replaced with real implementation"""
    if sql == "SELECT * FROM ROWS":
        return [{"id": 1, "name": "Test"}]
    elif sql == "SELECT * FROM NO ROWS":
        return []
    return None

def _validate_result(execution_result: Optional[List[Dict[str, Any]]], 
                    expected_type: str) -> tuple[bool, Optional[str]]:
    """Helper function to validate execution results against expected type"""
    if execution_result is None:
        return False, "SQL execution failed"
        
    try:
        if expected_type == ValidationType.NO_ROWS:
            return len(execution_result) == 0, None
        elif expected_type == ValidationType.HAS_ROWS:
            return len(execution_result) > 0, None
        else:
            return False, f"Invalid validation type: {expected_type}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"