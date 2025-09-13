import { Spinner, Text, VStack } from '@chakra-ui/react';

export const SectionLoader = () => {
  return (
    <VStack colorPalette="teal" justifyContent="center">
      <Spinner color="teal.500" animationDuration="0.7s" size={'lg'} />
      <Text color="teal.500" fontSize={'2xl'}>
        Loading...
      </Text>
    </VStack>
  );
};
