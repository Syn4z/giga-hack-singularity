import { Alert } from '@chakra-ui/react';

interface NotificationProps {
  status: 'info' | 'warning' | 'success' | 'error';
  title: string;
  description: string;
}

export const Notification = ({
  status,
  title,
  description,
}: NotificationProps) => {
  return (
    <Alert.Root status={status}>
      <Alert.Indicator />
      <Alert.Content>
        <Alert.Title>{title}</Alert.Title>
        {description && <Alert.Description>{description}</Alert.Description>}
      </Alert.Content>
    </Alert.Root>
  );
};
