// API response types
export interface FaqCollectionInfo {
  name: string;
  vector_size: number;
  distance: string;
  points_count: number;
}

export interface ListFaqsResponse {
  message: string;
  data: FaqCollectionInfo[];
}

export interface FaqListItem {
  question: string;
  answer: string;
  id?: string | null;
}

export interface ReadFaqResponse {
  message: string;
  data: FaqListItem[];
}

export interface SearchResultItem {
  id: string;
  question: string;
  answer: string;
  score: number;
}

export interface SearchResponse {
  message: string;
  data: SearchResultItem[];
}

// Request types
export interface SearchRequest {
  question: string;
  faq_name: string;
  limit?: number;
}

// UI types and extensions
export interface FAQ {
  id: string;
  question: string;
  answer: string;
  category: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export interface FAQCategory {
  id: string;
  name: string;
  description: string;
}

export interface FAQSearchResult {
  faqs: FAQ[];
  totalCount: number;
  page: number;
  totalPages: number;
}
