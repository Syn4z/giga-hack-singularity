import { Box, Button } from '@chakra-ui/react';
import { NavLink } from 'react-router-dom';

export const Navbar = () => {
  const defaultStyles = {
    borderRadius: '30px',
    variant: 'outline' as const,
    color: 'black',
  };

  const activeStyles = {
    bg: 'teal.500',
    color: 'white',
  };

  const links = [
    { label: 'Analytics', to: '/analytics' },
    { label: 'Forecast', to: '/forecast' },
    { label: 'Profile', to: '/profile' },
  ];

  return (
    <Box display="flex" justifyContent="center" gap={2} mb={8}>
      {links.map(({ label, to }) => (
        <NavLink key={label} to={to}>
          {({ isActive }) => (
            <Button {...defaultStyles} {...(isActive ? activeStyles : {})}>
              {label}
            </Button>
          )}
        </NavLink>
      ))}
    </Box>
  );
};
