"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { faqApi } from '@/lib/api';
import { FAQ } from '@/types/faq';
import { formatDate, toTitleCase } from '@/lib/utils';

export default function FAQDetailPage() {
  const params = useParams();
  const id = params.id as string;

  const [faq, setFaq] = useState<FAQ | null>(null);
  const [relatedFaqs, setRelatedFaqs] = useState<FAQ[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFaqDetails = async () => {
      try {
        setIsLoading(true);
        const faqData = await faqApi.getFAQById(id);
        setFaq(faqData);

        // Fetch related FAQs
        const relatedFaqsData = await faqApi.getRelatedFAQs(id);
        setRelatedFaqs(relatedFaqsData);
        
        setError(null);
      } catch (err) {
        setError('Failed to load FAQ details. Please try again later.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    if (id) {
      fetchFaqDetails();
    }
  }, [id]);

  if (isLoading) {
    return (
      <div className="text-center py-16">
        <p className="text-lg">Loading FAQ details...</p>
      </div>
    );
  }

  if (error || !faq) {
    return (
      <div className="text-center py-16">
        <h1 className="text-2xl font-bold text-red-500 mb-4">Error</h1>
        <p className="text-lg">{error || 'FAQ not found'}</p>
        <Link href="/faq" className="mt-6 inline-block text-primary hover:text-primary-dark">
          ← Back to FAQs
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <Link href="/faq" className="text-primary hover:text-primary-dark inline-flex items-center mb-6">
        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to FAQs
      </Link>
      
      <article className="bg-white p-8 rounded-lg shadow-md border border-gray-200">
        <header className="mb-6">
          <h1 className="text-2xl font-bold mb-4">{faq.question}</h1>
          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
            <div className="bg-gray-100 px-3 py-1 rounded-full">
              Category: {toTitleCase(faq.category)}
            </div>
            {faq.updatedAt && (
              <div>
                Last updated: {formatDate(faq.updatedAt)}
              </div>
            )}
          </div>
        </header>
        
        <div className="prose max-w-none">
          <p className="text-gray-800 whitespace-pre-line">{faq.answer}</p>
        </div>
        
        {faq.tags && faq.tags.length > 0 && (
          <div className="mt-8 pt-6 border-t border-gray-100">
            <div className="flex flex-wrap gap-2">
              {faq.tags.map((tag) => (
                <span key={tag} className="bg-blue-50 px-3 py-1 rounded-full text-sm text-blue-700">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}
      </article>
      
      {relatedFaqs.length > 0 && (
        <section className="mt-12">
          <h2 className="text-xl font-bold mb-4">Related FAQs</h2>
          <div className="space-y-4">
            {relatedFaqs.map((relatedFaq) => (
              <Link 
                key={relatedFaq.id} 
                href={`/faq/${relatedFaq.id}`}
                className="block bg-white p-5 rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200"
              >
                <h3 className="text-lg font-medium">{relatedFaq.question}</h3>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
