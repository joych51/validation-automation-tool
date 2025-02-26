import styled from "styled-components";

export const FormContainer = styled.form`
  max-width: 28rem;
  margin: 0 auto;
`;

export const InputWrapper = styled.div`
  position: relative;
`;

export const Input = styled.input`
  width: 100%;
  padding: 0.75rem 1rem;
  background-color: #2d3748;
  color: white;
  border: 1px solid #4a5568;
  border-radius: 0.5rem;
  outline: none;

  &:focus {
    border-color: #4299e1;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5);
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

export const Button = styled.button`
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  padding: 0.5rem 1rem;
  background-color: #4a5568;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #2d3748;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;
