import { Box, Button } from '@chakra-ui/react';
import ctaIcon from '../../assets/img/tips/tip_3.png';

interface NavigationButtonProps {
  onClick?: () => void;
}

export const NavigationButton = ({ onClick }: NavigationButtonProps) => {
  return (
    <Box
      width={"175px"}
      borderWidth="1.5px"
      borderColor={'teal.500'}
      rounded={'md'}
      display={'flex'}
      flexDirection={'column'}
      justifyContent={'flex-end'}
      alignItems={'center'}
      gap={1.5}
    >
      <Box width={35} height={35} bg={'transparent'} borderRadius={50} p={0.5}>
        <img src={ctaIcon} alt="Call to Action" width={35} />
      </Box>
      <Button
        fontWeight={'bold'}
        fontSize={'sm'}
        w={'full'}
        h={'50%'}
        bg={'teal.500'}
        onClick={onClick}
      >
        Forecast & Save &rarr;
      </Button>
    </Box>
  );
};
