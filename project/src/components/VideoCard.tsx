import React, { useState } from 'react';
import { Play, Heart, Bookmark, Share2, Eye, Star, User } from 'lucide-react';
import { VideoPost } from '../types';

interface VideoCardProps {
  post: VideoPost;
  onVideoInteraction: (postId: number, action: 'view' | 'like' | 'bookmark') => void;
  isLiked: boolean;
  isBookmarked: boolean;
}

const VideoCard: React.FC<VideoCardProps> = ({ post, onVideoInteraction, isLiked, isBookmarked }) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [showVideo, setShowVideo] = useState(false);

  const handlePlay = () => {
    setShowVideo(true);
    onVideoInteraction(post.id, 'view');
  };

  const handleLike = (e: React.MouseEvent) => {
    e.stopPropagation();
    onVideoInteraction(post.id, 'like');
  };

  const handleBookmark = (e: React.MouseEvent) => {
    e.stopPropagation();
    onVideoInteraction(post.id, 'bookmark');
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const getMoodColor = (mood?: string) => {
    switch (mood) {
      case 'energetic': return 'bg-red-500';
      case 'calm': return 'bg-blue-500';
      case 'inspiring': return 'bg-yellow-500';
      case 'educational': return 'bg-green-500';
      case 'entertainment': return 'bg-purple-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="group bg-gray-800 rounded-xl overflow-hidden hover:scale-105 transition-transform duration-300 shadow-lg hover:shadow-xl">
      <div className="relative aspect-video bg-gray-700">
        {!imageLoaded && (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
          </div>
        )}
        
        <img
          src={post.thumbnail_url}
          alt={post.title}
          onLoad={() => setImageLoaded(true)}
          className={`w-full h-full object-cover transition-opacity duration-300 ${
            imageLoaded ? 'opacity-100' : 'opacity-0'
          }`}
        />
        
        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-300 flex items-center justify-center">
          <button
            onClick={handlePlay}
            className="opacity-0 group-hover:opacity-100 transform scale-50 group-hover:scale-100 transition-all duration-300 bg-white bg-opacity-20 backdrop-blur-sm rounded-full p-4 hover:bg-opacity-30"
          >
            <Play size={24} className="text-white ml-1" fill="white" />
          </button>
        </div>

        {/* Mood indicator */}
        {post.mood && (
          <div className={`absolute top-3 left-3 px-2 py-1 rounded-full text-xs font-medium text-white ${getMoodColor(post.mood)}`}>
            {post.mood}
          </div>
        )}

        {/* Rating */}
        <div className="absolute top-3 right-3 flex items-center space-x-1 bg-black bg-opacity-50 rounded-full px-2 py-1">
          <Star size={12} className="text-yellow-400 fill-current" />
          <span className="text-white text-xs font-medium">{post.average_rating}</span>
        </div>
      </div>

      <div className="p-4">
        <h3 className="font-semibold text-white text-sm mb-2 line-clamp-2 group-hover:text-blue-400 transition-colors">
          {post.title}
        </h3>
        
        <div className="flex items-center space-x-2 mb-3">
          <div className="w-6 h-6 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
            <User size={12} className="text-white" />
          </div>
          <span className="text-gray-400 text-xs">{post.owner.name}</span>
        </div>

        <div className="flex items-center justify-between text-xs text-gray-400 mb-3">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-1">
              <Eye size={12} />
              <span>{formatNumber(post.view_count)}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Heart size={12} />
              <span>{formatNumber(post.upvote_count)}</span>
            </div>
          </div>
          <span className="text-gray-500">{post.category.name}</span>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex space-x-2">
            <button
              onClick={handleLike}
              className={`p-2 rounded-full transition-colors ${
                isLiked 
                  ? 'bg-red-500 text-white' 
                  : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
              }`}
            >
              <Heart size={14} className={isLiked ? 'fill-current' : ''} />
            </button>
            <button
              onClick={handleBookmark}
              className={`p-2 rounded-full transition-colors ${
                isBookmarked 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
              }`}
            >
              <Bookmark size={14} className={isBookmarked ? 'fill-current' : ''} />
            </button>
            <button className="p-2 rounded-full bg-gray-700 text-gray-400 hover:bg-gray-600 transition-colors">
              <Share2 size={14} />
            </button>
          </div>
          
          {post.tags && post.tags.length > 0 && (
            <div className="flex space-x-1">
              {post.tags.slice(0, 2).map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded-full"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VideoCard;