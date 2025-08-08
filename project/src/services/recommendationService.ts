import { VideoPost, UserPreferences, FilterOptions } from '../types';
import { apiService, ApiResponse } from './apiService';

export const mockPosts: VideoPost[] = [
  {
    id: 1,
    owner: {
      first_name: "Sachin",
      last_name: "Kinha",
      name: "Sachin Kinha",
      username: "sachin",
      picture_url: "https://assets.socialverseapp.com/profile/19.png",
      user_type: null,
      has_evm_wallet: false,
      has_solana_wallet: false
    },
    category: {
      id: 13,
      name: "Flic",
      count: 125,
      description: "Where Creativity Meets Opportunity",
      image_url: "https://socialverse-assets.s3.us-east-1.amazonaws.com/categories/NEW_COLOR.png"
    },
    topic: {
      id: 1,
      name: "Social Media",
      description: "Short form content making and editing.",
      image_url: "https://ui-avatars.com/api/?size=300&name=Social%20Media&color=fff&background=random",
      slug: "b9f5413f04ec58e47874",
      is_public: true,
      project_code: "flic",
      posts_count: 18,
      language: null,
      created_at: "2025-02-15 15:02:41",
      owner: {
        first_name: "Shivam",
        last_name: "Flic",
        name: "Shivam Flic",
        username: "random",
        profile_url: "https://assets.socialverseapp.com/profile/random1739306567image_cropper_1739306539349.jpg.png",
        user_type: "hirer"
      }
    },
    title: "Morning Motivation: Start Your Day Strong",
    is_available_in_public_feed: true,
    is_locked: false,
    slug: "0dcff38b97c646a37ebcfa4f039c332812aa3857",
    upvoted: false,
    bookmarked: false,
    following: false,
    identifier: "QCp8ffL",
    comment_count: 15,
    upvote_count: 1240,
    view_count: 15400,
    exit_count: 149,
    rating_count: 87,
    average_rating: 92,
    share_count: 234,
    bookmark_count: 456,
    video_link: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    thumbnail_url: "https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg?auto=compress&cs=tinysrgb&w=800",
    gif_thumbnail_url: "https://video-cdn.socialverseapp.com/sachin_d323e3b5-0012-4e55-85cc-b15dbe47a470.gif",
    contract_address: "",
    chain_id: "",
    chart_url: "",
    baseToken: {
      address: "",
      name: "",
      symbol: "",
      image_url: ""
    },
    created_at: 1739791247000,
    tags: ["motivation", "morning", "productivity"],
    mood: 'energetic'
  },
  {
    id: 2,
    owner: {
      first_name: "Priya",
      last_name: "Sharma",
      name: "Priya Sharma",
      username: "priya_wellness",
      picture_url: "https://assets.socialverseapp.com/profile/25.png",
      user_type: "creator",
      has_evm_wallet: true,
      has_solana_wallet: false
    },
    category: {
      id: 14,
      name: "Wellness",
      count: 89,
      description: "Mind, Body, and Soul",
      image_url: "https://socialverse-assets.s3.us-east-1.amazonaws.com/categories/wellness.png"
    },
    topic: {
      id: 2,
      name: "Mindfulness",
      description: "Meditation and mindful living practices.",
      image_url: "https://ui-avatars.com/api/?size=300&name=Mindfulness&color=fff&background=6366f1",
      slug: "mindfulness-practices",
      is_public: true,
      project_code: "wellness",
      posts_count: 24,
      language: null,
      created_at: "2025-02-10 10:30:15",
      owner: {
        first_name: "Priya",
        last_name: "Sharma",
        name: "Priya Sharma",
        username: "priya_wellness",
        profile_url: "https://assets.socialverseapp.com/profile/25.png",
        user_type: "creator"
      }
    },
    title: "5-Minute Morning Meditation for Inner Peace",
    is_available_in_public_feed: true,
    is_locked: false,
    slug: "morning-meditation-inner-peace",
    upvoted: false,
    bookmarked: false,
    following: false,
    identifier: "MED5min",
    comment_count: 28,
    upvote_count: 892,
    view_count: 12300,
    exit_count: 85,
    rating_count: 156,
    average_rating: 95,
    share_count: 178,
    bookmark_count: 523,
    video_link: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    thumbnail_url: "https://images.pexels.com/photos/3822861/pexels-photo-3822861.jpeg?auto=compress&cs=tinysrgb&w=800",
    gif_thumbnail_url: "",
    contract_address: "",
    chain_id: "",
    chart_url: "",
    baseToken: {
      address: "",
      name: "",
      symbol: "",
      image_url: ""
    },
    created_at: 1739394615000,
    tags: ["meditation", "mindfulness", "peace"],
    mood: 'calm'
  },
  {
    id: 3,
    owner: {
      first_name: "David",
      last_name: "Chen",
      name: "David Chen",
      username: "david_entrepreneur",
      picture_url: "https://assets.socialverseapp.com/profile/42.png",
      user_type: "verified",
      has_evm_wallet: true,
      has_solana_wallet: true
    },
    category: {
      id: 15,
      name: "Business",
      count: 156,
      description: "Entrepreneurship and Leadership",
      image_url: "https://socialverse-assets.s3.us-east-1.amazonaws.com/categories/business.png"
    },
    topic: {
      id: 3,
      name: "Entrepreneurship",
      description: "Building successful businesses and startups.",
      image_url: "https://ui-avatars.com/api/?size=300&name=Entrepreneurship&color=fff&background=16a34a",
      slug: "entrepreneurship-journey",
      is_public: true,
      project_code: "business",
      posts_count: 67,
      language: null,
      created_at: "2025-02-08 14:20:30",
      owner: {
        first_name: "David",
        last_name: "Chen",
        name: "David Chen",
        username: "david_entrepreneur",
        profile_url: "https://assets.socialverseapp.com/profile/42.png",
        user_type: "verified"
      }
    },
    title: "From Idea to $1M: My Startup Journey",
    is_available_in_public_feed: true,
    is_locked: false,
    slug: "startup-journey-1million",
    upvoted: false,
    bookmarked: false,
    following: false,
    identifier: "STARTUP1M",
    comment_count: 156,
    upvote_count: 2340,
    view_count: 28700,
    exit_count: 234,
    rating_count: 298,
    average_rating: 88,
    share_count: 567,
    bookmark_count: 1234,
    video_link: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    thumbnail_url: "https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=800",
    gif_thumbnail_url: "",
    contract_address: "",
    chain_id: "",
    chart_url: "",
    baseToken: {
      address: "",
      name: "",
      symbol: "",
      image_url: ""
    },
    created_at: 1739221230000,
    tags: ["startup", "business", "success"],
    mood: 'inspiring'
  },
  {
    id: 4,
    owner: {
      first_name: "Maya",
      last_name: "Johnson",
      name: "Maya Johnson",
      username: "maya_fitness",
      picture_url: "https://assets.socialverseapp.com/profile/33.png",
      user_type: "trainer",
      has_evm_wallet: false,
      has_solana_wallet: false
    },
    category: {
      id: 16,
      name: "Health",
      count: 203,
      description: "Fitness and Healthy Living",
      image_url: "https://socialverse-assets.s3.us-east-1.amazonaws.com/categories/health.png"
    },
    topic: {
      id: 4,
      name: "Fitness",
      description: "Workout routines and fitness tips.",
      image_url: "https://ui-avatars.com/api/?size=300&name=Fitness&color=fff&background=dc2626",
      slug: "fitness-workouts",
      is_public: true,
      project_code: "health",
      posts_count: 89,
      language: null,
      created_at: "2025-02-12 08:45:20",
      owner: {
        first_name: "Maya",
        last_name: "Johnson",
        name: "Maya Johnson",
        username: "maya_fitness",
        profile_url: "https://assets.socialverseapp.com/profile/33.png",
        user_type: "trainer"
      }
    },
    title: "15-Minute High-Intensity Workout",
    is_available_in_public_feed: true,
    is_locked: false,
    slug: "hiit-15minute-workout",
    upvoted: false,
    bookmarked: false,
    following: false,
    identifier: "HIIT15",
    comment_count: 89,
    upvote_count: 1876,
    view_count: 21400,
    exit_count: 156,
    rating_count: 234,
    average_rating: 91,
    share_count: 345,
    bookmark_count: 789,
    video_link: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    thumbnail_url: "https://images.pexels.com/photos/416778/pexels-photo-416778.jpeg?auto=compress&cs=tinysrgb&w=800",
    gif_thumbnail_url: "",
    contract_address: "",
    chain_id: "",
    chart_url: "",
    baseToken: {
      address: "",
      name: "",
      symbol: "",
      image_url: ""
    },
    created_at: 1739567120000,
    tags: ["fitness", "hiit", "workout"],
    mood: 'energetic'
  },
  {
    id: 5,
    owner: {
      first_name: "Alex",
      last_name: "Rodriguez",
      name: "Alex Rodriguez",
      username: "alex_tech",
      picture_url: "https://assets.socialverseapp.com/profile/67.png",
      user_type: "expert",
      has_evm_wallet: true,
      has_solana_wallet: false
    },
    category: {
      id: 17,
      name: "Technology",
      count: 178,
      description: "Latest in Tech and Innovation",
      image_url: "https://socialverse-assets.s3.us-east-1.amazonaws.com/categories/tech.png"
    },
    topic: {
      id: 5,
      name: "Innovation",
      description: "Cutting-edge technology and innovations.",
      image_url: "https://ui-avatars.com/api/?size=300&name=Innovation&color=fff&background=7c3aed",
      slug: "tech-innovation",
      is_public: true,
      project_code: "technology",
      posts_count: 134,
      language: null,
      created_at: "2025-02-09 16:30:45",
      owner: {
        first_name: "Alex",
        last_name: "Rodriguez",
        name: "Alex Rodriguez",
        username: "alex_tech",
        profile_url: "https://assets.socialverseapp.com/profile/67.png",
        user_type: "expert"
      }
    },
    title: "AI Revolution: What's Coming Next?",
    is_available_in_public_feed: true,
    is_locked: false,
    slug: "ai-revolution-future",
    upvoted: false,
    bookmarked: false,
    following: false,
    identifier: "AIREV2025",
    comment_count: 267,
    upvote_count: 3421,
    view_count: 45600,
    exit_count: 289,
    rating_count: 456,
    average_rating: 93,
    share_count: 789,
    bookmark_count: 1567,
    video_link: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    thumbnail_url: "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&w=800",
    gif_thumbnail_url: "",
    contract_address: "",
    chain_id: "",
    chart_url: "",
    baseToken: {
      address: "",
      name: "",
      symbol: "",
      image_url: ""
    },
    created_at: 1739307045000,
    tags: ["ai", "technology", "future"],
    mood: 'educational'
  }
];

