import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import styles from "./Markdown.module.css";

interface MarkdownProps {
  text: string;
}
const Markdown = (props: MarkdownProps) => {
  return (
    <ReactMarkdown
      className={styles.markdown}
      linkTarget="_blank"
      remarkPlugins={[remarkGfm]}
    >
      {props.text}
    </ReactMarkdown>
  );
};

export default Markdown;
