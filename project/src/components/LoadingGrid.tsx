import React from 'react';

const LoadingGrid: React.FC = () => {
  return (
    <div className="p-6">
      <div className="mb-6">
        <div className="h-8 bg-gray-700 rounded-lg w-64 mb-2 animate-pulse"></div>
        <div className="h-4 bg-gray-800 rounded w-96 animate-pulse"></div>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-6">
        {Array.from({ length: 15 }).map((_, index) => (
          <div key={index} className="bg-gray-800 rounded-xl overflow-hidden animate-pulse">
            <div className="aspect-video bg-gray-700"></div>
            <div className="p-4">
              <div className="h-4 bg-gray-700 rounded mb-2"></div>
              <div className="h-3 bg-gray-700 rounded w-2/3 mb-3"></div>
              <div className="flex items-center space-x-2 mb-3">
                <div className="w-6 h-6 bg-gray-700 rounded-full"></div>
                <div className="h-3 bg-gray-700 rounded w-20"></div>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex space-x-2">
                  <div className="w-8 h-8 bg-gray-700 rounded-full"></div>
                  <div className="w-8 h-8 bg-gray-700 rounded-full"></div>
                  <div className="w-8 h-8 bg-gray-700 rounded-full"></div>
                </div>
                <div className="flex space-x-1">
                  <div className="h-6 bg-gray-700 rounded-full w-12"></div>
                  <div className="h-6 bg-gray-700 rounded-full w-12"></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LoadingGrid;