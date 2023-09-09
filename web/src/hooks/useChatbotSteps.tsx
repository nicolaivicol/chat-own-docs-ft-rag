import { ChatbotStep } from "../types/chatbot.types.ts";
import ChatbotFetchResponseContainer from "../containers/ChatbotFetchResponseContainer.tsx";
import { useEffect, useRef, useState } from "react";

const useChatbotSteps = () => {
  const [steps, setSteps] = useState<ChatbotStep[]>([]);
  const selectedOptionRef = useRef<string | string[] | null>(null);
  const lastTimestampRef = useRef<null | number>(null);

  useEffect(() => {
    setSteps([
      {
        id: "1",
        message: "Welcome! How can I help you today?",
        trigger: "user-question",
      },
      {
        id: "user-question",
        user: true,
        trigger: "fetch-response",
      },
      {
        id: "fetch-response",
        component: (
          <ChatbotFetchResponseContainer
            lastTimestampRef={lastTimestampRef}
            selectedOptionRef={selectedOptionRef}
          />
        ),
        asMessage: true,
        waitAction: true,
      },
    ]);
  }, []);

  return steps;
};

export default useChatbotSteps;
