import { useState } from "react";
import styled from "styled-components";
import GlobalStyles from "./styles/GlobalStyles";
import Header from "./components/Header/Header";
import JiraForm from "./components/JiraForm/JiraForm";
import ResultDisplay from "./components/ResultDisplay/ResultDisplay";
import Footer from "./components/Footer/Footer";

const Container = styled.div`
  min-height: 100vh;
  background-color: #1a1a1a;
`;

const Content = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 4rem 1rem;
`;

function App() {
  const [jiraKey, setJiraKey] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Mock API response
  const mockApiResponse = {
    "PROJ-123": {
      status: "success",
      query: "SELECT * FROM users WHERE id = 123",
      executionTime: 500,
    },
    "PROJ-456": {
      status: "error",
      message: "Invalid Jira key format",
      executionTime: 100,
    },
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Mock validation
      if (!jiraKey.match(/^[A-Z]+-\d+$/)) {
        throw new Error("Invalid Jira key format. Example: PROJ-123");
      }

      // Get mock response
      const response = mockApiResponse[jiraKey] || {
        status: "success",
        query: `SELECT * FROM validation WHERE jira_key = '${jiraKey}'`,
        executionTime: Math.floor(Math.random() * 1000),
      };

      if (response.status === "error") {
        throw new Error(response.message);
      }

      setResult(response);
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <GlobalStyles />
      <Container>
        <Content>
          <Header />
          <JiraForm jiraKey={jiraKey} setJiraKey={setJiraKey} loading={loading} handleSubmit={handleSubmit} />
          <ResultDisplay result={result} error={error} />
          <Footer />
        </Content>
      </Container>
    </>
  );
}

export default App;
