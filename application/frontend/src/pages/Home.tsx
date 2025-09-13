import { Box, Button, Text, VStack } from '@chakra-ui/react';
import { Link } from 'react-router-dom';

export const Home = () => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      h="100vh"
      px={4}
      gap={6}
      textAlign="center"
    >
      <VStack gap={2}>
        <Text fontSize="5xl" fontWeight="bold" lineHeight={1.3}>
          Welcome to SmartEnergy
        </Text>
        <Text fontSize="lg" color="gray.600">
          Understand your consumption and optimize energy use for cost and
          sustainability.
        </Text>
      </VStack>

      <Box
        display="flex"
        flexDirection={{ base: 'column', md: 'row' }}
        gap={4}
        mt={10}
      >
        <Link to="/contract">
          <Button bg="teal.500" size="lg" w={{ base: '100%', md: '180px' }}>
            I am a Provider
          </Button>
        </Link>
        <strong>OR</strong>
        <Link to="/contract">
          <Button bg="blue.500" size="lg" w={{ base: '100%', md: '180px' }}>
            I am a Consumer
          </Button>
        </Link>
      </Box>
    </Box>
  );
};
