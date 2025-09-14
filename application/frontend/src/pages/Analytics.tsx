import { Expenses } from '@/components/stats/Expenses';
import { PeakLoad } from '@/components/stats/PeakLoad';
import { Usage } from '@/components/stats/Usage';
import { Box, Flex, Heading, Separator } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { ChartFilters } from '@/components/charts/ChartFilters';
import { NavigationButton } from '@/components/stats/NavigationButton';
import { useNavigate } from 'react-router-dom';
import { PageLoader } from '@/components/loader/PageLoader';
import { Navbar } from '@/components/common/Navbar';
import { FloatingButton } from '@/components/chat/FloatingButton';

export const Analytics = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [isRedirecting, setIsRedirecting] = useState(false);
  const navigate = useNavigate();

  const handleClick = () => {
    setIsRedirecting(true);

    setTimeout(() => {
      navigate('/forecast');
    }, 2000);
  };

  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  }, []);

  if (isLoading) {
    return <PageLoader title="Loading the analytics..." />;
  }

  if (isRedirecting) {
    return <PageLoader title="Preparing your forecast..." />;
  }

  return (
    <Box p={4} position={'relative'}>
      <Navbar />
      <FloatingButton />

      <Flex
        flexDirection={'column'}
        alignItems={'center'}
        mb={8}
        borderWidth={2}
        borderColor={'teal.500'}
        p={4}
        borderRadius={8}
      >
        <Heading size="2xl">Hi, Andrei!</Heading>
        <Heading size="md" fontWeight="normal" color="gray.600" mb={4}>
          Sunday, Sept 14, 2025
        </Heading>
        <Heading size="md" fontWeight="bold" color="teal.500" mb={2}>
          You're on track this week
        </Heading>
      </Flex>

      <Heading size="2xl" mb={2}>
        Energy Insights
      </Heading>
      <Separator mb="4" />
      <Box
        display={'flex'}
        justifyContent={'center'}
        gap={4}
        flexWrap={'wrap'}
        mb={4}
      >
        <Expenses />
        <Usage />
        <PeakLoad />
        <NavigationButton onClick={handleClick} />
      </Box>

      <Box mt={16}>
        <Heading size="2xl" mb={2}>
          Usage History
        </Heading>
        <Separator />
        <ChartFilters />
      </Box>
    </Box>
  );
};
