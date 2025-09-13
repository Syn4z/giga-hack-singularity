import { Chart, useChart } from '@chakra-ui/charts';
import {
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Line,
} from 'recharts';

export const DayForecast = () => {
  type HourPoint = {
    hour: number; // 0..23
    consumption?: number; // actual kWh used
    forecast?: number; // predicted kWh
  };

  // Example: full day with both actual + forecast values
  const hourlyData: HourPoint[] = [
    { hour: 0, consumption: 0.25, forecast: 2.8 },
    { hour: 1, consumption: 0.18, forecast: 2.9 },
    { hour: 2, consumption: 0.14, forecast: 2.7 },
    { hour: 3, consumption: 0.12, forecast: 3.0 },
    { hour: 4, consumption: 0.1, forecast: 2.6 },
    { hour: 5, consumption: 0.22, forecast: 3.1 },
    { hour: 6, consumption: 0.45, forecast: 3.3 },
    { hour: 7, consumption: 0.75, forecast: 3.5 },
    { hour: 8, consumption: 0.6, forecast: 3.7 },
    { hour: 9, consumption: 0.4, forecast: 3.2 },
    { hour: 10, consumption: 0.35, forecast: 3.4 },
    { hour: 11, consumption: 0.3, forecast: 3.0 },
    { hour: 12, consumption: 0.55, forecast: 3.6 },
    { hour: 13, consumption: 0.65, forecast: 3.5 },
    { hour: 14, consumption: 0.48, forecast: 3.7 },
    { hour: 15, consumption: 0.52, forecast: 3.8 },
    { hour: 16, consumption: 0.9, forecast: 4.0 },
    { hour: 17, consumption: 1.2, forecast: 4.2 },
    { hour: 18, consumption: 1.4, forecast: 4.5 },
    { hour: 19, consumption: 1.05, forecast: 4.3 },
    { hour: 20, consumption: 0.85, forecast: 3.9 },
    { hour: 21, consumption: 0.65, forecast: 3.6 },
    { hour: 22, consumption: 0.4, forecast: 3.1 },
    { hour: 23, consumption: 0.3, forecast: 2.9 },
  ];

  const chart = useChart({
    data: hourlyData,
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
            dataKey={chart.key('hour')}
            tickFormatter={(v) => `${v}:00`}
            interval={window.innerWidth < 500 ? 4 : 0}
            height={30}
          />
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

          {/* Forecast (dashed line for whole day) */}
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
