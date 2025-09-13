import { Chart, useChart } from '@chakra-ui/charts';
import {
  AreaChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Line,
} from 'recharts';

export const WeekForecast = () => {
  type DayPoint = {
    day: string; // Mon..Sun
    consumption?: number; // actual kWh used
    forecast?: number; // predicted kWh
  };

  // Weekly data with forecast errors
  const weeklyData: DayPoint[] = [
    { day: 'Mon', consumption: 12.4, forecast: 3.2 }, // slight over
    { day: 'Tue', consumption: 10.8, forecast: 3.0 }, // over
    { day: 'Wed', consumption: 14.2, forecast: 3.5 }, // under
    { day: 'Thu', consumption: 11.6, forecast: 3.1 }, // over
    { day: 'Fri', consumption: 15.9, forecast: 3.8 }, // over
    { day: 'Sat', consumption: 18.3, forecast: 4.0 }, // under
    { day: 'Sun', consumption: 9.7, forecast: 2.7 }, // over
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
          <XAxis axisLine={false} tickLine={false} dataKey={chart.key('day')} />
          <YAxis
            axisLine={false}
            tickLine={false}
            unit=" MDL/kWh"
            domain={[2.5, 5]}
          />
          <Tooltip
            cursor={{ strokeDasharray: '3 3' }}
            content={<Chart.Tooltip />}
          />
          <Legend content={<Chart.Legend />} />

          {/* Forecast (dashed line across week) */}
          <Line
            type="monotone"
            dataKey={chart.key('forecast')}
            stroke={chart.color('orange.solid')}
            strokeDasharray="4 4"
            strokeWidth={2}
            dot={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </Chart.Root>
  );
};
