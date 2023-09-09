import { ChatbotBodyPart } from "../../types/chatbot.types.ts";

interface LinkPartProps {
  value: ChatbotBodyPart;
}

const LinkPart = ({ value }: LinkPartProps) => {
  return (
    <a href={value.value} target="_blank">
      {value.value}
    </a>
  );
};

export default LinkPart;
