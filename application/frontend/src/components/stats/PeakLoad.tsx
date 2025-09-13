import { Stat } from '@chakra-ui/react';

export const PeakLoad = () => {
  return (
    <Stat.Root
      borderWidth="1px"
      p={4}
      rounded={'md'}
      display={'flex'}
      alignItems={'center'}
      justifyContent={'center'}
    >
      <Stat.Label>Peak Load Time</Stat.Label>
      <Stat.ValueText alignItems="baseline">14:20</Stat.ValueText>
    </Stat.Root>
  );
};
