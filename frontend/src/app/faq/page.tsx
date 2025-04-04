"use client";

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { faqApi } from '@/lib/api';
import { FAQ, FAQSearchResult } from '@/types/faq';
import { truncateText, toTitleCase } from '@/lib/utils';

export default function FAQListPage() {
  const searchParams = useSearchParams();
  const categoryParam = searchParams.get('category');
  
  const [faqResults, setFaqResults] = useState<FAQSearchResult | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(categoryParam);

  const categories = [
    { id: 'all', name: 'All Categories' },
    { id: 'general', name: 'General' },
    { id: 'account', name: 'Account' },
    { id: 'billing', name: 'Billing' },
    { id: 'technical', name: 'Technical' },
  ];

  useEffect(() => {
    const fetchFaqs = async () => {
      try {
        setIsLoading(true);
        const category = selectedCategory !== 'all' ? selectedCategory : undefined;
        const result = await faqApi.getFAQs(currentPage, 10, category || undefined);
        setFaqResults(result);
        setError(null);
      } catch (err) {
        setError('Failed to load FAQs. Please try again later.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchFaqs();
  }, [currentPage, selectedCategory]);

  const handleCategoryChange = (categoryId: string) => {
    setSelectedCategory(categoryId);
    setCurrentPage(1);
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo(0, 0);
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
        <h1 className="text-3xl font-bold">Frequently Asked Questions</h1>
        <Link href="/search" className="bg-primary hover:bg-primary-dark text-white px-4 py-2 rounded-md transition-colors">
          Search FAQs
        </Link>
      </div>

      <div className="flex flex-wrap gap-2 mb-6">
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => handleCategoryChange(category.id)}
            className={`px-4 py-2 rounded-md border transition-colors ${
              selectedCategory === category.id || (!selectedCategory && category.id === 'all')
                ? 'bg-primary text-white border-primary'
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            }`}
          >
            {category.name}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="text-center py-8">
          <p>Loading FAQs...</p>
        </div>
      ) : error ? (
        <div className="text-center py-8 text-red-500">
          <p>{error}</p>
        </div>
      ) : faqResults && faqResults.faqs.length > 0 ? (
        <>
          <div className="space-y-4">
            {faqResults.faqs.map((faq) => (
              <Link 
                key={faq.id} 
                href={`/faq/${faq.id}`}
                className="block bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200"
              >
                <h3 className="text-lg font-medium mb-2">{faq.question}</h3>
                <p className="text-gray-600 mb-3">{truncateText(faq.answer, 200)}</p>
                <div className="flex items-center space-x-2">
                  <span className="bg-gray-100 px-2 py-1 rounded text-sm text-gray-700">
                    {toTitleCase(faq.category)}
                  </span>
                  {faq.tags && faq.tags.length > 0 && faq.tags.slice(0, 3).map((tag) => (
                    <span key={tag} className="bg-blue-50 px-2 py-1 rounded text-sm text-blue-700">
                      {tag}
                    </span>
                  ))}
                </div>
              </Link>
            ))}
          </div>
          
          {faqResults.totalPages > 1 && (
            <div className="flex justify-center mt-8">
              <div className="flex space-x-2">
                {Array.from({ length: faqResults.totalPages }, (_, i) => i + 1).map((page) => (
                  <button
                    key={page}
                    onClick={() => handlePageChange(page)}
                    className={`w-10 h-10 rounded-md flex items-center justify-center ${
                      currentPage === page
                        ? 'bg-primary text-white'
                        : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    {page}
                  </button>
                ))}
              </div>
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <p className="text-xl text-gray-600">No FAQs found in this category.</p>
          <p className="mt-2 text-gray-500">Try selecting a different category or search for specific topics.</p>
        </div>
      )}
    </div>
  );
}
