import React, { useState } from 'react';
import { FileText, Plus, Edit2, Save, X, User, Calendar, Search } from 'lucide-react';
import { toast } from '../ui/toast';

const mockDiagnoses = [
  {
    id: '1',
    patientName: 'John Doe',
    patientId: '1',
    date: '2024-01-15',
    diagnosis: 'Hypertension',
    symptoms: 'Elevated blood pressure readings, headaches, dizziness',
    treatment: 'Prescribed ACE inhibitor, lifestyle modifications including diet and exercise',
    notes: 'Patient should monitor blood pressure daily and return for follow-up in 2 weeks',
    prescriptions: ['Lisinopril 10mg - Take once daily', 'Low sodium diet', 'Regular exercise 30min/day'],
    followUp: '2024-01-29'
  },
  {
    id: '2',
    patientName: 'Jane Smith',
    patientId: '2',
    date: '2024-01-18',
    diagnosis: 'Type 2 Diabetes',
    symptoms: 'Frequent urination, increased thirst, fatigue',
    treatment: 'Metformin therapy, dietary counseling, glucose monitoring',
    notes: 'Patient education on diabetes management provided. Referral to nutritionist scheduled',
    prescriptions: ['Metformin 500mg - Take twice daily with meals', 'Blood glucose monitor', 'Diabetic diet plan'],
    followUp: '2024-02-01'
  }
];

