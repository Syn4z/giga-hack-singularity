import { Box, Text } from '@chakra-ui/react';
import { DayForecast } from './DayForecast';
import { WeekForecast } from './WeekForecast';
import { MonthForecast } from './MonthForecast';
import { YearForecast } from './YearForecast';

interface HistoryProps {
  period: string[];
}

export const HistoryForecast = ({ period }: HistoryProps) => {
  if (period[0] === 'day') {
    return (
      <>
        <Text textAlign="center" fontWeight="bold" mb={4}>
          Hourly Energy Forecast
        </Text>
        <DayForecast />
      </>
    );
  }

  if (period[0] === 'week') {
    return (
      <>
        <Text textAlign="center" fontWeight="bold" mb={4}>
          Daily Energy Forecast
        </Text>
        <WeekForecast />
      </>
    );
  }

  if (period[0] === 'month') {
    return (
      <>
        <Text textAlign="center" fontWeight="bold" mb={4}>
          Weekly Energy Forecast
        </Text>
        <MonthForecast />
      </>
    );
  }

  if (period[0] === 'year') {
    return (
      <>
        <Text textAlign="center" fontWeight="bold" mb={4}>
          Monthly Energy Forecast
        </Text>
        <YearForecast />
      </>
    );
  }

  return (
    <Box textAlign="center" fontSize="xl" fontStyle="italic" color={'red.500'}>
      Not implemented yet for the {period} period!
    </Box>
  );
};
