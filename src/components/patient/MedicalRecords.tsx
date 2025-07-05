import React, { useState } from 'react';
import { FileText, Upload, Download, Eye, Trash2, Calendar } from 'lucide-react';
import { toast } from '../ui/toast';

const mockRecords = [
  {
    id: '1',
    name: 'Blood Test Report',
    type: 'PDF',
    date: '2024-01-15',
    size: '2.4 MB',
    uploadedBy: 'Dr. Sarah Wilson'
  },
  {
    id: '2',
    name: 'X-Ray Chest',
    type: 'JPG',
    date: '2024-01-10',
    size: '1.8 MB',
    uploadedBy: 'Dr. Michael Chen'
  },
  {
    id: '3',
    name: 'Prescription',
    type: 'PDF',
    date: '2024-01-08',
    size: '456 KB',
    uploadedBy: 'Dr. Emily Rodriguez'
  }
];

export default function MedicalRecords() {
  const [records, setRecords] = useState(mockRecords);
  const [dragActive, setDragActive] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);

  const handleFileUpload = (files: FileList | null) => {
    if (!files || files.length === 0) return;

    const file = files[0];
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
    
    if (!allowedTypes.includes(file.type)) {
      toast.error('Please upload only PDF, JPG, or PNG files');
      return;
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      toast.error('File size must be less than 10MB');
      return;
    }

    const newRecord = {
      id: Date.now().toString(),
      name: file.name,
      type: file.type.includes('pdf') ? 'PDF' : 'JPG',
      date: new Date().toISOString().split('T')[0],
      size: `${(file.size / 1024 / 1024).toFixed(1)} MB`,
      uploadedBy: 'Self'
    };

    setRecords([newRecord, ...records]);
    setShowUploadModal(false);
    toast.success('Medical record uploaded successfully!');
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    handleFileUpload(e.dataTransfer.files);
  };

  const handleDelete = (id: string) => {
    setRecords(records.filter(record => record.id !== id));
    toast.success('Record deleted successfully');
  };

  return (
    <div className="p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Medical Records</h1>
            <p className="text-gray-600">Upload and manage your medical documents</p>
          </div>
          <button
            onClick={() => setShowUploadModal(true)}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center"
          >
            <Upload className="w-5 h-5 mr-2" />
            Upload Record
          </button>
        </div>

        {/* Upload Modal */}
        {showUploadModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Upload Medical Record</h2>
              
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center ${
                  dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 mb-4">
                  Drag and drop your file here, or click to select
                </p>
                <input
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  onChange={(e) => handleFileUpload(e.target.files)}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors cursor-pointer"
                >
                  Select File
                </label>
                <p className="text-sm text-gray-500 mt-2">
                  Supported formats: PDF, JPG, PNG (Max 10MB)
                </p>
              </div>

              <div className="flex space-x-4 mt-6">
                <button
                  onClick={() => setShowUploadModal(false)}
                  className="flex-1 bg-gray-200 text-gray-800 py-3 rounded-lg hover:bg-gray-300 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Records List */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="p-6 border-b">
            <h2 className="text-lg font-semibold text-gray-900">Your Records ({records.length})</h2>
          </div>
          
          {records.length === 0 ? (
            <div className="p-12 text-center">
              <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No medical records uploaded yet</p>
              <button
                onClick={() => setShowUploadModal(true)}
                className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Upload Your First Record
              </button>
            </div>
          ) : (
            <div className="divide-y">
              {records.map((record) => (
                <div key={record.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                        <FileText className="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{record.name}</h3>
                        <div className="flex items-center text-sm text-gray-600 mt-1">
                          <span className="bg-gray-100 px-2 py-1 rounded text-xs mr-2">
                            {record.type}
                          </span>
                          <Calendar className="w-4 h-4 mr-1" />
                          <span>{record.date}</span>
                          <span className="mx-2">•</span>
                          <span>{record.size}</span>
                          <span className="mx-2">•</span>
                          <span>By {record.uploadedBy}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => toast.info('Preview functionality would open here')}
                        className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="Preview"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => toast.info('Download would start here')}
                        className="p-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                        title="Download"
                      >
                        <Download className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(record.id)}
                        className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}