"use client";

import { useState, useEffect, FormEvent } from 'react';
import { faqApi } from '@/lib/api';
import { SearchRequest, SearchResultItem, FaqCollectionInfo, FaqListItem } from '@/types/faq';

export default function Home() {
  // FAQ Collections
  const [faqCollections, setFaqCollections] = useState<FaqCollectionInfo[]>([]);
  const [selectedFaq, setSelectedFaq] = useState<string>('');
  const [isLoadingCollections, setIsLoadingCollections] = useState(true);
  
  // FAQ Items
  const [faqItems, setFaqItems] = useState<FaqListItem[]>([]);
  const [isLoadingItems, setIsLoadingItems] = useState(false);
  
  // Search
  const [question, setQuestion] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResultItem[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  
  // Error states
  const [error, setError] = useState<string | null>(null);

  // Fetch FAQ collections on mount
  useEffect(() => {
    const fetchFaqCollections = async () => {
      try {
        setIsLoadingCollections(true);
        const result = await faqApi.listFaqs();
        setFaqCollections(result.data);
        setError(null);
      } catch (err) {
        setError('Failed to load FAQ collections. Please try again later.');
        console.error(err);
      } finally {
        setIsLoadingCollections(false);
      }
    };

    fetchFaqCollections();
  }, []);

  // Fetch FAQ items when a collection is selected
  useEffect(() => {
    if (!selectedFaq) {
      setFaqItems([]);
      return;
    }

    const fetchFaqItems = async () => {
      try {
        setIsLoadingItems(true);
        const result = await faqApi.getFaqItems(selectedFaq);
        setFaqItems(result.data);
        setError(null);
      } catch (err) {
        setError(`Failed to load FAQ items for "${selectedFaq}". Please try again later.`);
        console.error(err);
      } finally {
        setIsLoadingItems(false);
      }
    };

    fetchFaqItems();
  }, [selectedFaq]);

  // Handle search form submission
  const handleSearch = async (e: FormEvent) => {
    e.preventDefault();
    
    if (!selectedFaq || !question.trim()) {
      return;
    }

    try {
      setIsSearching(true);
      const searchRequest: SearchRequest = {
        question: question,
        faq_name: selectedFaq,
        limit: 10
      };
      
      const result = await faqApi.searchFaqs(searchRequest);
      setSearchResults(result.data);
      
      // Re-order the FAQ items based on search results
      if (result.data.length > 0) {
        const orderedItems = result.data.map(item => ({
          question: item.question,
          answer: item.answer,
          id: item.id,
          score: item.score
        }));
        
        // Convert to FaqListItem type but keep the score for relevance display
        const orderedFaqItems = orderedItems as (FaqListItem & { score: number })[];
        setFaqItems(orderedFaqItems);
      }
      
      setError(null);
    } catch (err) {
      setError('Failed to search FAQs. Please try again later.');
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  // Render a relevance indicator based on the score
  const renderRelevanceIndicator = (score?: number) => {
    if (!score) return null;
    
    let width = `${Math.round(score * 100)}%`;
    let relevanceClass = '';
    
    if (score >= 0.7) {
      relevanceClass = 'bg-green-relevance';
    } else if (score >= 0.4) {
      relevanceClass = 'bg-blue-relevance';
    } else {
      relevanceClass = 'bg-gray-300';
    }
    
    return (
      <div className="mt-2 w-full bg-gray-200 rounded-full h-2.5">
        <div 
          className={`h-2.5 rounded-full ${relevanceClass}`} 
          style={{ width }}
          aria-label={`Relevance score: ${Math.round(score * 100)}%`}
        ></div>
      </div>
    );
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h1 className="text-2xl font-bold mb-6">FAQ Recommendations</h1>
        
        <form onSubmit={handleSearch} className="space-y-4 md:space-y-0 md:flex md:items-end md:space-x-4">
          <div className="flex-1">
            <label htmlFor="faq-select" className="block mb-2 text-sm font-medium text-text">
              Select FAQ Collection <span className="text-red-500">*</span>
            </label>
            <select
              id="faq-select"
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:border-primary"
              value={selectedFaq}
              onChange={(e) => setSelectedFaq(e.target.value)}
              required
              aria-required="true"
            >
              <option value="">Select a FAQ collection</option>
              {faqCollections.map((faq) => (
                <option key={faq.name} value={faq.name}>
                  {faq.name} ({faq.points_count} items)
                </option>
              ))}
            </select>
          </div>
          
          <div className="flex-1">
            <label htmlFor="question-input" className="block mb-2 text-sm font-medium text-text">
              Your Question
            </label>
            <input
              id="question-input"
              type="text"
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:border-primary"
              placeholder="Type your question here..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
          </div>
          
          <div>
            <button
              type="submit"
              className="search-button"
              disabled={!selectedFaq || isSearching}
            >
              {isSearching ? 'Searching...' : 'Search'}
            </button>
          </div>
        </form>
      </div>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}
      
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-bold mb-4">
          {searchResults.length > 0 
            ? 'Search Results' 
            : selectedFaq 
              ? `FAQs from "${selectedFaq}"` 
              : 'Select a FAQ Collection to View Questions and Answers'}
        </h2>
        
        {isLoadingItems ? (
          <div className="text-center py-8">
            <p>Loading FAQ items...</p>
          </div>
        ) : faqItems.length > 0 ? (
          <div className="space-y-2">
            {faqItems.map((item, index) => (
              <div 
                key={item.id || index} 
                className={`faq-item ${searchResults.length > 0 ? 'p-4 rounded-md' : ''}`}
              >
                <h3 className="faq-question">{item.question}</h3>
                <p className="faq-answer">{item.answer}</p>
                {(item as any).score !== undefined && renderRelevanceIndicator((item as any).score)}
              </div>
            ))}
          </div>
        ) : selectedFaq ? (
          <p className="text-center py-4">No FAQ items found in this collection.</p>
        ) : (
          <p className="text-center py-4">Please select a FAQ collection to view its items.</p>
        )}
      </div>
    </div>
  );
}
