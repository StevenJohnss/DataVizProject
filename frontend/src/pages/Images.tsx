import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../api';
import ImageUploader from '../components/ImageUploader';
import ImageList from '../components/ImageList';
import ImageManipulator from '../components/ImageManipulator';

interface Image {
  id: number;
  filename: string;
  filepath: string;
  data: string;
}

const Images: React.FC = () => {
  const [images, setImages] = useState<Image[]>([]);
  const [selectedImage, setSelectedImage] = useState<Image | null>(null);

  useEffect(() => {
    fetchImages();
  }, []);

  const fetchImages = async () => {
    try {
      const response = await api.get('/images');
      setImages(response.data);
    } catch (error) {
      console.error('Error fetching images:', error);
    }
  };

  const handleImageUpload = async (uploadedImages: any[]) => {
    setImages([...images, ...uploadedImages]);
  };

  const handleImageSelect = (image: Image) => {
    setSelectedImage(image);
  };

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="px-4 py-6 sm:px-0"
      >
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Images</h1>
        <ImageUploader onUpload={handleImageUpload} />
        <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2">
          <ImageList images={images} onSelect={handleImageSelect} />

        </div>
        {selectedImage && (
          <ImageManipulator image={selectedImage} />
        )}
      </motion.div>
    </div>
  );
};

export default Images;
