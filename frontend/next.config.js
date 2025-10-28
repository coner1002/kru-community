const withNextIntl = require('next-intl/plugin')(
  // Specify a custom path for your i18n configuration file
  './i18n.ts'
);

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['localhost'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
}

module.exports = withNextIntl(nextConfig);