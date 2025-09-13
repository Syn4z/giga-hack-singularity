import { Portal, Select, createListCollection } from '@chakra-ui/react';

interface ChartSelectProps {
  period: string[];
  setPeriod: (period: string[]) => void;
}

export const ChartSelect = ({ period, setPeriod }: ChartSelectProps) => {
  return (
    <Select.Root
      collection={periods}
      defaultValue={['daily']}
      value={period}
      onValueChange={(e) => setPeriod(e.value)}
      mb={4}
    >
      <Select.HiddenSelect />
      <Select.Label>Period</Select.Label>
      <Select.Control>
        <Select.Trigger>
          <Select.ValueText placeholder="Select period" />
        </Select.Trigger>
        <Select.IndicatorGroup>
          <Select.Indicator />
        </Select.IndicatorGroup>
      </Select.Control>
      <Portal>
        <Select.Positioner>
          <Select.Content>
            {periods.items.map((period) => (
              <Select.Item item={period} key={period.value}>
                {period.label}
                <Select.ItemIndicator />
              </Select.Item>
            ))}
          </Select.Content>
        </Select.Positioner>
      </Portal>
    </Select.Root>
  );
};

const periods = createListCollection({
  items: [
    { label: 'Last 24 hours', value: 'day' },
    { label: 'Last 7 days', value: 'week' },
    { label: 'Last 30 days', value: 'month' },
    { label: 'Last 12 months', value: 'year' },
  ],
});
