import { Flex, Spinner } from "@chakra-ui/react";
import { BotMessage } from "./BotMessage";

export type MessageProps = {
  text: string;
  actor: 'user' | 'bot';
  isThinking?: boolean;
  speed?: number; // ms between characters
};

export const Message = ({ text, actor, isThinking, speed }: MessageProps) => {
  if (isThinking) {
    return (
      <Flex
        p={4}
        bg="gray.100"
        color="gray.600"
        borderRadius="lg"
        w="fit-content"
        alignSelf="flex-start"
      >
        <Spinner size="sm" color="gray.500" />
      </Flex>
    );
  }

  if (actor === 'bot') {
    return <BotMessage text={text} speed={speed} />;
  }

  return (
    <Flex
      p={4}
      bg="blue.500"
      color="white"
      borderRadius="lg"
      w="fit-content"
      alignSelf="flex-end"
    >
      {text}
    </Flex>
  );
};
