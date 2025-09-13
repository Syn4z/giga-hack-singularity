import { Box, Tabs } from '@chakra-ui/react';
import { ChartTip } from '../ChartTip';
import { HistoryForecast } from './HistoryForecast';
import { DAILY_FORECAST_TIPS, MONTHLY_FORECAST_TIPS, WEEKLY_FORECAST_TIPS, YEARLY_FORECAST_TIPS } from '@/assets/data/forecast_tips';

export const ChartTabsForecast = () => {
  return (
    <Tabs.Root defaultValue="daily">
      <Tabs.List display={'flex'} justifyContent={'center'}>
        <Tabs.Trigger value="daily">Daily</Tabs.Trigger>
        <Tabs.Trigger value="weekly">Weekly</Tabs.Trigger>
        <Tabs.Trigger value="monthly">Monthly</Tabs.Trigger>
        <Tabs.Trigger value="yearly">Yearly</Tabs.Trigger>
      </Tabs.List>
      <Tabs.Content value="daily">
        <HistoryForecast period={['day']} />
        <Box position={'relative'} zIndex={100} top={'-60px'}>
          {DAILY_FORECAST_TIPS.map((tip, index) => (
            <ChartTip
              key={index}
              heading={tip.title}
              desc={tip.desc}
              img={tip.img}
              defaultOpen={index === 0}
            />
          ))}
        </Box>
      </Tabs.Content>
      <Tabs.Content value="weekly">
        <HistoryForecast period={['week']} />
        <Box position={'relative'} zIndex={100} top={'-60px'}>
          {WEEKLY_FORECAST_TIPS.map((tip, index) => (
            <ChartTip
              key={index}
              heading={tip.title}
              desc={tip.desc}
              img={tip.img}
              defaultOpen={index === 0}
            />
          ))}
        </Box>
      </Tabs.Content>
      <Tabs.Content value="monthly">
        <HistoryForecast period={['month']} />
        <Box position={'relative'} zIndex={100} top={'-60px'}>
          {MONTHLY_FORECAST_TIPS.map((tip, index) => (
            <ChartTip
              key={index}
              heading={tip.title}
              desc={tip.desc}
              img={tip.img}
              defaultOpen={index === 0}
            />
          ))}
        </Box>
      </Tabs.Content>
      <Tabs.Content value="yearly">
        <HistoryForecast period={['year']} />
          <Box position={'relative'} zIndex={100} top={'-60px'}>
          {YEARLY_FORECAST_TIPS.map((tip, index) => (
            <ChartTip
              key={index}
              heading={tip.title}
              desc={tip.desc}
              img={tip.img}
              defaultOpen={index === 0}
            />
          ))}
        </Box>
      </Tabs.Content>
    </Tabs.Root>
  );
};
