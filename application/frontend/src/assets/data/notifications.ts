export const NOTIFICATIONS = [
  {
    id: 1,
    status: 'success',
    title: 'Meter synced successfully',
    description: 'Your smart meter data was fetched successfully.',
  },
  {
    id: 2,
    status: 'warning',
    title: 'High peak consumption',
    description: 'Your energy usage is higher than usual during peak hours.',
  },
  {
    id: 3,
    status: 'error',
    title: 'Invalid device configuration',
    description: 'Some devices in your household are missing or misconfigured.',
  },
  {
    id: 4,
    status: 'warning',
    title: 'Upcoming tariff spike',
    description:
      'Energy rates will increase in the next 2 hours. Consider delaying usage.',
  },
];
