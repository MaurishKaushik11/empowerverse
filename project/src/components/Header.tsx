import React, { useState } from 'react';
import { Search, Menu, User, Settings, Bell } from 'lucide-react';
import { UserPreferences } from '../types';
import PreferencesModal from './PreferencesModal';

interface HeaderProps {
  onMenuClick: () => void;
  userPreferences: UserPreferences;
  onPreferencesUpdate: (prefs: UserPreferences) => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick, userPreferences, onPreferencesUpdate }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [showPreferences, setShowPreferences] = useState(false);

  return (
    <>
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={onMenuClick}
              className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
            >
              <Menu size={24} />
            </button>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              EmpowerVerse
            </h1>
          </div>

          <div className="flex-1 max-w-2xl mx-8">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search for motivational content..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
              />
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors relative">
              <Bell size={20} />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            <button
              onClick={() => setShowPreferences(true)}
              className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
            >
              <Settings size={20} />
            </button>
            <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors">
              <User size={20} />
            </button>
          </div>
        </div>
      </header>

      <PreferencesModal
        isOpen={showPreferences}
        onClose={() => setShowPreferences(false)}
        preferences={userPreferences}
        onUpdate={onPreferencesUpdate}
      />
    </>
  );
};

export default Header;