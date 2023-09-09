import { ChatbotBodyPart } from "../../types/chatbot.types.ts";
import ReactMarkdown from "react-markdown";

interface ListPartProps {
  value: ChatbotBodyPart;
}

const ListPart = ({ value }: ListPartProps) => {
  if (!value.options?.length) {
    return null;
  }

  return (
    <ul>
      {value.options.map((option) => (
        <li key={option.value}>
          <ReactMarkdown>{option.value || option.label}</ReactMarkdown>
        </li>
      ))}
    </ul>
  );
};

export default ListPart;
