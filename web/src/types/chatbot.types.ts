export interface ChatbotStep {
  id: string;
  asMessage?: boolean;
  message?: string;
  user?: boolean;
  trigger?: string;
  end?: boolean;
  waitAction?: boolean;
  component?: JSX.Element;
}

export enum ChatbotOptionTypeEnum {
  TEXT = "text",
  RADIO = "radio",
}

export interface ChatbotQuestionResponse {
  text: string;
  options?: string[];
  optionType?: ChatbotOptionTypeEnum;
}
