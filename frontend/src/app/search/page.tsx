"use client";

import { useState, useEffect, FormEvent } from 'react';
import Link from 'next/link';
import { useSearchParams, useRouter } from 'next/navigation';
import { faqApi } from '@/lib/api';
import { FAQ, FAQSearchResult } from '@/types/faq';
import { truncateText } from '@/lib/utils';

export default function SearchPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const queryParam = searchParams.get('q') || '';
  
  const [searchQuery, setSearchQuery] = useState(queryParam);
  const [results, setResults] = useState<FAQSearchResult | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    if (queryParam) {
      performSearch(queryParam, 1);
    }
  }, [queryParam]);

  const performSearch = async (query: string, page: number) => {
    if (!query.trim()) return;
    
    try {
      setIsSearching(true);
      setError(null);
      const searchResults = await faqApi.searchFAQs(query, page, 10);
      setResults(searchResults);
      setCurrentPage(page);
    } catch (err) {
      setError('An error occurred while searching. Please try again.');
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSearchSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  const handlePageChange = (page: number) => {
    performSearch(queryParam, page);
    window.scrollTo(0, 0);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Search FAQs</h1>
      
      <form onSubmit={handleSearchSubmit} className="mb-8">
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for answers to your questions..."
            className="flex-grow px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary focus:border-primary transition-colors outline-none"
            aria-label="Search query"
          />
          <button
            type="submit"
            className="bg-primary hover:bg-primary-dark text-white font-medium px-6 py-3 rounded-lg transition-colors"
            disabled={isSearching}
          >
            {isSearching ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>
      
      {isSearching ? (
        <div className="text-center py-8">
          <p className="text-lg">Searching...</p>
        </div>
      ) : error ? (
        <div className="text-center py-8 text-red-500">
          <p>{error}</p>
        </div>
      ) : results ? (
        <div>
          <div className="mb-6">
            <p className="text-gray-600">
              {results.totalCount} results found for "{queryParam}"
            </p>
          </div>
          
          {results.faqs.length > 0 ? (
            <>
              <div className="space-y-6">
                {results.faqs.map((faq) => (
                  <Link 
                    key={faq.id} 
                    href={`/faq/${faq.id}`}
                    className="block bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200"
                  >
                    <h2 className="text-lg font-medium mb-2">{faq.question}</h2>
                    <p className="text-gray-600 mb-2">{truncateText(faq.answer, 200)}</p>
                    {faq.tags && faq.tags.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {faq.tags.slice(0, 3).map((tag) => (
                          <span key={tag} className="bg-blue-50 px-2 py-1 rounded text-sm text-blue-700">
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </Link>
                ))}
              </div>
              
              {results.totalPages > 1 && (
                <div className="flex justify-center mt-10">
                  <div className="flex space-x-2">
                    {currentPage > 1 && (
                      <button
                        onClick={() => handlePageChange(currentPage - 1)}
                        className="px-4 py-2 rounded-md bg-white text-gray-700 border border-gray-300 hover:bg-gray-50"
                      >
                        Previous
                      </button>
                    )}
                    
                    {Array.from({ length: Math.min(5, results.totalPages) }, (_, i) => {
                      const pageNumber = i + 1;
                      return (
                        <button
                          key={pageNumber}
                          onClick={() => handlePageChange(pageNumber)}
                          className={`w-10 h-10 rounded-md flex items-center justify-center ${
                            currentPage === pageNumber
                              ? 'bg-primary text-white'
                              : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                          }`}
                        >
                          {pageNumber}
                        </button>
                      );
                    })}
                    
                    {currentPage < results.totalPages && (
                      <button
                        onClick={() => handlePageChange(currentPage + 1)}
                        className="px-4 py-2 rounded-md bg-white text-gray-700 border border-gray-300 hover:bg-gray-50"
                      >
                        Next
                      </button>
                    )}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-12 bg-gray-50 rounded-lg">
              <p className="text-xl text-gray-600">No results found for "{queryParam}"</p>
              <p className="mt-2 text-gray-500">Try different keywords or browse our categories</p>
              <Link href="/faq" className="mt-6 inline-block bg-primary hover:bg-primary-dark text-white font-medium px-6 py-2 rounded-lg transition-colors">
                Browse all FAQs
              </Link>
            </div>
          )}
        </div>
      ) : queryParam ? (
        <div className="text-center py-8">
          <p>Loading results...</p>
        </div>
      ) : (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <p className="text-xl text-gray-600">Enter a search term to find answers</p>
          <p className="mt-2 text-gray-500">Or browse our categories of Frequently Asked Questions</p>
          <Link href="/faq" className="mt-6 inline-block text-primary hover:text-primary-dark font-medium">
            Browse all FAQs →
          </Link>
        </div>
      )}
    </div>
  );
}
