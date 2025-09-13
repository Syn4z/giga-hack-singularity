import { Badge, HStack, Stat } from "@chakra-ui/react";

export const Expenses = () => {
  return (
    <Stat.Root borderWidth={1} p={4} rounded={'md'}>
      <Stat.Label>Expenses</Stat.Label>
      <HStack>
        <Stat.ValueText minWidth={'110px'}>
          MDL 974
        </Stat.ValueText>
        <Badge colorPalette="green" gap="0">
          <Stat.DownIndicator color="green.500" />
          12%
        </Badge>
      </HStack>
      <Stat.HelpText>since last month</Stat.HelpText>
    </Stat.Root>
  );
};
