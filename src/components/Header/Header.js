import { HeaderContainer, Title, Subtitle } from "./Header.styles";

const Header = () => {
  return (
    <HeaderContainer>
      <Title>Validation Automation Tool</Title>
      <Subtitle>Enter your Jira story key to start the validation process</Subtitle>
    </HeaderContainer>
  );
};

export default Header;
