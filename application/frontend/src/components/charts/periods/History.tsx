import { Box, Text } from '@chakra-ui/react';
import { Day } from './Day';
import { Week } from './Week';
import { Month } from './Month';
import { Year } from './Year';

interface HistoryProps {
  period: string[];
}

export const History = ({ period }: HistoryProps) => {
  if (period[0] === 'day') {
    return (
      <>
        <Text textAlign="center" fontWeight="bold" mb={4}>
          Hourly Energy Consumption
        </Text>
        <Day />
      </>
    );
  }

  if (period[0] === 'week') {
    return (
      <>
        <Text textAlign="center" fontWeight="bold" mb={4}>
          Daily Energy Consumption
        </Text>
        <Week />
      </>
    );
  }

  if (period[0] === 'month') {
    return (
      <>
        <Text textAlign="center" fontWeight="bold" mb={4}>
          Weekly Energy Consumption
        </Text>
        <Month />
      </>
    );
  }

  if (period[0] === 'year') {
    return (
      <>
        <Text textAlign="center" fontWeight="bold" mb={4}>
          Monthly Energy Consumption
        </Text>
        <Year />
      </>
    );
  }

  return (
    <Box textAlign="center" fontSize="xl" fontStyle="italic" color={'red.500'}>
      Not implemented yet for the {period} period!
    </Box>
  );
};
