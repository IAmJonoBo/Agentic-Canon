module.exports = {
  name: 'size-limit-config',
  limit: [
    {
      name: 'Main bundle',
      path: 'dist/assets/index-*.js',
      limit: '100 KB',
      webpack: false
    },
    {
      name: 'CSS',
      path: 'dist/assets/index-*.css',
      limit: '10 KB'
    },
    {
      name: 'Total bundle size',
      path: 'dist/**/*',
      limit: '250 KB'
    }
  ]
};
