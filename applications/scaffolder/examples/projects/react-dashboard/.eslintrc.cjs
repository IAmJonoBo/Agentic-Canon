const js = require('@eslint/js');
const tsParser = require('@typescript-eslint/parser');
const typescript = require('@typescript-eslint/eslint-plugin');
const reactRefresh = require('eslint-plugin-react-refresh');
const reactHooks = require('eslint-plugin-react-hooks');

module.exports = [
  {
    ignores: ['dist', 'storybook-static', 'coverage', 'node_modules'],
  },
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: './tsconfig.json',
        tsconfigRootDir: __dirname,
      },
    },
    plugins: {
      '@typescript-eslint': typescript,
      'react-refresh': reactRefresh,
      'react-hooks': reactHooks,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...typescript.configs['recommended-type-checked'].rules,
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    },
  },
];
