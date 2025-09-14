import { IconButton, Float } from '@chakra-ui/react';
import { HiChatBubbleLeftRight } from 'react-icons/hi2';
import { useNavigate } from 'react-router-dom';

export const FloatingButton = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/chat');
  };

  return (
    <Float
      placement="bottom-end"
      position="fixed"
      zIndex={1000}
      right={8}
      bottom={8}
    >
      <IconButton
        aria-label="Open Chat"
        bg="blue.500"
        color="white"
        _hover={{ bg: 'blue.600' }}
        borderRadius="full"
        size="lg"
        boxShadow="md"
        onClick={handleClick}
      >
        <HiChatBubbleLeftRight />
      </IconButton>
    </Float>
  );
};
