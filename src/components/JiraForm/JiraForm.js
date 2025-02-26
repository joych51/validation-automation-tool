import { FaSearch, FaSpinner } from "react-icons/fa";
import { FormContainer, InputWrapper, Input, Button } from "./JiraForm.styles";

const JiraForm = ({ jiraKey, setJiraKey, loading, handleSubmit }) => {
  return (
    <FormContainer onSubmit={handleSubmit}>
      <InputWrapper>
        <Input type="text" value={jiraKey} onChange={(e) => setJiraKey(e.target.value)} placeholder="Enter Jira Key (e.g., PROJ-123)" />
        <Button type="submit" disabled={loading || !jiraKey}>
          {loading ? <FaSpinner style={{ animation: "spin 1s linear infinite" }} /> : <FaSearch />}
        </Button>
      </InputWrapper>
    </FormContainer>
  );
};

export default JiraForm;
