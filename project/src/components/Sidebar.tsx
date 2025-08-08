import React from 'react';
import { X, Filter, TrendingUp, Clock, Star, Zap, Heart, BookOpen, Smile, Brain } from 'lucide-react';
import { FilterOptions } from '../types';

interface SidebarProps {
  isOpen: boolean;
  filters: FilterOptions;
  onFiltersChange: (filters: Partial<FilterOptions>) => void;
  onClose: () => void;
}

const categories = [
  { id: 'all', name: 'All Categories', icon: Filter },
  { id: 'flic', name: 'Flic', icon: Zap },
  { id: 'motivation', name: 'Motivation', icon: Heart },
  { id: 'education', name: 'Education', icon: BookOpen },
  { id: 'entertainment', name: 'Entertainment', icon: Smile },
  { id: 'wellness', name: 'Wellness', icon: Brain }
];

const moods = [
  { id: 'all', name: 'All Moods', emoji: '🌈' },
  { id: 'energetic', name: 'Energetic', emoji: '⚡' },
  { id: 'calm', name: 'Calm', emoji: '🧘' },
  { id: 'inspiring', name: 'Inspiring', emoji: '✨' },
  { id: 'educational', name: 'Educational', emoji: '📚' },
  { id: 'entertainment', name: 'Fun', emoji: '🎉' }
];

const sortOptions = [
  { id: 'recommended', name: 'Recommended', icon: Star },
  { id: 'trending', name: 'Trending', icon: TrendingUp },
  { id: 'recent', name: 'Recent', icon: Clock },
  { id: 'popular', name: 'Popular', icon: Heart }
];

const Sidebar: React.FC<SidebarProps> = ({ isOpen, filters, onFiltersChange, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 lg:relative lg:inset-auto">
      <div className="absolute inset-0 bg-black bg-opacity-50 lg:hidden" onClick={onClose}></div>
      
      <div className="absolute left-0 top-0 h-full w-80 bg-gray-800 border-r border-gray-700 transform transition-transform lg:relative lg:transform-none">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold">Filters</h2>
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-700 rounded lg:hidden"
            >
              <X size={20} />
            </button>
          </div>

          <div className="space-y-6">
            {/* Sort By */}
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-3 uppercase tracking-wide">Sort By</h3>
              <div className="space-y-2">
                {sortOptions.map((option) => {
                  const Icon = option.icon;
                  return (
                    <button
                      key={option.id}
                      onClick={() => onFiltersChange({ sortBy: option.id as any })}
                      className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-colors ${
                        filters.sortBy === option.id
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                      }`}
                    >
                      <Icon size={18} />
                      <span>{option.name}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Categories */}
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-3 uppercase tracking-wide">Categories</h3>
              <div className="space-y-2">
                {categories.map((category) => {
                  const Icon = category.icon;
                  return (
                    <button
                      key={category.id}
                      onClick={() => onFiltersChange({ category: category.id })}
                      className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-colors ${
                        filters.category === category.id
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                      }`}
                    >
                      <Icon size={18} />
                      <span>{category.name}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Mood */}
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-3 uppercase tracking-wide">Mood</h3>
              <div className="space-y-2">
                {moods.map((mood) => (
                  <button
                    key={mood.id}
                    onClick={() => onFiltersChange({ mood: mood.id })}
                    className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-colors ${
                      filters.mood === mood.id
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                    }`}
                  >
                    <span className="text-lg">{mood.emoji}</span>
                    <span>{mood.name}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;