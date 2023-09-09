import { ChatbotBodyPart } from "../../types/chatbot.types.ts";

interface ImagePartProps {
  value: ChatbotBodyPart;
}

const ImagePart = ({ value }: ImagePartProps) => {
  return <img src={value.value} />;
};

export default ImagePart;
