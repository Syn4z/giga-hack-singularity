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

export const OptimizedDayForecast = () => {
  type HourPoint = {
    hour: number;
    consumption: number; // actual
    optimized?: number; // optimized kWh
  };

  // Example optimized data: lower peaks during late afternoon/evening
  const hourlyData2: HourPoint[] = [
    { hour: 0, consumption: 0.25, optimized: 0.35 },
    { hour: 1, consumption: 0.18, optimized: 0.28 },
    { hour: 2, consumption: 0.14, optimized: 0.25 },
    { hour: 3, consumption: 0.12, optimized: 0.22 },
    { hour: 4, consumption: 0.1,  optimized: 0.2 },
    { hour: 5, consumption: 0.22, optimized: 0.3 },
    { hour: 6, consumption: 0.45, optimized: 0.4 },
    { hour: 7, consumption: 0.75, optimized: 0.6 },
    { hour: 8, consumption: 0.6,  optimized: 0.55 },
    { hour: 9, consumption: 0.4,  optimized: 0.45 },
    { hour: 10, consumption: 0.35, optimized: 0.45 },
    { hour: 11, consumption: 0.3,  optimized: 0.4 },
    { hour: 12, consumption: 0.55, optimized: 0.65 },
    { hour: 13, consumption: 0.65, optimized: 0.7 },
    { hour: 14, consumption: 0.48, optimized: 0.55 },
    { hour: 15, consumption: 0.52, optimized: 0.55 },
    { hour: 16, consumption: 0.9,  optimized: 0.65 },
    { hour: 17, consumption: 1.2,  optimized: 0.8 },
    { hour: 18, consumption: 1.4,  optimized: 0.9 },
    { hour: 19, consumption: 1.05, optimized: 0.75 },
    { hour: 20, consumption: 0.85, optimized: 0.65 },
    { hour: 21, consumption: 0.65, optimized: 0.55 },
    { hour: 22, consumption: 0.4,  optimized: 0.35 },
    { hour: 23, consumption: 0.3,  optimized: 0.3 },
  ];

  const chart = useChart({ data: hourlyData2 });

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
            unit=" kWh"
            domain={[0, 'dataMax + 0.5']}
          />
          <Tooltip
            cursor={{ strokeDasharray: '3 3' }}
            content={<Chart.Tooltip />}
          />
          {/* Actual consumption */}
          <Area
            type="monotone"
            dataKey={chart.key('consumption')}
            fill={chart.color('red.solid')}
            fillOpacity={0.1}
            stroke={chart.color('red.solid')}
            strokeWidth={2}
            dot={{ r: 0 }}
            name="Actual"
          />

          {/* Optimized consumption */}
          <Area
            type="monotone"
            dataKey={chart.key('optimized')}
            fill={chart.color('green.solid')}
            fillOpacity={0.1}
            stroke={chart.color('green.solid')}
            strokeWidth={2}
            dot={{ r: 0 }}
            name="Optimized"
          />
        </AreaChart>
      </ResponsiveContainer>
    </Chart.Root>
  );
};
