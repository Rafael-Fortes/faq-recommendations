# FAQ Recommendations Frontend

## Purpose

This is the frontend application for the FAQ Recommendations project. It provides a user interface for browsing, searching, and receiving personalized FAQ recommendations. Built with Next.js and React, it offers a modern, responsive interface to interact with the FAQ recommendation system.

## Folder Structure

```
frontend/
├── .next/               # Next.js build output
├── .cursor/             # Cursor IDE configuration
├── docs/                # Documentation files
├── node_modules/        # Dependencies
├── public/              # Static assets
├── src/                 # Source code
│   ├── app/             # Next.js app router pages
│   ├── components/      # Reusable UI components
│   ├── contexts/        # React context providers
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utility libraries
│   ├── styles/          # Global styles
│   └── types/           # TypeScript type definitions
├── .dockerignore        # Files to exclude from Docker builds
├── .env.local           # Environment variables
├── .eslintrc.json       # ESLint configuration
├── .gitignore           # Git ignore configuration
├── .prettierrc.json     # Prettier configuration
├── Dockerfile           # Production Docker configuration
├── Dockerfile.dev       # Development Docker configuration
├── next-env.d.ts        # Next.js TypeScript declarations
├── next.config.js       # Next.js configuration
├── package-lock.json    # Dependency lock file
├── package.json         # Project metadata and scripts
├── postcss.config.js    # PostCSS configuration
├── tailwind.config.js   # Tailwind CSS configuration
└── tsconfig.json        # TypeScript configuration
```

## Installation and Execution

### Using npm

1. Install dependencies:
   ```
   npm install
   ```

2. Development mode:
   ```
   npm run dev
   ```
   This will start the development server at [http://localhost:3000](http://localhost:3000).

3. Build for production:
   ```
   npm run build
   ```

4. Start production server:
   ```
   npm start
   ```

### Using Docker

#### Development Mode

1. Build the development Docker image:
   ```
   docker build -t faq-recommendations-frontend-dev -f Dockerfile.dev .
   ```

2. Run the container:
   ```
   docker run -p 3000:3000 -v $(pwd):/app -v /app/node_modules --env-file .env.local faq-recommendations-frontend-dev
   ```
   This mounts your local directory to enable hot-reloading.

#### Production Mode

1. Build the production Docker image:
   ```
   docker build -t faq-recommendations-frontend .
   ```

2. Run the container:
   ```
   docker run -p 3000:3000 --env-file .env.local faq-recommendations-frontend
   ```

The application will be available at [http://localhost:3000](http://localhost:3000).
