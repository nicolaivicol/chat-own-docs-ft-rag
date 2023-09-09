import { useEffect } from "react";
import useFetchPost from "../hooks/useFetchPost.ts";
import { ASK_QUESTION_ENDPOINT } from "../config.ts";
import {
  ChatbotBodyPartOption,
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

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error...</p>;
  }

  return (
    <div className="chatbot-message">
      <Markdown text={``} />
      <ChatbotOptions options={["Option 1", "Option 2", "Option 3"]} />
    </div>
  );
};

export default ChatbotFetchResponseContainer;
