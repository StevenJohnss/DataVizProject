import React, { useState } from 'react';
import api from '../api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface Image {
  id: number;
  filename: string;
  data: string;
}

interface ImageManipulatorProps {
  image: Image;
}

const ImageManipulator: React.FC<ImageManipulatorProps> = ({ image }) => {
  const [histogram, setHistogram] = useState<any>(null);
  const [segmentationMask, setSegmentationMask] = useState<string | null>(null);
  const [manipulatedImage, setManipulatedImage] = useState<string | null>(null);

  const getHistogram = async () => {
    try {
      const response = await api.get(`/images/histogram/${image.id}`);
      setHistogram(response.data.histogram);
    } catch (error) {
      console.error('Error getting histogram:', error);
    }
  };

  const segmentImage = async () => {
    try {
      const response = await api.get(`/images/segment/${image.id}`);
      setSegmentationMask(response.data.mask);
    } catch (error) {
      console.error('Error segmenting image:', error);
    }
  };

  const manipulateImage = async () => {
    try {
      const response = await api.post(`/images/manipulate/${image.id}`, {
        // Add manipulation parameters here
        resize: [300, 300],
        crop: [0, 0, 200, 200]
      });
      setManipulatedImage(response.data.filename);
    } catch (error) {
      console.error('Error manipulating image:', error);
    }
  };

  // Function to prepare the histogram data for the chart
  const prepareHistogramData = (histogram: any) => {
    const data = [];
    const bins = histogram.r.length; // Assuming all channels have the same number of bins
    for (let i = 0; i < bins; i++) {
      data.push({
        bin: i,
        Red: histogram.r[i],
        Green: histogram.g[i],
        Blue: histogram.b[i]
      });
    }
    return data;
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mt-5 flex flex-col items-center">
      <h2 className="text-xl font-bold mb-4">Image Manipulation</h2>
      <img src={`data:image/jpeg;base64,${image.data}`} alt={image.filename} className="w-auto h-[500px] object-cover" />
      <div className="space-y-4">
        <button
          onClick={getHistogram}
          className="w-full sm:w-auto mt-6 sm:mx-4  bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Get Histogram
        </button>
        <button
          onClick={segmentImage}
          className="w-full sm:w-auto my-6 sm:mx-4  bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
        >
          Segment Image
        </button>
        <button
          onClick={manipulateImage}
          className="w-full sm:w-auto my-6 sm:mx-4  bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
        >
          Manipulate Image
        </button>
      </div>

      <div className="flex flex-col md:flex-row justify-between w-full md:space-x-4">
        {histogram && (
          <div className="mt-4 flex-1">
            <h3 className="text-lg font-semibold mb-2">Histogram</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={prepareHistogramData(histogram)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="bin" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="Red" fill="#FF0000" />
                <Bar dataKey="Green" fill="#00FF00" />
                <Bar dataKey="Blue" fill="#0000FF" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
        {segmentationMask && (
          <div className="mt-4 flex-1">
            <h3 className="text-lg font-semibold mb-2">Segmentation Mask</h3>
            <img
              src={`data:image/jpeg;base64,${segmentationMask}`}
              alt="Segmentation Mask"
              className="w-full h-auto object-cover"
            />
          </div>
        )}
        {manipulatedImage && (
          <div className="mt-4 flex-1">
            <h3 className="text-lg font-semibold mb-2">Manipulated Image (crop/resize)</h3>
            <img
              src={`data:image/jpeg;base64,${manipulatedImage}`}
              alt="Manipulated Image"
              className="w-full h-auto object-cover"
            />
          </div>
        )}
      </div>

    </div>
  );
};

export default ImageManipulator;
