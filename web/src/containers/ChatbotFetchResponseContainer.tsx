import { useEffect, useRef, useState } from "react";
import useFetchPost from "../hooks/useFetchPost.ts";
import { ASK_QUESTION_ENDPOINT } from "../config.ts";
import { Loading } from "react-simple-chatbot";
import {
  ChatbotOptionTypeEnum,
  ChatbotQuestionResponse,
} from "../types/chatbot.types.ts";
import ChatbotOptions from "../components/ChatbotOptions/ChatbotOptions.tsx";
import Markdown from "../components/Markdown";

interface ChatbotFetchResponseContainerProps {
  previousStep: { value: string };
  triggerNextStep: (data?: unknown) => void;
  selectedOptionRef: React.MutableRefObject<string | string[] | null>;
  lastTimestampRef: any;
}

const ChatbotFetchResponseContainer = (
  props: ChatbotFetchResponseContainerProps,
) => {
  const { previousStep, triggerNextStep } = props;
  const timestampRef = useRef(Date.now());
  const [optionsVisible, setOptionsVisible] = useState(true);

  const { error, isLoading, data, triggerRequest } =
    useFetchPost<ChatbotQuestionResponse>({
      url: ASK_QUESTION_ENDPOINT,
      // mockResponse: async () => {
      //   return QUESTION_RESPONSE;
      // },
    });

  useEffect(() => {
    if (
      timestampRef.current < props.lastTimestampRef.current &&
      optionsVisible
    ) {
      setOptionsVisible(false);
    }
  });

  useEffect(() => {
    handleFetchAnswer();

    triggerNextStep({
      trigger: "user-question",
    });

    props.lastTimestampRef.current = timestampRef.current;
  }, []);

  async function handleFetchAnswer() {
    const value = previousStep.value || props.selectedOptionRef.current;
    await triggerRequest(value);

    props.selectedOptionRef.current = null;
  }

  async function handleSelectOptions(body: string[] | string) {
    props.selectedOptionRef.current = body;

    triggerNextStep({
      trigger: "fetch-response",
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
  return <Loading />;
  }

  if (error) {
    return <p>Error...</p>;
  }

  return (
    <div className="chatbot-message">
      {data?.text && <Markdown text={data?.text} />}
      {optionsVisible && renderOptions()}
    </div>
  );
};

export default ChatbotFetchResponseContainer;