// Generate more mock posts
const generateMoreMockPosts = (): VideoPost[] => {
  const additionalPosts: VideoPost[] = [];
  const titles = [
    "Building Resilience in Tough Times",
    "The Power of Positive Thinking",
    "Mastering Time Management",
    "Creative Problem Solving",
    "Leadership in the Digital Age",
    "Sustainable Living Tips",
    "Financial Freedom Journey",
    "Art of Public Speaking",
    "Healthy Meal Prep Ideas",
    "Photography Basics for Beginners"
  ];

  const thumbnails = [
    "https://images.pexels.com/photos/1629236/pexels-photo-1629236.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1181675/pexels-photo-1181675.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1181677/pexels-photo-1181677.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1181719/pexels-photo-1181719.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/3184405/pexels-photo-3184405.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/3182743/pexels-photo-3182743.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1264210/pexels-photo-1264210.jpeg?auto=compress&cs=tinysrgb&w=800"
  ];

  const moods: Array<'energetic' | 'calm' | 'inspiring' | 'educational' | 'entertainment'> = 
    ['energetic', 'calm', 'inspiring', 'educational', 'entertainment'];

  for (let i = 6; i <= 25; i++) {
    additionalPosts.push({
      ...mockPosts[0],
      id: i,
      title: titles[(i - 6) % titles.length],
      thumbnail_url: thumbnails[(i - 6) % thumbnails.length],
      mood: moods[(i - 6) % moods.length],
      view_count: Math.floor(Math.random() * 50000) + 1000,
      upvote_count: Math.floor(Math.random() * 5000) + 100,
      average_rating: Math.floor(Math.random() * 20) + 80,
      comment_count: Math.floor(Math.random() * 300) + 10,
      created_at: Date.now() - Math.floor(Math.random() * 10000000000)
    });
  }

  return additionalPosts;
};

