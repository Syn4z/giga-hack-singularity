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

export const MonthForecast = () => {
  type DayPoint = {
    date: string; // "1", "2", ... "30"
    consumption?: number; // actual kWh used
    forecast?: number; // predicted kWh
  };

  const monthlyData: DayPoint[] = [
    { date: '1', consumption: 12.4, forecast: 3.1 },
    { date: '2', consumption: 11.8, forecast: 2.8 },
    { date: '3', consumption: 13.2, forecast: 3.3 },
    { date: '4', consumption: 15.6, forecast: 4.2 }, // weekend bump
    { date: '5', consumption: 16.4, forecast: 4.5 }, // weekend bump
    { date: '6', consumption: 12.1, forecast: 3.0 },
    { date: '7', consumption: 11.9, forecast: 2.9 },
    { date: '8', consumption: 13.7, forecast: 3.4 },
    { date: '9', consumption: 12.8, forecast: 3.2 },
    { date: '10', consumption: 14.1, forecast: 3.7 },
    { date: '11', consumption: 17.2, forecast: 4.6 }, // weekend
    { date: '12', consumption: 18.0, forecast: 4.8 }, // weekend
    { date: '13', consumption: 12.6, forecast: 3.1 },
    { date: '14', consumption: 11.4, forecast: 2.7 },
    { date: '15', consumption: 13.5, forecast: 3.5 },
    { date: '16', consumption: 12.7, forecast: 3.0 },
    { date: '17', consumption: 14.3, forecast: 3.8 },
    { date: '18', consumption: 16.9, forecast: 4.3 }, // weekend
    { date: '19', consumption: 17.8, forecast: 4.5 }, // weekend
    { date: '20', consumption: 13.2, forecast: 3.3 },
    { date: '21', consumption: 12.0, forecast: 2.8 },
    { date: '22', consumption: 13.8, forecast: 3.4 },
    { date: '23', consumption: 12.9, forecast: 3.2 },
    { date: '24', consumption: 14.5, forecast: 3.9 },
    { date: '25', consumption: 18.4, forecast: 4.7 }, // weekend
    { date: '26', consumption: 19.1, forecast: 4.9 }, // weekend
    { date: '27', consumption: 12.3, forecast: 3.0 },
    { date: '28', consumption: 11.7, forecast: 2.8 },
    { date: '29', consumption: 13.9, forecast: 3.5 },
    { date: '30', consumption: 12.6, forecast: 3.1 },
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
          <XAxis axisLine={false} tickLine={false} dataKey={chart.key('date')} />
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
