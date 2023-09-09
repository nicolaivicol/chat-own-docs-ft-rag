import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownProps {
  text: string;
}
const Markdown = (props: MarkdownProps) => {
  return (
    <ReactMarkdown linkTarget="_blank" remarkPlugins={[remarkGfm]}>
      {props.text}
    </ReactMarkdown>
  );
};

export default Markdown;
