import { Chart, useChart } from '@chakra-ui/charts';
import {
  Area,
  AreaChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

export const Year = () => {
  type MonthPoint = {
    month: string; // "Jan", "Feb", ...
    consumption: number;
  };

  const yearlyData: MonthPoint[] = [
    { month: 'Jan', consumption: 18.2 }, // winter heating
    { month: 'Feb', consumption: 17.5 },
    { month: 'Mar', consumption: 14.8 },
    { month: 'Apr', consumption: 13.2 },
    { month: 'May', consumption: 12.4 },
    { month: 'Jun', consumption: 15.3 }, // AC season starting
    { month: 'Jul', consumption: 18.7 }, // summer peak
    { month: 'Aug', consumption: 19.1 }, // summer peak
    { month: 'Sep', consumption: 15.6 },
    { month: 'Oct', consumption: 14.0 },
    { month: 'Nov', consumption: 16.3 },
    { month: 'Dec', consumption: 18.9 }, // winter heating
  ];

  const chart = useChart({
    data: yearlyData,
  });

  return (
    <Chart.Root maxH="md" chart={chart}>
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
            unit=" kWh"
            domain={[0, 'dataMax + 2']}
          />
          <Tooltip
            cursor={{ strokeDasharray: '3 3' }}
            content={<Chart.Tooltip />}
          />
          <Legend content={<Chart.Legend />} />
          <Area
            type="monotone"
            isAnimationActive={false}
            dataKey={chart.key('consumption')}
            fill={chart.color('orange.solid')}
            fillOpacity={0.15}
            stroke={chart.color('orange.solid')}
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </Chart.Root>
  );
};
