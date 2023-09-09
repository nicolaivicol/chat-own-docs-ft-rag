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

const RadioPart = ({ value, onSubmit }: ListPartProps) => {
  const groupName = useRef(uuid());
  const [selectedOption, setSelectedOption] = useState<ChatbotBodyPartOption>();

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    if (selectedOption == null) {
      return;
    }

    onSubmit([selectedOption]);
  }

  function handleCheck(value: ChatbotBodyPartOption) {
    setSelectedOption(value);
  }

  if (!value.options?.length) {
    return null;
  }

  return (
    <form onSubmit={handleSubmit}>
      {value.options.map((option) => (
        <div key={option.value}>
          <input
            type="radio"
            name={groupName.current}
            value={option.value}
            checked={option.value === selectedOption?.value}
            onPointerDown={() => handleCheck(option)}
          />
          <label>{option.label || option.value}</label>
        </div>
      ))}

      <button type="submit">Submit</button>
    </form>
  );
};

export default RadioPart;
