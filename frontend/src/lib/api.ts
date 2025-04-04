import axios from 'axios';
import { 
  FAQ, 
  FAQSearchResult, 
  ListFaqsResponse, 
  ReadFaqResponse, 
  SearchRequest, 
  SearchResponse 
} from '@/types/faq';

// Use the API proxy we configured in next.config.js
const API_URL = '/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const faqApi = {
  /**
   * List all available FAQs
   */
  listFaqs: async (): Promise<ListFaqsResponse> => {
    const response = await apiClient.get('/faqs');
    return response.data;
  },

  /**
   * Get all items from a specific FAQ collection
   */
  getFaqItems: async (faqName: string, limit?: number, offset = 0): Promise<ReadFaqResponse> => {
    const response = await apiClient.get(`/faq/${faqName}/items`, {
      params: { limit, offset },
    });
    return response.data;
  },

  /**
   * Search FAQs based on a question
   */
  searchFaqs: async (searchRequest: SearchRequest): Promise<SearchResponse> => {
    const response = await apiClient.post('/', searchRequest);
    return response.data;
  },

  // Legacy API methods
  /**
   * Get all FAQs with optional pagination and filters
   */
  getFAQs: async (page = 1, limit = 10, category?: string): Promise<FAQSearchResult> => {
    const response = await apiClient.get('/faqs', {
      params: { page, limit, category },
    });
    return response.data;
  },

  /**
   * Get a single FAQ by ID
   */
  getFAQById: async (id: string): Promise<FAQ> => {
    const response = await apiClient.get(`/faqs/${id}`);
    return response.data;
  },

  /**
   * Search FAQs by query string
   */
  searchFAQs: async (query: string, page = 1, limit = 10): Promise<FAQSearchResult> => {
    const response = await apiClient.get('/faqs/search', {
      params: { query, page, limit },
    });
    return response.data;
  },

  /**
   * Get recommended FAQs related to the current FAQ
   */
  getRelatedFAQs: async (faqId: string, limit = 5): Promise<FAQ[]> => {
    const response = await apiClient.get(`/faqs/${faqId}/related`, {
      params: { limit },
    });
    return response.data;
  },
};

export default apiClient;
