import styled from "styled-components";

export const ResultContainer = styled.div`
  margin-top: 1.5rem;
  padding: 1.5rem;
  background-color: ${(props) => (props.error ? "#2d2a2a" : "#2d3748")};
  border-radius: 0.5rem;
  border: 1px solid ${(props) => (props.error ? "#742a2a" : "#4a5568")};
`;

export const ResultTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: white;
`;

export const ResultRow = styled.div`
  display: flex;
  justify-content: space-between;
  color: #a0aec0;
  margin-bottom: 0.75rem;
`;

export const QuerySection = styled.div`
  margin-top: 1rem;
`;

export const QueryTitle = styled.h3`
  color: white;
  margin-bottom: 0.5rem;
`;

export const QueryBox = styled.pre`
  padding: 0.75rem;
  background-color: #1a202c;
  border-radius: 0.375rem;
  overflow-x: auto;
  color: #a0aec0;
  font-size: 0.875rem;
`;

export const StatusText = styled.span`
  color: ${(props) => (props.success ? "#48bb78" : "#f56565")};
`;

export const ErrorMessage = styled.div`
  color: #f56565;
  padding: 1rem;
  background-color: #742a2a;
  border-radius: 0.375rem;
  margin-top: 1rem;
`;
