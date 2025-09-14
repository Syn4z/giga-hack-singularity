import { PageLoader } from '@/components/loader/PageLoader';
import { setLocalStorageItem } from '@/utils/localStorage';
import {
  Box,
  Button,
  CheckboxCard,
  CheckboxGroup,
  Float,
  Icon,
  SimpleGrid,
  Text,
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import {
  HiChip,
} from 'react-icons/hi';
import { useNavigate } from 'react-router-dom';

const items = [
  { icon: <HiChip />, label: 'Fridge' },
  { icon: <HiChip />, label: 'Dryer' },
  { icon: <HiChip />, label: 'Washing Machine' },
  { icon: <HiChip />, label: 'Iron' },
  { icon: <HiChip />, label: 'Kettle' },
  { icon: <HiChip />, label: 'Air Conditioner' }
];

export const Survey = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [selected, setSelected] = useState<string[]>([]); // track selections
  const navigate = useNavigate();

  const handleSubmit = () => {
    setIsSubmitted(true);
  };

  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    if (isSubmitted) {
      setTimeout(() => {
        navigate('/profile');
      }, 2000);
    }
  }, [isSubmitted, navigate]);

  if (isSubmitted) {
    setLocalStorageItem('surveyCompleted', 'true');
    return <PageLoader title="Analyzing your responses..." />;
  }

  if (isLoading) {
    return <PageLoader title="Loading the survey..." />;
  }

  return (
    <Box
      p={4}
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      h="100vh"
    >
      <Text fontSize="xl" textAlign="center">
        Which of the following appliances do you have in your household?
      </Text>
      <Text fontSize="md" mb="8" textAlign="center" fontStyle="italic">
        (Select at least two)
      </Text>

      <CheckboxGroup
        value={selected}
        onValueChange={(values: string[]) => setSelected(values)}
        w="full"
      >
        <SimpleGrid minChildWidth="150px" gap="2">
          {items.map((item) => (
            <CheckboxCard.Root
              align="center"
              key={item.label}
              value={item.label}
            >
              <CheckboxCard.HiddenInput />
              <CheckboxCard.Control>
                <CheckboxCard.Content>
                  <Icon fontSize="2xl" mb="2">
                    {item.icon}
                  </Icon>
                  <CheckboxCard.Label>{item.label}</CheckboxCard.Label>
                  <CheckboxCard.Description>
                    {item.description}
                  </CheckboxCard.Description>
                </CheckboxCard.Content>
                <Float placement="top-end" offset="6">
                  <CheckboxCard.Indicator />
                </Float>
              </CheckboxCard.Control>
            </CheckboxCard.Root>
          ))}
        </SimpleGrid>
      </CheckboxGroup>

      <Button
        bg="blue.500"
        w="full"
        mt={8}
        onClick={handleSubmit}
        disabled={isSubmitted}
        style={{
          visibility: selected.length >= 2 ? 'visible' : 'hidden',
        }}
      >
        Submit
      </Button>
    </Box>
  );
};
