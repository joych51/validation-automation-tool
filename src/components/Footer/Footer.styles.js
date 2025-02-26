import styled from "styled-components";

export const FooterContainer = styled.footer`
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #4a5568;
  text-align: center;
`;

export const FooterText = styled.p`
  color: #a0aec0;
  font-size: 0.875rem;
`;

export const FooterLink = styled.a`
  color: #4299e1;
  text-decoration: none;
  margin-left: 1rem;

  &:hover {
    text-decoration: underline;
  }
`;