export default function DiagnosisNotes() {
  const [diagnoses, setDiagnoses] = useState(mockDiagnoses);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingDiagnosis, setEditingDiagnosis] = useState<any>(null);
  const [formData, setFormData] = useState({
    patientName: '',
    patientId: '',
    diagnosis: '',
    symptoms: '',
    treatment: '',
    notes: '',
    prescriptions: [''],
    followUp: ''
  });

  const filteredDiagnoses = diagnoses.filter(diagnosis =>
    diagnosis.patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    diagnosis.diagnosis.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handlePrescriptionChange = (index: number, value: string) => {
    const newPrescriptions = [...formData.prescriptions];
    newPrescriptions[index] = value;
    setFormData({
      ...formData,
      prescriptions: newPrescriptions
    });
  };

  const addPrescription = () => {
    setFormData({
      ...formData,
      prescriptions: [...formData.prescriptions, '']
    });
  };

  const removePrescription = (index: number) => {
    const newPrescriptions = formData.prescriptions.filter((_, i) => i !== index);
    setFormData({
      ...formData,
      prescriptions: newPrescriptions
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (editingDiagnosis) {
      setDiagnoses(diagnoses.map(d => 
        d.id === editingDiagnosis.id 
          ? { ...formData, id: editingDiagnosis.id, date: editingDiagnosis.date }
          : d
      ));
      setEditingDiagnosis(null);
      toast.success('Diagnosis updated successfully!');
    } else {
      const newDiagnosis = {
        ...formData,
        id: Date.now().toString(),
        date: new Date().toISOString().split('T')[0]
      };
      setDiagnoses([newDiagnosis, ...diagnoses]);
      toast.success('Diagnosis added successfully!');
    }
    
    setShowAddForm(false);
    setFormData({
      patientName: '',
      patientId: '',
      diagnosis: '',
      symptoms: '',
      treatment: '',
      notes: '',
      prescriptions: [''],
      followUp: ''
    });
  };

  const handleEdit = (diagnosis: any) => {
    setEditingDiagnosis(diagnosis);
    setFormData(diagnosis);
    setShowAddForm(true);
  };

  const handleCancel = () => {
    setShowAddForm(false);
    setEditingDiagnosis(null);
    setFormData({
      patientName: '',
      patientId: '',
      diagnosis: '',
      symptoms: '',
      treatment: '',
      notes: '',
      prescriptions: [''],
      followUp: ''
    });
  };

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Diagnosis Notes</h1>
            <p className="text-gray-600">Create and manage patient diagnosis records</p>
          </div>
          <button
            onClick={() => setShowAddForm(true)}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center"
          >
            <Plus className="w-5 h-5 mr-2" />
            Add Diagnosis
          </button>
        </div>

        {/* Search Bar */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search by patient name or diagnosis..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        {/* Add/Edit Form */}
        {showAddForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl p-8 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">
                  {editingDiagnosis ? 'Edit Diagnosis' : 'Add New Diagnosis'}
                </h2>
                <button
                  onClick={handleCancel}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Patient Name
                    </label>
                    <input
                      type="text"
                      name="patientName"
                      value={formData.patientName}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Patient ID
                    </label>
                    <input
                      type="text"
                      name="patientId"
                      value={formData.patientId}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Diagnosis
                  </label>
                  <input
                    type="text"
                    name="diagnosis"
                    value={formData.diagnosis}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Symptoms
                  </label>
                  <textarea
                    name="symptoms"
                    value={formData.symptoms}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Treatment Plan
                  </label>
                  <textarea
                    name="treatment"
                    value={formData.treatment}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Notes
                  </label>
                  <textarea
                    name="notes"
                    value={formData.notes}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Prescriptions
                  </label>
                  <div className="space-y-2">
                    {formData.prescriptions.map((prescription, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <input
                          type="text"
                          value={prescription}
                          onChange={(e) => handlePrescriptionChange(index, e.target.value)}
                          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          placeholder="Enter prescription"
                        />
                        {formData.prescriptions.length > 1 && (
                          <button
                            type="button"
                            onClick={() => removePrescription(index)}
                            className="p-2 text-red-600 hover:text-red-700"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    ))}
                    <button
                      type="button"
                      onClick={addPrescription}
                      className="text-blue-600 hover:text-blue-700 text-sm"
                    >
                      + Add Prescription
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Follow-up Date
                  </label>
                  <input
                    type="date"
                    name="followUp"
                    value={formData.followUp}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div className="flex justify-end space-x-4">
                  <button
                    type="button"
                    onClick={handleCancel}
                    className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center"
                  >
                    <Save className="w-5 h-5 mr-2" />
                    {editingDiagnosis ? 'Update' : 'Save'} Diagnosis
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Diagnosis List */}
        <div className="space-y-6">
          {filteredDiagnoses.map((diagnosis) => (
            <div key={diagnosis.id} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                    <FileText className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{diagnosis.diagnosis}</h3>
                    <div className="flex items-center text-sm text-gray-600 mt-1">
                      <User className="w-4 h-4 mr-1" />
                      <span className="mr-4">{diagnosis.patientName}</span>
                      <Calendar className="w-4 h-4 mr-1" />
                      <span>{diagnosis.date}</span>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => handleEdit(diagnosis)}
                  className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                >
                  <Edit2 className="w-4 h-4" />
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Symptoms</h4>
                  <p className="text-gray-700 text-sm">{diagnosis.symptoms}</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Treatment</h4>
                  <p className="text-gray-700 text-sm">{diagnosis.treatment}</p>
                </div>
              </div>

              {diagnosis.notes && (
                <div className="mt-4">
                  <h4 className="font-medium text-gray-900 mb-2">Notes</h4>
                  <p className="text-gray-700 text-sm">{diagnosis.notes}</p>
                </div>
              )}

              {diagnosis.prescriptions.length > 0 && (
                <div className="mt-4">
                  <h4 className="font-medium text-gray-900 mb-2">Prescriptions</h4>
                  <ul className="text-sm text-gray-700 space-y-1">
                    {diagnosis.prescriptions.map((prescription, index) => (
                      <li key={index} className="flex items-center">
                        <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                        {prescription}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {diagnosis.followUp && (
                <div className="mt-4 p-3 bg-yellow-50 rounded-lg">
                  <p className="text-sm text-yellow-800">
                    <strong>Follow-up scheduled:</strong> {diagnosis.followUp}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}