import { Chart, useChart } from '@chakra-ui/charts';
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

export const Week = () => {
  type DayPoint = {
    day: string; // e.g. "Mon", "Tue"
    consumption: number; // kWh used in that day
    baseline?: number;
    renewableAvailable?: number;
    timestamp?: string;
  };

  const weeklyData: DayPoint[] = [
    { day: 'Mon', consumption: 12.4 },
    { day: 'Tue', consumption: 10.8 },
    { day: 'Wed', consumption: 14.2 },
    { day: 'Thu', consumption: 11.6 },
    { day: 'Fri', consumption: 15.9 },
    { day: 'Sat', consumption: 18.3 },
    { day: 'Sun', consumption: 9.7 },
  ];

  const chart = useChart({
    data: weeklyData,
  });

  return (
    <Chart.Root maxH="sm" chart={chart}>
      <ResponsiveContainer width="100%" aspect={1.5}>
        <AreaChart data={chart.data}>
          <CartesianGrid
            stroke={chart.color('border.muted')}
            vertical={false}
          />
          <XAxis
            axisLine={false}
            tickLine={false}
            dataKey={chart.key('day')}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            unit=" kWh"
            domain={[0, 'dataMax + 2']}
          />
          <Tooltip
            cursor={{ strokeDasharray: '3 3' }}
            content={<Chart.Tooltip />}
          />
          <Area
            type="monotone"
            isAnimationActive={false}
            dataKey={chart.key('consumption')}
            fill={chart.color('blue.solid')}
            fillOpacity={0.15}
            stroke={chart.color('blue.solid')}
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </Chart.Root>
  );
};
