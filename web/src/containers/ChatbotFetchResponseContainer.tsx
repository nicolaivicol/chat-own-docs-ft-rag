import { useEffect } from "react";
import useFetchPost from "../hooks/useFetchPost.ts";
import { ASK_QUESTION_ENDPOINT } from "../config.ts";
import {
  ChatbotBodyPartOption,
  ChatbotComponentsEnum,
  ChatbotQuestionResponse,
  ChatbotStep,
} from "../types/chatbot.types.ts";
import TextPart from "../components/TextPart";
import LinkPart from "../components/LinkPart";
import ImagePart from "../components/ImagePart";
import ListPart from "../components/ListPart";
import RadioPart from "../components/RadioPart";
import CheckboxPart from "../components/CheckboxPart";
import { QUESTION_RESPONSE } from "../__mocks__/root-api.mocks.ts";

interface ChatbotFetchResponseContainerProps {
  previousStep: { value: string };
  triggerNextStep: (data?: unknown) => void;
  setSteps: (
    state: React.Dispatch<React.SetStateAction<ChatbotStep[]>>,
  ) => void;
}

const ChatbotFetchResponseContainer = (
  props: ChatbotFetchResponseContainerProps,
) => {
  const { previousStep, triggerNextStep } = props;

  const { error, isLoading, data, triggerRequest } =
    useFetchPost<ChatbotQuestionResponse>({
      url: ASK_QUESTION_ENDPOINT,
      mockResponse: async () => {
        return QUESTION_RESPONSE;
      },
    });

  useEffect(() => {
    console.log({ props, value: previousStep.value });
    handleFetchAnswer();
  }, []);

  async function handleFetchAnswer() {
    if (!previousStep?.value) {
      return;
    }

    const value = previousStep.value;
    await triggerRequest({ value });
  }

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error...</p>;
  }

  async function handleSelectOptions(options: ChatbotBodyPartOption[]) {
    const body = {
      value: previousStep.value,
      selectedOptions: options,
    };

    triggerNextStep({
      trigger: "fetch-response",
      value: body,
    });
  }

  return (
    <div className="chatbot-message">
      {data?.parts.map((part) => {
        switch (part.type) {
          case ChatbotComponentsEnum.LINK:
            return <LinkPart value={part} />;
          case ChatbotComponentsEnum.IMAGE:
            return <ImagePart value={part} />;
          case ChatbotComponentsEnum.LIST:
            return <ListPart value={part} />;
          case ChatbotComponentsEnum.RADIO:
            return <RadioPart value={part} onSubmit={handleSelectOptions} />;
          case ChatbotComponentsEnum.CHECKBOX:
            return <CheckboxPart value={part} onSubmit={handleSelectOptions} />;
          case ChatbotComponentsEnum.TEXT:
          default:
            return <TextPart value={part} />;
        }
      })}
    </div>
  );
};

export default ChatbotFetchResponseContainer;
