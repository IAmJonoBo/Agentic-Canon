import type { Meta, StoryObj } from '@storybook/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RealtimeToggle } from './RealtimeToggle';

const queryClient = new QueryClient();

const meta: Meta<typeof RealtimeToggle> = {
  component: RealtimeToggle,
  title: 'Dashboard/RealtimeToggle',
  decorators: [
    (Story) => (
      <QueryClientProvider client={queryClient}>
        <Story />
      </QueryClientProvider>
    ),
  ],
};

export default meta;

type Story = StoryObj<typeof RealtimeToggle>;

export const Default: Story = {};
