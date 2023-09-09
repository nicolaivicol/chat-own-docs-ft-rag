import styles from "./ChatbotOptions.module.css";
import Markdown from "../Markdown";
import { useState } from "react";

interface ChatbotOptionsProps {
  options: string[];
  onSelect: (option: string) => void;
}

const ChatbotOptions = (props: ChatbotOptionsProps) => {
  const [isVisible, setVisible] = useState(true);

  function handleSelectOption(option: string) {
    props.onSelect(option);
    setVisible(false);
  }

  if (!isVisible) {
    return null;
  }

  return (
    <div className={styles.container}>
      {props.options.map((option) => (
        <div
          key={option}
          className={styles.option}
          onPointerDown={() => handleSelectOption(option)}
        >
          <Markdown text={option} />
        </div>
      ))}
    </div>
  );
};

export default ChatbotOptions;
