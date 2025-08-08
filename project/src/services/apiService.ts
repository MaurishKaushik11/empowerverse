import { VideoPost, UserPreferences, FilterOptions } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface ApiResponse<T> {
  status: string;
  post: T[];
  algorithm_used: string;
  total_count: number;
  page: number;
  page_size: number;
  confidence_scores?: number[];
}

export interface InteractionRequest {
  username: string;
  post_id: number;
  interaction_type: 'view' | 'like' | 'bookmark' | 'share' | 'rate';
  interaction_value?: number;
}

class ApiService {
  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async getPersonalizedFeed(
    username: string,
    options: {
      project_code?: string;
      page?: number;
      page_size?: number;
      mood?: string;
      category?: string;
    } = {}
  ): Promise<ApiResponse<VideoPost>> {
    const params = new URLSearchParams({
      username,
      page: (options.page || 1).toString(),
      page_size: (options.page_size || 20).toString(),
    });

    if (options.project_code) params.append('project_code', options.project_code);
    if (options.mood) params.append('mood', options.mood);
    if (options.category) params.append('category', options.category);

    return this.makeRequest<ApiResponse<VideoPost>>(`/feed?${params}`);
  }

  async getCategoryFeed(
    username: string,
    project_code: string,
    page: number = 1,
    page_size: number = 20
  ): Promise<ApiResponse<VideoPost>> {
    const params = new URLSearchParams({
      username,
      project_code,
      page: page.toString(),
      page_size: page_size.toString(),
    });

    return this.makeRequest<ApiResponse<VideoPost>>(`/feed/category?${params}`);
  }

  async getTrendingContent(
    page: number = 1,
    page_size: number = 20,
    category?: string
  ): Promise<ApiResponse<VideoPost>> {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: page_size.toString(),
    });

    if (category) params.append('category', category);

    return this.makeRequest<ApiResponse<VideoPost>>(`/trending?${params}`);
  }

  async getSimilarContent(
    post_id: number,
    username?: string,
    page: number = 1,
    page_size: number = 20
  ): Promise<ApiResponse<VideoPost>> {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: page_size.toString(),
    });

    if (username) params.append('username', username);

    return this.makeRequest<ApiResponse<VideoPost>>(`/similar/${post_id}?${params}`);
  }

  async recordInteraction(interaction: InteractionRequest): Promise<{ status: string; message: string }> {
    return this.makeRequest<{ status: string; message: string }>('/interaction', {
      method: 'POST',
      body: JSON.stringify(interaction),
    });
  }

  async getHealthCheck(): Promise<{ status: string; service: string }> {
    return this.makeRequest<{ status: string; service: string }>('/health');
  }
}

export const apiService = new ApiService();
export default apiService;