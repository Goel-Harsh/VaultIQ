import React, { useState } from 'react';

interface Props {
    onFilterChange: (filters: any) => void;
}

const FileSearchFilter: React.FC<Props> = ({ onFilterChange }) => {
    const [originalFilename, setOriginalFilename] = useState('');
    const [fileType, setFileType] = useState('');
    const [sizeMin, setSizeMin] = useState('');
    const [sizeMax, setSizeMax] = useState('');
    const [uploadDate, setUploadDate] = useState('');

    const handleFilterChange = () => {
        onFilterChange({
            original_filename: originalFilename,
            file_type: fileType,
            size_min: sizeMin,
            size_max: sizeMax,
            upload_date: uploadDate,
        });
    };

    return (
        <div className="flex flex-col gap-4 p-4">
            <input
                type="text"
                placeholder="Search by filename"
                value={originalFilename}
                onChange={(e) => setOriginalFilename(e.target.value)}
                className="input"
            />
            <select
                value={fileType}
                onChange={(e) => setFileType(e.target.value)}
                className="input"
            >
                <option value="">All File Types</option>
                <option value="application/pdf">PDF</option>
                <option value="image/jpeg">JPEG</option>
                <option value="image/png">PNG</option>
            </select>
            <div className="flex gap-2">
                <input
                    type="number"
                    placeholder="Min Size (Bytes)"
                    value={sizeMin}
                    onChange={(e) => setSizeMin(e.target.value)}
                    className="input"
                />
                <input
                    type="number"
                    placeholder="Max Size (Bytes)"
                    value={sizeMax}
                    onChange={(e) => setSizeMax(e.target.value)}
                    className="input"
                />
            </div>
            <input
                type="date"
                value={uploadDate}
                onChange={(e) => setUploadDate(e.target.value)}
                className="input"
            />
            <button onClick={handleFilterChange} className="btn-primary">
                Apply Filters
            </button>
        </div>
    );
};

export default FileSearchFilter;
