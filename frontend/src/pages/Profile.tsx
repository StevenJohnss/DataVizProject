import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../api';
import { toast } from 'react-toastify';

interface ProfileData {
  email: string;
  summary: string;
}

interface AnalysisResult {
  summary: string;
  keywords: string[];
  sentiment: {
    polarity: number;
    subjectivity: number;
  };
}

interface Visualization {
  x: number;
  y: number;
}

const Profile: React.FC = () => {
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [visualization, setVisualization] = useState<Visualization | null>(null);
  const [newSummary, setNewSummary] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await api.get<ProfileData>('/text/profile');
      setProfile(response.data);
      setNewSummary(response.data.summary);
    } catch (error) {
      console.error('Error fetching profile:', error);
      setError('Failed to load profile data');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    try {
      const response = await api.post<AnalysisResult>('/text/analyze', { summary: newSummary });
      setAnalysis(response.data);
      toast.success('Text analyzed successfully');
    } catch (error) {
      console.error('Error analyzing text:', error);
      setError('Failed to analyze text');
      toast.error('Failed to analyze text');
    }
  };

  const handleUpdateSummary = async () => {
    try {
      await api.put('/text/profile/update', { summary: newSummary });
      fetchProfile();
      toast.success('Profile updated successfully');
    } catch (error) {
      console.error('Error updating profile:', error);
      setError('Failed to update profile');
      toast.error('Failed to update profile');
    }
  };

  const handleVisualize = async () => {
    try {
      const response = await api.post<Visualization>('/text/visualize', { summary: newSummary });
      setVisualization(response.data);
      toast.success('Text visualized successfully');
    } catch (error) {
      console.error('Error visualizing text:', error);
      setError('Failed to visualize text');
      toast.error('Failed to visualize text');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="px-4 py-6 sm:px-0"
      >
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Profile</h1>
        {profile && (
          <div>
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">User Information</h3>
                <p>Email: {profile.email}</p>
                <textarea
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  value={newSummary}
                  onChange={(e) => setNewSummary(e.target.value)}
                />
                <div className="mt-4 space-x-2">
                  <button onClick={handleUpdateSummary} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Update Summary
                  </button>
                  <button onClick={handleAnalyze} className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
                    Analyze Text
                  </button>
                  <button onClick={handleVisualize} className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">
                    Visualize Text
                  </button>
                </div>
              </div>
            </div>
            {analysis && (
              <div className="mt-4">
                <h4>Analysis Result:</h4>
                <p>Summary: {analysis.summary}</p>
                <p>Keywords: {analysis.keywords}</p>
                <p>Sentiment - Polarity: {analysis.sentiment.polarity}, Subjectivity: {analysis.sentiment.subjectivity}</p>
              </div>
            )}
            {visualization && (
              <div className="mt-4">
                <h4>Text Visualization (t-SNE):</h4>
                <div className="w-64 h-64 border border-gray-300 relative">
                  <div
                    className="absolute w-2 h-2 bg-red-500 rounded-full"
                    style={{
                      left: `${(visualization.x + 1) * 32}px`,
                      top: `${(visualization.y + 1) * 32}px`,
                    }}
                  ></div>
                </div>
                <p className="mt-2">
                  X: {visualization.x.toFixed(4)}, Y: {visualization.y.toFixed(4)}
                </p>
            </div>
            )}
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default Profile;
