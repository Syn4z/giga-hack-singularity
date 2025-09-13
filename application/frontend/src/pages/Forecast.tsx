import { ForecastCharts } from '@/components/charts/ForecastCharts';
import { Navbar } from '@/components/common/Navbar';
import { PageLoader } from '@/components/loader/PageLoader';
import { Box, Heading, Separator } from '@chakra-ui/react';
import { useEffect, useState } from 'react';

export const Forecast = () => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  }, []);
  
  if (isLoading) {
    return <PageLoader title='Loading the forecast...' />;
  }

  return (
    <Box p={4}>
      <Navbar />
      <Box mt={4}>
        <Heading size="2xl" mb={2}>Predictions</Heading>
        <Separator />
        <ForecastCharts />
      </Box>
      {/* <Box mt={4}>
        <Heading size="2xl" mb={2}>Optimized Energy Consumption</Heading>
        <Separator />
        <ForecastCharts />
      </Box> */}
    </Box>
  );
};
