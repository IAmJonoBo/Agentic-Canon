import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    size: {
      control: "select",
      options: ["small", "medium", "large"],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    label: "Click me",
    primary: true,
  },
};

export const Default: Story = {
  args: {
    label: "Click me",
  },
};

export const Small: Story = {
  args: {
    label: "Small button",
    size: "small",
  },
};

export const Large: Story = {
  args: {
    label: "Large button",
    size: "large",
    primary: true,
  },
};
