import { Navbar } from '@/components/common/Navbar';
import { Box, Text } from '@chakra-ui/react';

export const Profile = () => {
  return (
    <Box p={4}>
      <Navbar />
      <Text fontSize="4xl">Profile page</Text>
    </Box>
  );
};
