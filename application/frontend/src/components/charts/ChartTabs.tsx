import { Box, Tabs } from '@chakra-ui/react';
import { ChartTip } from './ChartTip';
import { DAILY_TIPS, MONTHLY_TIPS, WEEKLY_TIPS, YEARLY_TIPS } from '@/assets/data/tips';
import { History } from './periods/History';

export const ChartTabs = () => {
  return (
    <Tabs.Root defaultValue="daily">
      <Tabs.List display={'flex'} justifyContent={'center'}>
        <Tabs.Trigger value="daily">Daily</Tabs.Trigger>
        <Tabs.Trigger value="weekly">Weekly</Tabs.Trigger>
        <Tabs.Trigger value="monthly">Monthly</Tabs.Trigger>
        <Tabs.Trigger value="yearly">Yearly</Tabs.Trigger>
      </Tabs.List>
      <Tabs.Content value="daily">
        <History period={['day']} />
        <Box position={'relative'} zIndex={100} top={'-60px'}>
          {DAILY_TIPS.map((tip, index) => (
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
        <History period={['week']} />
        <Box position={'relative'} zIndex={100} top={'-60px'}>
          {WEEKLY_TIPS.map((tip, index) => (
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
        <History period={['month']} />
        <Box position={'relative'} zIndex={100} top={'-60px'}>
          {MONTHLY_TIPS.map((tip, index) => (
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
        <History period={['year']} />
          <Box position={'relative'} zIndex={100} top={'-60px'}>
          {YEARLY_TIPS.map((tip, index) => (
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
