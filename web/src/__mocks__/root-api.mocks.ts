import {
  ChatbotComponentsEnum,
  ChatbotQuestionResponse,
} from "../types/chatbot.types.ts";

export const QUESTION_RESPONSE: ChatbotQuestionResponse = {
  parts: [
    {
      type: ChatbotComponentsEnum.TEXT,
      value:
        "**Lorem Ipsum** is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    },
    {
      type: ChatbotComponentsEnum.LINK,
      value: "https://servicii.gov.md/",
    },
    {
      type: ChatbotComponentsEnum.IMAGE,
      value:
        "https://images.unsplash.com/photo-1693856759370-96692b463ab9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3474&q=80",
    },
    {
      type: ChatbotComponentsEnum.LIST,
      value: "",
      options: [
        {
          label:
            "Poti obtine **aaaaaa** visitand [https://servicii.gov.md/](https://servicii.gov.md/).",
          value: "",
        },
        {
          label:
            "Poti obtine **qqqqqq** visitand [https://servicii.gov.md/](https://servicii.gov.md/).",
          value: "",
        },
        {
          label:
            "Poti obtine **fffffff** visitand [https://servicii.gov.md/](https://servicii.gov.md/).",
          value: "",
        },
      ],
    },
    {
      type: ChatbotComponentsEnum.RADIO,
      value: "",
      options: [
        {
          label: "Radio 1",
          value: "radio_1",
        },
        {
          label: "Radio 2",
          value: "radio_2",
        },
        {
          label: "Radio 3",
          value: "radio_3",
        },
      ],
    },
    {
      type: ChatbotComponentsEnum.CHECKBOX,
      value: "",
      options: [
        {
          label: "Checkbox 1",
          value: "checkbox_1",
        },
        {
          label: "Checkbox 2",
          value: "checkbox_2",
        },
        {
          label: "Checkbox 3",
          value: "checkbox_3",
        },
      ],
    },
  ],
};