export const allMockPosts = [...mockPosts, ...generateMoreMockPosts()];

// Recommendation Engine Implementation
export class RecommendationEngine {
  static calculateUserSimilarity(user1: UserPreferences, user2: UserPreferences): number {
    let similarity = 0;
    let factors = 0;

    // Category similarity
    const categoryIntersection = user1.categories.filter(c => user2.categories.includes(c));
    const categoryUnion = [...new Set([...user1.categories, ...user2.categories])];
    if (categoryUnion.length > 0) {
      similarity += categoryIntersection.length / categoryUnion.length;
      factors++;
    }

    // Topic similarity
    const topicIntersection = user1.topics.filter(t => user2.topics.includes(t));
    const topicUnion = [...new Set([...user1.topics, ...user2.topics])];
    if (topicUnion.length > 0) {
      similarity += topicIntersection.length / topicUnion.length;
      factors++;
    }

    // Mood similarity
    if (user1.mood === user2.mood) {
      similarity += 1;
    }
    factors++;

    return factors > 0 ? similarity / factors : 0;
  }

  static getContentBasedRecommendations(userPrefs: UserPreferences, posts: VideoPost[]): VideoPost[] {
    return posts
      .map(post => ({
        post,
        score: this.calculateContentScore(post, userPrefs)
      }))
      .sort((a, b) => b.score - a.score)
      .map(item => item.post);
  }

