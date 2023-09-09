import ChatBot from "react-simple-chatbot";
import { ChatbotStep } from "../../types/chatbot.types.ts";
import { ThemeProvider } from "styled-components";

interface ChatbotProps {
  steps: ChatbotStep[];
}

const theme = {
  background: "#f5f8fb",
  fontFamily: "Helvetica Neue",
  headerBgColor: "#EF6C00",
  headerFontColor: "#fff",
  headerFontSize: "15px",
  botBubbleColor: "#EF6C00",
  botFontColor: "#fff",
  userBubbleColor: "#fff",
  userFontColor: "#4a4a4a",
};

const Chatbot = (props: ChatbotProps) => {
  return (
    <ThemeProvider theme={theme}>
      <ChatBot
        className="chatbot"
        width="100%"
        height="100%"
        steps={props.steps}
      />
    </ThemeProvider>
  );
};

export default Chatbot;
