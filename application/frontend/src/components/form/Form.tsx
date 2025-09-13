import { Box, Text } from '@chakra-ui/react';
import { Button, Field, Input, Stack } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';

interface FormValues {
  firstName: string;
  lastName: string;
}

export const Form = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>();

  const onSubmit = handleSubmit((data) => console.log(data));

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      h="100vh"
    >
      <Text fontSize="4xl">Form page</Text>
      <form onSubmit={onSubmit}>
        <Stack gap="4" align="flex-start" maxW="sm">
          <Field.Root invalid={!!errors.firstName}>
            <Field.Label>First name</Field.Label>
            <Input {...register('firstName')} />
            <Field.ErrorText>{errors.firstName?.message}</Field.ErrorText>
          </Field.Root>

          <Field.Root invalid={!!errors.lastName}>
            <Field.Label>Last name</Field.Label>
            <Input {...register('lastName')} />
            <Field.ErrorText>{errors.lastName?.message}</Field.ErrorText>
          </Field.Root>

          <Button type="submit">Submit</Button>
        </Stack>
      </form>
    </Box>
  );
};
