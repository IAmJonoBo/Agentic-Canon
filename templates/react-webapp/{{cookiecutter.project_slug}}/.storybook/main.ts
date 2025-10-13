import type { StorybookConfig } from "@storybook/react-vite";

const INCLUDE_A11Y =
  "{{ 'true' if cookiecutter.enable_accessibility_tests == 'yes' else 'false' }}" === "true";

const addons: StorybookConfig["addons"] = ["@storybook/addon-essentials"];

if (INCLUDE_A11Y) {
  addons.push("@storybook/addon-a11y");
}

const config: StorybookConfig = {
  framework: {
    name: "@storybook/react-vite",
    options: {},
  },
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons,
  docs: {
    autodocs: "tag",
  },
};

export default config;
