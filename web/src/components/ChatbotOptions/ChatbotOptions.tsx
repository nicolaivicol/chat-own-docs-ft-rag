import styles from "./ChatbotOptions.module.css";
import Markdown from "../Markdown";

interface ChatbotOptionsProps {
  options: string[];
}

const ChatbotOptions = (props: ChatbotOptionsProps) => {
  return (
    <div className={styles.container}>
      {props.options.map((option) => (
        <div key={option} className={styles.option}>
          <Markdown text={option} />
        </div>
      ))}
    </div>
  );
};

export default ChatbotOptions;
