import { Message, type MessageProps } from '@/components/chat/Message';
import { Button, Flex, Heading, HStack, IconButton, Input, Stack } from '@chakra-ui/react';
import { useState } from 'react';
import { IoIosArrowBack } from 'react-icons/io';
import { useNavigate } from 'react-router-dom';

export const Chat = () => {
  const [messages, setMessages] = useState<MessageProps[]>([
    {
      text: "Hello! I'm your SmartEnergy Assistant ⚡️",
      actor: 'bot',
      speed: 25,
    },
  ]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const navigate = useNavigate();
  console.log(isThinking);

  const predefinedAnswers: Record<string, { text: string; speed: number }> = {
    hello: { text: 'Hi there! How can I help you today?', speed: 40 },
    forecast: {
      text: 'Today’s forecast shows higher usage during evening peak hours (6–9 PM).',
      speed: 30,
    },
    tips: {
      text: 'You can save energy by running your dishwasher after 10 PM when tariffs are lower.',
      speed: 20,
    },
    devices: {
      text: 'Based on your profile, your AC and washing machine are the biggest contributors.',
      speed: 35,
    },
    save: {
      text: 'Running your washing machine during off-peak hours can reduce its cost by 10–20%, depending on your local tariff structure. For example, if one cycle normally costs 25 MDL in the evening peak (6–9 PM), that same cycle might cost around 20–22 MDL if shifted to late night or midday hours.',
      speed: 25,
    },
  };

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage: MessageProps = { text: input, actor: 'user' };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    // Simulate thinking
    setIsThinking(true);
    setMessages((prev) => [
      ...prev,
      { text: '...', actor: 'bot', isThinking: true },
    ]);

    setTimeout(() => {
      setIsThinking(false);

      const normalized = input.toLowerCase();

      // Find the first keyword that matches inside the user input
      const matchedKey = Object.keys(predefinedAnswers).find((key) =>
        normalized.includes(key)
      );

      const response =
        matchedKey !== undefined
          ? predefinedAnswers[matchedKey]
          : {
              text: 'Sorry, I didn’t quite get that. Could you rephrase?',
              speed: 25,
            };

      setMessages((prev) => [
        ...prev.slice(0, -1), // remove the "thinking" message
        { text: response.text, actor: 'bot', speed: response.speed },
      ]);
    }, 1200);
  };

  return (
    <Flex h="100vh">
      <Flex
        flexDirection="column"
        w="2xl"
        m="auto"
        h="full"
        borderWidth="1px"
        roundedTop="lg"
      >
        {/* Header */}
        <HStack p={4} bg="blue.500" justifyContent="flex-start">
          <IconButton onClick={() => navigate('/analytics')} bg={'transparent'}>
            <IoIosArrowBack />
          </IconButton>

          <Heading size="lg" color="white" textAlign="center">
            SmartEnergy Assistant
          </Heading>
        </HStack>

        {/* Messages */}
        <Stack
          px={4}
          py={8}
          overflow="auto"
          flex={1}
          gap={3}
          css={{
            '&::-webkit-scrollbar': { width: '4px' },
            '&::-webkit-scrollbar-thumb': {
              background: '#d5e3f7',
              borderRadius: '24px',
            },
          }}
        >
          {messages.map((m, i) => (
            <Message key={i} {...m} />
          ))}
        </Stack>

        {/* Input */}
        <HStack p={4} bg="gray.100">
          <Input
            bg="white"
            placeholder="Ask me about your energy usage"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <Button bg="blue.500" color="white" onClick={handleSend}>
            Send
          </Button>
        </HStack>
      </Flex>
    </Flex>
  );
};
