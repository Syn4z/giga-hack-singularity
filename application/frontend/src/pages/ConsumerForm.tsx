import { PageLoader } from '@/components/loader/PageLoader';
import { Box, Button, Field, Input, Separator } from '@chakra-ui/react';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';

interface FormValues {
  meterNumber: number;
  email: string;
}

export const ConsumerForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>();
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const submitHandler = handleSubmit((data) => {
    console.log(data);
    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      navigate('/analytics');
    }, 1500);
  });

  if (isLoading) {
    return <PageLoader />;
  }

  return (
    <Box
      height={'100vh'}
      display={'flex'}
      flexDirection={'column'}
      justifyContent={'center'}
      alignItems={'center'}
    >
      <Box textAlign="center" mb={6}>
        <Box fontSize="2xl" fontWeight="bold">
          Set Up Your Household
        </Box>
        <Box fontSize="sm" color="gray.500" mt={2} maxWidth="340px">
          Enter your meter number and email so we can personalize your energy
          analytics and forecasts.
        </Box>
        <Separator mt={4} />
      </Box>
      <Box borderWidth={1} borderRadius="md" p={6} boxShadow="md">
        <form onSubmit={submitHandler} style={{ width: '300px' }}>
          <Field.Root invalid={!!errors.email} mb={3}>
            <Field.Label alignSelf={'center'}>Email</Field.Label>
            <Input
              {...register('email', {
                required: 'Email is required',
              })}
              type="email"
              autoComplete="off"
            />
            <Field.ErrorText>{errors.email?.message}</Field.ErrorText>
          </Field.Root>
          <Field.Root invalid={!!errors.meterNumber} mb={3}>
            <Field.Label alignSelf={'center'}>Meter number</Field.Label>
            <Input
              {...register('meterNumber', {
                required: 'Meter number is required',
              })}
              type="number"
              autoComplete="off"
            />
            <Field.ErrorText>{errors.meterNumber?.message}</Field.ErrorText>
          </Field.Root>
          <Button type="submit" bgColor={'blue.500'} w={'full'}>
            Submit
          </Button>
        </form>
      </Box>
    </Box>
  );
};
