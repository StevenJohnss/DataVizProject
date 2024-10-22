import React from 'react';

interface Image {
  id: number;
  filename: string;
  filepath: string;
  data: string;
}

interface ImageListProps {
  images: Image[];
  onSelect: (image: Image) => void;
}

const ImageList: React.FC<ImageListProps> = ({ images, onSelect }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {images.map((image) => (
        <div
          key={image.id}
          className="bg-white shadow-md rounded-lg overflow-hidden cursor-pointer"
          onClick={() => onSelect(image)}
        >
          <img src={`data:image/jpeg;base64,${image.data}`} alt={image.filename} className="w-full h-48 object-cover" />
          <div className="p-4">
            <p className="text-sm text-gray-600 truncate">{image.filename}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ImageList;
