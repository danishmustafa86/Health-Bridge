import React, { useState } from 'react';
import { Calendar, Clock, User, FileText, Star, CheckCircle, XCircle } from 'lucide-react';

const mockAppointments = [
  {
    id: '1',
    doctor: 'Dr. Sarah Wilson',
    specialty: 'Cardiology',
    date: '2024-01-20',
    time: '10:00 AM',
    status: 'completed',
    fee: 150,
    rating: 5,
    diagnosis: 'Regular checkup completed. Heart rate and blood pressure normal.',
    prescriptions: ['Aspirin 81mg - Take daily', 'Lisinopril 10mg - Take twice daily']
  },
  {
    id: '2',
    doctor: 'Dr. Michael Chen',
    specialty: 'Neurology',
    date: '2024-01-25',
    time: '2:30 PM',
    status: 'upcoming',
    fee: 180,
    rating: null,
    diagnosis: null,
    prescriptions: []
  },
  {
    id: '3',
    doctor: 'Dr. Emily Rodriguez',
    specialty: 'Dermatology',
    date: '2024-01-18',
    time: '11:00 AM',
    status: 'completed',
    fee: 120,
    rating: 4,
    diagnosis: 'Skin examination completed. Minor eczema treated.',
    prescriptions: ['Hydrocortisone cream - Apply twice daily']
  },
  {
    id: '4',
    doctor: 'Dr. David Kim',
    specialty: 'Orthopedics',
    date: '2024-01-12',
    time: '3:00 PM',
    status: 'cancelled',
    fee: 200,
    rating: null,
    diagnosis: null,
    prescriptions: []
  }
];

export default function AppointmentHistory() {
  const [appointments, setAppointments] = useState(mockAppointments);
  const [selectedAppointment, setSelectedAppointment] = useState<any>(null);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'upcoming':
        return 'bg-blue-100 text-blue-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4" />;
      case 'upcoming':
        return <Clock className="w-4 h-4" />;
      case 'cancelled':
        return <XCircle className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-4 h-4 ${i < rating ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}`}
      />
    ));
  };

  return (
    <div className="p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Appointment History</h1>
          <p className="text-gray-600">View your past and upcoming appointments</p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6">
          <div className="flex flex-wrap gap-4">
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              All
            </button>
            <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
              Upcoming
            </button>
            <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
              Completed
            </button>
            <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
              Cancelled
            </button>
          </div>
        </div>

        {/* Appointments List */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {appointments.map((appointment) => (
            <div
              key={appointment.id}
              className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                    <User className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">{appointment.doctor}</h3>
                    <p className="text-sm text-gray-600">{appointment.specialty}</p>
                  </div>
                </div>
                <div className={`px-3 py-1 rounded-full text-xs font-medium flex items-center ${getStatusColor(appointment.status)}`}>
                  {getStatusIcon(appointment.status)}
                  <span className="ml-1 capitalize">{appointment.status}</span>
                </div>
              </div>

              <div className="flex items-center text-sm text-gray-600 mb-4">
                <Calendar className="w-4 h-4 mr-2" />
                <span>{appointment.date}</span>
                <Clock className="w-4 h-4 ml-4 mr-2" />
                <span>{appointment.time}</span>
              </div>

              <div className="flex justify-between items-center">
                <div className="text-sm">
                  <span className="text-gray-600">Fee: </span>
                  <span className="font-semibold">${appointment.fee}</span>
                </div>
                
                {appointment.status === 'completed' && (
                  <div className="flex items-center">
                    {appointment.rating && (
                      <div className="flex items-center mr-3">
                        {renderStars(appointment.rating)}
                      </div>
                    )}
                    <button
                      onClick={() => setSelectedAppointment(appointment)}
                      className="text-blue-600 hover:text-blue-700 font-medium text-sm"
                    >
                      View Details
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Appointment Details Modal */}
        {selectedAppointment && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Appointment Details</h2>
                <button
                  onClick={() => setSelectedAppointment(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>

              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Doctor</label>
                    <p className="text-gray-900">{selectedAppointment.doctor}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Specialty</label>
                    <p className="text-gray-900">{selectedAppointment.specialty}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                    <p className="text-gray-900">{selectedAppointment.date}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Time</label>
                    <p className="text-gray-900">{selectedAppointment.time}</p>
                  </div>
                </div>

                {selectedAppointment.rating && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Your Rating</label>
                    <div className="flex items-center">
                      {renderStars(selectedAppointment.rating)}
                    </div>
                  </div>
                )}

                {selectedAppointment.diagnosis && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Diagnosis</label>
                    <p className="text-gray-900 bg-gray-50 p-4 rounded-lg">{selectedAppointment.diagnosis}</p>
                  </div>
                )}

                {selectedAppointment.prescriptions.length > 0 && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Prescriptions</label>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      {selectedAppointment.prescriptions.map((prescription: string, index: number) => (
                        <div key={index} className="flex items-center mb-2 last:mb-0">
                          <FileText className="w-4 h-4 text-gray-500 mr-2" />
                          <span className="text-gray-900">{prescription}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="border-t pt-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Total Fee:</span>
                    <span className="text-lg font-semibold text-gray-900">${selectedAppointment.fee}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}