import { NOTIFICATIONS } from '@/assets/data/notifications';
import { Navbar } from '@/components/common/Navbar';
import { Notification } from '@/components/common/Notification';
import { PageLoader } from '@/components/loader/PageLoader';
import { Box, Heading, Separator } from '@chakra-ui/react';
import { useEffect, useState } from 'react';

export const Profile = () => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  }, []);

  if (isLoading) {
    return <PageLoader title="Loading the profile..." />;
  }

  return (
    <Box p={4}>
      <Navbar />
      <Heading size="2xl" mb={2}>
        Notifications
      </Heading>
      <Separator />
      {NOTIFICATIONS.map((note) => (
        <Box key={note.id} mt={4}>
          <Notification
            status={note.status as 'info' | 'warning' | 'success' | 'error'}
            title={note.title}
            description={note.description}
          />
        </Box>
      ))}
    </Box>
  );
};
