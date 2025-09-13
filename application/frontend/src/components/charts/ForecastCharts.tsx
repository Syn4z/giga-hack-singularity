import { Box } from '@chakra-ui/react';
import { ChartTabsForecast } from './forecasts/ChartTabsForecast';

export const ForecastCharts = () => {
  const onSubmit = (data: unknown) => console.log(data);

  return (
    <Box>
      <form onSubmit={onSubmit}>
        <ChartTabsForecast />
      </form>
    </Box>
  );
};
