import React from 'react';
import { VideoPost, UserPreferences } from '../types';
import VideoCard from './VideoCard';
import LoadingGrid from './LoadingGrid';

interface VideoGridProps {
  posts: VideoPost[];
  loading: boolean;
  onVideoInteraction: (postId: number, action: 'view' | 'like' | 'bookmark') => void;
  userPreferences: UserPreferences;
}

const VideoGrid: React.FC<VideoGridProps> = ({ posts, loading, onVideoInteraction, userPreferences }) => {
  if (loading) {
    return <LoadingGrid />;
  }

  if (posts.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-6xl mb-4">🎬</div>
          <h2 className="text-2xl font-semibold text-gray-400 mb-2">No videos found</h2>
          <p className="text-gray-500">Try adjusting your filters or preferences</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">Recommended for You</h2>
        <p className="text-gray-400">Discover motivational content tailored to your interests</p>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-6">
        {posts.map((post) => (
          <VideoCard
            key={post.id}
            post={post}
            onVideoInteraction={onVideoInteraction}
            isLiked={userPreferences.likedPosts.includes(post.id)}
            isBookmarked={userPreferences.bookmarkedPosts.includes(post.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default VideoGrid;