import { Progress, Stat } from '@chakra-ui/react';

export const Usage = () => {
  return (
    <Stat.Root maxW="240px" borderWidth="1px" p={4} rounded={'md'}>
      <Stat.Label>This month</Stat.Label>
      <Stat.ValueText>37 kW</Stat.ValueText>
      <Stat.HelpText mb="2">+25% from last month</Stat.HelpText>
      <Progress.Root rounded={'md'}>
        <Progress.Track>
          <Progress.Range bg="red.500" />
        </Progress.Track>
      </Progress.Root>
    </Stat.Root>
  );
};
