import { Box, Collapsible, Heading, Text } from '@chakra-ui/react';

interface ChartTipProps {
  heading: string;
  desc: string;
  img: string;
  defaultOpen?: boolean;
}

export const ChartTip = ({
  heading,
  desc,
  img,
  defaultOpen = false,
}: ChartTipProps) => {
  return (
    <Collapsible.Root
      display={'flex'}
      flexDirection={'column'}
      defaultOpen={defaultOpen}
    >
      <Collapsible.Trigger paddingY="3">
        <Box
          borderBottomWidth="3px"
          borderColor={'blue.500'}
          display={'flex'}
          alignItems={'center'}
          gap={3}
          padding="2"
        >
          <Box display={'flex'} alignItems={'center'}>
            <img src={img} alt={heading} width={'35px'} />
          </Box>
          <Heading size="md">{heading}</Heading>
        </Box>
      </Collapsible.Trigger>
      <Collapsible.Content>
        <Box padding="4" borderWidth="1px">
          <Text textStyle="sm" lineHeight={1.6}>
            {desc}
          </Text>
        </Box>
      </Collapsible.Content>
    </Collapsible.Root>
  );
};
