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

export enum ChatbotComponentsEnum {
  TEXT = "text",
  LINK = "link",
  RADIO = "radio",
  CHECKBOX = "checkbox",
  IMAGE = "image",
  LIST = "list",
}

export interface ChatbotBodyPartOption {
  label: string;
  value: string;
}

export interface ChatbotBodyPart {
  type: ChatbotComponentsEnum;
  value: string;
  options?: ChatbotBodyPartOption[];
}

export interface ChatbotQuestionResponse {
  parts: ChatbotBodyPart[];
}
