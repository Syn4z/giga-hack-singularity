import { Flex, Text } from '@chakra-ui/react';
import { useEffect, useState } from 'react';

type BotMessageProps = {
  text: string;
  speed?: number; // ms between characters
};

export const BotMessage = ({ text, speed = 30 }: BotMessageProps) => {
  const [displayed, setDisplayed] = useState('');
  const [cursorVisible, setCursorVisible] = useState(true);
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    let i = 0;
    setDisplayed('');
    setIsTyping(true);

    const typingInterval = setInterval(() => {
      setDisplayed(text.slice(0, i + 1));
      i++;
      if (i >= text.length) {
        clearInterval(typingInterval);
        setIsTyping(false);
      }
    }, speed);

    return () => clearInterval(typingInterval);
  }, [text, speed]);

  useEffect(() => {
    if (!isTyping) return;
    const cursorInterval = setInterval(() => {
      setCursorVisible((prev) => !prev);
    }, 500);
    return () => clearInterval(cursorInterval);
  }, [isTyping]);

  return (
    <Flex
      p={4}
      bg="gray.100"
      color="gray.600"
      borderRadius="lg"
      w="fit-content"
      alignSelf="flex-start"
    >
      <Text whiteSpace="pre-line">
        {displayed}
        {isTyping && cursorVisible && <Text as="span" color="bg.500">|</Text>}
      </Text>
    </Flex>
  );
};
