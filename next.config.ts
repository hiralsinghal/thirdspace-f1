import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns : [
      {
        protocol: 'https',
        hostname: "media.formula1.com",

      },
      {
        protocol: 'https',
        hostname: "i.pinimg.com",

      },
    ],
  },
};

export default nextConfig;
