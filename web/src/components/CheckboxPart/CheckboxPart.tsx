import {
  ChatbotBodyPart,
  ChatbotBodyPartOption,
} from "../../types/chatbot.types.ts";
import { useRef, useState } from "react";
import { v4 as uuid } from "uuid";

interface ListPartProps {
  value: ChatbotBodyPart;
  onSubmit: (value: ChatbotBodyPartOption[]) => void;
}

const CheckboxPart = ({ value, onSubmit }: ListPartProps) => {
  const groupName = useRef(uuid());
  const [selectedOptions, setSelectedOptions] = useState(
    new Set<ChatbotBodyPartOption>(),
  );
  const [_, setRender] = useState(false);

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    if (selectedOptions.size === 0) {
      return;
    }

    onSubmit([...selectedOptions]);
  }

  function handleCheck(option: ChatbotBodyPartOption) {
    setSelectedOptions((prev) => {
      if (prev.has(option)) {
        prev.delete(option);
      } else {
        prev.add(option);
      }

      return prev;
    });

    setRender((prev) => !prev); // Toggle to force re-render
  }

  if (!value.options?.length) {
    return null;
  }

  return (
    <form onSubmit={handleSubmit}>
      {value.options.map((option) => (
        <div key={option.value}>
          <input
            type="checkbox"
            name={groupName.current}
            value={option.value}
            checked={selectedOptions.has(option)}
            onChange={() => handleCheck(option)}
          />
          <label>{option.label || option.value}</label>
        </div>
      ))}

      <button type="submit">Submit</button>
    </form>
  );
};

export default CheckboxPart;
