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

export const Month = () => {
  type DayPoint = {
    date: string; // e.g. "1", "2", ..., "30"
    consumption: number; // kWh used in that day
    baseline?: number;
    renewableAvailable?: number;
    timestamp?: string;
  };

  // Example 30-day dataset (mock numbers)
  const monthlyData: DayPoint[] = [
  { date: '1', consumption: 12.4 },
  { date: '2', consumption: 11.8 },
  { date: '3', consumption: 13.2 },
  { date: '4', consumption: 15.6 }, // weekend bump
  { date: '5', consumption: 16.4 }, // weekend bump
  { date: '6', consumption: 12.1 },
  { date: '7', consumption: 11.9 },
  { date: '8', consumption: 13.7 },
  { date: '9', consumption: 12.8 },
  { date: '10', consumption: 14.1 },
  { date: '11', consumption: 17.2 }, // weekend
  { date: '12', consumption: 18.0 }, // weekend
  { date: '13', consumption: 12.6 },
  { date: '14', consumption: 11.4 },
  { date: '15', consumption: 13.5 },
  { date: '16', consumption: 12.7 },
  { date: '17', consumption: 14.3 },
  { date: '18', consumption: 16.9 }, // weekend
  { date: '19', consumption: 17.8 }, // weekend
  { date: '20', consumption: 13.2 },
  { date: '21', consumption: 12.0 },
  { date: '22', consumption: 13.8 },
  { date: '23', consumption: 12.9 },
  { date: '24', consumption: 14.5 },
  { date: '25', consumption: 18.4 }, // weekend
  { date: '26', consumption: 19.1 }, // weekend
  { date: '27', consumption: 12.3 },
  { date: '28', consumption: 11.7 },
  { date: '29', consumption: 13.9 },
  { date: '30', consumption: 12.6 },
];

  const chart = useChart({
    data: monthlyData,
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
            dataKey={chart.key('date')}
            tickFormatter={(v) => `Day ${v}`}
            interval={window.innerWidth < 500 ? 4 : 1} // fewer ticks on mobile
            height={30}
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
            fill={chart.color('purple.solid')}
            fillOpacity={0.15}
            stroke={chart.color('purple.solid')}
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </Chart.Root>
  );
};
