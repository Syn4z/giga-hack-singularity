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

export const Day = () => {
  type HourPoint = {
    hour: number; // 0..23
    consumption: number; // kWh used in that hour
    baseline?: number; // expected / historical baseline kWh
    renewableAvailable?: number; // e.g. kWh available from home PV at that hour
    deviceBreakdown?: Record<string, number>; // optional per-device kWh (for drilldown)
    timestamp?: string; // ISO timestamp for the hour
  };

  const hourlyData: HourPoint[] = [
    { hour: 0, consumption: 0.25 },
    { hour: 1, consumption: 0.18 },
    { hour: 2, consumption: 0.14 },
    { hour: 3, consumption: 0.12 },
    { hour: 4, consumption: 0.1 },
    { hour: 5, consumption: 0.22 },
    { hour: 6, consumption: 0.45 },
    { hour: 7, consumption: 0.75 },
    { hour: 8, consumption: 0.6 },
    { hour: 9, consumption: 0.4 },
    { hour: 10, consumption: 0.35 },
    { hour: 11, consumption: 0.3 },
    { hour: 12, consumption: 0.55 },
    { hour: 13, consumption: 0.65 },
    { hour: 14, consumption: 0.48 },
    { hour: 15, consumption: 0.52 },
    { hour: 16, consumption: 0.9 },
    { hour: 17, consumption: 1.2 },
    { hour: 18, consumption: 1.4 },
    { hour: 19, consumption: 1.05 },
    { hour: 20, consumption: 0.85 },
    { hour: 21, consumption: 0.65 },
    { hour: 22, consumption: 0.4 },
    { hour: 23, consumption: 0.3 },
  ];
  const chart = useChart({
    data: hourlyData,
    // series: [{ name: 'consumption', color: 'teal.solid' }],
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
            interval={window.innerWidth < 500 ? 4 : 0} // fewer ticks on mobile
            height={30}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            unit=" kWh"
            domain={[0, 'dataMax + 0.5']}
            interval={1}
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
            fill={chart.color('teal.solid')}
            fillOpacity={0.12}
            stroke={chart.color('teal.solid')}
            strokeWidth={2}
            dot={{ r: 0 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </Chart.Root>
  );
};
