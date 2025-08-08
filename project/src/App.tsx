import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import VideoGrid from './components/VideoGrid';
import Sidebar from './components/Sidebar';
import { VideoPost, UserPreferences, FilterOptions } from './types';
import { mockPosts, RecommendationService } from './services/recommendationService';

function App() {
  const [posts, setPosts] = useState<VideoPost[]>([]);
  const [filteredPosts, setFilteredPosts] = useState<VideoPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentUser] = useState('demo_user'); // In real app, this would come from auth
  const [userPreferences, setUserPreferences] = useState<UserPreferences>({
    categories: [],
    topics: [],
    mood: 'energetic',
    viewHistory: [],
    likedPosts: [],
    bookmarkedPosts: []
  });
  const [filters, setFilters] = useState<FilterOptions>({
    category: 'all',
    topic: 'all',
    mood: 'all',
    sortBy: 'recommended'
  });

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        let recommendations: VideoPost[];
        
        if (filters.sortBy === 'trending') {
          recommendations = await RecommendationService.getTrendingContent(
            1, 
            20, 
            filters.category !== 'all' ? filters.category : undefined
          );
        } else {
          recommendations = await RecommendationService.getRecommendations(
            currentUser,
            userPreferences,
            filters,
            1,
            20
          );
        }
        
        setPosts(mockPosts);
        setFilteredPosts(recommendations);
      } catch (error) {
        console.error('Failed to load recommendations:', error);
        // Fallback to mock data
        setFilteredPosts(mockPosts);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [userPreferences, filters, currentUser]);

  const handleVideoInteraction = async (postId: number, action: 'view' | 'like' | 'bookmark') => {
    // Record interaction with API
    try {
      await RecommendationService.recordInteraction(currentUser, postId, action);
    } catch (error) {
      console.error('Failed to record interaction:', error);
    }

    // Update local state
    setUserPreferences(prev => ({
      ...prev,
      viewHistory: action === 'view' ? [...prev.viewHistory, postId] : prev.viewHistory,
      likedPosts: action === 'like' ? [...prev.likedPosts, postId] : prev.likedPosts,
      bookmarkedPosts: action === 'bookmark' ? [...prev.bookmarkedPosts, postId] : prev.bookmarkedPosts
    }));
  };

  const updateFilters = (newFilters: Partial<FilterOptions>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header 
        onMenuClick={() => setSidebarOpen(!sidebarOpen)}
        userPreferences={userPreferences}
        onPreferencesUpdate={setUserPreferences}
      />
      
      <div className="flex">
        <Sidebar 
          isOpen={sidebarOpen}
          filters={filters}
          onFiltersChange={updateFilters}
          onClose={() => setSidebarOpen(false)}
        />
        
        <main className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'ml-80' : 'ml-0'}`}>
          <VideoGrid 
            posts={filteredPosts}
            loading={loading}
            onVideoInteraction={handleVideoInteraction}
            userPreferences={userPreferences}
          />
        </main>
      </div>
    </div>
  );
}

export default App;