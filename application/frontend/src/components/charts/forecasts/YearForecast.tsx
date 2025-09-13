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

export const YearForecast = () => {
  type MonthPoint = {
    month: string; // "Jan", "Feb", ...
    consumption: number; // actual kWh used
    forecast?: number;   // predicted MDL/kWh
  };

  const yearlyData: MonthPoint[] = [
    { month: 'Jan', consumption: 18.2, forecast: 4.8 }, // winter heating
    { month: 'Feb', consumption: 17.5, forecast: 4.5 },
    { month: 'Mar', consumption: 14.8, forecast: 3.7 },
    { month: 'Apr', consumption: 13.2, forecast: 3.2 },
    { month: 'May', consumption: 12.4, forecast: 3.0 },
    { month: 'Jun', consumption: 15.3, forecast: 3.6 }, // AC season
    { month: 'Jul', consumption: 18.7, forecast: 4.9 }, // summer peak
    { month: 'Aug', consumption: 19.1, forecast: 5.0 }, // summer peak
    { month: 'Sep', consumption: 15.6, forecast: 3.8 },
    { month: 'Oct', consumption: 14.0, forecast: 3.3 },
    { month: 'Nov', consumption: 16.3, forecast: 4.1 },
    { month: 'Dec', consumption: 18.9, forecast: 4.9 }, // winter heating
  ];

  const chart = useChart({
    data: yearlyData,
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
            dataKey={chart.key('month')}
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
          <Legend content={<Chart.Legend />} />

          {/* Forecast (dashed line) */}
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
