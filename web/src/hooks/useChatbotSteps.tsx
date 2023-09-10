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
        message: "Bună, cum te pot ajuta?",
        trigger: "user-question",
        delay: 0,
      },
      {
        id: "user-question",
        user: true,
        delay: 0,
        trigger: "fetch-response",
      },
      {
        id: "fetch-response",
        delay: 0,
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
