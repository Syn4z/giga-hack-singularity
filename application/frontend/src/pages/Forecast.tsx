import { DAILY_OPTIMIZE_TIPS } from '@/assets/data/optimize_tips';
import { ChartTip } from '@/components/charts/ChartTip';
import { ForecastCharts } from '@/components/charts/ForecastCharts';
import { OptimizedDayForecast } from '@/components/charts/forecasts/OptimizedDayForecast';
import { Navbar } from '@/components/common/Navbar';
import { PageLoader } from '@/components/loader/PageLoader';
import { Box, Heading, Separator, Text } from '@chakra-ui/react';
import { useEffect, useState } from 'react';

export const Forecast = () => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  }, []);

  if (isLoading) {
    return <PageLoader title="Loading the forecast..." />;
  }

  return (
    <Box p={4}>
      <Navbar />
      <Box mt={4}>
        <Heading size="2xl" mb={2}>
          Predictions
        </Heading>
        <Separator />
        <ForecastCharts />
      </Box>
      <Box mt={4}>
        <Heading size="2xl" mb={2}>
          Optimized Energy Consumption
        </Heading>
        <Separator mb={4} />
        <Text mb={6}>
          This optimized forecast suggests a more balanced energy consumption
          pattern, reducing peaks during high-demand hours.
        </Text>
        <OptimizedDayForecast />
        <Box position={'relative'} zIndex={100} top={'-60px'}>
          {DAILY_OPTIMIZE_TIPS.map((tip, index) => (
            <ChartTip
              key={index}
              heading={tip.title}
              desc={tip.desc}
              img={tip.img}
              defaultOpen={index === 0}
            />
          ))}
        </Box>
      </Box>
    </Box>
  );
};
