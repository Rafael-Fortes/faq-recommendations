'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="max-w-3xl mx-auto py-12 px-4 text-center">
      <h2 className="text-2xl font-bold text-text mb-4">Something went wrong!</h2>
      <p className="mb-6 text-gray-600">
        We apologize for the inconvenience. Please try again later or contact support if the issue persists.
      </p>
      <button
        onClick={reset}
        className="bg-primary hover:bg-primary-dark text-white font-medium px-6 py-3 rounded-md transition-colors"
      >
        Try again
      </button>
    </div>
  );
} 