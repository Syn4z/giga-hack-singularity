import { Spinner, Text, VStack } from '@chakra-ui/react';

interface PageLoaderProps {
  title?: string;
}

export const PageLoader = ({ title }: PageLoaderProps) => {
  return (
    <VStack colorPalette="teal" height={'100vh'} justifyContent="center">
      <Spinner color="teal.500" animationDuration="0.7s" size={'lg'} />
      <Text color="teal.500" fontSize={'2xl'}>
       {title || 'Loading...'}
      </Text>
    </VStack>
  );
};
