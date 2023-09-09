import useChatbotSteps from "../hooks/useChatbotSteps.tsx";
import Chatbot from "../components/Chatbot";

const ChatbotContainer = () => {
  const steps = useChatbotSteps();

  if (!steps.length) {
    return null;
  }

  return <Chatbot steps={steps} />;
};

export default ChatbotContainer;
