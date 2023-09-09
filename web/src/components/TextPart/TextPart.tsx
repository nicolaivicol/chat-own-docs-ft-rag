import { ChatbotBodyPart } from "../../types/chatbot.types.ts";
import ReactMarkdown from "react-markdown";

interface TextPartProps {
  value: ChatbotBodyPart;
}

const TextPart = ({ value }: TextPartProps) => {
  return (
    <div>
      <ReactMarkdown>{value.value}</ReactMarkdown>
    </div>
  );
};

export default TextPart;
