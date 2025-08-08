import React, { useState } from 'react';
import { X, Save } from 'lucide-react';
import { UserPreferences } from '../types';

interface PreferencesModalProps {
  isOpen: boolean;
  onClose: () => void;
  preferences: UserPreferences;
  onUpdate: (prefs: UserPreferences) => void;
}

const categories = [
  'Flic', 'Motivation', 'Education', 'Entertainment', 'Wellness', 'Technology', 'Business', 'Health'
];

const topics = [
  'Social Media', 'Personal Growth', 'Entrepreneurship', 'Fitness', 'Mindfulness', 'Leadership', 'Innovation', 'Success Stories'
];

const moods = [
  { id: 'energetic', name: 'Energetic', emoji: '⚡', desc: 'High-energy, motivational content' },
  { id: 'calm', name: 'Calm', emoji: '🧘', desc: 'Peaceful, relaxing content' },
  { id: 'inspiring', name: 'Inspiring', emoji: '✨', desc: 'Uplifting, inspiring stories' },
  { id: 'educational', name: 'Educational', emoji: '📚', desc: 'Learning-focused content' },
  { id: 'entertainment', name: 'Entertainment', emoji: '🎉', desc: 'Fun, entertaining videos' }
];

const PreferencesModal: React.FC<PreferencesModalProps> = ({ isOpen, onClose, preferences, onUpdate }) => {
  const [localPrefs, setLocalPrefs] = useState(preferences);

  if (!isOpen) return null;

  const handleSave = () => {
    onUpdate(localPrefs);
    onClose();
  };

  const toggleCategory = (category: string) => {
    setLocalPrefs(prev => ({
      ...prev,
      categories: prev.categories.includes(category)
        ? prev.categories.filter(c => c !== category)
        : [...prev.categories, category]
    }));
  };

  const toggleTopic = (topic: string) => {
    setLocalPrefs(prev => ({
      ...prev,
      topics: prev.topics.includes(topic)
        ? prev.topics.filter(t => t !== topic)
        : [...prev.topics, topic]
    }));
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-gray-800 rounded-xl p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Content Preferences</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
          >
            <X size={20} className="text-gray-400" />
          </button>
        </div>

        <div className="space-y-6">
          {/* Mood Selection */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-3">Preferred Mood</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {moods.map((mood) => (
                <button
                  key={mood.id}
                  onClick={() => setLocalPrefs(prev => ({ ...prev, mood: mood.id as any }))}
                  className={`p-4 rounded-lg border-2 transition-colors text-left ${
                    localPrefs.mood === mood.id
                      ? 'border-blue-500 bg-blue-500 bg-opacity-20'
                      : 'border-gray-600 hover:border-gray-500'
                  }`}
                >
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-2xl">{mood.emoji}</span>
                    <span className="font-semibold text-white">{mood.name}</span>
                  </div>
                  <p className="text-sm text-gray-400">{mood.desc}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Category Selection */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-3">Favorite Categories</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => toggleCategory(category)}
                  className={`p-3 rounded-lg transition-colors ${
                    localPrefs.categories.includes(category)
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          {/* Topic Selection */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-3">Interested Topics</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {topics.map((topic) => (
                <button
                  key={topic}
                  onClick={() => toggleTopic(topic)}
                  className={`p-3 rounded-lg transition-colors text-left ${
                    localPrefs.topics.includes(topic)
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  {topic}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="flex justify-end space-x-4 mt-8">
          <button
            onClick={onClose}
            className="px-6 py-2 text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
          >
            <Save size={18} />
            <span>Save Preferences</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default PreferencesModal;