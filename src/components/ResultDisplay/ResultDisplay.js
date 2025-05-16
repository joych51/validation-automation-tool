import { ResultContainer, ResultTitle, ResultRow, QuerySection, QueryTitle, QueryBox, StatusText, ErrorMessage } from "./ResultDisplay.styles";

const ResultDisplay = ({ result, error }) => {

  if (error) {
    return (
      <ResultContainer error>
        <ErrorMessage>{error}</ErrorMessage>
      </ResultContainer>
    );
  }

  if (!result) return null;

  return (
    <ResultContainer>
      <ResultTitle>Validation Results</ResultTitle>
      <ResultRow>
        <span>Status:</span>
        <StatusText success={result.status === "success"}>{result.status}</StatusText>
      </ResultRow>
      <ResultRow>
        <span>Execution Time:</span>
        <span>{result.executionTime}ms</span>
      </ResultRow>
      <QuerySection>
        <QueryTitle>Query:</QueryTitle>
        <QueryBox>{result.query}</QueryBox>
      </QuerySection>
    </ResultContainer>
  );
};

export default ResultDisplay;
