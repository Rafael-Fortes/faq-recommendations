# FAQ Recommendations Frontend

This is the frontend application for the FAQ Recommendations system, built with Next.js according to the requirements in the PRD.

## Features

- **Header Display:** Application title with social media links (GitHub and LinkedIn)
- **FAQ Search:** Select a FAQ collection, enter a question, and search for relevant answers
- **FAQ Display:** View questions and answers with relevance indicators after search

## Project Structure

The project follows a well-organized structure:

```
faq-recommendations-frontend/
├── public/          # Static assets
├── src/             # Source code
│   ├── app/         # Next.js App Router
│   │   ├── layout.tsx     # Root layout with header and footer
│   │   ├── page.tsx       # Main FAQ Recommendations page
│   ├── components/    # Reusable UI components
│   ├── contexts/      # React Contexts for state management
│   ├── hooks/         # Custom React Hooks
│   ├── lib/           # Utility functions, API clients
│   │   ├── api.ts     # API client for backend communication
│   │   ├── utils.ts   # Utility functions
│   ├── styles/        # Global styles
│   │   ├── global.css # Global CSS with Tailwind
│   ├── types/         # TypeScript types
│   │   ├── faq.d.ts   # Types related to FAQ data
```

## Backend API Integration

The frontend integrates with the backend API documented in `openapi.json`, which provides:

- List of available FAQ collections
- FAQ items for a selected collection
- Search functionality based on user questions

## Getting Started

First, install the dependencies:

```bash
npm install
# or
yarn install
```

Then, run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Environment Variables

You can configure the application with the following environment variables:

- `NEXT_PUBLIC_API_URL`: URL of the backend API (default: http://localhost:8000)

## Technologies Used

- Next.js
- React
- TypeScript
- Tailwind CSS
- Axios

## Design System

The application follows the design system specified in the styling guide, including:

- Color palette with Primary Purple (#6400E4)
- Typography using system fonts
- Responsive design for various screen sizes
- Accessibility features including proper focus states and semantic HTML
