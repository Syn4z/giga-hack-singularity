import { NOTIFICATIONS } from '@/assets/data/notifications';
import { PERSONALIZED_TIPS } from '@/assets/data/personalized_tips';
import { ChartTip } from '@/components/charts/ChartTip';
import { Navbar } from '@/components/common/Navbar';
import { Notification } from '@/components/common/Notification';
import { PageLoader } from '@/components/loader/PageLoader';
import { getLocalStorageItem } from '@/utils/localStorage';
import { Box, Button, Heading, Separator, Text } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const Profile = () => {
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/survey');
  };

  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  }, []);

  if (isLoading) {
    return <PageLoader title="Loading the profile..." />;
  }

  let insightsContent = (
    <>
      <Text mb={6}>
        Answer these questions to help us tailor your energy consumption
        insights. It will only take a minute!
      </Text>
      <Button bg={'teal.500'} w={'full'} onClick={handleClick}>
        Take the Survey
      </Button>
    </>
  );

  if (getLocalStorageItem('surveyCompleted')) {
    insightsContent = (
      <Box>
        <Text>
          Based on your survey responses, here are some personalized energy
          consumption tips:
        </Text>
        {PERSONALIZED_TIPS.map((tip, index) => (
          <ChartTip
            key={index}
            heading={tip.title}
            desc={tip.desc}
            img={tip.img}
            defaultOpen={index === 0}
          />
        ))}
      </Box>
    );
  }

  return (
    <Box p={4}>
      <Navbar />
      <Box mb={6}>
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

      <Box>
        <Heading size="2xl" mb={2}>
          Personalized Insights
        </Heading>
        <Separator mb={4} />
        {insightsContent}
      </Box>
    </Box>
  );
};
