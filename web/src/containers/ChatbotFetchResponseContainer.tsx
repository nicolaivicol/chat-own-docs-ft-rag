import { useEffect } from "react";
import useFetchPost from "../hooks/useFetchPost.ts";
import { ASK_QUESTION_ENDPOINT } from "../config.ts";
import {
  ChatbotOptionTypeEnum,
  ChatbotQuestionResponse,
  ChatbotStep,
} from "../types/chatbot.types.ts";
import { QUESTION_RESPONSE } from "../__mocks__/root-api.mocks.ts";
import ChatbotOptions from "../components/ChatbotOptions/ChatbotOptions.tsx";
import Markdown from "../components/Markdown";

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

  async function handleSelectOptions(body: string[] | string) {
    triggerNextStep({
      trigger: "fetch-response",
      value: body,
    });
  }

  function renderOptions() {
    const optionType = data?.optionType;
    const options = data?.options ?? [];

    switch (optionType) {
      case ChatbotOptionTypeEnum.RADIO:
      default:
        return (
          <ChatbotOptions options={options} onSelect={handleSelectOptions} />
        );
    }
  }

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error...</p>;
  }

  return (
    <div className="chatbot-message">
      {data?.text && <Markdown text={data?.text} />}
      {renderOptions()}
    </div>
  );
};

export default ChatbotFetchResponseContainer;
