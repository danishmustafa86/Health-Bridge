import React, { useState } from 'react';
import { FileText, Download, Eye, Calendar, User, Filter } from 'lucide-react';

const mockRecords = [
  {
    id: '1',
    patientName: 'John Doe',
    patientId: '1',
    fileName: 'Blood Test Report',
    type: 'PDF',
    uploadDate: '2024-01-15',
    size: '2.4 MB',
    category: 'Lab Results',
    status: 'Reviewed'
  },
  {
    id: '2',
    patientName: 'Jane Smith',
    patientId: '2',
    fileName: 'MRI Scan',
    type: 'JPG',
    uploadDate: '2024-01-18',
    size: '5.2 MB',
    category: 'Imaging',
    status: 'Pending'
  },
  {
    id: '3',
    patientName: 'Bob Johnson',
    patientId: '3',
    fileName: 'ECG Report',
    type: 'PDF',
    uploadDate: '2024-01-10',
    size: '1.1 MB',
    category: 'Cardiology',
    status: 'Reviewed'
  },
  {
    id: '4',
    patientName: 'Alice Brown',
    patientId: '4',
    fileName: 'X-Ray Chest',
    type: 'JPG',
    uploadDate: '2024-01-12',
    size: '3.8 MB',
    category: 'Imaging',
    status: 'Pending'
  }
];

export default function PatientRecords() {
  const [records, setRecords] = useState(mockRecords);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [selectedRecord, setSelectedRecord] = useState<any>(null);

  const filteredRecords = records.filter(record => {
    if (selectedFilter === 'all') return true;
    if (selectedFilter === 'pending') return record.status === 'Pending';
    if (selectedFilter === 'reviewed') return record.status === 'Reviewed';
    return record.category.toLowerCase() === selectedFilter.toLowerCase();
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Reviewed':
        return 'bg-green-100 text-green-800';
      case 'Pending':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'Lab Results':
        return 'bg-blue-100 text-blue-800';
      case 'Imaging':
        return 'bg-purple-100 text-purple-800';
      case 'Cardiology':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const handleStatusChange = (recordId: string, newStatus: string) => {
    setRecords(records.map(record => 
      record.id === recordId 
        ? { ...record, status: newStatus }
        : record
    ));
  };

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Patient Records</h1>
            <p className="text-gray-600">Review and manage medical records from your patients</p>
          </div>
          <div className="text-sm text-gray-600">
            Total Records: <span className="font-semibold">{records.length}</span>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6">
          <div className="flex items-center space-x-4">
            <Filter className="w-5 h-5 text-gray-500" />
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setSelectedFilter('all')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedFilter === 'all'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                All Records
              </button>
              <button
                onClick={() => setSelectedFilter('pending')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedFilter === 'pending'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Pending Review
              </button>
              <button
                onClick={() => setSelectedFilter('reviewed')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedFilter === 'reviewed'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Reviewed
              </button>
              <button
                onClick={() => setSelectedFilter('lab results')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedFilter === 'lab results'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Lab Results
              </button>
              <button
                onClick={() => setSelectedFilter('imaging')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedFilter === 'imaging'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Imaging
              </button>
            </div>
          </div>
        </div>

        {/* Records List */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="p-6 border-b">
            <h2 className="text-lg font-semibold text-gray-900">
              Records ({filteredRecords.length})
            </h2>
          </div>
          
          <div className="divide-y">
            {filteredRecords.map((record) => (
              <div key={record.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                      <FileText className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">{record.fileName}</h3>
                      <div className="flex items-center text-sm text-gray-600 space-x-4">
                        <div className="flex items-center">
                          <User className="w-4 h-4 mr-1" />
                          <span>{record.patientName}</span>
                        </div>
                        <div className="flex items-center">
                          <Calendar className="w-4 h-4 mr-1" />
                          <span>{record.uploadDate}</span>
                        </div>
                        <span className="bg-gray-100 px-2 py-1 rounded text-xs">
                          {record.type}
                        </span>
                        <span className="text-xs">{record.size}</span>
                      </div>
                      <div className="flex items-center mt-2 space-x-2">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getCategoryColor(record.category)}`}>
                          {record.category}
                        </span>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(record.status)}`}>
                          {record.status}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setSelectedRecord(record)}
                      className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                      title="View Details"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      className="p-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                      title="Download"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                    {record.status === 'Pending' && (
                      <button
                        onClick={() => handleStatusChange(record.id, 'Reviewed')}
                        className="bg-green-600 text-white px-3 py-1 rounded-lg text-sm hover:bg-green-700 transition-colors"
                      >
                        Mark Reviewed
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Record Details Modal */}
        {selectedRecord && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Record Details</h2>
                <button
                  onClick={() => setSelectedRecord(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ×
                </button>
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">File Information</h3>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">File Name</label>
                      <p className="text-gray-900">{selectedRecord.fileName}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Type</label>
                      <p className="text-gray-900">{selectedRecord.type}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Size</label>
                      <p className="text-gray-900">{selectedRecord.size}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Upload Date</label>
                      <p className="text-gray-900">{selectedRecord.uploadDate}</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Patient Information</h3>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Patient Name</label>
                      <p className="text-gray-900">{selectedRecord.patientName}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Category</label>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getCategoryColor(selectedRecord.category)}`}>
                        {selectedRecord.category}
                      </span>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Status</label>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(selectedRecord.status)}`}>
                        {selectedRecord.status}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-8 flex justify-end space-x-4">
                <button className="bg-gray-200 text-gray-800 px-6 py-2 rounded-lg hover:bg-gray-300 transition-colors">
                  Close
                </button>
                <button className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors">
                  Download
                </button>
                {selectedRecord.status === 'Pending' && (
                  <button
                    onClick={() => {
                      handleStatusChange(selectedRecord.id, 'Reviewed');
                      setSelectedRecord(null);
                    }}
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Mark as Reviewed
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}