  static calculateContentScore(post: VideoPost, userPrefs: UserPreferences): number {
    let score = 0;

    // Category preference
    if (userPrefs.categories.includes(post.category.name)) {
      score += 3;
    }

    // Topic preference
    if (userPrefs.topics.includes(post.topic.name)) {
      score += 3;
    }

    // Mood preference
    if (post.mood === userPrefs.mood) {
      score += 2;
    }

    // Engagement metrics
    score += Math.log(post.view_count + 1) / 10;
    score += Math.log(post.upvote_count + 1) / 5;
    score += post.average_rating / 25;

    // Recency boost
    const daysSinceCreation = (Date.now() - post.created_at) / (1000 * 60 * 60 * 24);
    if (daysSinceCreation < 7) {
      score += 1;
    }

    return score;
  }

  static getMoodBasedRecommendations(mood: string, posts: VideoPost[]): VideoPost[] {
    if (mood === 'all') return posts;
    
    return posts.filter(post => post.mood === mood);
  }
}

// Enhanced recommendation service with API integration
export class RecommendationService {
  private static fallbackToMock = true; // Toggle for development

  static async getRecommendations(
    username: string,
    userPrefs: UserPreferences, 
    filters: FilterOptions,
    page: number = 1,
    pageSize: number = 20
  ): Promise<VideoPost[]> {
    try {
      // Try to get recommendations from API first
      if (!this.fallbackToMock) {
        const response = await apiService.getPersonalizedFeed(username, {
          page,
          page_size: pageSize,
          mood: filters.mood !== 'all' ? filters.mood : undefined,
          category: filters.category !== 'all' ? filters.category : undefined,
        });
        
        if (response.status === 'success' && response.post.length > 0) {
          return response.post;
        }
      }
    } catch (error) {
      console.warn('API call failed, falling back to mock data:', error);
    }

    // Fallback to mock data with filtering
    return this.getMockRecommendations(userPrefs, filters);
  }

