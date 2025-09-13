import tip1 from '../../assets/img/tips/tip_1.png';
// import tip2 from '../../assets/img/tips/tip_2.png';
import tip3 from '../../assets/img/tips/tip_3.png';
// import tip4 from '../../assets/img/tips/tip_4.png';
import tip5 from '../../assets/img/tips/tip_5.png';
import tip6 from '../../assets/img/tips/tip_6.png';

export const DAILY_FORECAST_TIPS = [
  {
    img: tip3,
    title: 'High variance window',
    desc: 'Forecast error widens after 17:00, where actuals spike higher than predicted. Evening variability suggests that adaptive or real-time adjustments could help.',
  },
];

export const WEEKLY_FORECAST_TIPS = [
  {
    img: tip5,
    title: 'Friday rebound',
    desc: 'Energy usage climbs back up on Fridays, suggesting pre-weekend activity. Be aware of this increase if you want to keep weekly totals balanced.',
  },
];

export const MONTHLY_FORECAST_TIPS = [
  {
    img: tip1,
    title: 'Steady weekdays',
    desc: 'Weekday consumption is more predictable, with narrower forecast errors. These days are more reliable for automating recurring tasks.',
  },
];

export const YEARLY_FORECAST_TIPS = [
  {
    img: tip6,
    title: 'Spring and autumn alignment',
    desc: 'Shoulder months (April–May, September–October) show strong forecast alignment, meaning consumption is stable and predictable. These are the best periods to experiment with shifting usage without surprises.',
  },
];