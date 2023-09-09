import {
  ChatbotOptionTypeEnum,
  ChatbotQuestionResponse,
} from "../types/chatbot.types.ts";

export const QUESTION_RESPONSE: ChatbotQuestionResponse = {
  text: 'Probabil va referiti la "cazier judiciar". Am gasit cateva servicii care ar putea fi relevante: \n - Cazier judiciar privind verificarea persoanelor fizice sau juridice peste hotare (CSI) (https://servicii.gov.md/ro/service/006000190) \n - Cazier judiciar/ detaliat/ contravenţional pentru persoanele fizice și juridice (de pe teritoriul RM) (https://servicii.gov.md/ro/service/006000022) \n Selectati serviciul din lista sau oferiti-mi detalii noi daca serviciul pe care il cautati nu este in aceasta lista',
  options: ["cazier judiciar", "Alt cazier"],
  optionType: ChatbotOptionTypeEnum.RADIO,
};