  static async getTrendingContent(
    page: number = 1,
    pageSize: number = 20,
    category?: string
  ): Promise<VideoPost[]> {
    try {
      if (!this.fallbackToMock) {
        const response = await apiService.getTrendingContent(page, pageSize, category);
        if (response.status === 'success' && response.post.length > 0) {
          return response.post;
        }
      }
    } catch (error) {
      console.warn('Trending API call failed, falling back to mock data:', error);
    }

    // Fallback to mock trending
    return this.getMockTrending(category);
  }

  static async recordInteraction(
    username: string,
    postId: number,
    interactionType: 'view' | 'like' | 'bookmark' | 'share' | 'rate',
    interactionValue?: number
  ): Promise<boolean> {
    try {
      if (!this.fallbackToMock) {
        const response = await apiService.recordInteraction({
          username,
          post_id: postId,
          interaction_type: interactionType,
          interaction_value: interactionValue,
        });
        return response.status === 'success';
      }
    } catch (error) {
      console.warn('Interaction recording failed:', error);
    }
    
    // Mock success for development
    console.log(`Mock interaction recorded: ${username} ${interactionType} post ${postId}`);
    return true;
  }

  private static getMockRecommendations(userPrefs: UserPreferences, filters: FilterOptions): VideoPost[] {
    let filteredPosts = [...allMockPosts];

    // Apply category filter
    if (filters.category !== 'all') {
      filteredPosts = filteredPosts.filter(post => 
        post.category.name.toLowerCase() === filters.category.toLowerCase()
      );
    }

    // Apply mood filter
    if (filters.mood !== 'all') {
      filteredPosts = RecommendationEngine.getMoodBasedRecommendations(filters.mood, filteredPosts);
    }

    // Apply sorting
    switch (filters.sortBy) {
      case 'recommended':
        filteredPosts = RecommendationEngine.getContentBasedRecommendations(userPrefs, filteredPosts);
        break;
      case 'trending':
        filteredPosts = filteredPosts.sort((a, b) => {
          const trendingScoreA = (a.view_count * 0.3) + (a.upvote_count * 0.4) + (a.share_count * 0.3);
          const trendingScoreB = (b.view_count * 0.3) + (b.upvote_count * 0.4) + (b.share_count * 0.3);
          return trendingScoreB - trendingScoreA;
        });
        break;
      case 'recent':
        filteredPosts = filteredPosts.sort((a, b) => b.created_at - a.created_at);
        break;
      case 'popular':
        filteredPosts = filteredPosts.sort((a, b) => b.view_count - a.view_count);
        break;
    }

    return filteredPosts;
  }

  private static getMockTrending(category?: string): VideoPost[] {
    let posts = [...allMockPosts];
    
    if (category && category !== 'all') {
      posts = posts.filter(post => 
        post.category.name.toLowerCase() === category.toLowerCase()
      );
    }

    return posts.sort((a, b) => {
      const trendingScoreA = (a.view_count * 0.3) + (a.upvote_count * 0.4) + (a.share_count * 0.3);
      const trendingScoreB = (b.view_count * 0.3) + (b.upvote_count * 0.4) + (b.share_count * 0.3);
      return trendingScoreB - trendingScoreA;
    });
  }
}

// Legacy function for backward compatibility
export const getRecommendations = (userPrefs: UserPreferences, filters: FilterOptions): VideoPost[] => {
  return RecommendationService.getMockRecommendations(userPrefs, filters);
};

// Cold start problem handler
export const getColdStartRecommendations = (mood: string): VideoPost[] => {
  const moodBasedPosts = RecommendationEngine.getMoodBasedRecommendations(mood, allMockPosts);
  
  // If no mood-specific posts, return trending posts
  if (moodBasedPosts.length === 0) {
    return allMockPosts.sort((a, b) => {
      const trendingScoreA = (a.view_count * 0.3) + (a.upvote_count * 0.4) + (a.share_count * 0.3);
      const trendingScoreB = (b.view_count * 0.3) + (b.upvote_count * 0.4) + (b.share_count * 0.3);
      return trendingScoreB - trendingScoreA;
    }).slice(0, 12);
  }

  return moodBasedPosts.slice(0, 12);
};