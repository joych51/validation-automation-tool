import { FooterContainer, FooterText, FooterLink } from "./Footer.styles";

const Footer = () => {
  return (
    <FooterContainer>
      <FooterText>Validation Automation Tool © {new Date().getFullYear()}</FooterText>
      <FooterLink href="https://github.com/yourusername" target="_blank">
        GitHub
      </FooterLink>
    </FooterContainer>
  );
};

export default Footer;
