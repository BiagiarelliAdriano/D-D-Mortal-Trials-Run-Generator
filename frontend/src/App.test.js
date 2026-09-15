import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the Mortal Trials landing page', () => {
  render(<App />);
  expect(screen.getByText(/Step into the Tower/i)).toBeInTheDocument();
});
