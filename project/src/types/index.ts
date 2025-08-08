export interface VideoPost {
  id: number;
  owner: {
    first_name: string;
    last_name: string;
    name: string;
    username: string;
    picture_url: string;
    user_type: string | null;
    has_evm_wallet: boolean;
    has_solana_wallet: boolean;
  };
  category: {
    id: number;
    name: string;
    count: number;
    description: string;
    image_url: string;
  };
  topic: {
    id: number;
    name: string;
    description: string;
    image_url: string;
    slug: string;
    is_public: boolean;
    project_code: string;
    posts_count: number;
    language: string | null;
    created_at: string;
    owner: {
      first_name: string;
      last_name: string;
      name: string;
      username: string;
      profile_url: string;
      user_type: string;
    };
  };
  title: string;
  is_available_in_public_feed: boolean;
  is_locked: boolean;
  slug: string;
  upvoted: boolean;
  bookmarked: boolean;
  following: boolean;
  identifier: string;
  comment_count: number;
  upvote_count: number;
  view_count: number;
  exit_count: number;
  rating_count: number;
  average_rating: number;
  share_count: number;
  bookmark_count: number;
  video_link: string;
  thumbnail_url: string;
  gif_thumbnail_url: string;
  contract_address: string;
  chain_id: string;
  chart_url: string;
  baseToken: {
    address: string;
    name: string;
    symbol: string;
    image_url: string;
  };
  created_at: number;
  tags: string[];
  mood?: 'energetic' | 'calm' | 'inspiring' | 'educational' | 'entertainment';
}

export interface UserPreferences {
  categories: string[];
  topics: string[];
  mood: 'energetic' | 'calm' | 'inspiring' | 'educational' | 'entertainment';
  viewHistory: number[];
  likedPosts: number[];
  bookmarkedPosts: number[];
}

export interface FilterOptions {
  category: string;
  topic: string;
  mood: string;
  sortBy: 'recommended' | 'trending' | 'recent' | 'popular';
}

export interface RecommendationEngine {
  calculateUserSimilarity(user1: UserPreferences, user2: UserPreferences): number;
  getContentBasedRecommendations(userPrefs: UserPreferences, posts: VideoPost[]): VideoPost[];
  getCollaborativeRecommendations(userPrefs: UserPreferences, posts: VideoPost[]): VideoPost[];
  getMoodBasedRecommendations(mood: string, posts: VideoPost[]): VideoPost[];
}