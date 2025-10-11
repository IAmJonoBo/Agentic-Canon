import type { StorybookConfig } from "@storybook/react-vite";

const config: StorybookConfig = {
  framework: {
    name: "@storybook/react-vite",
    options: {},
  },
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons: [
    "@storybook/addon-essentials",
    {% if cookiecutter.enable_accessibility_tests == "yes" %}
    "@storybook/addon-a11y",
    {% endif %}
  ],
  docs: {
    autodocs: "tag",
  },
};

export default config;
