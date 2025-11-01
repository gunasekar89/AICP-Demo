/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['@formkit/auto-animate'],
  },
};

module.exports = nextConfig;
