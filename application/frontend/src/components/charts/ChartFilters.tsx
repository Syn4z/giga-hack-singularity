import { Box } from '@chakra-ui/react';
import { ChartTabs } from './ChartTabs';

export const ChartFilters = () => {
  const onSubmit = (data: unknown) => console.log(data);

  return (
    <Box>
      <form onSubmit={onSubmit}>
        <ChartTabs />
      </form>
    </Box>
  );
};
